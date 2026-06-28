import unittest
from unittest.mock import patch
import os
import digest

class TestSecurity(unittest.TestCase):

    def setUp(self):
        # Default valid environment variables for testing
        # Using .test instead of example.com to avoid placeholder check
        self.valid_env = {
            "SENDER_EMAIL": "sender@test.test",
            "SENDER_APP_PASSWORD": "abcd efgh ijkl mnop",
            "RECEIVER_EMAIL": "receiver@test.test",
            "GROQ_API_KEY": "gsk_test_key_very_long_to_pass_validation"
        }

    def test_validate_env_valid(self):
        with patch.dict(os.environ, self.valid_env, clear=True):
            try:
                digest.validate_env()
            except ValueError as e:
                self.fail(f"validate_env raised ValueError unexpectedly: {e}")

    def test_validate_env_missing_var(self):
        for var in self.valid_env:
            env = self.valid_env.copy()
            del env[var]
            with patch.dict(os.environ, env, clear=True):
                with self.assertRaisesRegex(ValueError, f"Missing required environment variable: {var}"):
                    digest.validate_env()

    def test_validate_env_placeholder(self):
        env = self.valid_env.copy()
        env["SENDER_EMAIL"] = "your_email@domain.com"
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ValueError, "appears to contain a placeholder value"):
                digest.validate_env()

    def test_validate_env_invalid_email(self):
        env = self.valid_env.copy()
        env["SENDER_EMAIL"] = "invalid-email"
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ValueError, "SENDER_EMAIL does not appear to be a valid email address"):
                digest.validate_env()

    def test_validate_env_invalid_groq_key(self):
        env = self.valid_env.copy()
        env["GROQ_API_KEY"] = "not_a_groq_key"
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ValueError, "GROQ_API_KEY must start with 'gsk_'"):
                digest.validate_env()

    def test_validate_env_too_many_recipients(self):
        env = self.valid_env.copy()
        env["RECEIVER_EMAIL"] = ",".join([f"user{i}@test.test" for i in range(52)])
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ValueError, "Too many recipients"):
                digest.validate_env()

    def test_validate_env_control_characters_injection(self):
        # Test SENDER_EMAIL
        env = self.valid_env.copy()
        env["SENDER_EMAIL"] = "sender@test.test\r\nInjected-Header: value"
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ValueError, "contains forbidden control characters"):
                digest.validate_env()

        # Test SENDER_APP_PASSWORD
        env = self.valid_env.copy()
        env["SENDER_APP_PASSWORD"] = "password\r\nInjected-Header: value"
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ValueError, "contains forbidden control characters"):
                digest.validate_env()

    def test_validate_env_large_input_dos(self):
        env = self.valid_env.copy()
        env["SENDER_APP_PASSWORD"] = "a" * 1000000
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ValueError, "exceeds maximum length"):
                digest.validate_env()

    def test_clean_text_removes_control_characters(self):
        # Test string with null byte and other non-printable control characters
        dirty_text = "Hello\0 World\x01\x1f\x7f"
        cleaned_text = digest.clean_text(dirty_text)
        self.assertEqual(cleaned_text, "Hello World")

        # Test that allowed whitespace (tab, newline, carriage return) is NOT removed by CONTROL_CHAR_RE
        # but stripped by final .strip() if at ends
        whitespace_text = " \t\r\nHello\nWorld "
        cleaned_whitespace = digest.clean_text(whitespace_text)
        self.assertEqual(cleaned_whitespace, "Hello\nWorld")

if __name__ == "__main__":
    unittest.main()
