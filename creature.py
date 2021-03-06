import random
import gametools
from debug import dbg
from thing import Thing
from container import Container
from weapon import Weapon
from armor import Armor

class Creature(Container):
    def __init__(self, default_name, path, pref_id=None):
        Container.__init__(self, default_name, path, pref_id)
        self.closed = True
        self.closable = False
        self.see_inside = False
        self.hitpoints = 10           # default hitpoints
        self.health = self.hitpoints  # default full health (0 health --> dead)
        self.enemies = []
        self.viewed = False
        self.armor_class = 0
        self.combat_skill = 0
        self.strength = 0
        self.dexterity = 1
        self.default_weapon = gametools.clone("default_weapon")
        self.default_armor = gametools.clone("default_armor")
        self.weapon_wielding = self.default_weapon
        self.armor_worn = self.default_armor
        self.closed_err = "You can't put things in creatures!"
        self.visible_inventory = []     #Things the creature is holding, you can see them.
        self.invisible = False
        self.introduced = set()
        self.proper_name = default_name.capitalize()
        self.dead = False
        self.wizardry_element = None

    def get_saveable(self):
        saveable = super().get_saveable()
        try:
            del saveable['viewed']
        except KeyError:
            pass
        return saveable

    def set_default_weapon(self, name, damage, accuracy, unwieldiness, attack_verbs=["hit"]):
        self.default_weapon = Weapon(name, None, damage, accuracy, unwieldiness, attack_verbs)
        self.weapon_wielding = self.default_weapon

    def set_default_armor(self, name, bonus, unwieldiness):
        self.default_armor = Armor(name, None, bonus, unwieldiness)
        self.armor_worn = self.default_armor

    def set_combat_vars(self, armor_class, combat_skill, strength, dexterity):
        self.armor_class = armor_class
        self.combat_skill = combat_skill
        self.strength = strength
        self.dexterity = dexterity

    def _change_objs_to_IDs(self):
        super()._change_objs_to_IDs()
        self.armor_worn = self.armor_worn.id
        self.weapon_wielding = self.weapon_wielding.id
        self.default_armor = self.default_armor.id
        self.default_weapon = self.default_weapon.id

    def _restore_objs_from_IDs(self):
        super()._restore_objs_from_IDs()
        if isinstance(self.default_weapon, str):
            self.default_weapon = Thing.ID_dict[self.default_weapon]
        if isinstance(self.default_armor, str):
            self.default_armor = Thing.ID_dict[self.default_armor]
        if isinstance(self.weapon_wielding, str):
            self.weapon_wielding = Thing.ID_dict[self.weapon_wielding]
        if isinstance(self.armor_worn, str):
            self.armor_worn = Thing.ID_dict[self.armor_worn]

    def get_short_desc(self, perceiver=None, definite=False, indefinite=False):
        '''Overloads `Thing.get_short_desc()` to return short description of
        the creature, optionally prepended by a definite or indefinite article
        ('a', 'an', 'the', etc.), OR to return the creature's proper name if
        this creature has introduced itself to <perceiver> (usually the 
        player for whom the description is intended).'''
        if perceiver == None:
            dbg.debug("%s.get_short_desc() called with no perceiver specified" % self)
            return "<Error: no perceiver>" + self.short_desc
        if self.id in perceiver.introduced:
            return self.proper_name
        else:
            return super().get_short_desc(perceiver, definite, indefinite)

    def look_at(self, p, cons, oDO, oIDO):
        '''Print out the long description of the creature, as well as any 
        Weapons it is wielding and any armor it is wearing.'''
        self.viewed = cons.user
        if self == oDO or self == oIDO:
            cons.write(self.long_desc)
            if self.weapon_wielding and (self.weapon_wielding != self.default_weapon):
                cons.write("It is wielding a %s." % (self.weapon_wielding.short_desc))        #if we use "bare hands" we will have to change this XXX not true anymore
            if self.armor_worn and (self.armor_worn != self.default_armor):
                cons.write("It is wearing %s." % (self.armor_worn.short_desc))
            if self.visible_inventory and self.visible_inventory != [self.armor_worn, self.weapon_wielding] and self.visible_inventory != [self.weapon_wielding, self.armor_worn]:
                cons.write('It is holding:')
                for i in self.visible_inventory:
                    if i != self.armor_worn and i != self.weapon_wielding:
                        cons.write('/na '+i.short_desc)
            return True
        else:
            return "Not sure what you are trying to look at!"

    def perceive(self, message):
        """Receive a message emitted by an object carried by or in vicinity of this creature."""
        dbg.debug("%s perceived a message %s in Creature.perceive()" % (self.id, message), 2)

    def say(self, speech):
        """Emit a message to the room "The <creature> says: <speech>". """
        self.emit("&nd%s says: %s" % (self.id, speech))

    def take(self, p, cons, oDO, oIDO):
        return "You can't take creatures (or players, for that matter!)"

    def get_armor_class(self):
        return self.armor_class + (0 if not self.armor_worn else self.armor_worn.bonus)
    
    def take_damage(self, enemy, damage):
        self.health -= damage
        if self.health <= 0:
            enemy.gain_combat_skill(self)
            self.die('&nD%s dies!' % self.id)
            return True       # return True if dead, otherwise return False
        return False

    def weapon_and_armor_grab(self):
        if not self.weapon_wielding or self.weapon_wielding == self.default_weapon:
            for w in self.contents:
                if isinstance(w, Weapon) and w.damage > self.default_weapon.damage:
                    self.weapon_wielding = w
                    dbg.debug("weapon chosen: %s" % self.weapon_wielding)
                    self.visible_inventory.append(self.weapon_wielding)
                    self.perceive('You wield the %s, rather than using your %s.' % (self.weapon_wielding.short_desc, self.default_weapon.short_desc))
                    break
        if not self.armor_worn or self.armor_worn == self.default_armor:
            for a in self.contents:
                if isinstance(a, Armor) and a.bonus > self.default_armor.bonus:
                    self.armor_worn = a
                    dbg.debug("armor chosen: %s" % self.armor_worn)
                    self.visible_inventory.append(self.armor_worn)
                    self.perceive('You wear the %s, rather than your %s.' % (self.armor_worn.short_desc, self.default_armor.short_desc))
                    break
    
    def get_damage_message(self, percent_damage):
        if percent_damage <= 0.0:
            message = 'but inflicting no damage'
        elif percent_damage <= 0.1:
            message = 'making a small cut'
        elif percent_damage <= 0.2:
            message = 'doing minor damage'
        elif percent_damage <= 0.4:
            message = 'inflicting a terrible wound'
        elif percent_damage <= 0.6:
            message = 'landing a devastating blow'
        else:
            message = 'with unimaginable force'
        return message

    def gain_combat_skill(self, enemy):
        difficulty = enemy.get_armor_class() / 5.0
        margin_of_victory = self.health / self.hitpoints
        additional_skill_gained = int(difficulty * margin_of_victory)
        self.combat_skill += additional_skill_gained

    def attack(self, enemy):
        if (self == enemy):
            dbg.debug('Creature tried to attack self!', 0)
            return
        chance_of_hitting = self.combat_skill + self.weapon_wielding.accuracy - enemy.get_armor_class()
        if random.randint(1, 100) <= chance_of_hitting:
            d = self.weapon_wielding.damage
            damage_done = random.randint(int(d/2), d) + self.strength / 10.0
            percent_damage = damage_done/enemy.hitpoints
            message = self.get_damage_message(percent_damage)
            self.emit('&nD%s attacks &nd%s with its %s, %s!' % (self.id, enemy, self.weapon_wielding, message), ignore=[self, enemy])
            self.perceive('You attack &nd%s with your %s, %s!' % (enemy, self.weapon_wielding, message))
            enemy.perceive('&nD%s attacks you with its %s, %s!' % (self.id, self.weapon_wielding, message))
            enemy.take_damage(self, damage_done)
            #TODO: Proper names and introductions: The monster attacks you with its sword, Cedric attacks you with his sword, Madiline attacks you with her sword.
        else:
            self.emit('&nD%s attacks &nd%s with its %s, but misses.' % (self.id, enemy, self.weapon_wielding), ignore=[self, enemy])
            self.perceive('You attack &nd%s with your %s, but miss.' % (enemy, self.weapon_wielding))
            enemy.perceive('&nD%s attacks you with its %s, but misses.' % (self.id, self.weapon_wielding))
        if self not in enemy.enemies:
            enemy.enemies.append(self)

    def attack_freq(self):
        try:
            return (20.0/self.dexterity + self.weapon_wielding.unwieldiness + self.armor_worn.unwieldiness)
        except AttributeError:
            return (20.0/self.dexterity)
    
    def die(self, message=None):
        #What to do when 0 health
        self.emit("&nD%s dies!" % self.id, [self])
        corpse = gametools.clone('corpse', self)
        self.location.insert(corpse)
        for i in self.contents:
            i.move_to(corpse)
        if hasattr(self, 'cons'):
            self.move_to(gametools.load_room(self.start_loc_id) if self.start_loc_id else gametools.load_room(gametools.DEFAULT_START_LOC))     #Moves to a location for deletion. TODO: Make nulspace delete anything inside it.
        else:
            self.move_to(Thing.ID_dict['nulspace'])
            self.dead = True
        if message:
            self.emit(message)

    def attack_enemy(self, enemy=None):
        """Attack any enemies, if possible, or if a highly aggressive Creature, attack anyone in the room."""
        targets = [x for x in self.location.contents if (isinstance(x, Creature)) and (x != self) and (x.invisible == False)]
        assert self not in targets
        if not targets:
            return
        attacking = enemy
        if not attacking:
            for i in self.enemies:
                if i in self.location.contents and i.invisible == False:
                    attacking = i
                    assert attacking != self
                    break
        if self.aggressive == 2 and not attacking:
            attacking = random.choice(targets)
            self.enemies.append(attacking)
        
        if attacking == None:
            dbg.debug("%s didn't have anyone to attack!" % self.id, 0)
            return
        
        dbg.debug("%s: attacking %s" % (self.id, attacking))
        self.attacking = attacking
        # Figured out who to attack, wield any weapons/armor
        self.weapon_and_armor_grab()

        if self.attack_freq() <= self.attack_now:
            self.attack(attacking)
        else:
            self.attack_now += 1

