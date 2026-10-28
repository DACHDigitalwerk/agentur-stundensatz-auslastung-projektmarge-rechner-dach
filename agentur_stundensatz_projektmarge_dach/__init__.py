"""DACH Agentur-, Consulting- & IT-Dienstleister Stundensatz-, KSK (5,0 %) & Projektmarge-Engine 2026."""
from .calculator import DEFAULT_ONCOST_FACTOR, KSK_RATE_DE_2026, AgencyProjectInput, AgencyProjectResult, calculate_agency_margin

__all__ = [
    "DEFAULT_ONCOST_FACTOR",
    "KSK_RATE_DE_2026",
    "AgencyProjectInput",
    "AgencyProjectResult",
    "calculate_agency_margin",
]
__version__ = "1.0.0"
