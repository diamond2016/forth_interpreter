import unittest
from main import op_eval

class TestOpEval(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(op_eval(2, 3, "+"), 5)

    def test_subtraction(self):
        self.assertEqual(op_eval(5, 2, "-"), 3)

    def test_multiplication(self):
        self.assertEqual(op_eval(4, 3, "*"), 12)

    def test_integer_division(self):
        self.assertEqual(op_eval(10, 2, "/"), 5)

    def test_division_by_zero(self):
        self.assertEqual(op_eval(10, 0, "/"), -1)

    def test_modulo(self):
        self.assertEqual(op_eval(10, 3, "mod"), 1)

    def test_modulo_by_zero(self):
        self.assertEqual(op_eval(10, 0, "mod"), -1)

    def test_unknown_operation(self):
        self.assertEqual(op_eval(2, 2, "unknown"), -1)

if __name__ == "__main__":
    unittest.main()