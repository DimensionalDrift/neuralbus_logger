import requests
import json
from datetime import datetime
import os
import utils


class buslogger(object):
    """
    A wrapper for requests that retrieves the data from the api server
    and returns it as a JSON object as well as saves the data to a file.
    """

    def __init__(self):
        pass

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

        busurl = (
            "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid="
            + str(stopid)
            + "&format=json"
        )

        try:
            response = requests.get(busurl)

        except Exception as e:
            print("Error returing data from server")

        return response.json()

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
            root = utils.get_project_root()
            stopid = busjson["stopid"]
            date = datetime.now().strftime("%d%m%y")

            filename = "%s/data/%s_%s.json" % (root, date, stopid)

        # If the file does not already exist then create it and
        # write in an empty list
        if not os.path.exists(filename):
            with open(filename, "w+") as myfile:
                myfile.write("[]")

        # Open json file and load data to a list
        with open(filename, "r") as myfile:
            alldata = json.load(myfile)

        # Append the new data to the list
        alldata.append(busjson)

        # Open json file and save the list
        with open(filename, "w") as myfile:
            json.dump(alldata, myfile)

        # Future Note: I feel that one or more of the above steps could
        # be merged to reduce the amount of times that the file must be
        # interacted with

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