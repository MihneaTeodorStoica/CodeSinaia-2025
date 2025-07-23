def roman_converter(numeral):
    # ======== Step 1 ======== no input, return None
    # return None

    # ======== Step 2 ======== wrong type, return None
    if not isinstance(numeral, int):
        return None
    
    # ======== Step 3 ======== test valid range
    if numeral < 1 or numeral > 3999:
        return None
    
    # ======== Step 4 ======== test 1, return 'I'
    # if numeral == 1:
    #     return "I"

    # ======== Step 5 ======== test 2 to 4, return 'II' to 'IIII'
    out = ''
    num = numeral

    # while num >= 1:
    #     out += 'I'
    #     num -= 1

    # ======== Step 6 ======== test 5 and 6-9, return 'V' to 'VIIII'
    # while num >= 5:
    #     out += 'V'
    #     num -= 5
    # while num >= 1:
    #     out += 'I'
    #     num -= 1

    # ======== Step 7 ======== generalize for X, L, C, M
    ROMAN_VALUES = [
        (1000, 'M'),
        (100, 'C'),
        (50, 'L'),
        (10, 'X'),
        (5, 'V'),
        (1, 'I')
    ]

    for value, symbol in ROMAN_VALUES:
        while num >= value:
            out += symbol
            num -= value

    return out

