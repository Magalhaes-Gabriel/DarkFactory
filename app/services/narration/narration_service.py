from pathlib import Path
import shutil
import subprocess

import requests

from app.database.database import PROJECT_ROOT


class NarrationService:
    KOKORO_URL = "http://127.0.0.1:8880/v1/audio/speech"

    VOICE = "pf_dora"
    SPEED = 0.95

    @classmethod
    def generate(
        cls,
        project_id: int,
        script: str,
    ) -> Path:
        script = script.strip()

        if not script:
            raise ValueError(
                "O projeto não possui um roteiro."
            )

        project_dir = (
            PROJECT_ROOT
            / "data"
            / "projects"
            / f"project_{project_id}"
        )

        project_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = project_dir / "narration.wav"

        try:
            cls._generate_with_kokoro(
                script=script,
                output_path=output_path,
            )

        except Exception as kokoro_error:
            print(
                "Kokoro indisponível. "
                "Tentando espeak-ng como fallback."
            )
            print(
                f"Erro Kokoro: {kokoro_error}"
            )

            cls._generate_with_espeak(
                script=script,
                output_path=output_path,
            )

        if (
            not output_path.is_file()
            or output_path.stat().st_size == 0
        ):
            raise RuntimeError(
                "O arquivo de narração não foi "
                "criado corretamente."
            )

        return output_path

    @classmethod
    def _generate_with_kokoro(
        cls,
        script: str,
        output_path: Path,
    ):
        response = requests.post(
            cls.KOKORO_URL,
            json={
                "model": "kokoro",
                "input": script,
                "voice": cls.VOICE,
                "response_format": "wav",
                "speed": cls.SPEED,
            },
            timeout=1800,
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "content-type",
            "",
        )

        if (
            "audio" not in content_type.lower()
            and not response.content.startswith(b"RIFF")
        ):
            raise RuntimeError(
                "O Kokoro não retornou um arquivo "
                "de áudio válido."
            )

        temp_path = output_path.with_suffix(
            ".tmp.wav"
        )

        temp_path.write_bytes(
            response.content
        )

        temp_path.replace(
            output_path
        )

    @staticmethod
    def _generate_with_espeak(
        script: str,
        output_path: Path,
    ):
        espeak_path = (
            shutil.which("espeak-ng")
            or shutil.which("espeak")
        )

        if espeak_path is None:
            raise RuntimeError(
                "Kokoro não respondeu e o "
                "espeak-ng também não está instalado."
            )

        command = [
            espeak_path,
            "-v",
            "pt-br",
            "-s",
            "145",
            "-p",
            "45",
            "-a",
            "180",
            "-w",
            str(output_path),
        ]

        subprocess.run(
            command,
            input=script,
            check=True,
            capture_output=True,
            text=True,
            timeout=1800,
        )