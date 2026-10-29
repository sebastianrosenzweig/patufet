from huggingface_hub import hf_hub_download
from llama_cpp import Llama

DEVICE = "cpu"
N_CTX = 2048
N_THREADS = 4

model_path = hf_hub_download(
    repo_id="BSC-LT/salamandraTA-2B-instruct-GGUF",
    filename="salamandrata_2b_inst_q4.gguf"
)

# Global variable to hold the LLM instance
_llm: Llama = None


def translate(text: str, source_lang: str, target_lang: str) -> str:
    global _llm
    if _llm is None:
        _llm = Llama(
            model_path=model_path,
            context_size=N_CTX,
            n_threads=N_THREADS,
            verbose=False
        )

    output = _llm.create_chat_completion(
        messages=[
            {"role": "user",
             "content": f"Translate the following text from {source_lang} into {target_lang}.\\n{source_lang}: {text} \\n{target_lang}:"},
        ],
        max_tokens=64,
        temperature=0.7,
        top_p=0.8,
    )

    response = output["choices"][0]["message"]["content"].strip()
    return response if response else ""
