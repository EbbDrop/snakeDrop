
"""
Starter Unit Tests using the built-in Python unittest library.
See https://docs.python.org/3/library/unittest.html

You can expand these to cover more cases!

To run the unit tests, use the following command in your terminal,
in the folder where this file exists:

    python tests.py -v

"""
import unittest

from helper import V

class VectorTest(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(V(3, 2), V(3, 2))
        self.assertNotEqual(V(3, 2), V(0, 2))
        self.assertNotEqual(V(3, 2), V(3, 0))

    def test_from_dict(self):
        self.assertEqual(V({"x": 3, "y": 2}), V(3, 2))
  
    def test_from_dir(self):
        self.assertEqual(V("up"), V(0, 1))
        self.assertEqual(V("right"), V(1, 0))
        self.assertEqual(V("down"), V(0, -1))
        self.assertEqual(V("left"), V(-1, 0))

    def test_math(self):
        self.assertEqual(V(3, 2) + V(1, 2), V(4, 4))
        self.assertEqual(V(3, 2) - V(1, 2), V(2, 0))
        self.assertEqual(V(3, 2) * V(1, 2), V(3, 4))
        self.assertEqual(V(3, 2) * -1     , V(-3, -2))


if __name__ == "__main__":
    unittest.main()