class NPC(Creature):
    def __init__(self, ID, path, aggressive=0, pref_id=None):
        Creature.__init__(self, ID, path)
        self.aggressive = aggressive
        self.act_frequency = 3  # how many heartbeats between NPC actions
        self.act_soon = 0       # how many heartbeats till next action
        self.choices = [self.move_around, self.talk]  # list of things NPC might do
        if self.aggressive:     # aggressive: 0 = will never attack anyone, even if attacked by them. Will flee. 1 = only attacks enemies. 2 = attacks anyone. highly aggressive.
            self.choices.append(self.attack_enemy)
        # list of strings that the NPC might say
        self.scripts = []
        self.current_script = None
        self.current_script_idx = 0
        self.attack_now = 0
        self.attacking = False
        self.forbidden_rooms = []

        Thing.game.register_heartbeat(self)
    
    def add_script(self, s):
        self.scripts.append(s)

    def forbid_room(self, r):
        self.forbidden_rooms.append(r)

    def heartbeat(self):
        if self.dead:
            return
        self.act_soon += 1
        if self.act_soon >= self.act_frequency or (set(self.enemies) and set(self.location.contents)) or self.attacking:
            acting = False
            self.act_soon = 0
            if self.current_script:  # if currently reciting, continue
                self.talk()
                acting = True
            try:
                for i in self.location.contents: # if an enemy is in room, attack
                    if i in self.enemies:
                        if self.aggressive:
                            self.attack_enemy(i)
                        else:  #can't attack (e.g. bluebird)? Run away.
                            self.move_around()
                        acting = True
            except AttributeError:
                dbg.debug('AttributeError, not in any room.', 0)
                return
            if self.attacking:
                if (self.attacking not in self.location.contents):
                    for l in self.location.exits:
                        if l == self.attacking.location:
                            self.move_to(l)
                            moved = True
                            break

