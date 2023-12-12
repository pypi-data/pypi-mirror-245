"""Testing no module."""

# Standard libs
from unittest import TestCase


class TestNoTests(TestCase):
    """Unittest class to test the module."""

    def test_no_tests(self) -> None:
        """Test method: No tests here."""
        actual = 1
        result = 1
        self.assertEqual(result, actual)
