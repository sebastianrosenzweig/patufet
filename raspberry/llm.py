from typing import Optional
from llama_cpp import Llama

# Configuration for the LLM
# For Raspberry Pi 4 (4GB), TinyLlama-1.1B-Chat-v1.0-GGUF is a great choice.
# It's small enough to run on CPU while maintaining decent performance.
MODEL_PATH = "models/tinyllama-1.1b-chat-v1.0-q4_k_m.gguf"
DEVICE = "cpu"
N_CTX = 2048
N_THREADS = 4

# Global variable to hold the LLM instance
_llm: Optional[Llama] = None

def get_llm_instance() -> Llama:
    global _llm
    if _llm is None:
        _llm = Llama(
            model_path=MODEL_PATH,
            context_size=N_CTX,
            n_threads=N_THREADS,
            verbose=False
        )
    return _llm

def get_llm_response(transcript: str) -> str:
    """
    Sends the transcribed text to the LLM and returns a response in Catalan.
    """
    if not transcript.strip():
        return "No entenc la consulta. Pots repetir, si us plau?"

    # The system prompt instructs the model on how to behave.
    system_prompt = "Tu ets un assistent útil en català. Respon a la següent pregunta de manera concisa."
    full_prompt = f"{system_prompt}\n\nUsuari: {transcript}\nAssistents:"

    # Initialize the model
    llm_instance = get_llm_instance()

    output = llm_instance.create_completion(
        prompt=full_prompt,
        max_tokens=128,
        stop=["\n", "Usuari:"],
        temperature=0.7,
        top_p=0.9
    )
    response = output["choices"][0]["text"].strip()
    return response if response else "No he pogut generar una resposta."
