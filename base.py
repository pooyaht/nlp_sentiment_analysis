import re
import unicodedata


def persian_text_preprocessing(text, stop_words=None):
    if not isinstance(text, str):
        return ""

    text = unicodedata.normalize('NFC', text)

    persian_char_map = {
        # Arabic Kaf to Persian Kaf
        'ك': 'ک',  # U+0643 -> U+06A9
        '\u0643': '\u06A9',

        # Arabic Yeh variants to Persian Yeh
        'ي': 'ی',  # U+064A -> U+06CC
        '\u064A': '\u06CC',
        'ى': 'ی',  # U+0649 -> U+06CC
        '\u0649': '\u06CC',

        # Hamza variants
        'ء': 'ئ',  # U+0621 -> U+0626
        '\u0621': '\u0626',

        # Heh variants
        'ه': 'ه',  # Ensure consistent Heh
        'ة': 'ه',  # Teh Marbuta to Heh
        '\u0629': '\u0647',

        # Alef variants to standard Alef
        'أ': 'ا',  # U+0623 -> U+0627
        'إ': 'ا',  # U+0625 -> U+0627
        '\u0623': '\u0627',
        '\u0625': '\u0627',

        # Zero Width Non-Joiner and Joiner normalization
        '\u200C': '\u200C',  # ZWNJ - keep as is but normalize
        '\u200D': '',        # ZWJ - remove

        # Other Arabic/Persian inconsistencies
        'ؤ': 'و',  # Waw with Hamza above
        '\u0624': '\u0648',
    }

    for old_char, new_char in persian_char_map.items():
        text = text.replace(old_char, new_char)

    # Persian digits to ASCII
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    ascii_digits = '0123456789'
    persian_to_ascii = str.maketrans(persian_digits, ascii_digits)
    text = text.translate(persian_to_ascii)

    # Arabic-Indic digits to ASCII
    arabic_digits = '٠١٢٣٤٥٦٧٨٩'
    arabic_to_ascii = str.maketrans(arabic_digits, ascii_digits)
    text = text.translate(arabic_to_ascii)

    punctuation_map = {
        '؟': '?',   # Arabic question mark
        '؛': ';',   # Arabic semicolon
        '،': ',',   # Arabic comma
        '٪': '%',   # Arabic percent
        '٫': ',',   # Arabic decimal separator
        '٬': ',',   # Arabic thousands separator
    }

    for old_punct, new_punct in punctuation_map.items():
        text = text.replace(old_punct, new_punct)

    # Remove control characters except useful ones
    text = ''.join(char for char in text if unicodedata.category(
        char) != 'Cc' or char in '\n\t')

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\t+', ' ', text)

    text = text.strip()

    if len(text) == 0:
        return ""

    if stop_words is not None:
        stop_words_lower = [word.lower() for word in stop_words]
        words = text.split()
        words = [word for word in words if word not in stop_words_lower]
        text = ' '.join(words)

    text = unicodedata.normalize('NFC', text)

    return text
