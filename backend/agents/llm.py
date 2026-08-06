"""
LLM client – 3-Tier Fallback Cascade:
1. Gemini (Primary, with Google Search grounding option)
2. Groq API (Fallback 1: Llama-3.3-70b-versatile)
3. Ollama (Fallback 2: Local Qwen2.5)
"""

import asyncio
import json
import logging
import re
from typing import Any, Dict, Tuple

import httpx
from app.config import settings

logger = logging.getLogger(__name__)


async def ainvoke_llm(prompt: str, fast: bool = False, use_search: bool = False) -> Tuple[str, int]:
    """
    Invoke LLM with 3-tier fallback cascade:
    Gemini -> Groq -> Local Ollama
    Returns (response_text, token_count).
    """
    # 1. Try Gemini (if configured)
    if settings.gemini_api_key and settings.gemini_api_key.strip():
        res, tokens = await _invoke_gemini(prompt, use_search=use_search)
        if res and not res.startswith("[LLM unavailable"):
            return res, tokens

    # 2. Fallback to Groq (if configured)
    if settings.groq_api_key and settings.groq_api_key.strip():
        res, tokens = await _invoke_groq(prompt, fast=fast)
        if res and not res.startswith("[LLM unavailable"):
            return res, tokens

    # 3. Fallback to local Ollama
    return await _invoke_ollama(prompt, fast=fast)


async def _invoke_gemini(prompt: str, use_search: bool = False) -> Tuple[str, int]:
    """Call Gemini API with 30s timeout and search grounding option."""
    def _sync_call() -> str:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.gemini_api_key)

        config_kwargs = dict(
            temperature=0.4,
            max_output_tokens=2048,
        )

        if use_search:
            try:
                config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
            except Exception:
                pass

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
            logger.warning(f"Gemini error: {e} — cascading to Groq/Ollama")
            break

    return "", 0


async def _invoke_groq(prompt: str, fast: bool = False) -> Tuple[str, int]:
    """Call Groq API (Llama-3.3-70b-versatile) via async HTTP."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.groq_model or "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3 if fast else 0.5,
        "max_tokens": 1024 if fast else 2048,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                tokens = usage.get("total_tokens", len(text.split()) * 4 // 3)
                logger.info(f"Groq ({settings.groq_model}) response ({len(text)} chars)")
                return text, tokens
            else:
                logger.warning(f"Groq API error HTTP {resp.status_code}: {resp.text}")
    except Exception as e:
        logger.warning(f"Groq execution failed: {e}")

    return "", 0


async def _invoke_ollama(prompt: str, fast: bool = False) -> Tuple[str, int]:
    """Call local Ollama / Qwen2.5 as final fallback."""
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
        logger.warning(f"Ollama execution failed: {e}")
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
