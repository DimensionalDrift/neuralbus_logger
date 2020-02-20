import unittest
import time
import os
import json
from datetime import datetime
from neuralbus import buslogger
from neuralbus import helpers


class TestBuslogger(unittest.TestCase):
    """
    Test methods to test the features of the buslogger class.
    """

    def setUp(self):
        # Setup an instance of the buslogger class and find the current
        # directory of this test
        self.buslog = buslogger.buslogger()
        self.root = helpers.get_project_root()
        self.testfile = "%s/test.log" % self.root

    def tearDown(self):
        # Delete the test file after the test is done
        if os.path.exists(self.testfile):
            os.remove(self.testfile)

    def test_buscall_validjson(self):
        """
        Method to test that the buscall function returns a valid json dict.
        """
        data = self.buslog.buscall(3146)

        self.assertIs(type(data), dict)

    def test_buscall_url(self):
        """
        Method to test that the buscall function uses a correctly
        formatted url (ie a string).
        """
        # When giving a bus stop as an int, check that the url is
        # converted to a string
        self.buslog.buscall(3146)

        self.assertIs(type(self.buslog.busurl), str)

    def test_buscall_wrong_stop(self):
        """
        Method to check that when an incorrect stop id is given that an
        expected errorcode returns.
        """

        # Giving the bus stop id of derp (where it usually is a number)
        # should return an error code of 1
        data = self.buslog.buscall("derp")
        expected = {"errorcode": "1"}

        self.assertIn(expected["errorcode"], data["errorcode"])

    def test_buscall_404(self):
        """
        Method to check that when the bus times are down that an
        expected 404 response is given.

        X I'm not sure how to test for this, the best way to check that
        the 404 is working is by giving a incorrect url to response and
        seeing that it returns a 404 but I don't know how to pass a
        specifically incorrect variable without making it an input to
        the function. I feel like there is a way so look into this later.
        """
        pass

    def test_buslog_file_maker(self):
        """
        Method to test that when a logfile is given that does not exist, that
        buslog will generate one.
        """

        # Dummy json
        dummy = {"errorcode": "0"}

        # Log the dummy data to the file and check that it's there
        self.buslog.buslog(dummy, filename=self.testfile)

        self.assertTrue(os.path.exists(self.testfile))

    def test_buslog_append(self):
        """
        Method to test that the data is being appended correctly to a file.
        """

        # Dummy list of json data
        dummy = [{"errorcode": "0"}, {"errorcode": "0"}]

        # Append the items from the list seperately
        self.buslog.buslog(dummy[0], filename=self.testfile)
        self.buslog.buslog(dummy[1], filename=self.testfile)

        # Open the file and read the data to compare to the original data
        with open(self.testfile, "r") as myfile:
            alldata = json.load(myfile)

        self.assertEqual(alldata, dummy)

    def test_datetimer(self):
        """
        Method to test that a datetime object is returned when given a
        datetime string.
        """

        # Time string to check is converted
        timestr = "01/04/2020 01:02:03"

        # Datetime object that should be returned
        dtobj = self.buslog.datetimer(timestr)

        self.assertIsInstance(dtobj, datetime)
