from datetime import date, datetime, timedelta
import random


players = [
    "Jaron Turner",
    "Justin Ellefson",
    "Gina Woolfrey",
    "Brenna Pasch",
    # "Charles King",
    # "Corey Quick",
]
players_unavailable = {
    "Jaron Turner": [
        date(2024, 9, 4),
        date(2024, 9, 11),
        date(2024, 9, 18),
        date(2024, 9, 25),
        date(2024, 10, 30),
        date(2024, 11, 27),
    ],
    "Justin Ellefson": [date(2024, 10, 2), date(2024, 10, 9)],
    "Gina Woolfrey": [],
    "Brenna Pasch": [],
    "Erik LaVanier": [],
}
bowling_schedule = {}


def date_span(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    temp_players = players.copy()
    while currentDate <= endDate:
        if currentDate == date(2024, 12, 25) or currentDate == date(
            2025, 1, 1
        ):  # this week is skipped for bowling
            currentDate += delta
            continue
        if currentDate == date(2025, 1, 8):  # start of second half of the season
            players.append("Erik LaVanier")
            temp_players = players.copy()

        players_on_date = []
        for x in range(3):
            random.shuffle(temp_players)
            player = temp_players.pop(0)
            player_unavailable_dates = players_unavailable[player]
            if currentDate in player_unavailable_dates:
                if len(temp_players) == 0:
                    temp_players = players.copy()
                    temp_players.remove(player)
                    random.shuffle(temp_players)
                player = temp_players.pop(0)
            # if player is already playing on the date, loop until someone not on the date is chosen
            while player in players_on_date:
                if len(temp_players) == 0:
                    temp_players = players.copy()
                    random.shuffle(temp_players)
                player = temp_players.pop(0)
            players_on_date.append(player)

            bowling_schedule[currentDate] = players_on_date.copy()
            if len(temp_players) == 0:
                temp_players = players.copy()

        currentDate += delta


# bowling is Sept 4th 2024 - April 9rd 2025. No bowling Dec. 25th 2024, Jan 1 2025
date_span(date(2024, 9, 4), date(2025, 4, 9), timedelta(weeks=1))

# write schedule out into formatted file
f = open("temp.txt", "w")
for key in bowling_schedule:
    f.write(f"{key},")
    for x in bowling_schedule[key]:
        f.write(f"{x},")
    f.write("\n")
f.close()
