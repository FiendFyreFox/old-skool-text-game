import domains.school.elementQuest.lake_room as lake_room
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    lake_r = lake_room.LakeRoom_surface('lake', roomPath, 'domains.school.elementQuest.oysters')
    lake_r.set_description('clear lake', 'You are on a smooth lake surface. The water is a light blue.')
    lake_r.add_exit('east', 'domains.school.elementQuest.lake_ne')
    lake_r.add_exit('west', 'domains.school.elementQuest.lake_nw')
    lake_r.add_exit('south', 'domains.school.elementQuest.lake_center')

    return lake_r
