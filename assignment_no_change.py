import sys
from copy import deepcopy

sys.stdout = open('results/results_all_possibilities.txt', 'w')

from preprocessing_stats import *


def print_swap(l1: Session, l2: Session):
    print(f"Swap: {l1.code} {l1.title} ({l1.num_participants} people in {l1.allocated_room.name}"
          f" (capacity : {l1.allocated_room.capacity}) on {l1.timeslot.day} from {l1.timeslot.time[0]}:15 "
          f"till {l1.timeslot.time[1]}:00) with {l2.code} {l2.title} ({l2.num_participants} people in "
          f"{l2.allocated_room.name} (capacity : {l2.allocated_room.capacity}))")


def find_better_room(lecture, all_lectures) -> bool:
    candidate_lectures = [swap_lecture for swap_lecture in all_lectures if
                          (lecture.timeslot == swap_lecture.timeslot
                           and not swap_lecture.overbooked
                           and not swap_lecture.already_swapped
                           and lecture.num_participants > swap_lecture.num_participants
                           and lecture.allocated_room.capacity < swap_lecture.allocated_room.capacity
                           )
                          ]

    for candidate_lecture in candidate_lectures:
        print_swap(lecture, candidate_lecture)


sessions = construct_all_sessions("data/occup.csv")
overbooked_lectures = [lect for lect in sessions if lect.overbooked and lect.type == SessionType.Lecture]
overbooked_lectures.sort(key=lambda x: x.num_participants - x.allocated_room.capacity)

num_overbooked_students = 0
for lect in overbooked_lectures:
    num_overbooked_students += lect.num_participants - lect.allocated_room.capacity

print(f"Number of overbooked lectures: {len(overbooked_lectures)}")
print(f"Number of students in overbooked lectures: {num_overbooked_students}")
print("=========================================================================")
print("=========================================================================")

while len(overbooked_lectures) > 0:
    lecture = overbooked_lectures.pop()
    candidate_lectures = [swap_lecture for swap_lecture in sessions if
                          (lecture.timeslot == swap_lecture.timeslot
                           and lecture.num_participants > swap_lecture.num_participants
                           and lecture.allocated_room.capacity < swap_lecture.allocated_room.capacity
                           )
                          ]

    for candidate_lecture in candidate_lectures:
        print_swap(lecture, candidate_lecture)

new_overbooked_lectures = [lect for lect in sessions if lect.overbooked and lect.type == SessionType.Lecture]
new_num_overbooked_students = 0
for lect in overbooked_lectures:
    new_num_overbooked_students += lect.num_participants - lect.allocated_room.capacity

print("=========================================================================")
print("=========================================================================")
print(f"New number of overbooked lectures: {len(new_overbooked_lectures)}")

new_num_overbooked_students = 0
for lect in new_overbooked_lectures:
    new_num_overbooked_students += lect.num_participants - lect.allocated_room.capacity

print(f"New number of students in overbooked lectures: {new_num_overbooked_students}")
print(f"Improvement: {(1 - new_num_overbooked_students/num_overbooked_students) * 100:.2f}% less students in overbooked lectures")