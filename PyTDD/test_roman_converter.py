import unittest
from roman_converter import roman_converter

class TestRomanConverter(unittest.TestCase):
    def test_none(self):
        self.assertEqual(roman_converter(None), None)

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            roman_converter(10.5)
        with self.assertRaises(TypeError):
            roman_converter(["X"])

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            roman_converter(0)
        with self.assertRaises(ValueError):
            roman_converter(4000)

    def test_invalid_roman(self):
        with self.assertRaises(ValueError):
            roman_converter("INVALID")

    def test_arabic_to_roman(self):
        self.assertEqual(roman_converter(1), "I")
        self.assertEqual(roman_converter(4), "IV")
        self.assertEqual(roman_converter(44), "XLIV")
        self.assertEqual(roman_converter(3999), "MMMCMXCIX")

    def test_roman_to_arabic(self):
        self.assertEqual(roman_converter("I"), 1)
        self.assertEqual(roman_converter("IV"), 4)
        self.assertEqual(roman_converter("XLIV"), 44)
        self.assertEqual(roman_converter("mmmcmxcix"), 3999)  # lowercase support

if __name__ == "__main__":
    unittest.main()
