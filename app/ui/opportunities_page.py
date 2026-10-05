from PySide6.QtCore import Signal
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

    opportunity_selected = Signal(int)

    def __init__(self):
        super().__init__()

        self._create_interface()
        self._load_niches()

    def _create_interface(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(20)

        title = QLabel(
            "🔥 Radar de Ideias"
        )

        title.setObjectName(
            "pageTitle"
        )

        description = QLabel(
            "Encontre e organize oportunidades "
            "de conteúdo para o canal."
        )

        description.setObjectName(
            "pageDescription"
        )

        layout.addWidget(title)
        layout.addWidget(description)

        filters = QHBoxLayout()

        self.niche_combo = QComboBox()

        self.niche_combo.currentIndexChanged.connect(
            self._niche_changed
        )

        filters.addWidget(
            self.niche_combo
        )

        self.subniche_combo = QComboBox()

        self.subniche_combo.currentIndexChanged.connect(
            self.refresh
        )

        filters.addWidget(
            self.subniche_combo
        )

        self.search_button = QPushButton(
            "🔎 Pesquisar"
        )

        self.search_button.setObjectName(
            "primaryButton"
        )

        self.search_button.clicked.connect(
            self.refresh
        )

        filters.addWidget(
            self.search_button
        )

        layout.addLayout(filters)

        self.opportunity_list = QListWidget()

        self.opportunity_list.setObjectName(
            "projectList"
        )

        layout.addWidget(
            self.opportunity_list
        )

        self.create_button = QPushButton(
            "🎬 Criar projeto com esta ideia"
        )

        self.create_button.setEnabled(
            False
        )

        layout.addWidget(
            self.create_button
        )

    def _load_niches(self):

        self.niche_combo.blockSignals(True)

        self.niche_combo.clear()

        niches = NicheService.get_niches()

        for niche in niches:

            self.niche_combo.addItem(
                niche.name,
                niche.id,
            )

        self.niche_combo.blockSignals(
            False
        )

        self._niche_changed()

    def _niche_changed(self):

        self.subniche_combo.blockSignals(
            True
        )

        self.subniche_combo.clear()

        niche_id = (
            self.niche_combo.currentData()
        )

        if niche_id is not None:

            self.subniche_combo.addItem(
                "Todos os subnichos",
                None,
            )

            subniches = (
                SubnicheService
                .get_subniches(niche_id)
            )

            for subniche in subniches:

                self.subniche_combo.addItem(
                    subniche.name,
                    subniche.id,
                )

        self.subniche_combo.blockSignals(
            False
        )

        self.refresh()

    def refresh(self):

        self.opportunity_list.clear()

        niche_id = (
            self.niche_combo.currentData()
        )

        subniche_id = (
            self.subniche_combo.currentData()
        )

        if niche_id is None:
            return

        opportunities = (
            OpportunityService
            .get_opportunities(
                niche_id=niche_id,
                subniche_id=subniche_id,
            )
        )

        if not opportunities:

            item = QListWidgetItem(
                "Nenhuma oportunidade encontrada."
            )

            self.opportunity_list.addItem(
                item
            )

            return

        for opportunity in opportunities:

            item = QListWidgetItem()

            item.setData(
                32,
                opportunity.id,
            )

            item.setText(
                f"🔥 {opportunity.title}\n\n"
                f"{opportunity.description or ''}\n\n"
                f"Potencial: "
                f"{opportunity.potential.upper()}\n"
                f"Status: "
                f"{opportunity.status}"
            )

            self.opportunity_list.addItem(
                item
            )
