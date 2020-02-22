#! /usr/bin/python3

import time
import threading
from datetime import datetime
from random import choice
import schedule
from buslogger import buslogger
from screenwriter import screenwriter
import helpers


def busscreen(data, scr):
    # Function to correctly print the bus data to the screen

    # If at first there are no results then display a warning message
    if "results" not in data.keys() or len(data["results"]) == 0:
        # The emoticons are there to show that the program hasn't frozen
        # and is still running
        sadlist = ["(O_O)", "(>.<)", "(>_<)", "(-_-)", "(._.)"]
        sadface = choice(sadlist)
        scr.write("No bus times", line=0, center=True)
        scr.write(" ", line=1, center=True)
        scr.write(sadface, line=2, center=True)

        # Append any non results to a log file for debugging purposes
        now = datetime.now()
        date = now.strftime("%d%m%y")

        root = helpers.get_project_root()
        filename = root + "/data/noresult_" + date + ".log"

        helpers.jsonfile_append(
            filename, {"data": data, "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")},
        )

    else:
        # Iterating across all the results, make sure the data is justified
        # so that it displays correctly on the screen
        for i in range(len(data["results"])):
            # Justify the route number with spaces
            data["results"][i]["route"] = data["results"][i]["route"].rjust(3, " ")
            # Justify the due time with 0's
            data["results"][i]["duetime"] = data["results"][i]["duetime"].rjust(2, "0")

        # For each line of the screen, display the nth bus and the n+3 bus
        # (eg 1st and 4th)
        for i in range(3):
            blank = "   "

            # nth bus info, if there is no info then a blank item is added
            if len(data["results"]) > i:
                bus1 = [data["results"][i]["route"], data["results"][i]["duetime"]]
            else:
                bus1 = [blank, blank]

            # n+3 bus info, if there is no info then a blank item is added
            if len(data["results"]) > i + 3:
                bus2 = [
                    data["results"][i + 3]["route"],
                    data["results"][i + 3]["duetime"],
                ]
            else:
                bus2 = [blank, blank]

            # Specific string conditions when printing to the screen
            if bus1[1] == "Due":
                # print("Case1", bus1[0], bus1[1], bus2[0], bus2[1])
                text = "%s/%s  %s/%sm" % (bus1[0], bus1[1], bus2[0], bus2[1])
            elif bus2[1] == "Due":
                # print("Case2", bus1[0], bus1[1], bus2[0], bus2[1])
                text = "%s/%sm  %s/%s" % (bus1[0], bus1[1], bus2[0], bus2[1])
            elif bus1[1] == blank and bus2[1] == blank:
                # print("Case3", bus1[0], bus1[1], bus2[0], bus2[1])
                text = "%s %s  %s %s" % (bus1[0], bus1[1], bus2[0], bus2[1])
            elif bus2[1] == blank:
                # print("Case4", bus1[0], bus1[1], bus2[0], bus2[1])
                text = "%s/%sm  %s %s" % (bus1[0], bus1[1], bus2[0], bus2[1])
            else:
                # print("Case5", bus1[0], bus1[1], bus2[0], bus2[1])
                text = "%s/%sm  %s/%sm" % (bus1[0], bus1[1], bus2[0], bus2[1])

            scr.write(text, line=i)


def loopstops(stoplist, scr, blg):
    # Function to loop through the bus stops on the list and display
    # their times
    for stop in stoplist:
        busscreen(blg.stopdata[stop], scr)
        time.sleep(5)


def run_threaded(job_func, args):
    # Function to pass jobs to a new thread, using the example from here:
    # https://schedule.readthedocs.io/en/stable/faq.html#how-can-i-pass-arguments-to-the-job-function
    job_thread = threading.Thread(target=job_func, args=args)
    job_thread.start()


def main():
    # Start instance of buslogger and screenwriter, both objects need to
    # be created and passed around as buslogger will contain data and
    # screenwriter needs to initialize the screen only once per use.
    blg = buslogger()
    scr = screenwriter()

    # List of stops to be queried
    stoplist = [3146, 3224]

    # For each stop in the list add some initial dummy data and set up a
    # threaded schedule job to check the bus times every 20 seconds
    for stop in stoplist:
        blg.stopdata[stop] = {"results": [], "stopid": stop}
        schedule.every(20).seconds.do(run_threaded, blg.buscall, args=(stop,))

    # Set the delay to be 5 seconds per bus stop and set schedule to
    # display the times on the LCD screen
    delay = len(stoplist) * 5
    schedule.every(delay).seconds.do(run_threaded, loopstops, args=(stoplist, scr, blg))

    # Using a infinite loop, run pending schedule jobs once every second
    while True:
        schedule.run_pending()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
