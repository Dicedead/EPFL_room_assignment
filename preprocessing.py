import datetime

import pandas as pd
import numpy as np

from typing import Optional
from architecture import *


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def entry_to_lecture(entry, course_participants) -> Optional[Lecture]:
    same_course_code = course_participants[course_participants["course_code"] == entry["course_code"]]
    if len(same_course_code) > 0:
        num_participants = same_course_code.iloc[0]["participants"]
        if not np.isnan(num_participants):
            lecture = Lecture(
                code=entry["course_code"],
                title=entry["course_name"],
                num_participants=num_participants,
                allocated_room=Room(entry["room_capacity"], entry["room_name"]),
                timeslot=str_to_timeslot(entry["start_datetime"], entry["end_datetime"]),
                already_swapped=False,
                overbooked=num_participants > entry["room_capacity"]
            )
            return lecture
    return None


def str_to_timeslot(start_str: str, end_str: str, datetime_format='%Y-%m-%d %H:%M:%S') -> Timeslot:
    start_datetime_obj = datetime.datetime.strptime(start_str, datetime_format)
    end_datetime_obj = datetime.datetime.strptime(end_str, datetime_format)
    tmp = start_datetime_obj.weekday()
    weekday = WeekDay(start_datetime_obj.weekday() + 1).name
    start_hour = start_datetime_obj.hour
    end_hour = end_datetime_obj.hour

    return Timeslot(weekday, (start_hour, end_hour))


def construct_all_lectures(course_bookings_path: str, course_participants_path: str):
    all_lectures = []

    course_bookings = pd.read_csv(course_bookings_path)
    course_participants = pd.read_csv(course_participants_path)

    course_bookings = course_bookings[course_bookings["label"] == "cours"]

    for i in range(len(course_bookings)):
        entry = course_bookings.iloc[i]
        maybe_lect = entry_to_lecture(entry, course_participants)
        if maybe_lect:
            all_lectures.append(maybe_lect)

    return unique(all_lectures)


if __name__ == "__main__":
    all_lects = construct_all_lectures("data/course_bookings.csv", "data/courses_with_participants.csv")
    print(len(all_lects))
