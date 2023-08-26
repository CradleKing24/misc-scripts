from datetime import date, datetime, timedelta
import random


players = [
    "Jaron Turner",
    "Justin Ellefson",
    "Gina Woolfrey",
    "Brenna Pasch",
    "Linnea Ziebol",
]
bowling_schedule = {}


def date_span(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    temp_players = players.copy()
    while currentDate <= endDate:
        if currentDate == date(2023, 12, 27):  # this week is skipped for bowling
            currentDate += delta
            continue
        if currentDate == date(2024, 1, 3):  # start of second half of the season
            players.append("Erik LaVanier")
            temp_players = players.copy()

        players_on_date = []
        for x in range(3):
            random.shuffle(temp_players)
            player = temp_players.pop(0)
            # if player is already playing on the date, loop until someone not on the date is chosen
            while player in players_on_date:
                if len(temp_players) == 0:
                    temp_players = players.copy()
                player = temp_players.pop(0)
            players_on_date.append(player)

            bowling_schedule[currentDate] = players_on_date.copy()
            if len(temp_players) == 0:
                temp_players = players.copy()

        currentDate += delta


# bowling is Sept 6th 2023 - April 3rd 2024. No bowling Dec. 27th 2023
date_span(date(2023, 9, 6), date(2024, 4, 3), timedelta(weeks=1))

# write schedule out into formatted file
f = open("temp.txt", "w")
for key in bowling_schedule:
    f.write(f"{key},")
    for x in bowling_schedule[key]:
        f.write(f"{x},")
    f.write("\n")
f.close()
