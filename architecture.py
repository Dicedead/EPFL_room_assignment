from dataclasses import dataclass
from enum import Enum

WeekDay = Enum("WeekDay", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
Time = (int, int)
SessionType = Enum("CourseType", ["Lecture", "Other"])


@dataclass
class Timeslot:
    day: str
    time: Time


@dataclass
class Room:
    capacity: int
    name: str


@dataclass
class Session:
    type: SessionType
    code: str
    title: str
    num_participants: int
    allocated_room: Room
    timeslot: Timeslot
    already_swapped: bool
    overbooked: bool

def weekday_str_to_obj(weekday_str: str) -> WeekDay:
    return WeekDay(weekday_str)
