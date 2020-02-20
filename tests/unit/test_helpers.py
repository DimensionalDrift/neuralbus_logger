import unittest
import os
from neuralbus import helpers


class TestBuslogger(unittest.TestCase):
    """
    Test methods to test the features of the buslogger class.
    """

    def setUp(self):
        # Setup a test filename
        self.testfile = os.getcwd() + "/test.log"

    def tearDown(self):
        # Delete the test file after the test is done
        if os.path.exists(self.testfile):
            os.remove(self.testfile)

    def test_project_root(self):
        """
        Method to check that the get_project_root returns a string
        """
        root = helpers.get_project_root()

        self.assertIsInstance(root, str)

    def test_jsonfile_append_filecreator(self):
        """
        Method to check that the jsonfile_append function successfully
        creates a file
        """

        dummy = {"test": 0}

        helpers.jsonfile_append(self.testfile, dummy)

        self.assertTrue(os.path.isfile(self.testfile))
