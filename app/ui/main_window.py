from app.ui.niches_page import NichesPage
from app.ui.creator_page import CreatorPage
from app.ui.projects_page import ProjectsPage
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dark Factory")
        self.setMinimumSize(1200, 700)

        self._create_interface()

    def _create_interface(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = self._create_sidebar()
        content = self._create_content()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

    def _create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 25, 20, 20)
        layout.setSpacing(8)

        title = QLabel("DARK FACTORY")
        title.setObjectName("appTitle")

        subtitle = QLabel("Universo em uma Casca de Nós")
        subtitle.setObjectName("appSubtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)

        self.buttons = {}

        self._add_menu_button(
            layout,
            "🏠  Dashboard",
            0,
            "dashboard",
        )

        self._add_menu_button(
            layout,
            "🔎  Explorar",
            1,
            "explorer",
        )

        self._add_menu_button(
            layout,
            "🎯  Nichos",
            2,
            "niches",
        )

        self._add_menu_button(
            layout,
            "🎬  Criar conteúdo",
            3,
            "creator",
        )

        self._add_menu_button(
            layout,
            "📁  Projetos",
            4,
            "projects",
        )

        layout.addStretch()

        self._add_menu_button(
            layout,
            "⚙  Configurações",
            5,
            "settings",
        )

        return sidebar

    def _add_menu_button(self, layout, text, index, name):
        button = QPushButton(text)
        button.setObjectName("menuButton")
        button.setCursor(Qt.PointingHandCursor)

        button.clicked.connect(
            lambda checked=False, i=index: self._change_page(i)
        )

        self.buttons[name] = button
        layout.addWidget(button)

    def _create_content(self):
        container = QFrame()
        container.setObjectName("content")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(35, 30, 35, 30)

        self.pages = QStackedWidget()

        self.creator_page = CreatorPage()
        self.projects_page = ProjectsPage()
        self.niches_page = NichesPage()

        self.creator_page.project_created.connect(
        self.projects_page.refresh
        )

        self.pages.addWidget(self._create_dashboard())
        self.pages.addWidget(
         self._create_placeholder("🔎 Explorar")
        )
        self.pages.addWidget(
            self.niches_page
        )
        self.pages.addWidget(self.creator_page)
        self.pages.addWidget(self.projects_page)
        self.pages.addWidget(
            self._create_placeholder("⚙ Configurações")
        )

        layout.addWidget(self.pages)

        return container

    def _create_dashboard(self):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        title = QLabel("Bom dia!")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Bem-vindo à central de produção do "
            "Universo em uma Casca de Nós."
        )
        description.setObjectName("pageDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addSpacing(20)

        cards_layout = QHBoxLayout()

        cards_layout.addWidget(
            self._create_card("🎯", "Nichos", "0")
        )

        cards_layout.addWidget(
            self._create_card("💡", "Ideias", "0")
        )

        cards_layout.addWidget(
            self._create_card("🎬", "Vídeos", "0")
        )

        cards_layout.addWidget(
            self._create_card("📱", "Shorts", "0")
        )

        layout.addLayout(cards_layout)

        layout.addSpacing(30)

        opportunities_title = QLabel("🔥 Oportunidades")
        opportunities_title.setObjectName("sectionTitle")

        layout.addWidget(opportunities_title)

        opportunity = QLabel(
            "Ainda não existem oportunidades pesquisadas.\n\n"
            "Use o módulo Explorar para encontrar novos temas."
        )
        opportunity.setObjectName("emptyState")

        layout.addWidget(opportunity)
        layout.addStretch()

        return page

    def _create_card(self, icon, title, value):
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)

        icon_label = QLabel(icon)
        icon_label.setObjectName("cardIcon")

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        value_label = QLabel(value)
        value_label.setObjectName("cardValue")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card

    def _create_placeholder(self, title):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel(title)
        label.setObjectName("placeholderTitle")

        description = QLabel("Módulo em desenvolvimento.")
        description.setObjectName("placeholderDescription")

        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(description, alignment=Qt.AlignCenter)

        return page

    def _change_page(self, index):
        self.pages.setCurrentIndex(index)
