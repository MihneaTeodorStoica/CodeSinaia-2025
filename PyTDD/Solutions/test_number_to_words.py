import unittest
from number_to_words import number_to_words

class TestNums(unittest.TestCase):
    # ======== Step 1 ======== test 0, return 'zero'
    def test_zero(self):
        self.assertEqual(number_to_words(0), "zero")

    # ======== Step 2 ======== test 1 to 9
    def test_single_digits(self):
        self.assertEqual(number_to_words(1), "one")
        self.assertEqual(number_to_words(9), "nine")

    # ======== Step 3 ======== test 10 to 19
    def test_teens(self):
        self.assertEqual(number_to_words(10), "ten")
        self.assertEqual(number_to_words(13), "thirteen")
        self.assertEqual(number_to_words(19), "nineteen")

    # ======== Step 4 ======== test 20 to 99
    def test_tens(self):
        self.assertEqual(number_to_words(20), "twenty")
        self.assertEqual(number_to_words(45), "forty-five")
        self.assertEqual(number_to_words(99), "ninety-nine")

    # ======== Step 5 ======== test 100 to 999
    def test_hundreds(self):
        self.assertEqual(number_to_words(100), "one hundred")
        self.assertEqual(number_to_words(342), "three hundred forty-two")
        self.assertEqual(number_to_words(999), "nine hundred ninety-nine")