import requests


class OllamaService:
    BASE_URL = "http://localhost:11434"
    MODEL = "qwen3:4b"

    @classmethod
    def generate(
        cls,
        prompt: str,
    ) -> str:
        response = requests.post(
            f"{cls.BASE_URL}/api/generate",
            json={
                "model": cls.MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=180000,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

