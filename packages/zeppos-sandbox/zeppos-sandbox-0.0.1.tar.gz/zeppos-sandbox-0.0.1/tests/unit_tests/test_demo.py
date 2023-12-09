"""Testing demo module."""

# Standard libs
from unittest import TestCase

# Custom libs
from zeppos_sandbox.demo import Demo


class TestDemo(TestCase):
    """Unittest class to test the module."""

    def test_hello_world(self) -> None:
        """Test method: hello_world."""
        # Set Up
        demo = Demo()

        # Test
        actual = demo.hello_world()

        # Verify
        self.assertEqual("Hello world.", actual)

    def test_status(self) -> None:
        """Test method: status."""
        # Set Up
        demo = Demo()

        # Test
        actual = demo.status()

        # Verify
        self.assertEqual("good", actual)
