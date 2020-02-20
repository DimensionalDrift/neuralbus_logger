#! /usr/bin/python3

import time
from datetime import datetime
from random import choice
from buslogger import buslogger
from screenwriter import screenwriter


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


def main():
    # Start instance of buslogger, poll for the bus stop data and write
    # it to a file
    blg = buslogger()

    # Start instance of screenwriter and write the bus times to the
    # screen
    # The reason this is initialized here then passed to the busscreen
    # function above is to have the screen clear and initialize only
    # once every so often rather than every time. I'm not sure if it's
    # bad for the screen to clear ever time it's used but it certainly
    # takes a moment so it's better this way from a usability
    # perspective
    scr = screenwriter()

    data_3146 = {"results": []}
    data_3224 = {"results": []}

    # Using a infinite loop, the bus times will be checked at specific
    # second intervals and written to file, then every 5 seconds the bus
    # times alternate between the times of one bus stop and another

    # X There is a few things that could be changed in this code, while
    # this works for now it would be better to not have to rely on an
    # infinite loop. Look into something involving cron, maybe the
    # script would be called once a minute and then all these actions
    # would only need to last one minute.. Look into parallelizing the
    # part where the bus times are called by buslogger, this should help
    # with requests taking it's time to report back the times.
    while True:

        sec = int(datetime.now().strftime("%S"))

        if sec in [0, 10, 20, 30, 40, 50]:
            busscreen(data_3146, scr)
            time.sleep(0.75)
            if sec in [0, 20, 40]:
                data_3146 = blg.buscall(3146)
                blg.buslog(data_3146)

        elif sec in [5, 15, 25, 35, 45, 55]:
            busscreen(data_3224, scr)
            time.sleep(0.75)
            if sec in [5, 25, 45]:
                data_3224 = blg.buscall(3224)
                blg.buslog(data_3224)

        else:
            time.sleep(0.5)


if __name__ == "__main__":
    main()
