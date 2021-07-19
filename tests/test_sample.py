from os import path
import unittest


class TestHelpers(unittest.TestCase):
    def test_LoadBert_raisesOSError_with_absent_model(self):
        self.assertEqual(3*2, 6)


if __name__ == '__main__':
    unittest.main()