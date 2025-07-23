import unittest
from roman_converter import roman_converter

class TestInvalidInput(unittest.TestCase):
    # ======== Step 1 ======== no input, return None
    def test_no_input(self):
        self.assertEqual(roman_converter(None), None)

    # ======== Step 2 ======== wrong type, return None
    def test_string_input(self):
        self.assertEqual(roman_converter('lol'), None)
    
    def test_float_input(self):
        self.assertEqual(roman_converter(2.5), None)

    # ======== Step 3 ======== test valid range
    def test_out_of_range_zero(self):
        self.assertEqual(roman_converter(0), None)

    def test_out_of_range_large(self):
        self.assertEqual(roman_converter(4000), None)


class TestOnes(unittest.TestCase):
    # ======== Step 4 ======== test 1, return 'I'
    def test_base_1(self):
        self.assertEqual(roman_converter(1), 'I')
    
    # ======== Step 5 ======== test 2 to 4, return 'II' to 'IIII'
    def test_two(self):
        self.assertEqual(roman_converter(2), 'II')

    def test_three(self):
        self.assertEqual(roman_converter(3), 'III')

    def test_four(self):
        self.assertEqual(roman_converter(4), 'IIII')

class TestFives(unittest.TestCase):
    # ======== Step 6 ======== test 5 and 6-9, return 'V' to 'VIIII'
    def test_five(self):
        self.assertEqual(roman_converter(5), 'V')

    def test_six_to_nine(self):
        self.assertEqual(roman_converter(6), 'VI')
        self.assertEqual(roman_converter(9), 'VIIII')


# ======== Step 7 ======== generalize for X, L, C, M
class TestTens(unittest.TestCase):
    def test_base_10(self):
        self.assertEqual(roman_converter(10), 'X')

    def test_mid_25(self):
        self.assertEqual(roman_converter(25), 'XXV')

    def test_max_49(self):
        self.assertEqual(roman_converter(49), 'XXXXVIIII')

class TestFifties(unittest.TestCase):
    def test_base_50(self):
        self.assertEqual(roman_converter(50), 'L')

    def test_mid_75(self):
        self.assertEqual(roman_converter(75), 'LXXV')

    def test_max_99(self):
        self.assertEqual(roman_converter(99), 'LXXXXVIIII')

class TestHundreds(unittest.TestCase):
    def test_base_100(self):
        self.assertEqual(roman_converter(100), 'C')

    def test_mid_555(self):
        self.assertEqual(roman_converter(555), 'CCCCCLV')

    def test_max_999(self):
        self.assertEqual(roman_converter(999), 'CCCCCCCCCLXXXXVIIII')

class TestThousands(unittest.TestCase):
    def test_base_1000(self):
        self.assertEqual(roman_converter(1000), 'M')

    def test_mid_2555(self):
        self.assertEqual(roman_converter(2555), 'MMCCCCCLV')

    def test_max_3999(self):
        self.assertEqual(roman_converter(3999), 'MMMCCCCCCCCCLXXXXVIIII')

if __name__ == '__main__':
    unittest.main()

