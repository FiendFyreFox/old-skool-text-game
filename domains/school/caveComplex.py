from debug import dbg
import gametools

from thing import Thing
from container import Container
from room import Room
from action import Action
from creature import Creature
from player import Player
from creature import NPC

class Lair(Room):
    def go_to(self, p, cons, oDO, oIDO):
        if self.monster in self.contents:
            if p.words[1] == 'northwest':
                if cons.user.invisible != True:
                    cons.write('You try to enter the crawlway, but the monster blocks your path.')
                    return True
        return Room.go_to(self, p, cons, oDO, oIDO)

class CaveRoom(Room):
    def __init__(self, ID, path, monster_storage):
        Room.__init__(self, ID, path, light=0)
        self.monster_storage = monster_storage
        self.released_monster = False
        self.create_cave_moss()
        self.create_gold()

    def create_cave_moss(self):
        for i in self.contents:
            if i.names[0] == 'cave moss':
                return True
        cave_moss = gametools.clone('domains.school.cave.cave_moss')
        cave_moss.move_to(self)

    def create_gold(self):
        for i in self.contents:
            if i.names[0] == 'gold':
                return True
        gold = gametools.clone('domains.school.cave.gold')
        self.insert(gold)
    
    def attach_monster(self, monster):
        self.monster = monster
        del self.monster.choices[0]  #keeps monster from moving around except to attack people in the cave or lair
        del self.monster.choices[0]  #so the monster is quicker to choose the attack_enemy option. TODO: make monster automatically attack enemy when it is released.
        self.monster.move_to(self.monster_storage)
        self.monster_storage.monster = self.monster
    
    def go_to(self, p, cons, oDO, oIDO):
        if self.monster in self.contents:
            if p.words[1] == 'west':
                if cons.user.invisible != True:
                    cons.write('You try to go to the west, but the monster blocks your path.')
                    return True
        return Room.go_to(self, p, cons, oDO, oIDO)

    def heartbeat(self):
        gold_check = False
        cave_moss_check = False
        for k in self.contents:
            if k.names[0] == 'cave moss':
                cave_moss_check = True
            if k.names[0] == 'gold':
                gold_check = True
        if not cave_moss_check or not gold_check:
            if self.released_monster == False:
                if self.monster.location == self.monster_storage:
                    self.monster_storage.extract(self.monster)
                    self.insert(self.monster)
                    self.monster.emit('&nI%s arrives!' % self.monster.id)
                    self.released_monster == True
                    self.counter = 10
                    for m in self.contents:
                        if m != self.monster and isinstance(m, Creature):
                            self.monster.enemies.append(m)
        if self.released_monster:
            self.counter -= 1
            if self.counter <= 0:
                self.monster.move_to(self.monster_storage)
                self.create_cave_moss()
                self.create_gold()
                self.released_monster = False

