import requests
import json
from datetime import datetime
import os
import helpers


class buslogger(object):
    """
    A wrapper for requests that retrieves the data from the api server
    and returns it as a JSON object as well as saves the data to a file.
    """

    def __init__(self):
        self.stopdata = {}

    def buscall(self, stopid):
        """
        Function to call the api server for the bus time for a given bus
        stop number

        Parameters
        ----------
        stopid : int
            The bus stop number as an int.

        Returns
        -------
        dict
            a dict in json format containing the bus time information.

        """

        self.busurl = (
            "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid="
            + str(stopid)
            + "&format=json"
        )

        try:
            response = requests.get(self.busurl)
            # Sometimes the bus times will go down on smartdublins end
            # and so will return a 404, otherwise the code should be
            # valid json
            if response.status_code == 404:
                self.stopdata[stopid] = {"errorcode": "404", "results": [], "stopid": stopid}
            else:
                self.stopdata[stopid] = response.json()

            return self.stopdata[stopid]

        except Exception as e:
            # raise("Error returing data from server: %s" % (e))
            raise (e)

    def buslog(self, busjson, filename=None):
        """ Function to log data to a file

        Parameters
        ----------
        busjson : dict
            JSON formatted dict containing bus information.

        filename : string, optional
            A string containing a specific file to save to, otherwise
            the data is saved to a date specific file in the data folder
            of the project.
        """

        # If no file name is given then construct a file name using the
        # root directory, the date and the stop id number
        if filename is None:
            root = helpers.get_project_root()
            stopid = busjson["stopid"]
            date = datetime.now().strftime("%d%m%y")

            filename = "%s/data/%s_%s.json" % (root, date, stopid)

        helpers.jsonfile_append(filename, busjson)


        # Future Note: I feel that one or more of the above steps could
        # be merged to reduce the amount of times that the file must be
        # interacted with

    @staticmethod
    def datetimer(timestr):
        """
        Helper function to convert the date to a datetime object.

        Parameters
        ----------
        timestr : str
            date string in the format "DD/MM/YYYY HH:MM:SS".

        Returns
        -------
        datetime object
            A datetime object of the given date string.
        """
        return datetime.strptime(timestr, "%d/%m/%Y %H:%M:%S")
