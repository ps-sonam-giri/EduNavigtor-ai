"""
LLM client – supports Gemini (fast, free) and Ollama (local fallback).
Supports both AIzaSy and AQ. style Gemini API keys.
"""

import json
import logging
import re
from typing import Any, Dict, Tuple

from app.config import settings

logger = logging.getLogger(__name__)


async def ainvoke_llm(prompt: str, fast: bool = False) -> Tuple[str, int]:
    """
    Invoke LLM. Returns (response_text, approximate_token_count).
    Uses Gemini if configured, otherwise falls back to Ollama.
    """
    if settings.llm_provider == "gemini" and settings.gemini_api_key:
        return await _invoke_gemini(prompt)
    return await _invoke_ollama(prompt, fast)


async def _invoke_gemini(prompt: str) -> Tuple[str, int]:
    """Call Gemini API using google-genai SDK with retry on rate limit."""
    import asyncio

    max_retries = 3
    for attempt in range(max_retries):
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=settings.gemini_api_key)

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=2048,
                ),
            )

            text = response.text or ""
            tokens = len(text.split()) * 4 // 3
            logger.info(f"Gemini response received ({len(text)} chars)")
            return text, tokens

        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                if "GenerateRequestsPerDayPerProjectPerModel" in err:
                    # Daily quota exhausted – fall back to Ollama
                    logger.warning(f"Gemini daily quota exhausted, falling back to Ollama")
                    break
                # Per-minute rate limit – wait and retry
                wait = 15 * (attempt + 1)
                logger.warning(f"Gemini rate limited (attempt {attempt+1}), waiting {wait}s...")
                await asyncio.sleep(wait)
                continue
            else:
                logger.warning(f"Gemini failed ({e}), falling back to Ollama")
                break

    return await _invoke_ollama(prompt, fast=True)


async def _invoke_ollama(prompt: str, fast: bool = False) -> Tuple[str, int]:
    """Call local Ollama / Qwen2.5."""
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
    """Robustly extract a JSON object from LLM response."""
    # Try fenced code block first
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            pass

    # Try bare JSON object
    bare = re.search(r"\{.*\}", text, re.DOTALL)
    if bare:
        try:
            return json.loads(bare.group(0))
        except json.JSONDecodeError:
            pass

    return {}


# Legacy aliases
llm = None
llm_fast = None
