from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.niches.niche_service import NicheService
from app.services.subniches.subniche_service import (
    SubnicheService,
)


class NicheDetailPage(QWidget):

    back_requested = Signal()

    def __init__(self):
        super().__init__()

        self.niche_id = None

        self._create_interface()

    def _create_interface(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(20)

        self.back_button = QPushButton(
            "← Voltar para nichos"
        )

        self.back_button.clicked.connect(
            self.back_requested.emit
        )

        layout.addWidget(self.back_button)

        self.title = QLabel()
        self.title.setObjectName("pageTitle")

        layout.addWidget(self.title)

        self.description = QLabel()
        self.description.setObjectName(
            "pageDescription"
        )

        self.description.setWordWrap(True)

        layout.addWidget(self.description)

        subniche_title = QLabel(
            "Subnichos"
        )

        subniche_title.setObjectName(
            "sectionTitle"
        )

        layout.addWidget(subniche_title)

        self.subniche_list = QListWidget()
        self.subniche_list.setObjectName(
            "projectList"
        )

        layout.addWidget(
            self.subniche_list
        )

        self.add_subniche_button = QPushButton(
            "+ Adicionar subnicho"
        )

        self.add_subniche_button.setObjectName(
            "primaryButton"
        )

        self.add_subniche_button.clicked.connect(
            self.add_subniche
        )

        layout.addWidget(
            self.add_subniche_button
        )

        layout.addStretch()

    def load_niche(self, niche_id):

        self.niche_id = niche_id

        niche = NicheService.get_niche(
            niche_id
        )

        if niche is None:
            QMessageBox.warning(
                self,
                "Erro",
                "Nicho não encontrado.",
            )

            self.back_requested.emit()

            return

        self.title.setText(
            f"🎯 {niche.name}"
        )

        self.description.setText(
            niche.description or
            "Nenhuma descrição cadastrada."
        )

        self.refresh_subniches()

    def refresh_subniches(self):

        self.subniche_list.clear()

        if self.niche_id is None:
            return

        subniches = (
            SubnicheService.get_subniches(
                self.niche_id
            )
        )

        if not subniches:

            item = QListWidgetItem(
                "Nenhum subnicho cadastrado."
            )

            self.subniche_list.addItem(item)

            return

        for subniche in subniches:

            item = QListWidgetItem()

            item.setText(
                f"• {subniche.name}\n"
                f"{subniche.description or ''}"
            )

            self.subniche_list.addItem(item)

    def add_subniche(self):

        if self.niche_id is None:
            return

        name, ok = QInputDialog.getText(
            self,
            "Novo subnicho",
            "Nome do subnicho:",
        )

        if not ok or not name.strip():
            return

        name = name.strip()

        description, ok = QInputDialog.getText(
            self,
            "Descrição",
            "Descrição do subnicho:",
        )

        if not ok:
            return

        try:

            SubnicheService.create_subniche(
                niche_id=self.niche_id,
                name=name,
                description=description.strip(),
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Erro",
                (
                    "Não foi possível criar "
                    f"o subnicho:\n\n{error}"
                ),
            )

            return

        self.refresh_subniches()
