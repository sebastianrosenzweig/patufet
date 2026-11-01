import logging
from typing import Optional

import requests
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from .translation import translate

logger = logging.getLogger(__name__)

DEVICE = "cpu"
N_CTX = 2048
N_THREADS = 4
N_WIKI_PAGE_SEARCH = 1

model_path = hf_hub_download(
    repo_id="Qwen/Qwen2.5-0.5B-Instruct-GGUF",
    filename="qwen2.5-0.5b-instruct-fp16.gguf"
)

# Global variable to hold the LLM instance
_llm: Optional[Llama] = None

def get_llm_instance() -> Llama:
    global _llm
    if _llm is None:
        _llm = Llama(
            model_path=model_path,
            n_ctx=N_CTX,
            n_threads=N_THREADS,
            verbose=False
        )
    return _llm

API = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": (
        "Patufet/1.0 "
        "(A voice agent based on Wikipedia; "
        "contact: https://github.com/sebastianrosenzweig)"
    )
}

def get_sources(question: str) -> str:
    """
    Fetches relevant information from Wikipedia based on the provided question.
    """
    try:
        response = requests.get(
            API,
            params={
                "action": "query",
                "list": "search",
                "srsearch": question,
                "srlimit": N_WIKI_PAGE_SEARCH,
                "format": "json",
            },
            headers=HEADERS,
            timeout=20,
        )
        response.raise_for_status()
        pages = response.json().get("query", {}).get("search", [])

        if not pages:
            return ""

        resources = []
        for page in pages:
            logger.info(f"Fetching Wikipedia page: {page['title']}")
            title = page["title"]
            response = requests.get(
                API,
                params={
                    "action": "query",
                    "prop": "extracts",
                    "exintro": 1,
                    "explaintext": 1,
                    "exchars": 2000,
                    "redirects": 1,
                    "titles": title,
                    "format": "json",
                },
                headers=HEADERS,
                timeout=20,
            )
            response.raise_for_status()

            page_data = response.json().get("query", {}).get("pages", {})
            if not page_data:
                continue

            article = next(iter(page_data.values()))
            if "extract" in article:
                resources.append(article["extract"].strip())

        return " ".join(resources)
    except:
        return ""

def generate_response(transcript: str) -> str:
    """
    Finds relevant Wikipedia articles and generates the answer from the gathered information.
    """
    query_ca = transcript.strip()
    if not query_ca:
        return "No entenc la pregunta. Pots repetir, si us plau?"

    if "on ets" in query_ca.lower():
        return "Soc a la panxa del bou, que no hi neva ni hi plou! Quan el bou farà un pet, sortirà en Patufet."

    # Find wikipedia sources
    query_en = translate(query_ca, "Catalan", "English")
    context = get_sources(query_en)

    # Initialize the model
    llm_instance = get_llm_instance()

    # If context is empty, we might want to skip the LLM or handle it gracefully
    if not context:
        # We still want the LLM to know it has no context
        context = "No relevant information was found."

    output = llm_instance.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the question using only the provided context. "
                    "Reply in English in 1-2 short sentences. "
                    "If the answer is not explicitly supported by the context, "
                    "reply: I don't know. "
                    "Do not guess."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {query_en}\n\n"
                    f"Context:\n{context}\n\n"
                    "Answer:"
                ),
            },
        ],
        max_tokens=128,
        temperature=0.7,
        top_p=0.8,
        top_k=20,
    )

    response_en = output["choices"][0]["message"]["content"].strip()
    response_ca = translate(response_en, "English", "Catalan")
    return response_ca if response_ca else "No he pogut generar una resposta."
