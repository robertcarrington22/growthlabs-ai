"""
Industry-specific analysis dispatcher for GrowthLabs AI.
Detects industry and routes to the appropriate module.

Each industry module under analysis/industries/ is independently testable:
    python -m analysis.industries.professional_services
    python -m analysis.industries.saas
    python -m analysis.industries.local_services
    python -m analysis.industries.ecommerce
    python -m analysis.industries.b2b_manufacturing
"""

import pandas as pd
from typing import Optional

from analysis.industries.professional_services import analyze as analyze_professional_services
from analysis.industries.saas import analyze as analyze_saas
from analysis.industries.local_services import analyze as analyze_local_services
from analysis.industries.ecommerce import analyze as analyze_ecommerce
from analysis.industries.b2b_manufacturing import analyze as analyze_b2b_manufacturing


INDUSTRY_MAP = {
    "professional_services": analyze_professional_services,
    "digital_agency": analyze_professional_services,
    "consulting": analyze_professional_services,
    "legal_services": analyze_professional_services,
    "accounting": analyze_professional_services,
    "saas": analyze_saas,
    "tech": analyze_saas,
    "software": analyze_saas,
    "local_services": analyze_local_services,
    "healthcare": analyze_local_services,
    "real_estate": analyze_local_services,
    "education": analyze_local_services,
    "hospitality": analyze_local_services,
    "ecommerce": analyze_ecommerce,
    "e-commerce": analyze_ecommerce,
    "retail": analyze_ecommerce,
    "manufacturing": analyze_b2b_manufacturing,
    "distribution": analyze_b2b_manufacturing,
    "b2b": analyze_b2b_manufacturing,
    "wholesale": analyze_b2b_manufacturing,
}


def detect_industry(transactions: pd.DataFrame, customers: pd.DataFrame) -> str:
    """Auto-detect industry from customer data, default to generic."""
    if len(customers) > 0 and "industry" in customers.columns:
        inds = customers["industry"].dropna()
        if len(inds) > 0:
            return inds.value_counts().index[0].lower().replace(" ", "_")
    return "generic"


def run_industry_analysis(transactions: pd.DataFrame, customers: pd.DataFrame, industry: Optional[str] = None) -> dict:
    """
    Run industry-specific analysis by dispatching to the correct module.

    Args:
        transactions: Transaction DataFrame
        customers: Customer DataFrame
        industry: Override industry (auto-detected if None)

    Returns:
        dict with industry analysis results
    """
    if industry is None:
        industry = detect_industry(transactions, customers)

    analyzer = INDUSTRY_MAP.get(industry)
    if analyzer:
        result = analyzer(transactions, customers)
    else:
        result = {"note": f"No specific analyzer for '{industry}'. Using generic analysis."}

    result["industry_detected"] = industry
    return result