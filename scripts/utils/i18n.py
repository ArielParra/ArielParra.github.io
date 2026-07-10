def get_i18n_field(value, page_lang='en'):
    """Extract value from i18n object or string."""
    if isinstance(value, dict):
        return value.get(page_lang, value.get('en', ''))
    return value


def get_i18n_tags(value):
    """Get i18n tags string from object or plain value."""
    if isinstance(value, dict):
        en = value.get('en', '')
        es = value.get('es', en)
        if en and es:
            return f"((en)){en}((/en))((es)){es}((/es))"
        return en
    if isinstance(value, str):
        if '((en))' in value or '((es))' in value:
            return value
        return value
    return str(value) if value else ""


def format_date_i18n(date_str):
    """Convert date like 2025-04 to April 2025 / Abril 2025."""
    if not date_str:
        return ""

    en_months = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    es_months = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    parts = date_str.split("-")
    if len(parts) >= 2:
        year = parts[0]
        try:
            month = int(parts[1])
        except ValueError:
            return date_str

        en_month = en_months[month] if 1 <= month <= 12 else ""
        es_month = es_months[month] if 1 <= month <= 12 else ""

        if en_month and es_month:
            return f"((en)){en_month} {year}((/en))((es)){es_month} {year}((/es))"

    return date_str
