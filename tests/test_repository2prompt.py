import unittest
from repository2prompt import Repository2Prompt

class TestRepository2Prompt(unittest.TestCase):
    def test_initialization(self):
        converter = Repository2Prompt("https://github.com/user/repo")
        self.assertIsInstance(converter, Repository2Prompt)

if __name__ == '__main__':
    unittest.main()