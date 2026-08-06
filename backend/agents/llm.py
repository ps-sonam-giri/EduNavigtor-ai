"""
LLM client – Gemini with Google Search grounding + Ollama fallback.
Web search is automatically used by Gemini to provide current, accurate data.
"""

import asyncio
import json
import logging
import re
from typing import Any, Dict, Tuple

from app.config import settings

logger = logging.getLogger(__name__)


async def ainvoke_llm(prompt: str, fast: bool = False, use_search: bool = False) -> Tuple[str, int]:
    """
    Invoke LLM. Returns (response_text, token_count).
    use_search=True enables Gemini Google Search grounding for real-time data.
    """
    if settings.llm_provider == "gemini" and settings.gemini_api_key:
        return await _invoke_gemini(prompt, use_search=use_search)
    return await _invoke_ollama(prompt, fast)


async def _invoke_gemini(prompt: str, use_search: bool = False) -> Tuple[str, int]:
    """
    Call Gemini API in a thread executor (non-blocking).
    Enables Google Search grounding when use_search=True for real-time web data.
    Hard 30s timeout per call. Retries once on 429.
    """
    def _sync_call() -> str:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.gemini_api_key)

        # Build config — enable Google Search grounding for real-time data
        config_kwargs = dict(
            temperature=0.4,
            max_output_tokens=2048,
        )

        if use_search:
            try:
                config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
            except Exception:
                pass  # Search not available — proceed without it

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        return response.text or ""

    loop = asyncio.get_event_loop()

    for attempt in range(2):
        try:
            text = await asyncio.wait_for(
                loop.run_in_executor(None, _sync_call),
                timeout=30.0,
            )
            tokens = len(text.split()) * 4 // 3
            logger.info(f"Gemini{'[search]' if use_search else ''} response ({len(text)} chars)")
            return text, tokens

        except asyncio.TimeoutError:
            logger.warning(f"Gemini timeout (attempt {attempt+1})")
            if attempt == 0:
                await asyncio.sleep(2)
                continue
            break

        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                if "PerDay" in err:
                    logger.warning("Gemini daily quota exhausted — falling back to Ollama")
                    break
                if attempt == 0:
                    logger.warning("Gemini rate limited — waiting 10s and retrying")
                    await asyncio.sleep(10)
                    continue
                break
            else:
                logger.warning(f"Gemini error: {e} — falling back to Ollama")
                break

    return await _invoke_ollama(prompt, fast=True)


async def _invoke_ollama(prompt: str, fast: bool = False) -> Tuple[str, int]:
    """Call local Ollama / Qwen2.5 as fallback."""
    try:
        from langchain_ollama import ChatOllama
        model = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0.3 if fast else settings.ollama_temperature,
            num_predict=512 if fast else settings.ollama_max_tokens,
        )
        response = await model.ainvoke(prompt)
        text = response.content if hasattr(response, "content") else str(response)
        tokens = len(text.split()) * 4 // 3
        return text, tokens
    except Exception as e:
        return f"[LLM unavailable: {str(e)}]", 0


def extract_json_from_response(text: str) -> Dict[str, Any]:
    """Extract JSON from LLM response — handles markdown fences and bare objects."""
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            pass
    bare = re.search(r"\{.*\}", text, re.DOTALL)
    if bare:
        try:
            return json.loads(bare.group(0))
        except json.JSONDecodeError:
            pass
    return {}


llm = None
llm_fast = None
