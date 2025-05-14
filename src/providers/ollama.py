from crewai import LLM

ollama_llm = LLM(
    model="ollama/hf.co/stduhpf/google-gemma-3-27b-it-qat-q4_0-gguf-small:Q4_0_S",
    api_base="https://0fe9-35-226-94-49.ngrok-free.app",
    temperature=0
)

