from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.niches.niche_service import NicheService


class NichesPage(QWidget):

    def __init__(self):
        super().__init__()

        self._create_interface()
        self.refresh()

    def _create_interface(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(20)

        title = QLabel("🎯 Nichos")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Organize os nichos que serão utilizados "
            "pelo Universo em uma Casca de Nós."
        )

        description.setObjectName(
            "pageDescription"
        )

        layout.addWidget(title)
        layout.addWidget(description)

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Pesquisar nicho..."
        )

        self.search_input.textChanged.connect(
            self.search
        )

        search_layout.addWidget(
            self.search_input
        )

        layout.addLayout(search_layout)

        self.niche_list = QListWidget()

        self.niche_list.setObjectName(
            "projectList"
        )

        layout.addWidget(self.niche_list)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton(
            "+ Adicionar nicho"
        )

        self.add_button.setObjectName(
            "primaryButton"
        )

        self.add_button.clicked.connect(
            self.add_niche
        )

        button_layout.addWidget(
            self.add_button
        )

        button_layout.addStretch()

        layout.addLayout(button_layout)

    def refresh(self):

        self.niche_list.clear()

        niches = NicheService.get_niches()

        for niche in niches:

            item = QListWidgetItem()

            item.setText(
                f"🎯 {niche.name}\n"
                f"{niche.description or ''}"
            )

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

            item.setText(
                f"🎯 {niche.name}\n"
                f"{niche.description or ''}"
            )

            self.niche_list.addItem(item)

    def add_niche(self):

        from PySide6.QtWidgets import (
            QInputDialog,
        )

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
