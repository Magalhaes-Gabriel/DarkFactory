from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.niches.niche_service import NicheService
from app.services.subniches.subniche_service import (
    SubnicheService,
)


class NichesPage(QWidget):

    niche_selected = Signal(int)

    def __init__(self):
        super().__init__()

        self._create_interface()
        self.niche_list.itemDoubleClicked.connect(
            self._open_niche
        )
        self.refresh()

    def _create_interface(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(20)

        title = QLabel("🎯 Nichos")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Organize os nichos e subnichos "
            "do Universo em uma Casca de Nós."
        )

        description.setObjectName(
            "pageDescription"
        )

        layout.addWidget(title)
        layout.addWidget(description)

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Pesquisar nicho..."
        )

        self.search_input.textChanged.connect(
            self.search
        )

        layout.addWidget(self.search_input)

        self.niche_list = QListWidget()

        self.niche_list.setObjectName(
            "projectList"
        )

        layout.addWidget(self.niche_list)

        self.add_button = QPushButton(
            "+ Adicionar nicho"
        )

        self.add_button.setObjectName(
            "primaryButton"
        )

        self.add_button.clicked.connect(
            self.add_niche
        )

        layout.addWidget(self.add_button)

    def refresh(self):

        self.niche_list.clear()

        niches = NicheService.get_niches()

        for niche in niches:

            item = QListWidgetItem()
            item.setData(
                Qt.UserRole,
                niche.id,
            )

            text = (
                f"🎯 {niche.name}\n"
                f"{niche.description or ''}"
            )

            subniches = (
                SubnicheService
                .get_subniches(niche.id)
            )

            if subniches:

                text += "\n\nSubnichos:"

                for subniche in subniches:
                    text += (
                        f"\n   • {subniche.name}"
                    )

            item.setText(text)

            self.niche_list.addItem(item)

    def search(self, text):

        self.niche_list.clear()

        text = text.strip()

        if not text:
            self.refresh()
            return

        niches = NicheService.search_niches(
            text
        )

        for niche in niches:

            item = QListWidgetItem()

            text = (
                f"🎯 {niche.name}\n"
                f"{niche.description or ''}"
            )

            subniches = (
                SubnicheService
                .get_subniches(niche.id)
            )

            if subniches:

                text += "\n\nSubnichos:"

                for subniche in subniches:
                    text += (
                        f"\n   • {subniche.name}"
                    )

            item.setText(text)

            self.niche_list.addItem(item)

    def add_niche(self):

        name, ok = QInputDialog.getText(
            self,
            "Novo nicho",
            "Nome do nicho:",
        )

        if not ok or not name.strip():
            return

        name = name.strip()

        NicheService.create_niche(name)

        self.refresh()

    def _open_niche(self, item):

        niche_id = item.data(
            Qt.UserRole
        )

        if niche_id is not None:
            self.niche_selected.emit(
                niche_id
            )