from architecture import Room, Timeslot, WeekDay, Lecture, Time


def find_better_room(lecture, all_lectures):
    L = [l for l in all_lectures if (lecture.timeslot == l.timeslot and not l.overbooked and not l.already_swapped and l.allocated_room.capacity >= lecture.num_participants) ]
    if len(L) > 0 :
        L.sort(key=lambda x: x.num_participants, reverse=True)
        lecture.already_swapped = True
        L[0].already_swapped = True
        return L[0];
    return 0

t = Timeslot(WeekDay.Monday, (10,11))
poin = Room(50,"poin")
ce = Room(500,"CE")
lectures = [Lecture("cours1","nerdy things", 200,poin,t,False,True),Lecture("cours2","more nerdy things", 45,ce,t,False,False)]
overbooked_lectures = [l for l in lectures if l.overbooked]
overbooked_lectures.sort(key=lambda x: x.num_participants, reverse=True)
for l in overbooked_lectures:
    swap = find_better_room(l,lectures)
    if(swap != 0):
        print(f"swap de {l.code} ({l.num_participants} personnes en {l.allocated_room.name} (capacité : {l.allocated_room.capacity}) le {l.timeslot.day} de {l.timeslot.time[0]} à {l.timeslot.time[1]}) avec {swap.code} ({swap.num_participants} personnes en {swap.allocated_room.name} (capacité : {swap.allocated_room.capacity}))")
