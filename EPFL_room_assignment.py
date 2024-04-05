from architecture import Room, Timeslot, WeekDay, Lecture, Time

def print_swap(l1,l2):
    print(f"swap de {l1.code} ({l1.num_participants} personnes en {l1.allocated_room.name} (capacité : {l1.allocated_room.capacity}) le {l1.timeslot.day} de {l1.timeslot.time[0]} à {l1.timeslot.time[1]}) avec {l2.code} ({l2.num_participants} personnes en {l2.allocated_room.name} (capacité : {l2.allocated_room.capacity}))")

def find_better_room(lecture, all_lectures):
    L = [l for l in all_lectures if (lecture.timeslot == l.timeslot and not l.overbooked and not l.already_swapped and l.allocated_room.capacity >= lecture.num_participants) ]
    if len(L) > 0 :
        L.sort(key=lambda x: x.num_participants, reverse=True)
        print_swap(l, L[0])
        temp = lecture.allocated_room
        lecture.allocated_room = L[0].allocated_room
        L[0].allocated_room = temp
        lecture.overbooked = False
        lecture.already_swapped = True
        return L[0];
    return 0

t = Timeslot(WeekDay.Monday, (10,11))
poin = Room(50,"poin")
ce = Room(500,"CE")
co = Room(300,"CO")
lectures = [
    Lecture("Physique","nerdy things", 200,poin,t,False,True),
    Lecture("Analyse","more nerdy things", 45,ce,t,False,False),
    Lecture("ICC","extreme nerdiness", 350,co,t,False,True)
    ]
overbooked_lectures = [l for l in lectures if l.overbooked]
overbooked_lectures.sort(key=lambda x: x.num_participants, reverse=True)
for l in overbooked_lectures:
    find_better_room(l,lectures)
        
