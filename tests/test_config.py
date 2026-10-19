import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from settings import LabError, load_environment, load_file, make_settings


ROOT = Path(__file__).resolve().parents[1]


class ConfigTests(unittest.TestCase):
    def env(self):
        return {
            "APP_ENV": "dev",
            "MONGO_HOST": "mongo-dev",
            "MONGO_PORT": "27017",
            "MONGO_DATABASE": "school_dev",
            "MONGO_USERNAME": "dev_user",
            "MONGO_PASSWORD": "p%@!$word",
            "MONGO_AUTH_SOURCE": "school_dev",
        }

    def test_environment_is_loaded_without_embedding_password_in_repr(self):
        with patch.dict(os.environ, self.env(), clear=True):
            result = load_environment()
        self.assertEqual(result.port, 27017)
        self.assertEqual(result.password, "p%@!$word")
        self.assertNotIn(result.password, repr(result))

    def test_missing_password_has_no_fallback(self):
        values = self.env()
        del values["MONGO_PASSWORD"]
        with patch.dict(os.environ, values, clear=True):
            with self.assertRaisesRegex(LabError, "Missing MongoDB settings: password"):
                load_environment()

    def test_missing_environment_has_no_default(self):
        values = self.env()
        del values["APP_ENV"]
        with patch.dict(os.environ, values, clear=True):
            with self.assertRaisesRegex(LabError, "no default"):
                load_environment()

    def test_invalid_ports_do_not_echo_input(self):
        for value in ("27017secret", "0", "65536"):
            with self.subTest(port=value):
                values = self.env()
                values["MONGO_PORT"] = value
                with patch.dict(os.environ, values, clear=True):
                    with self.assertRaises(LabError) as caught:
                        load_environment()
                self.assertNotIn(value, str(caught.exception))

    def test_each_file_template_selects_distinct_endpoint_and_account(self):
        settings = []
        with tempfile.TemporaryDirectory() as directory:
            config_dir = Path(directory)
            for environment in ("dev", "test", "prod"):
                template = ROOT / "config-examples" / f"{environment}.ini.example"
                (config_dir / f"{environment}.ini").write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
                item = load_file(environment, config_dir)
                self.assertEqual(item.environment, environment)
                self.assertEqual(item.database, f"school_{environment}")
                self.assertEqual(item.auth_source, item.database)
                settings.append(item)
        self.assertEqual({item.host for item in settings}, {"mongo-dev", "mongo-test", "mongo-prod"})
        self.assertEqual({item.port for item in settings}, {27017})
        self.assertEqual(len({item.username for item in settings}), 3)
        self.assertEqual(len({item.password for item in settings}), 3)

    def test_percent_password_is_read_literally_from_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dev.ini"
            template = (ROOT / "config-examples" / "dev.ini.example").read_text(encoding="utf-8")
            path.write_text(template.replace("DevDemoOnly123!", "p%@(missing)s!"), encoding="utf-8")
            self.assertEqual(load_file("dev", Path(directory)).password, "p%@(missing)s!")

    def test_file_label_must_match_selected_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            template = (ROOT / "config-examples" / "test.ini.example").read_text(encoding="utf-8")
            (Path(directory) / "dev.ini").write_text(template, encoding="utf-8")
            with self.assertRaisesRegex(LabError, "does not match"):
                load_file("dev", Path(directory))

    def test_missing_file_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(LabError, "missing or unreadable"):
                load_file("dev", Path(directory))

    def test_bad_ini_errors_do_not_echo_credential_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "dev.ini").write_text("password=SECRET_TEST_VALUE", encoding="utf-8")
            with self.assertRaises(LabError) as caught:
                load_file("dev", Path(directory))
            self.assertNotIn("SECRET_TEST_VALUE", str(caught.exception))

    def test_file_mode_ignores_old_shell_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            template = (ROOT / "config-examples" / "dev.ini.example").read_text(encoding="utf-8")
            (Path(directory) / "dev.ini").write_text(template, encoding="utf-8")
            with patch.dict(os.environ, {"APP_ENV": "prod", "MONGO_PASSWORD": "old-value"}, clear=True):
                self.assertEqual(load_file("dev", Path(directory)).environment, "dev")


if __name__ == "__main__":
    unittest.main()
