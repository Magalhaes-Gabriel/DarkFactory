from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.projects.project_service import ProjectService


class ProjectsPage(QWidget):

    def __init__(self):
        super().__init__()

        self._create_interface()
        self.refresh()

    def _create_interface(self):
        layout = QVBoxLayout(self)
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

        self.refresh_button = QPushButton(
            "↻  Atualizar"
        )

        self.refresh_button.clicked.connect(
            self.refresh
        )

        toolbar.addWidget(self.refresh_button)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        self.project_list = QListWidget()
        self.project_list.setObjectName("projectList")

        layout.addWidget(self.project_list)

    def refresh(self):
        self.project_list.clear()

        projects = ProjectService.get_projects()

        if not projects:
            item = QListWidgetItem(
                "Nenhum projeto criado ainda."
            )

            self.project_list.addItem(item)

            return

        for project in projects:
            item = QListWidgetItem()

            item.setText(
                f"{project.name}\n"
                f"📌 {project.topic}   "
                f"•   {project.category}   "
                f"•   {project.status}"
            )

            self.project_list.addItem(item)
