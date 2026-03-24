import unittest
import os
from weather_app.configs.messageManager import MessageManager


class TestMessageManager(unittest.TestCase):

    def setUp(self):
        os.environ['APP_LANG'] = 'en'
        self.mm = MessageManager()

    def test_get_success_message(self):
        msg = self.mm.get("success.insert")
        self.assertIn("successfully", msg.lower())

    def test_missing_key(self):
        msg = self.mm.get("error.fake.key")
        self.assertTrue("not found" in msg.lower())

    def test_format_parameter(self):
        msg = self.mm.get("error.database.unknown", error="DB crash")
        self.assertIn("DB crash", msg)

    def test_language_switch(self):
        langs = self.mm.get_available_languages()

        if len(langs) > 1:
            self.assertTrue(self.mm.set_language(langs[0]))
            self.assertEqual(self.mm.get_language(), langs[0])

    def test_reload(self):
        old_lang = self.mm.get_language()
        self.mm.reload()
        self.assertIsInstance(self.mm.get_language(), str)


if __name__ == "__main__":
    unittest.main()