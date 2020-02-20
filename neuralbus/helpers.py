import os
import json
from pathlib import Path


def get_project_root() -> Path:
    """Returns project root folder.
    https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure
    """
    return str(Path(__file__).parent.parent)

def jsonfile_append(filename, data):
    """
    Function to append a json object to a list of json object in a given
    file. If the file does not exist, it will be created.
    """

    # If the file does not already exist then create it and
    # write in an empty list
    if not os.path.exists(filename):
        with open(filename, "w+") as myfile:
            myfile.write("[]")

    # Open json file and load data to a list
    with open(filename, "r") as myfile:
        alldata = json.load(myfile)

    # Append the new data to the list
    alldata.append(data)

    # Open json file and save the list
    with open(filename, "w") as myfile:
        json.dump(alldata, myfile)