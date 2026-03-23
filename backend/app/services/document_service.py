from datetime import datetime
from typing import Any

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML  # type: ignore[import-untyped]

from app.core.config import settings
from app.utils import format_currency

RISK_NOTE_TEMPLATES = {
    "motor private": "documents/motor_private.html",
}


def generate_risknote_html(
    risk_note: Any, client: Any, policy: Any, invoice: Any = None
) -> str:
    """
    Generates the HTML content for a Risk Note using Jinja2.
    """
    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader(settings.TEMPLATES_DIR))
    env.filters["format_currency"] = format_currency

    # Template Selection Logic
    template_path = RISK_NOTE_TEMPLATES.get(
        (policy.product.class_of_insurance or "").lower(), "documents/risknote.html"
    )
    template = env.get_template(template_path)

    # 1. Consolidate Dynamic Sections
    # Product template provides the structure/schema
    product_template = policy.product.product_details or {}
    # Instance snapshot provides the actual values
    instance = risk_note.cover_snapshot or {}

    dynamic_sections = []
    manual_sections = [
        "INSURED",
        "CLASS",
        "PERIOD",
        "COVER",
        "ANNUAL PREMIUM",
        "FINANCIAL SUMMARY",
        "INSURER",
        "AUTHENTICATION",
    ]

    # Process sections defined in the product template
    for name, template_content in product_template.items():
        upper_name = name.upper()
        if upper_name not in manual_sections:
            # Look for content in top-level or inside 'terms' dictionary
            instance_content = (
                instance.get(name)
                or instance.get(upper_name)
                or instance.get("terms", {}).get(name)
                or instance.get("terms", {}).get(name.lower().replace(" ", "_"))
            )

            merged_content = template_content
            if isinstance(template_content, dict):
                merged_content = template_content.copy()
                if isinstance(instance_content, dict):
                    for k, v in instance_content.items():
                        if v not in [None, "", "[ EMPTY ]"]:
                            merged_content[k] = v

                # Special mapping for Sum Insured
                sum_insured = instance.get("sum_insured")
                if sum_insured not in [None, "[ EMPTY ]"]:
                    merged_content["Value Kshs."] = format_currency(sum_insured)
            elif instance_content not in [None, "[ EMPTY ]"]:
                merged_content = instance_content

            dynamic_sections.append({"name": upper_name, "content": merged_content})

    # Add any sections from instance that weren't in template
    for name, content in instance.items():
        upper_name = name.upper()
        if (
            upper_name not in manual_sections
            and name != "terms"
            and not any(s["name"] == upper_name for s in dynamic_sections)
        ):
            dynamic_sections.append({"name": upper_name, "content": content})

    # Add any terms from the 'terms' dictionary not yet covered
    if "terms" in instance:
        for name, content in instance["terms"].items():
            upper_name = name.upper().replace("_", " ")
            if not any(s["name"] == upper_name for s in dynamic_sections):
                dynamic_sections.append({"name": upper_name, "content": content})

    # 2. Prepare Financial Breakdown
    # Ensure it has the expected structure for the template
    breakdown = risk_note.financial_breakdown or {}
    financial_summary = {
        "benefits": breakdown.get("benefits", []),
        "taxes": breakdown.get("taxes", {}),
    }

    # 3. Render HTML
    context = {
        "risk_note": risk_note,
        "client": client,
        "policy": policy,
        "invoice": invoice,
        "dynamic_sections": dynamic_sections,
        "financial_breakdown": financial_summary,
        "current_date": datetime.now().strftime("%d/%m/%Y"),
    }

    return template.render(context)


def generate_risknote_pdf(
    risk_note: Any, client: Any, policy: Any, invoice: Any = None
) -> bytes:
    """
    Generates a Risk Note PDF using WeasyPrint and Jinja2.
    Mirrors the data consolidation logic from the frontend RiskNoteTemplate.tsx.
    """
    html_content = generate_risknote_html(risk_note, client, policy, invoice)

    from typing import cast
    # Generate PDF bytes
    # base_url allows WeasyPrint to resolve relative paths if needed
    pdf_bytes = cast(bytes, HTML(string=html_content).write_pdf())

    return pdf_bytes
