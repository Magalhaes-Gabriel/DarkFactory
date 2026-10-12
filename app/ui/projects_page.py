from PySide6.QtCore import QThread, Slot
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.projects.project_service import ProjectService
from app.services.narration.narration_worker import (
    NarrationWorker,
)


class ProjectsPage(QWidget):
    PROJECT_ID_ROLE = 1000

    def __init__(self):
        super().__init__()

        self.current_project_id: int | None = None
        self.current_project_status = "draft"

        self.narration_thread: QThread | None = None
        self.narration_worker: NarrationWorker | None = None
        self.narration_project_id: int | None = None

        self._create_interface()
        self.refresh()

    def _create_interface(self):
        self.stack = QStackedWidget()

        root_layout = QVBoxLayout(self)
        root_layout.addWidget(self.stack)

        self._create_list_page()
        self._create_editor_page()

        self.stack.addWidget(self.list_page)
        self.stack.addWidget(self.editor_page)

        self.stack.setCurrentWidget(self.list_page)

    def _create_list_page(self):
        self.list_page = QWidget()
        layout = QVBoxLayout(self.list_page)
        layout.setSpacing(20)

        title = QLabel("Projetos")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Todos os projetos do Universo em uma Casca de Nós."
        )
        description.setObjectName("pageDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        toolbar = QHBoxLayout()

        self.refresh_button = QPushButton("↻  Atualizar")
        self.refresh_button.clicked.connect(self.refresh)

        toolbar.addWidget(self.refresh_button)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        self.project_list = QListWidget()
        self.project_list.setObjectName("projectList")
        self.project_list.itemDoubleClicked.connect(
            self._open_selected_project
        )

        layout.addWidget(self.project_list)

        hint = QLabel(
            "Dê dois cliques em um projeto para abrir o editor."
        )
        hint.setObjectName("pageDescription")
        layout.addWidget(hint)

    def _create_editor_page(self):
        self.editor_page = QWidget()
        layout = QVBoxLayout(self.editor_page)
        layout.setSpacing(16)

        title = QLabel("Editar projeto")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        description = QLabel(
            "Revise o roteiro e gere a narração do projeto."
        )
        description.setObjectName("pageDescription")
        layout.addWidget(description)

        form = QFormLayout()
        form.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setReadOnly(True)

        self.topic_input = QLineEdit()
        self.topic_input.setReadOnly(True)

        self.category_input = QLineEdit()
        self.category_input.setReadOnly(True)

        self.status_label = QLabel("draft")

        form.addRow("Nome:", self.name_input)
        form.addRow("Tema:", self.topic_input)
        form.addRow("Categoria:", self.category_input)
        form.addRow("Status:", self.status_label)

        layout.addLayout(form)

        script_title = QLabel("Roteiro")
        script_title.setObjectName("sectionTitle")
        layout.addWidget(script_title)

        self.script_input = QTextEdit()
        self.script_input.setPlaceholderText(
            "O roteiro deste projeto aparecerá aqui..."
        )
        self.script_input.setMinimumHeight(400)

        layout.addWidget(self.script_input)

        self.audio_path_label = QLabel("")
        self.audio_path_label.setWordWrap(True)
        layout.addWidget(self.audio_path_label)

        buttons = QHBoxLayout()

        self.back_button = QPushButton("← Voltar")
        self.back_button.clicked.connect(
            self._return_to_projects
        )

        self.save_button = QPushButton("💾  Salvar roteiro")
        self.save_button.setObjectName("primaryButton")
        self.save_button.clicked.connect(
            self._save_current_script
        )

        self.narration_button = QPushButton(
            "🎙  Gerar narração"
        )
        self.narration_button.setObjectName("primaryButton")
        self.narration_button.clicked.connect(
            self._generate_current_narration
        )

        buttons.addWidget(self.back_button)
        buttons.addStretch()
        buttons.addWidget(self.save_button)
        buttons.addWidget(self.narration_button)

        layout.addLayout(buttons)

    def refresh(self):
        self.project_list.clear()

        projects = ProjectService.get_projects()

        if not projects:
            self.project_list.addItem(
                QListWidgetItem("Nenhum projeto criado ainda.")
            )
            return

        for project in projects:
            item = QListWidgetItem(
                f"{project.name}\n"
                f"📌 {project.topic}   "
                f"•   {project.category}   "
                f"•   {project.status}"
            )

            item.setData(
                self.PROJECT_ID_ROLE,
                project.id,
            )

            self.project_list.addItem(item)

    def _open_selected_project(
        self,
        item: QListWidgetItem,
    ):
        project_id = item.data(self.PROJECT_ID_ROLE)

        if project_id is None:
            return

        self._open_project(project_id)

    def _open_project(self, project_id: int):
        project = ProjectService.get_project(project_id)

        if project is None:
            QMessageBox.warning(
                self,
                "Projeto não encontrado",
                "O projeto selecionado não existe mais.",
            )
            self.refresh()
            return

        self.current_project_id = project.id
        self.current_project_status = project.status

        self.name_input.setText(project.name)
        self.topic_input.setText(project.topic)
        self.category_input.setText(project.category)
        self.status_label.setText(project.status)
        self.script_input.setPlainText(project.script or "")

        audio_path = (
            self._get_audio_path(project.id)
        )

        if audio_path.is_file():
            self.audio_path_label.setText(
                f"Áudio existente: {audio_path}"
            )
        else:
            self.audio_path_label.setText(
                "Nenhuma narração gerada para este projeto."
            )

        self.stack.setCurrentWidget(self.editor_page)

    def _get_audio_path(self, project_id: int):
        from app.database.database import PROJECT_ROOT

        return (
            PROJECT_ROOT
            / "data"
            / "projects"
            / f"project_{project_id}"
            / "narration.wav"
        )

    def _save_current_script(self):
        if self.current_project_id is None:
            return

        script = self.script_input.toPlainText().strip()

        if not script:
            QMessageBox.warning(
                self,
                "Roteiro vazio",
                "Digite algum conteúdo antes de salvar.",
            )
            return

        try:
            project = ProjectService.update_script(
                self.current_project_id,
                script,
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro ao salvar",
                f"Não foi possível salvar o roteiro.\n\n{error}",
            )
            return

        if project is None:
            QMessageBox.warning(
                self,
                "Projeto não encontrado",
                "O projeto não existe mais.",
            )
            return

        QMessageBox.information(
            self,
            "Roteiro salvo",
            "O roteiro foi salvo com sucesso.",
        )

    def _return_to_projects(self):
        self.refresh()
        self.stack.setCurrentWidget(self.list_page)

    def _generate_current_narration(self):
        project_id = self.current_project_id
        self.narration_project_id = project_id

        if project_id is None:
            return

        if self.narration_thread is not None:
            QMessageBox.information(
                self,
                "Narração em andamento",
                "Aguarde a narração atual terminar.",
            )
            return

        script = self.script_input.toPlainText().strip()

        if not script:
            QMessageBox.warning(
                self,
                "Roteiro vazio",
                "Escreva ou gere um roteiro antes de narrar.",
            )
            return

        # Salva as alterações antes de iniciar o áudio.
        try:
            project = ProjectService.update_script(
                project_id,
                script,
            )

            if project is None:
                raise ValueError(
                    "O projeto não foi encontrado."
                )

            ProjectService.update_status(
                project_id,
                "narration_generating",
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro ao preparar narração",
                f"Não foi possível salvar o roteiro.\n\n{error}",
            )
            return

        self.current_project_status = "script_ready"
        self.status_label.setText("narration_generating")
        self.audio_path_label.setText(
            "Gerando áudio. Isso pode levar alguns minutos..."
        )

        self.narration_button.setEnabled(False)
        self.narration_button.setText(
            "⏳  Gerando narração..."
        )
        self.save_button.setEnabled(False)

        thread = QThread(self)
        worker = NarrationWorker(
            project_id=project_id,
            script=script,
        )
        worker.moveToThread(thread)

        self.narration_thread = thread
        self.narration_worker = worker

        thread.started.connect(worker.run)

        worker.finished.connect(self._on_narration_generated)
        worker.error.connect(self._on_narration_error)

        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)

        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(self._cleanup_narration_thread)
        thread.finished.connect(thread.deleteLater)

        thread.start()

    @Slot(str)
    def _on_narration_generated(self, output_path: str):
        project_id = self.narration_project_id

        # O usuário pode ter navegado para outro projeto
        # enquanto a geração estava em andamento.
        if project_id is not None:
            audio_path = self._get_audio_path(project_id)

            if str(audio_path) == output_path:
                ProjectService.update_status(
                    project_id,
                    "narration_ready",
                )
                self.current_project_status = "narration_ready"
                self.status_label.setText("narration_ready")
                self.audio_path_label.setText(
                    f"Narração pronta: {output_path}"
                )

        self._finish_narration_controls()
        self.refresh()

        QMessageBox.information(
            self,
            "Narração concluída",
            "A narração foi criada com sucesso!\n\n"
            f"Arquivo:\n{output_path}",
        )

    @Slot(str)
    def _on_narration_error(self, error: str):
        project_id = self.narration_project_id

        if project_id is not None:
            ProjectService.update_status(
                project_id,
                "script_ready",
            )
            self.current_project_status = "script_ready"
            self.status_label.setText("script_ready")
            self.audio_path_label.setText(
                "A geração falhou. Corrija o problema e tente novamente."
            )

        self._finish_narration_controls()
        self.refresh()

        QMessageBox.critical(
            self,
            "Erro na narração",
            "Não foi possível gerar a narração.\n\n"
            f"{error}",
        )

    def _finish_narration_controls(self):
        self.narration_button.setEnabled(True)
        self.narration_button.setText("🎙  Gerar narração")
        self.save_button.setEnabled(True)

    @Slot()
    def _cleanup_narration_thread(self):
        self.narration_worker = None
        self.narration_thread = None