def roman_converter(value):
    if value is None:
        return None

    # Roman numeral lookup tables
    roman_numerals = [
        ("M", 1000), ("CM", 900), ("D", 500), ("CD", 400),
        ("C", 100),  ("XC", 90),  ("L", 50),  ("XL", 40),
        ("X", 10),   ("IX", 9),   ("V", 5),   ("IV", 4),
        ("I", 1)
    ]
    
    if isinstance(value, int):
        if not (1 <= value <= 3999):
            raise ValueError("Number must be between 1 and 3999")
        result = ""
        for roman, arabic in roman_numerals:
            while value >= arabic:
                result += roman
                value -= arabic
        return result

    elif isinstance(value, str):
        value = value.upper()
        i = 0
        result = 0
        while i < len(value):
            if i+1 < len(value) and value[i:i+2] in dict(roman_numerals):
                result += dict(roman_numerals)[value[i:i+2]]
                i += 2
            elif value[i] in dict(roman_numerals):
                result += dict(roman_numerals)[value[i]]
                i += 1
            else:
                raise ValueError("Invalid Roman numeral character")
        return result

    else:
        raise TypeError("Input must be int, str, or None")
