from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.ai.ollama_worker import OllamaWorker
from app.services.projects.project_service import ProjectService


class CreatorPage(QWidget):
    project_created = Signal()

    def __init__(self):
        super().__init__()

        self.current_niche_id: int | None = None
        self.current_subniche_id: int | None = None
        self.current_opportunity_id: int | None = None

        self.ai_thread: QThread | None = None
        self.ai_worker: OllamaWorker | None = None

        self._create_interface()

    def _create_interface(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)

        title = QLabel("Criar conteúdo")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Crie um novo projeto para o canal."
        )
        description.setObjectName("pageDescription")

        card = QFrame()
        card.setObjectName("card")

        form = QFormLayout()
        form.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Ex: 5 carros usados que ainda valem a pena"
        )

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText(
            "Tema principal do conteúdo"
        )

        self.category_input = QComboBox()
        self.category_input.addItems(
            [
                "Carros",
                "Motos",
                "Jogos",
                "Tecnologia",
                "Curiosidades",
                "Mistérios",
                "Ciência",
                "História",
                "Outro",
            ]
        )

        form.addRow(
            "Nome do projeto:",
            self.name_input,
        )

        form.addRow(
            "Tema:",
            self.topic_input,
        )

        form.addRow(
            "Categoria:",
            self.category_input,
        )

        card.setLayout(form)

        self.generate_button = QPushButton(
            "🤖  Gerar roteiro com IA"
        )

        self.generate_button.clicked.connect(
            self._generate_script
        )

        self.script_input = QTextEdit()

        self.script_input.setPlaceholderText(
            "O roteiro gerado pela IA aparecerá aqui..."
        )

        self.script_input.setMinimumHeight(300)

        self.create_button = QPushButton(
            "🎬  Criar projeto"
        )

        self.create_button.setObjectName(
            "primaryButton"
        )

        self.create_button.clicked.connect(
            self._create_project
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(card)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.script_input)
        layout.addWidget(self.create_button)
        layout.addStretch()

        self.setLayout(layout)

    def load_opportunity(
        self,
        title: str,
        topic: str,
        category: str,
        niche_id: int | None = None,
        subniche_id: int | None = None,
        opportunity_id: int | None = None,
    ):
        self.name_input.setText(title)
        self.topic_input.setText(topic)

        index = self.category_input.findText(
            category
        )

        if index >= 0:
            self.category_input.setCurrentIndex(
                index
            )
        else:
            self.category_input.setCurrentText(
                "Outro"
            )

        self.current_niche_id = niche_id
        self.current_subniche_id = subniche_id
        self.current_opportunity_id = opportunity_id

    def _generate_script(self):
        topic = self.topic_input.text().strip()
        category = self.category_input.currentText()

        if not topic:
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Digite o tema antes de gerar o roteiro.",
            )
            return

        prompt = f"""
Você é o roteirista principal do canal brasileiro
"Universo em uma Casca de Nós".

O canal produz vídeos de curiosidades, ciência, história,
tecnologia, carros, motos, jogos e assuntos interessantes
que despertem a curiosidade do público.

Crie um roteiro original para um vídeo do YouTube.

Categoria: {category}
Tema: {topic}

Requisitos:
- Escreva em português brasileiro.
- Comece com um gancho forte nos primeiros segundos.
- Desenvolva o assunto de forma clara e interessante.
- Use narrativa, curiosidades e contexto.
- Evite informações inventadas.
- Não copie textos de outras fontes.
- Não use marcações como "[imagem]" ou "[música]".
- O texto deve funcionar bem para narração.
- Termine com uma conclusão que deixe uma ideia marcante.
- Não diga que o texto foi escrito por inteligência artificial.

Produza apenas o roteiro.
"""

        self.generate_button.setEnabled(False)

        self.generate_button.setText(
            "⏳  Gerando roteiro..."
        )

        self.script_input.setPlainText(
            "A IA está trabalhando no roteiro...\n\n"
            "Isso pode levar alguns minutos."
        )

        self.ai_thread = QThread()
        self.ai_worker = OllamaWorker(prompt)

        self.ai_worker.moveToThread(
            self.ai_thread
        )

        self.ai_thread.started.connect(
            self.ai_worker.run
        )

        self.ai_worker.finished.connect(
            self._on_script_generated
        )

        self.ai_worker.error.connect(
            self._on_script_error
        )

        self.ai_worker.finished.connect(
            self.ai_thread.quit
        )

        self.ai_worker.error.connect(
            self.ai_thread.quit
        )

        self.ai_thread.finished.connect(
            self._cleanup_ai_thread
        )

        self.ai_thread.start()

    def _on_script_generated(
        self,
        script: str,
    ):
        self.script_input.setPlainText(
            script
        )

        self.generate_button.setEnabled(
            True
        )

        self.generate_button.setText(
            "🤖  Gerar roteiro com IA"
        )

    def _on_script_error(
        self,
        error: str,
    ):
        self.script_input.clear()

        self.generate_button.setEnabled(
            True
        )

        self.generate_button.setText(
            "🤖  Gerar roteiro com IA"
        )

        QMessageBox.critical(
            self,
            "Erro ao gerar roteiro",
            "Não foi possível gerar o roteiro.\n\n"
            f"{error}",
        )

    def _cleanup_ai_thread(self):
        if self.ai_worker is not None:
            self.ai_worker.deleteLater()

        if self.ai_thread is not None:
            self.ai_thread.deleteLater()

        self.ai_worker = None
        self.ai_thread = None

    def _create_project(self):
        name = self.name_input.text().strip()
        topic = self.topic_input.text().strip()
        category = self.category_input.currentText()

        script = self.script_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Digite um nome para o projeto.",
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
            project = ProjectService.create_project(
                name=name,
                topic=topic,
                category=category,
                niche_id=self.current_niche_id,
                subniche_id=self.current_subniche_id,
                opportunity_id=self.current_opportunity_id,
                script=script or None,
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro",
                "Não foi possível criar o projeto.\n\n"
                f"{error}",
            )
            return

        QMessageBox.information(
            self,
            "Projeto criado",
            f"O projeto #{project.id} foi criado com sucesso!\n\n"
            "O roteiro também foi salvo.",
        )

        self.name_input.clear()
        self.topic_input.clear()
        self.script_input.clear()

        self.current_niche_id = None
        self.current_subniche_id = None
        self.current_opportunity_id = None

        self.project_created.emit()
