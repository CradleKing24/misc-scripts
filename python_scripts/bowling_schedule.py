from datetime import date, datetime, timedelta
import random


players = [
    "Jaron Turner",
    "Justin Ellefson",
    "Gina Woolfrey",
    "Brenna Pasch",
    "Stephanie Roy",
    "Sam Butler",
    "Linnea Madera",
]
players_unavailable = {
    "Jaron Turner": [
        date(2025, 9, 24),
        date(2025, 10, 29),
        date(2025, 11, 26),
        date(2026, 1, 28),
        date(2026, 2, 25),
        date(2026, 3, 25),
        date(2026, 4, 1),
        date(2026, 4, 8),
    ],
    "Justin Ellefson": [
        date(2025, 9, 17),
        date(2025, 11, 5),
        date(2025, 12, 10),
        date(2026, 1, 7),
        date(2026, 3, 25),
    ],
    "Gina Woolfrey": [
        date(2025, 11, 12),
        date(2025, 11, 19),
    ],
    "Brenna Pasch": [],
    "Erik LaVanier": [],
    "Sam Butler": [
        date(2025, 9, 17),
        date(2025, 11, 12),
        date(2025, 11, 26),
        date(2025, 12, 3),
        date(2026, 3, 11),
        date(2026, 4, 1),
    ],
    "Stephanie Roy": [
        date(2025, 9, 24),
        date(2025, 11, 19),
    ],
    "Linnea Madera": [
        date(2025, 9, 17),
        date(2025, 9, 24),
        date(2025, 10, 1),
        date(2025, 10, 29),
        date(2025, 11, 26),
        date(2025, 12, 17),
        date(2026, 1, 7),
        date(2026, 2, 11),
        date(2026, 2, 18),
    ],
}
bowling_schedule = {}


def date_span(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    temp_players = players.copy()
    while currentDate <= endDate:
        if currentDate == date(2025, 12, 24) or currentDate == date(
            2025, 12, 31
        ):  # this week is skipped for bowling
            currentDate += delta
            continue
        if currentDate == date(2026, 1, 7):  # start of second half of the season
            players.append("Erik LaVanier")
            temp_players = players.copy()

        players_on_date = []
        for _ in range(3):
            # filter out unavailable players and already scheduled ones
            eligible_players = [
                p for p in temp_players
                if currentDate not in players_unavailable.get(p, [])
                and p not in players_on_date
            ]

            if not eligible_players:
                # fallback: reset pool from master list
                eligible_players = [
                    p for p in players
                    if currentDate not in players_unavailable.get(p, [])
                    and p not in players_on_date
                ]

            if not eligible_players:
                raise RuntimeError(f"No available players for {currentDate}")

            random.shuffle(eligible_players)
            player = eligible_players.pop(0)

            players_on_date.append(player)

            # remove selected player from temp pool
            temp_players = [p for p in temp_players if p != player]
            if not temp_players:
                temp_players = players.copy()

        bowling_schedule[currentDate.strftime("%m/%d/%Y")] = players_on_date.copy()
        currentDate += delta


# bowling is Sept 3rd 2025 - April 8th 2026. No bowling Dec. 24th 2025, Dec. 31 2025
date_span(date(2025, 9, 10), date(2026, 4, 8), timedelta(weeks=1))

# write schedule out into formatted file
f = open("schedule.txt", "w")
for key in bowling_schedule:
    f.write(f"{key},")
    for x in bowling_schedule[key]:
        f.write(f"{x},")
    f.write("\n")
f.close()
