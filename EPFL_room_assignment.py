import sys
sys.stdout = open('results/results.txt', 'w')

from architecture import Lecture, CourseType
from preprocessing import construct_all_lectures


def print_swap(l1: Lecture, l2: Lecture):
    print(f"Swap: {l1.code} {l1.title} ({l1.num_participants} people in {l1.allocated_room.name}"
          f" (capacity : {l1.allocated_room.capacity}) on {l1.timeslot.day} from {l1.timeslot.time[0]}:15 "
          f"till {l1.timeslot.time[1]}:00) with {l2.code} {l2.title} ({l2.num_participants} people in "
          f"{l2.allocated_room.name} (capacity : {l2.allocated_room.capacity}))")


def find_better_room(lecture, all_lectures) -> bool:
    candidate_lectures = [swap_lecture for swap_lecture in all_lectures if
                          (lecture.timeslot == swap_lecture.timeslot
                           and not swap_lecture.overbooked
                           and not swap_lecture.already_swapped
                           and swap_lecture.allocated_room.capacity >= lecture.num_participants
                           > swap_lecture.num_participants)
                          ]

    if len(candidate_lectures) > 0:
        candidate_lectures.sort(key=lambda x: x.num_participants, reverse=True)
        print_swap(lecture, candidate_lectures[0])
        temp = lecture.allocated_room
        lecture.allocated_room = candidate_lectures[0].allocated_room
        candidate_lectures[0].allocated_room = temp
        lecture.overbooked = False
        lecture.already_swapped = True
        return True
    return False


lectures = construct_all_lectures("data/course_bookings.csv", "data/courses_with_participants.csv")
overbooked_lectures = [lect for lect in lectures if lect.overbooked and lect.type == CourseType.Lecture]
overbooked_lectures.sort(key=lambda x: x.num_participants, reverse=True)

num_overbooked_students = 0
for lect in overbooked_lectures:
    num_overbooked_students += lect.num_participants - lect.allocated_room.capacity

print(f"Number of overbooked lectures: {len(overbooked_lectures)}")
print(f"Number of students in overbooked lectures: {num_overbooked_students}")
print("=========================================================================")
print("=========================================================================")
overbooked_lectures_no_solution = []
for overbooked_lecture in overbooked_lectures:
    if not find_better_room(overbooked_lecture, lectures):
        overbooked_lectures_no_solution.append(overbooked_lecture)
print("=========================================================================")
print("=========================================================================")
print(f"Number of overbooked lectures for which no solution is found: {len(overbooked_lectures_no_solution)}")
print(f"Number of overbooked lectures for which a solution is found: "
      f"{len(overbooked_lectures) - len(overbooked_lectures_no_solution)}")

new_num_overbooked_students = 0
for lect in overbooked_lectures:
    new_num_overbooked_students += lect.num_participants - lect.allocated_room.capacity

print(f"New number of students in overbooked lectures: {new_num_overbooked_students}")
print(f"Improvement: {(1 - new_num_overbooked_students/num_overbooked_students) * 100:.2f}% less students in overbooked lectures")


