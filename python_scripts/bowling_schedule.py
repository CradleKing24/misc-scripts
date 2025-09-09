from datetime import date, timedelta
import random
from collections import defaultdict

# Players with frequency preference
# frequency can be "MONTHLY" or "ANY"
players = {
    "Jaron Turner": "ANY",
    "Justin Ellefson": "ANY",
    "Gina Woolfrey": "ANY",
    "Brenna Pasch": "ANY",
    "Stephanie Roy": "ANY",
    "Sam Butler": "MONTHLY",
    "Linnea Madera": "MONTHLY",
}

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

# Track monthly assignments: {(year, month): {player: count}}
monthly_assignments = defaultdict(lambda: defaultdict(int))


def date_span(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    temp_players = list(players.keys())
    prev_week_players = []
    prev2_week_players = []

    while currentDate <= endDate:
        if currentDate in (date(2025, 12, 24), date(2025, 12, 31)):
            currentDate += delta
            prev_week_players = []
            prev2_week_players = []
            continue

        if currentDate == date(2026, 1, 7):
            players["Erik LaVanier"] = "ANY"
            temp_players = list(players.keys())

        players_on_date = []
        year_month = (currentDate.year, currentDate.month)

        for _ in range(3):
            # Step 1: prefer players not in last week and not repeating 2+ weeks
            eligible_players = [
                p for p in temp_players
                if currentDate not in players_unavailable.get(p, [])
                and p not in players_on_date
                and not (
                    players[p] == "MONTHLY"
                    and monthly_assignments[year_month][p] >= 1
                )
                and not (p in prev_week_players and p in prev2_week_players)
                and p not in prev_week_players  # soft avoid back-to-back
            ]

            # Step 2: relax — allow back-to-back but still forbid 3 weeks in a row
            if not eligible_players:
                eligible_players = [
                    p for p in players.keys()
                    if currentDate not in players_unavailable.get(p, [])
                    and p not in players_on_date
                    and not (
                        players[p] == "MONTHLY"
                        and monthly_assignments[year_month][p] >= 1
                    )
                    and not (p in prev_week_players and p in prev2_week_players)
                ]

            # Step 3: absolute fallback (if schedule would fail) — allow anyone
            if not eligible_players:
                eligible_players = [
                    p for p in players.keys()
                    if currentDate not in players_unavailable.get(p, [])
                    and p not in players_on_date
                ]

            if not eligible_players:
                raise RuntimeError(f"No available players for {currentDate}")

            random.shuffle(eligible_players)
            player = eligible_players.pop(0)

            players_on_date.append(player)
            monthly_assignments[year_month][player] += 1

            temp_players = [p for p in temp_players if p != player]
            if not temp_players:
                temp_players = list(players.keys())

        # Save schedule
        bowling_schedule[currentDate.strftime("%m/%d/%Y")] = players_on_date.copy()

        # Update tracking (slide the window)
        prev2_week_players = prev_week_players.copy()
        prev_week_players = players_on_date.copy()

        currentDate += delta



# bowling is Sept 10th 2025 - April 8th 2026
date_span(date(2025, 9, 17), date(2026, 4, 8), timedelta(weeks=1))

# write schedule out into formatted file
with open("schedule.txt", "w") as f:
    for key in bowling_schedule:
        f.write(f"{key},")
        for x in bowling_schedule[key]:
            f.write(f"{x},")
        f.write("\n")
