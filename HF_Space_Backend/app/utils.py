import re

def is_sinhala(text):
    """Checks if the text contains Sinhala characters."""
    for char in text:
        if '\u0D80' <= char <= '\u0DFF':
            return True
    return False
    
def normalize_numbers(text):
    
    ABBREVIATIONS = {
        r"ෙප\.ව\.": "perawaru",
        r"ප\.ව\.": "paswaru",
    }

    CURRENCY_MAP = {
        r"(රු\.|RS\.|Rs\.)": " rupiyal ",
        r"\$": " dollar ",
        r"£": "pawum"
    }


    units = {
        0: "",
        1: " eka ",
        2: " deka ",
        3: " thuna ",
        4: " hathara ",
        5: " paha ",
        6: " haya ",
        7: " hatha ",
        8: " ata ",
        9: " nawaya "
    }

    tens = {
        2: " wisi ",
        3: " this ",
        4: " hathalis ",
        5: " panas ",
        6: " hata ",
        7: " hatha ",
        8: " asu ",
        9: " anu "
    }

    exact_0_to_20 = {
        0: " shunya ",
        1: " eka ",
        2: " deka ",
        3: " thuna ",
        4: " hathara ",
        5: " paha ",
        6: " haya ",
        7: " hatha ",
        8: " ata ",
        9: " navaya ",
        10: " daha ",
        11: " ekaloha ",
        12: " dolaha ",
        13: " dahathuna ",
        14: " dahahathara ",
        15: " pahalosa ",
        16: " dahasaya ",
        17: " dahahatha ",
        18: " dahaata ",
        19: " dahanavaya ",
        20: " wisi "
    }

    groups = [" ", " dahas ", " miliyana ", " biliyana ", " triliyana "]

    def convert_0_to_99(n):
        if n in exact_0_to_20:
            return exact_0_to_20[n]
        else:
            tens_digit = n // 10
            unit_digit = n % 10
            tens_text = tens.get(tens_digit, "")
            unit_text = units.get(unit_digit, "")
            return tens_text + unit_text

    def convert_group(n):
        if n == 0:
            return ""
        hundreds = n // 100
        remaining = n % 100
        text = ""
        if hundreds > 0:
            text += units[hundreds] + " siya "
        if remaining > 0:
            if text:
                text += " "
            text += convert_0_to_99(remaining)
        return text

    def number_to_text(number):
        if not number.isdigit():
            return number
        num = int(number)
        if num == 0:
            return " shunya "

        parts = []
        group_index = 0
        while num > 0:
            part = num % 1000
            if part != 0:
                group_text = convert_group(part)
                if group_index > 0:
                    group_text += " " + groups[group_index]
                parts.append(group_text)
            num //= 1000
            group_index += 1

        return " ".join(reversed(parts))

    def normalize_abbreviations(text):
        for abbr, pron in ABBREVIATIONS.items():
            text = re.sub(abbr, pron, text)
        return text

    def normalize_currency(text):
        for symbol, pron in CURRENCY_MAP.items():
            text = re.sub(symbol, pron, text)
        return text

    def normalize_decimals(text):
        def replace_decimal(match):
            whole = match.group(1)
            decimal = match.group(2)
            whole_text = number_to_text(whole)
            decimal_text = number_to_text(decimal)
            return f"{whole_text} dashama {decimal_text}"
        text = re.sub(r"(\d+)\.(\d+)", replace_decimal, text)
        return text

    def normalize_numbers(text):
        text = re.sub(r"(\d+)", lambda m: number_to_text(m.group(1)), text)
        return text

    def collapse_whitespaces(text):
        return re.sub(r"\s+", " ", text).strip()


    text = normalize_abbreviations(text)
    text = normalize_currency(text)
    text = normalize_decimals(text)
    text = normalize_numbers(text)
    # text = collapse_whitespaces(text)
    return text
