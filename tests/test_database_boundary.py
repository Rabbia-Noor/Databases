import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

from pymongo.errors import ConnectionFailure, OperationFailure

from mongo_demo import run_demo
from settings import LabError, MongoSettings


class DatabaseBoundaryTests(unittest.TestCase):
    def settings(self):
        return MongoSettings("dev", "mongo-dev", 27017, "school_dev", "dev_user", "SECRET_TEST_VALUE", "school_dev")

    def client_and_db(self, factory):
        client = factory.return_value.__enter__.return_value
        return client, client.__getitem__.return_value

    @patch("mongo_demo.MongoClient")
    def test_wrong_marker_blocks_all_writes(self, factory):
        _, database = self.client_and_db(factory)
        database.environment_info.find_one.return_value = {"name": "prod"}
        with self.assertRaisesRegex(LabError, "no student was written"):
            run_demo(self.settings(), "test")
        database.students.update_one.assert_not_called()

    @patch("mongo_demo.MongoClient")
    def test_missing_marker_blocks_all_writes(self, factory):
        _, database = self.client_and_db(factory)
        database.environment_info.find_one.return_value = None
        with self.assertRaises(LabError):
            run_demo(self.settings(), "test")
        database.students.update_one.assert_not_called()

    @patch("mongo_demo.MongoClient")
    def test_valid_marker_writes_and_output_excludes_password(self, factory):
        client, database = self.client_and_db(factory)
        database.environment_info.find_one.return_value = {"name": "dev"}
        database.students.find.return_value.sort.return_value = [{"roll_no": "DEMO-001", "name": "Ali"}]
        output = io.StringIO()
        with redirect_stdout(output):
            run_demo(self.settings(), "test")
        client.admin.command.assert_called_once_with("ping")
        database.students.update_one.assert_called_once()
        self.assertIn("marker: dev", output.getvalue())
        self.assertIn("PASS:", output.getvalue())
        self.assertNotIn("SECRET_TEST_VALUE", output.getvalue())

    @patch("mongo_demo.MongoClient")
    def test_authentication_error_does_not_echo_raw_error(self, factory):
        client, database = self.client_and_db(factory)
        database.environment_info.find_one.side_effect = OperationFailure("SECRET_TEST_VALUE", code=18)
        with self.assertRaisesRegex(LabError, "Authentication failed") as caught:
            run_demo(self.settings(), "test")
        self.assertNotIn("SECRET_TEST_VALUE", str(caught.exception))
        database.students.update_one.assert_not_called()

    @patch("mongo_demo.MongoClient")
    def test_network_error_is_distinct_from_authentication(self, factory):
        client, database = self.client_and_db(factory)
        client.admin.command.side_effect = ConnectionFailure("SECRET_TEST_VALUE")
        with self.assertRaisesRegex(LabError, "Cannot reach MongoDB") as caught:
            run_demo(self.settings(), "test")
        self.assertNotIn("SECRET_TEST_VALUE", str(caught.exception))
        database.students.update_one.assert_not_called()


if __name__ == "__main__":
    unittest.main()
