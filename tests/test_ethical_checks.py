import unittest
from agent.ethical_checks import EthicalChecks

class TestEthicalChecks(unittest.TestCase):
    def test_complies_with_guidelines(self):
        self.assertTrue(EthicalChecks.complies_with_guidelines("This is a safe text"))
        self.assertFalse(EthicalChecks.complies_with_guidelines("This text contains hate"))

    def test_is_safe(self):
        self.assertTrue(EthicalChecks.is_safe("This is a safe text"))
        self.assertFalse(EthicalChecks.is_safe("This text is unsafe"))

    def test_validate(self):
        self.assertTrue(EthicalChecks.validate("This is a safe text"))
        self.assertFalse(EthicalChecks.validate("This text contains violence and is unsafe"))

if __name__ == '__main__':
    unittest.main()