#                if not moved:
#                    self.attacking = None
            if not acting:           # otherwise pick a random action
                choice = random.choice(self.choices)
                try:
                    try:
                        choice()
                    except TypeError:
                        choice(self)
                except NameError:
                    dbg.debug("Object "+str(self.id)+" heartbeat tried to run non-existant action choice "+str(choice)+"!", 0)
            
    def move_around(self):
        """The NPC leaves the room, taking a random exit"""
        try:
            exit_list = list(self.location.exits)
            exit = random.choice(exit_list)
        except (AttributeError, IndexError):
            dbg.debug('NPC %s sees no exits, returning from move_around()' % self.id)
            return

        dbg.debug("Trying to move to the %s exit!" % (exit))
        current_room = self.location
        new_room_string = self.location.exits[exit]
        new_room = gametools.load_room(new_room_string)
        if new_room.monster_safe:
            dbg.debug('Can\'t go to %s; monster safe room!' % new_room_string)
            return

        if new_room_string in self.forbidden_rooms:
            dbg.debug('Can\'t go to %s: forbidden to %s!' % (new_room_string, self))
 
        self.emit("&nD%s goes %s." % (self.id, exit))
        self.move_to(new_room)
        self.emit("&nI%s arrives." % self.id)
        dbg.debug("Creature %s moved to new room %s" % (self.names[0], new_room_string), 1)
        return

    def talk(self):
        if self.scripts:
            if self.current_script:
                lines = self.current_script.splitlines()
                index = self.current_script_idx
                self.say(lines[index])
                self.current_script_idx += 1
                if self.current_script_idx == len(lines):
                    self.current_script = None
                    self.current_script_idx = 0
            else:
                self.current_script = random.choice(self.scripts)
    