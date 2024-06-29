import pandas as pd
import numpy as np

from architecture import *
from typing import Optional

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def entry_to_lecture(entry) -> Optional[Session]:
    num_participants = entry["nb étudiants"]
    if not np.isnan(num_participants) and not np.isnan(entry["nombre total de places"]):
        session = Session(
                type=SessionType.Lecture if entry["type d'enseignement"] == "Cours" and entry["nb.places dans l'espace"] == entry["nombre total de places"] else SessionType.Other,
                code=entry["code matière"],
                title=entry["matière"],
                num_participants=int(num_participants),
                allocated_room=Room(int(entry["nb.places dans l'espace"] if not np.isnan(entry["nb.places dans l'espace"]) else 0), entry["espace (code)"]),
                timeslot=str_to_timeslot(entry["jour"], entry["heure début séance"], entry["heure fin séance"]),
                already_swapped=False,
                overbooked=entry["overbooking"] == "oui"
        )
        return session
    return None


def str_to_timeslot(weekday_str, start_time, end_time) -> Timeslot:
    return Timeslot(weekday_str, (int(start_time[:2]), int(end_time[:2])))


def construct_all_sessions(path="data/occup.csv") -> list:
    df = pd.read_csv(path)
    all_sessions = []
    for i in range(len(df)):
        entry = df.iloc[i]
        maybe_lect = entry_to_lecture(entry)
        if maybe_lect:
            all_sessions.append(maybe_lect)

    return all_sessions


if __name__ == "__main__":
    df = pd.read_csv("data/occup.csv")
    print(construct_all_sessions(df))
