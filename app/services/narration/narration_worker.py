from PySide6.QtCore import QObject, Signal, Slot

from app.services.narration.narration_service import (
    NarrationService,
)


class NarrationWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(
        self,
        project_id: int,
        script: str,
    ):
        super().__init__()

        self.project_id = project_id
        self.script = script

    @Slot()
    def run(self):
        try:
            output_path = NarrationService.generate(
                project_id=self.project_id,
                script=self.script,
            )

            self.finished.emit(
                str(output_path)
            )

        except Exception as error:
            self.error.emit(
                str(error)
            )
