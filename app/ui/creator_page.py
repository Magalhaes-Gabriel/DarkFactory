from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.projects.project_service import ProjectService


class CreatorPage(QWidget):
    project_created = Signal()

    def __init__(self):
        super().__init__()

        self._create_interface()

    def _create_interface(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        title = QLabel("Criar conteúdo")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Crie um novo projeto para o Universo em uma Casca de Nós."
        )
        description.setObjectName("pageDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addSpacing(20)

        form_frame = QFrame()
        form_frame.setObjectName("card")

        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(15)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Ex.: A história da CB 300"
        )

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText(
            "Ex.: Honda CB 300"
        )

        self.category_input = QComboBox()

        self.category_input.addItems([
            "Carros",
            "Motos",
            "Jogos",
            "Tecnologia",
            "Curiosidades",
            "Mistérios",
            "Ciência",
            "História",
            "Outro",
        ])

        form_layout.addRow("Nome:", self.name_input)
        form_layout.addRow("Tema:", self.topic_input)
        form_layout.addRow("Categoria:", self.category_input)

        layout.addWidget(form_frame)

        self.create_button = QPushButton(
            "🎬  Criar projeto"
        )

        self.create_button.setObjectName("primaryButton")
        self.create_button.clicked.connect(
            self._create_project
        )

        layout.addWidget(self.create_button)

        layout.addStretch()

    def _create_project(self):
        name = self.name_input.text().strip()
        topic = self.topic_input.text().strip()
        category = self.category_input.currentText()

        if not name:
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Digite o nome do projeto.",
            )
            return

        if not topic:
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Digite o tema do projeto.",
            )
            return

        try:
            ProjectService.create_project(
                name=name,
                topic=topic,
                category=category,
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível criar o projeto:\n\n{error}",
            )
            return

        QMessageBox.information(
            self,
            "Projeto criado",
            "O projeto foi criado com sucesso!",
        )

        self.name_input.clear()
        self.topic_input.clear()

        self.project_created.emit()
