from os import path
import unittest


class TestHelpers(unittest.TestCase):
    def test_basic_multiplication(self):
        self.assertEqual(3*2, 6)


if __name__ == '__main__':
    unittest.main()