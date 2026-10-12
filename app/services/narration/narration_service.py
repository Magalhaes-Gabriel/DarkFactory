from pathlib import Path
import shutil
import subprocess

from app.database.database import PROJECT_ROOT


class NarrationService:
    @staticmethod
    def generate(
        project_id: int,
        script: str,
    ) -> Path:
        script = script.strip()

        if not script:
            raise ValueError(
                "O projeto não possui um roteiro."
            )

        espeak_path = (
            shutil.which("espeak-ng")
            or shutil.which("espeak")
        )

        if espeak_path is None:
            raise RuntimeError(
                "O espeak não foi encontrado. "
                "Instale-o no sistema antes de continuar."
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

        command = [
            espeak_path,
            "-v", "pt-br",
            "-s", "145",
            "-p", "45",
            "-a", "180",
            "-w", str(output_path),
        ]

        try:
            subprocess.run(
                command,
                input=script,
                check=True,
                capture_output=True,
                text=True,
                timeout=1800,
            )
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(
                "A geração da narração ultrapassou "
                "30 minutos."
            ) from error
        except subprocess.CalledProcessError as error:
            details = error.stderr or str(error)
            raise RuntimeError(
                f"O espeak não conseguiu gerar o áudio: {details}"
            ) from error

        if (
            not output_path.is_file()
            or output_path.stat().st_size == 0
        ):
            raise RuntimeError(
                "O arquivo WAV não foi criado corretamente."
            )

        return output_path