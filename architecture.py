from dataclasses import dataclass
from enum import Enum

WeekDay = Enum("WeekDay", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
Time = (int, int)


@dataclass
class Timeslot:
    day: WeekDay
    time: Time


@dataclass
class Room:
    capacity: int
    name: str


@dataclass
class Lecture:
    num_participants: int
    allocated_room: Room
    timeslot: Timeslot
    already_swapped: bool
