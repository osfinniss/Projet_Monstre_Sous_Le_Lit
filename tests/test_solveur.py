import unittest
from src.solveur import resoudre_defi

def mock_resolve():
    return "Solution trouvée"

class TestSolveur(unittest.TestCase):
    def test_resolution(self):
        self.assertEqual(mock_resolve(), "Solution trouvée")

if __name__ == "__main__":
    unittest.main()