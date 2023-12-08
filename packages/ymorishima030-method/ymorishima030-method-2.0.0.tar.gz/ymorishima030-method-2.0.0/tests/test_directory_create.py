import os
import sys
import unittest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from my_method.directory_create import directory_create  # noqa: E402


class UnitTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(directory_create("test1"), True)

    def test2(self):
        self.assertEqual(directory_create("test1"), True)

    def test3(self):
        self.assertEqual(directory_create(1), False)


if __name__ == "__main__":
    unittest.main()
