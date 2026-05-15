import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
        self.max_retries = 3

    def chat(self, prompt: str, system: str = "", temp: float = 0.7, max_tokens: int = 512) -> dict:
        url = f"{self.host}/api/chat"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "options": {
                "temperature": temp,
                "num_predict": max_tokens,
            },
            "stream": False,
        }

        for attempt in range(self.max_retries):
            try:
                start = time.time()
                response = requests.post(url, json=payload, timeout=180)
                elapsed = int((time.time() - start) * 1000)
                response.raise_for_status()
                data = response.json()

                resposta = data.get("message", {}).get("content", "").strip()
                tokens_prompt = data.get("prompt_eval_count", 0)
                tokens_resposta = data.get("eval_count", 0)

                return {
                    "resposta": resposta,
                    "tokens_prompt": tokens_prompt,
                    "tokens_resposta": tokens_resposta,
                    "tempo_ms": elapsed,
                }

            except requests.Timeout:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"Timeout após {self.max_retries} tentativas.")
                time.sleep(2 ** attempt)

            except requests.ConnectionError:
                raise RuntimeError(
                    f"Não foi possível conectar ao Ollama em {self.host}. "
                    "Verifique se o Ollama está rodando: 'ollama serve'"
                )

            except requests.HTTPError as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"Erro HTTP {response.status_code}: {e}")
                time.sleep(2 ** attempt)
