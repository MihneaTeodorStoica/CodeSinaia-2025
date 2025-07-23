def roman_converter(num):
    if not isinstance(num, int):
        return None
    
    if num <= 0 or num >= 4000:
        return None
    
    ROMAN_NUMS = [
        (1, "I")
    ]

    out = ''
    while num >= 5:
        out += 'V'
        num -= 5
    while num >= 1:
        out += 'I'
        num -= 1

    return out