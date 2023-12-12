import unittest

from typing import List

from letterboxed import Letterbox

class TestLetterbox(unittest.TestCase):

    def setUp(self):
        with open("/usr/share/dict/american-english-small", "r") as fp:
            self.dictionary: List[str] = fp.read().split("\n")

        self.letterbox: Letterbox = Letterbox.create_random(self.dictionary)

    def test_get_solutions(self):
        self.solutions = self.letterbox.solve()
        self.assertTrue(len(self.solutions) > 0)

    def test_correct_guess(self):
        self.solutions = self.letterbox.solve()
        self.assertTrue(self.letterbox.guess(self.solutions[0]))

    def test_wrong_guess(self):
        self.assertFalse(self.letterbox.guess(['aaa', 'zzz']))

if __name__ == '__main__':
    unittest.main()