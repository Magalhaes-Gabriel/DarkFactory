from PySide6.QtCore import QObject, Signal, Slot

from app.services.ai.ollama_service import OllamaService


class OllamaWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, prompt: str):
        super().__init__()

        self.prompt = prompt

    @Slot()
    def run(self):
        try:
            result = OllamaService.generate(
                self.prompt
            )

            self.finished.emit(result)

        except Exception as error:
            self.error.emit(str(error))

