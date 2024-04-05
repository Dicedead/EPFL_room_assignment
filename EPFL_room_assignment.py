from architecture import Lecture
from preprocessing import construct_all_lectures


def print_swap(l1: Lecture, l2: Lecture):
    print(f"Swap: {l1.code} {l1.title} ({l1.num_participants} people in {l1.allocated_room.name}"
          f" (capacity : {l1.allocated_room.capacity}) on {l1.timeslot.day} from {l1.timeslot.time[0]}:15 "
          f"till {l1.timeslot.time[1]}):00 with {l2.code} {l2.title} ({l2.num_participants} people in "
          f"{l2.allocated_room.name} (capacity : {l2.allocated_room.capacity}))")


def find_better_room(lecture, all_lectures):
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
        return candidate_lectures[0]
    return 0


lectures = construct_all_lectures("data/course_bookings.csv", "data/courses_with_participants.csv")
overbooked_lectures = [overbooked_lecture for overbooked_lecture in lectures if overbooked_lecture.overbooked]
overbooked_lectures.sort(key=lambda x: x.num_participants, reverse=True)
for candidate_lecture in overbooked_lectures:
    find_better_room(candidate_lecture, lectures)
