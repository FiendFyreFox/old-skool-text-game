from thing import Thing
from container import Container
from room import Room
from scenery import Scenery
from liquid import Liquid
from book import Book
from cauldron import Cauldron

from domains.school.bookcase import Bookcase
from domains.school.scroll import Scroll

from debug import dbg 

grand_entry = Room('grand entry', safe=True)
great_hall = Room('great hall', safe=True)
landing = Room('landing', safe=True)
gallery = Room('gallery', safe=True)
library = Room('library', safe=True)
hmasters_office = Room('office', safe=True)
towerstairs = Room('towerstairs', safe=True)
lookout = Room('lookout', safe=True)
potion_storage = Room('potion storage', safe=True)
hallway = Room('hallway', safe=True)

grand_entry.set_description('grand school entryway', 'This is the most magnificent entryway you have ever seen. The enormous front door is at the top of the marble staircase, with huge pillars on either side.')
great_hall.set_description('Great Hall', 'This is the biggest room in the entire school, and it is enormous. It is made of ancient stones. To the east a grand staircase rises to an elevated landing.')
landing.set_description('elevated landing overlooking the great hall', 'You stand on a landing of a grand staircase, overlooking the cavernous Great Hall. From here the staircase splits to two smaller staircases, to the northeast and southeast, which lead to the next level.')
gallery.set_description('portrait gallery', "This gradiose portrait gallery overlooks the Great Hall through a pillared colonade.")
library.set_description('library', "You find yourself in a comfortable library filled from floor to ceiling with books and bookcases. The room is circular, and must be built into a round tower as windows look out in every direction. A spiral staircase in the center of the room leads upwards.")
hmasters_office.set_description('grandiose headmasters office', 'You look at a giant room with a large bay window in the back. There is a giant carved oak desk in the middle of the room. There are many bookcases lining the walls, and stacks of papers on the desk.')
towerstairs.set_description('spiral staircase leading up the tower', 'You find yourself in a enormous tower, with winding stairs leading up it. There is a small door to the east.')
lookout.set_description('circular lookout', 'This lookout looks over the entire school and surrounding area. With 360 degree views, you see:'+  \
'\n'+'a thick forest \n'+'a little house \n'+'a garden \n'+'a distant mountain range \n'+'more thick forest, and some school grounds \n'+'even more forest that streaches on for hundreds of miles')
potion_storage.set_description('potion storage room', 'This is a stonewalled potion storage room, dimly lit. It has many cauldrons on a open shelf, and many burners for stirring cauldrons. It has many ingredients in a different open shelf across the room.'
'You have to step carefully here, as the floor is covered in shards of broken glass.')
hallway.set_description('staff office hallway', 'This hallway leads to all of the staff offices. It is very blank on the walls, however, the walls themselves are intricate and have little carved patterens in them.')

grand_entry.add_names('entry', 'entryway')
grand_entry.add_adjectives('grand', 'magnificent')
great_hall.add_names('hall', 'chamber')
great_hall.add_adjectives('grand', 'enourmous')
hmasters_office.add_adjectives("grandiose", 'headmaster\'s')
towerstairs.add_names('stairs')
towerstairs.add_adjectives('tower', 'spiral')
lookout.add_adjectives('circular')
potion_storage.add_names('potion', 'storage')
potion_storage.add_names('room')
hallway.add_adjectives('staff', 'office')

grand_entry.add_exit('southwest', 'field')
grand_entry.add_exit('northwest', 'garden')
grand_entry.add_exit('east', great_hall.id)
great_hall.add_exit('west', grand_entry.id)
great_hall.add_exit('east', landing.id)
landing.add_exit('northeast', gallery.id)
landing.add_exit('southeast', library.id)
landing.add_exit('west', great_hall.id)
gallery.add_exit('east', landing.id)
gallery.add_exit('north', hmasters_office.id)
gallery.add_exit('northeast', hallway.id)
library.add_exit('northwest', landing.id)
library.add_exit('up', towerstairs.id)
hmasters_office.add_exit('south', gallery.id)
towerstairs.add_exit('down', library.id)
towerstairs.add_exit('up', lookout.id)
lookout.add_exit('down', towerstairs.id)
potion_storage.add_exit('up', library.id)
hallway.add_exit('south', gallery.id)
Thing.ID_dict['field'].add_exit('northeast', grand_entry.id)
Thing.ID_dict['garden'].add_exit('southeast', grand_entry.id)

bookcase = Bookcase('bookcase', potion_storage)
library.insert(bookcase)

potion_book = Book("leather book", "leather-bound tome", "This is an old leather-bound book titled \"Potion Recipies for the Beggining and Intermediate Sorcerer (First Edition).\"")
potion_book.add_names("tome", "book")
potion_book.add_adjectives("leather-bound", "leather")
potion_book.set_message('''


Potion Recipies for the Beggining and Intermediate Wizard (First Edition)

#*
Table of Contents:

Invisibility Potion on page 3
Pink Potion on page 4

#*
Invisibility Potion

The First Step: Gather thyself moss from a cave, water, truffles, a petal from a sunflower, and molasses.
The Second Step: Put the ingredients in thy cauldron and put the cauldron over a burner.
The Third Step: Drink thys potion, and turn thyself invisible.
The Fourth Step: Beware, becuase thy will not be invisible forever.
#*
Pink Potion

The First Step: Gather thyself water, molasses, and a seed from a poppy.
The Second Step: Put the ingredients in a cauldron and put the cauldron over a burner.
The Third Step: Drink thys potion, and turn thyself pink.
The Fourth Step: Beware, because thy will not be pink for long.
#*
''')
potion_book.move_to(library)

b_table = Container('table')
b_table.set_description('banquet-size table', 'This is a extremely long banquet table, stretching almost from one end of the room to the other.')
b_table.fix_in_place('Moving this table would require a lot of help.')
b_table.add_adjectives('massive', 'enormous', 'long', 'banquet')
b_table.set_prepositions('on', "onto")
b_table.set_max_weight_carried(4e9)
b_table.set_max_volume_carried(3e9)
great_hall.insert(b_table)

desk = Container('desk')
desk.set_description('carved oak desk', 'This carved oak desk is clearly more than 100 years old, and is carved out in the shapes of dragons and other vicious creatures.')
desk.fix_in_place('The desk is very, very heavy, and feels rooted to the floor.')
desk.add_adjectives('carved', 'oak')
desk.set_prepositions('on', 'onto', 'in', 'into')
desk.set_max_weight_carried(4e9)
desk.set_max_volume_carried(80)
desk.move_to(hmasters_office)

cauldron = Cauldron('cauldron')
cauldron.set_description('iron cauldron', 'This is a iron cauldron.')
cauldron.set_max_weight_carried(2000)
cauldron.set_max_volume_carried(30)
cauldron.move_to(potion_storage)

scale = Thing('dragon scale')
scale.set_description('golden dragon scale', 'This is a golden dragon scale. It is used in many very strong potions.')
scale.add_adjectives('dragon', 'golden')
scale.add_names('scale')
scale.move_to(potion_storage)
scale.set_spawn(Thing.ID_dict['nulspace'].game, potion_storage, 4)

scroll = Scroll('scroll')