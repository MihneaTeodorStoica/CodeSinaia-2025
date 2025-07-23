def number_to_words(n):

    # ======== Step 1 ======== test 0, return 'zero'
    if n == 0:
        return "zero"

    # ======== Step 2 ======== test 1 to 9
    ONES = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine"
    ]

    if 0 < n < 10:
        return ONES[n]
    
    # ======== Step 3 ======== test 10 to 19

    TEENS = [
        "ten", "eleven", "twelve", "thirteen", "fourteen",
        "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"
    ]

    if 10 <= n < 20:
        return TEENS[n - 10]
    
    # ======== Step 4 ======== test 20 to 99
    TENS = [
        "", "", "twenty", "thirty", "forty", "fifty",
        "sixty", "seventy", "eighty", "ninety"
    ]

    if 20 <= n < 100:
        tens, ones = divmod(n, 10)
        return TENS[tens] + ("-" + ONES[ones] if ones else "")
    
    # ======== Step 5 ======== test 100 to 999
    if 100 <= n < 1000:
        hundreds, remainder = divmod(n, 100)
        rest = number_to_words(remainder) if remainder else ""
        return ONES[hundreds] + " hundred" + (" " + rest if rest else "")