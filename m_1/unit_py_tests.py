import unittest


def multiply(a, b):
    return a * b


class MultiplyTest(unittest.TestCase):
    def test_multiply(self):
        result = multiply(2, 3)
        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main()


def multiply(a, b):
    return a * b


def test_multiply():
    result = multiply(2, 3)
    assert result == 6
