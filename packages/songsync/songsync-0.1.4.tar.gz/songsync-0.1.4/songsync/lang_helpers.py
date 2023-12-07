"""Language helpers"""
import re
import langid

# Mapping of ISO 639-1 language codes to ISO 3166-1 alpha-2 country codes
# List of ISO 639-1 codes: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
# List of ISO 3166-1 alpha-2 codes: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
# TODO: Add the rest of the Spotify markets from https://developer.spotify.com/documentation/web-api/reference/get-available-markets
LANG_TO_COUNTRY_MAP = {
    "en": ["US", "GB"],
    "es": ["ES"],
    "fr": ["FR"],
    "de": ["DE"],
    "ru": ["RU"],
    # Note: Spotify does not have a market in China
    "zh": ["TW", "SG"],
    "ko": ["KR"],
    "ja": ["JP"],
    "hi": ["IN"],
    "ar": ["SA"],
    "pt": ["BR"],
    "bn": ["BD"],
    "id": ["ID"],
    "vi": ["VN"],
}


def detect_languages(text: str) -> set[str]:
    """Find potential languages in text

    Args:
        text (str): Text to parse

    Returns:
        set[str]: Set of potential languages
    """
    words = text.split()
    detected_languages = set()

    # Detect language of entire text
    lang, _ = langid.classify(text)
    detected_languages.add(lang)

    for word in words:
        # Detect the language of the current word
        lang, _ = langid.classify(word)
        detected_languages.add(lang)
    return detected_languages


def get_country_codes_from_langs(language_codes: set[str]) -> set[str]:
    """Convert ISO 639-1 language codes to ISO 3166-1 alpha-2 country codes

    Args:
        language_codes (set[str]): language codes

    Returns:
        set[str]: country codes
    """
    country_codes = set()
    for language_code in language_codes:
        lang_code = language_code.lower()
        if lang_code in LANG_TO_COUNTRY_MAP:
            country_codes.update(LANG_TO_COUNTRY_MAP[lang_code])
    return country_codes


def get_country_codes_from_text(text: str):
    """Get possible country codes from text

    Args:
        text (str): Text to parse

    Returns:
        set[str]: Possible country codes
    """
    lang_codes = detect_languages(text)
    return get_country_codes_from_langs(lang_codes)


def split_text_by_language(text: str):
    """Split text by language

    Args:
        text (str): Text to split

    Returns:
        list[str]: Substrings of text divided by language
    """
    # Remove everything after feat. since the track name is often before artist features in the title)
    text = text.split("feat.")[0]

    cleaned_text = re.sub(r"[\(\)\[\]「」【】]", "", text)
    substrings = re.split(r"([a-zA-Z]+)", cleaned_text)
    return [s for s in substrings if s and s.strip()]
