from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.niches.niche_service import NicheService
from app.services.opportunities.opportunity_service import (
    OpportunityService,
)
from app.services.subniches.subniche_service import (
    SubnicheService,
)


class OpportunitiesPage(QWidget):

    opportunity_create_project_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self._create_interface()
        self._load_niches()
        self._load_opportunities()

    def _create_interface(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        # -------------------------------------------------
        # Título
        # -------------------------------------------------

        title = QLabel("🔥 Radar de Ideias")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Encontre oportunidades de conteúdo "
            "e transforme boas ideias em projetos."
        )
        description.setObjectName("pageDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        # -------------------------------------------------
        # Filtros
        # -------------------------------------------------

        filters_layout = QHBoxLayout()

        self.niche_combo = QComboBox()

        self.niche_combo.setPlaceholderText(
            "Todos os nichos"
        )

        self.subniche_combo = QComboBox()

        self.subniche_combo.setPlaceholderText(
            "Todos os subnichos"
        )

        self.search_button = QPushButton(
            "🔎 Buscar"
        )

        filters_layout.addWidget(
            self.niche_combo
        )

        filters_layout.addWidget(
            self.subniche_combo
        )

        filters_layout.addWidget(
            self.search_button
        )

        layout.addLayout(filters_layout)

        # -------------------------------------------------
        # Lista de oportunidades
        # -------------------------------------------------

        self.opportunity_list = QListWidget()

        self.opportunity_list.itemSelectionChanged.connect(
            self._on_opportunity_selected
        )

        layout.addWidget(
            self.opportunity_list
        )

        # -------------------------------------------------
        # Botão criar projeto
        # -------------------------------------------------

        self.create_project_button = QPushButton(
            "🎬 Criar projeto com esta ideia"
        )

        self.create_project_button.setEnabled(
            False
        )

        self.create_project_button.clicked.connect(
            self._create_project_from_opportunity
        )

        layout.addWidget(
            self.create_project_button
        )

        # -------------------------------------------------
        # Eventos
        # -------------------------------------------------

        self.search_button.clicked.connect(
            self._search_opportunities
        )

        self.niche_combo.currentIndexChanged.connect(
            self._niche_changed
        )

    # =====================================================
    # Nichos
    # =====================================================

    def _load_niches(self):

        self.niche_combo.blockSignals(True)

        self.niche_combo.clear()

        self.niche_combo.addItem(
            "Todos os nichos",
            None,
        )

        niches = NicheService.get_niches()

        for niche in niches:

            self.niche_combo.addItem(
                niche.name,
                niche.id,
            )

        self.niche_combo.blockSignals(False)

        self._load_subniches()

    # =====================================================
    # Subnichos
    # =====================================================

    def _load_subniches(self):

        self.subniche_combo.blockSignals(True)

        self.subniche_combo.clear()

        self.subniche_combo.addItem(
            "Todos os subnichos",
            None,
        )

        niche_id = self.niche_combo.currentData()

        if niche_id is not None:

            subniches = (
                SubnicheService.get_subniches(
                    niche_id
                )
            )

            for subniche in subniches:

                self.subniche_combo.addItem(
                    subniche.name,
                    subniche.id,
                )

        self.subniche_combo.blockSignals(False)

    # =====================================================
    # Mudança de nicho
    # =====================================================

    def _niche_changed(self):

        self._load_subniches()

    # =====================================================
    # Carregar oportunidades
    # =====================================================

    def _load_opportunities(
        self,
        niche_id=None,
        subniche_id=None,
    ):

        self.opportunity_list.clear()

        opportunities = (
            OpportunityService.get_opportunities(
                niche_id=niche_id,
                subniche_id=subniche_id,
            )
        )

        niches = {
            niche.id: niche.name
            for niche in NicheService.get_niches()
        }

        for opportunity in opportunities:

            item = QListWidgetItem()

            niche_name = niches.get(
                opportunity.niche_id,
                "Sem nicho",
            )

            text = (
                f"{opportunity.title}\n"
                f"{opportunity.description or ''}\n"
                f"📂 {niche_name} "
                f"• Potencial: "
                f"{opportunity.potential} "
                f"• Status: "
                f"{opportunity.status}"
            )

            item.setText(text)

            item.setData(
                Qt.UserRole,
                opportunity.id,
            )

            self.opportunity_list.addItem(
                item
            )

        self.create_project_button.setEnabled(
            False
        )

    # =====================================================
    # Buscar
    # =====================================================

    def _search_opportunities(self):

        niche_id = (
            self.niche_combo.currentData()
        )

        subniche_id = (
            self.subniche_combo.currentData()
        )

        self._load_opportunities(
            niche_id=niche_id,
            subniche_id=subniche_id,
        )

    # =====================================================
    # Seleção de oportunidade
    # =====================================================

    def _on_opportunity_selected(self):

        has_selection = bool(
            self.opportunity_list.selectedItems()
        )

        self.create_project_button.setEnabled(
            has_selection
        )

    # =====================================================
    # Criar projeto a partir da oportunidade
    # =====================================================

    def _create_project_from_opportunity(self):

        selected_items = (
            self.opportunity_list.selectedItems()
        )

        if not selected_items:
            return

        item = selected_items[0]

        opportunity_id = item.data(
            Qt.UserRole
        )

        if opportunity_id is None:
            return

        self.opportunity_create_project_requested.emit(
            opportunity_id
        )
