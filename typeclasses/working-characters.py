"""
GO!
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter, TICKER_HANDLER
import random

class Character(DefaultCharacter):
# [...]

    PHYSICAL_STATS = ('strength', 'dexterity', 'stamina')
    SOCIAL_STATS = ('charisma', 'manipulation', 'appearance')
    MENTAL_STATS = ('perception', 'intelligence', 'wits')
    ALL_STATS = PHYSICAL_STATS + SOCIAL_STATS + MENTAL_STATS
   
    def randomize_stats(self, stats, max):
        while max > 0:
            max -= 1
            stat = random.choice(stats)
            current_value = self.attributes.get(stat, 1)
            self.attributes.add(stat, current_value + 1)
 
    def at_object_creation(self):
        """
        Called only at initial creation. This is a rather silly
        example since ability scores should vary from Character to
        Character and is usually set during some character
        generation step instead.
        """
        #set persistent attributes
        self.db.tradition = "Orphans"
        genum = random.randint(1,4)
        if genum == 1:
            self.db.essence = "Dynamic"
        if genum == 2:
            self.db.essence = "Pattern"
        if genum == 3:
            self.db.essence = "Primordial"
        if genum == 4:
            self.db.essence = "Questing"

        genum = random.randint(1,20)
        if genum == 1:
            self.db.concept = "Activist"
        if genum == 2:
            self.db.concept = "Artist"
        if genum == 3:
            self.db.concept = "Criminal"
        if genum == 4:
            self.db.concept = "Crusader"
        if genum == 5:
            self.db.concept = "Hacker"
        if genum == 6:
            self.db.concept = "Intellectual"
        if genum == 7:
            self.db.concept = "Kid"
        if genum ==8:
           self.db.concept = "Loner"
        if genum == 9:
           self.db.concept = "Mystic"
        if genum == 10:
           self.db.concept = "Night-Owl"
        if genum == 11:
           self.db.concept = "Official"
        if genum ==12:
           self.db.concept = "Prophet"
        if genum ==13:
           self.db.concept = "Rebel"
        if genum ==14:
           self.db.concept = "Rogue"
        if genum ==15:
           self.db.concept = "Scientist"
        if genum ==16:
           self.db.concept = "Survivor"
        if genum ==17:
           self.db.concept = "Techie"
        if genum == 18:
           self.db.concept = "Trickster"
        if genum == 19:
           self.db.concept = "Visionary"
        if genum == 20:
           self.db.concept = "Wage-Slave"


        self.db.strength = 1
        self.db.dexterity = 1
        self.db.stamina = 1
        self.db.charisma = 1
        self.db.manipulation = 1
        self.db.appearance = 1
        self.db.perception = 1
        self.db.intelligence = 1
        self.db.wits = 1        

        for stat in self.ALL_STATS:
            self.attributes.add(stat, 0)        
 
        priorities = random.randint(1,6)

        if priorities == 1:
            self.randomize_stats(self.PHYSICAL_STATS, 10)
 
            self.randomize_stats(self.SOCIAL_STATS, 8)
 
            self.randomize_stats(self.MENTAL_STATS, 6)

        if priorities == 2:
            self.randomize_stats(self.PHYSICAL_STATS, 10)
 
            self.randomize_stats(self.SOCIAL_STATS, 6)
 
            self.randomize_stats(self.MENTAL_STATS, 8)

        if priorities == 3:
            self.randomize_stats(self.PHYSICAL_STATS, 8)
 
            self.randomize_stats(self.SOCIAL_STATS, 10)
 
            self.randomize_stats(self.MENTAL_STATS, 6)

        if priorities == 4:
            self.randomize_stats(self.PHYSICAL_STATS, 8)
 
            self.randomize_stats(self.SOCIAL_STATS, 6)
 
            self.randomize_stats(self.MENTAL_STATS, 10)
     
        if priorities == 5:
            self.randomize_stats(self.PHYSICAL_STATS, 6)
 
            self.randomize_stats(self.SOCIAL_STATS, 8)
 
            self.randomize_stats(self.MENTAL_STATS, 6)

        if priorities == 6:
            self.randomize_stats(self.PHYSICAL_STATS, 6)
 
            self.randomize_stats(self.SOCIAL_STATS, 10)
 
            self.randomize_stats(self.MENTAL_STATS, 8)


        self.db.conscious = 1
        self.db.alive = 1
        self.db.sight = 0
        self.db.conscious = 1
        self.db.alertness = 0
        self.db.athletics = 0
        self.db.awareness = 0
        self.db.brawl = 0
        self.db.intimidation = 0
        self.db.streetwise = 0
        self.db.drive = 0
        self.db.firearms = 0
        self.db.martialarts = 0
        self.db.melee = 0
        self.db.meditation = 0
        self.db.stealth = 0
        self.db.astrology = 0
        self.db.computer = 0
        self.db.language = 0
        self.db.medicine = 0
        self.db.occult = 0
        self.db.rituals = 0
        self.db.correspondence = 0
        self.db.entropy = 0
        self.db.forces = 0
        self.db.life = 0
        self.db.matter = 0
        self.db.mind = 0
        self.db.prime = 0
        self.db.spirit = 0
        self.db.time = 0
        self.db.quintessence = 0
        self.db.arete = 0
        self.db.willpower = 0
        self.db.arcane = 0
        self.db.belief = 0
        self.db.familiar = 0
        self.db.luck = 0
        self.db.resources = 0
        self.db.target = self
        self.db.attacker = self
        self.db.bashing = 0
        self.db.lethal = 0
        self.db.weapon = 0
        self.db.invis = 0
        self.db.blessed = 0
        self.db.cursed = 0
        self.db.burned = 0
        self.db.astro = 0
        self.db.starsign = 0
        self.db.attack_not = 1
        self.touch = 0
        self.intimidated = 0

        TICKER_HANDLER.add(60, self.heal)
        TICKER_HANDLER.add(120, self.heal_lethal)
        TICKER_HANDLER.add(180, self.spells)
        TICKER_HANDLER.add(15, self.ban)
        return

    def ban(self, *args, **kwards):
        if(self.db.ban  == self.location):
            self.msg("This area does not want you here!.")
            self.db.cursed = int(self.db.cursed) + 1

    def spells(self, *args, **kwards):
        if(self.ndb.sap):
            self.ndb.sap = self.ndb.sap -1
            self.db.strength = self.db.strength + 1
            self.db.dexterity = self.db.dexterity + 1
            self.db.stamina = self.db.stamina + 1
            self.msg("You regain some of your energy.")
        if(self.ndb.portA):
            self.msg("The portal has closed.")
            self.ndb.portA.delete()
            self.ndb.portB.delete()
        if(self.db.spy):
           self.db.spy = None
        if(int(self.db.attack_not) == 0):
            self.db.attack_not = 1
        if(self.db.astro == 1):
            self.db.astro = 0
        if(self.db.burned > 0):
            self.msg("You recover some of your natural luck.")
            self.db.burned = self.db.burned - 1
        if(self.db.invis == 1):
            self.db.invis = 0
            self.msg("You have become visible.")
        if(self.db.move_speed == "freeze"):
            self.msg("Time begins to move normally again.")
        if(self.db.sight == 1):
            self.msg("Your vision to the spirit world fades.")
            self.db.sight = 0
        if self.db.blessed > 0:
           self.msg("Your luck is starting to fade.")
           self.db.blessed = int(self.db.blessed) - 1
        if self.db.blessed < 0:
           self.msg("The hex has begun to leave you.")
           self.db.blessed = int(self.db.blessed) + 1
        if(self.db.touch == 1):
            if self.db.alive:
                self.msg("You lose grasp on the spirit world.")
            else:
                self.msg("You lose graph on the physical world.")
            self.db.touch = 0
        if(self.db.alive == 0):
            self.db.conscious = 1
            self.msg("You take a deep breath of astral air.")


    def heal_lethal(self, *args, **kwargs):

        if(self.db.cursed > 0):
            self.db.cursed = int(self.db.cursed) - 1

        if(self.db.lethal > 0 and self.db.alive == 1):
            self.msg("You heal 1 point of lethal damage.")
            self.db.lethal = self.db.lethal  - 1
            healthbar = "|X|[wHealth:"
            total = self.db.lethal + self.db.bashing

            diff = 8 - self.db.lethal

            if self.db.bashing > diff:
                self.db.lethal += self.db.bashing - diff
                self.db.bashing -= self.db.bashing - diff
            for i in range(0,8):
                if i < self.db.lethal:
                    healthbar += " X"
                elif i < total:
                    healthbar += " /"
                else:
                    healthbar += " 0"

            healthbar += "|/"
            self.msg(prompt=healthbar)

            if(total<8):
                self.db.conscious = 1
               
    def heal(self, *args, **kwargs):
        if(self.ndb.nameSave):
            self.key = self.ndb.nameSave
            self.db.desc = self.ndb.descSave
            self.db.image = self.ndb.imageSave
            self.ndb.nameSave = None
            self.ndb.descSave = None
            self.ndb.imageSave = None
            self.msg("You have changed back.")

        if(self.ndb.frozen_room):
            self.ndb.frozen_room.db.freeze = 0
            for item in self.ndb.frozen_room.contents:
                    item.msg("Time has started again.")
            self.ndb.frozen_room = None

        if(self.db.bashing > 0 and self.db.alive == 1):
            self.msg("You heal 1 point of bashing damage.")
            self.db.bashing = self.db.bashing - 1

            healthbar = "|X|[wHealth:"
            total = self.db.lethal + self.db.bashing

            diff = 8 - self.db.lethal
            if self.db.bashing > diff:
                self.db.lethal += self.db.bashing - diff
                self.db.bashing -= self.db.bashing - diff
            for i in range(0,8):
                if i < self.db.lethal:
                    healthbar += " X"
                elif i < total:
                    healthbar += " /"
                else:
                    healthbar += " 0"
            healthbar += "|/"
            self.msg(prompt=healthbar)
            if(total<8):
                self.db.conscious = 1

    def get_abilities(self):
        """
        Simple access method to return ability
        scores as a tuple (str,agi,mag)
        """
        return self.db.strength, self.db.agility, self.db.magic

    def is_alive(self):
        return self.db.alive

    def at_post_puppet(self):

        super(Character, self).at_post_puppet()
        healthbar = "|X|[wHealth:"
        total = self.db.lethal + self.db.bashing

        diff = 8 - self.db.lethal

        if self.db.bashing > diff:
            self.db.lethal += self.db.bashing - diff
            self.db.bashing -= self.db.bashing - diff
        for i in range(0,8):
            if i < self.db.lethal:
                healthbar += " X"
            elif i < total:
                healthbar += " /"
            else:
                healthbar += " 0"
        healthbar += "|/"
        self.msg(prompt=healthbar)

    def return_appearance(self, looker):
        looker.msg(image=[self.db.image, self.db.desc])

        def at_post_unpuppet(self, account, session=None):
            """
            We stove away the character when the account goes ooc/logs off,
            otherwise the character object will remain in the room also
            after the account logged off ("headless", so to say).
            Args:
            account (Account): The account object that just disconnected
                from this object.
            session (Session): Session controlling the connection that
                just disconnected.
            """
            if not self.sessions.count():
               # only remove this char from grid if no sessions control it anymore.
               if self.location:
                  self.location.for_contents(message, exclude=[self], from_obj=self)
                  self.db.prelogout_location = self.location
                  self.location = self.db.prelogout_location
                  self.ndb._menutree.close_menu()
                  self.db.target.ndb._menutree.close_menu()


    def at_after_move(self, source_location):
        """
        We make sure to look around after a move.
        """
        if self.location.access(self, "view"):
            self.msg(self.at_look(self.location))

            healthbar = "|X|[wHealth:"
            total = self.db.lethal + self.db.bashing

            diff = 8 - self.db.lethal
            if self.db.bashing > diff:
                self.db.lethal += self.db.bashing - diff
                self.db.bashing -= self.db.bashing - diff
            for i in range(0,8):
                if i < self.db.lethal:
                    healthbar += " X"
                elif i < total:
                    healthbar += " /"
                else:
                    healthbar += " 0"
            healthbar += "|/"
            self.msg(prompt=healthbar)


    def announce_move_from(self, destination, msg=None, mapping=None):
        """
        Called if the move is to be announced. This is
        called while we are still standing in the old
        location.
        Args:
            destination (Object): The place we are going to.
            msg (str, optional): a replacement message.
            mapping (dict, optional): additional mapping objects.
        You can override this method and call its parent with a
        message to simply change the default message.  In the string,
        you can use the following as mappings (between braces):
            object: the object which is moving.
            exit: the exit from which the object is moving (if found).
            origin: the location of the object before the move.
            destination: the location of the object after moving.
        """
        if not self.location:
            return
        if msg:
            string = msg
        else:
            string = "{object} is leaving {origin}, heading for {destination}."

        location = self.location
        exits = [o for o in location.contents if o.location is location and o.destination is destination]
        if not mapping:
            mapping = {}

        mapping.update({
                "object": self,
                "exit": exits[0] if exits else "somwhere",
                "origin": location or "nowhere",
                "destination": destination or "nowhere",
        })


        out = []
        for objects in self.location.contents:
            if(objects.db.conscious == 0 or objects.db.alive == 0) or (objects.db.freeze == 1 and self.caller.db.present == 0):
                out.append(objects)
        out.append(self)
        self.location.msg_contents(string, exclude=out, mapping=mapping)

      #  out = []
      #  for objects in self.location.contents:
      #      if objects.db.conscious == 0 or objects.db.alive == 0:
      #          out.append(objects)
      #  if(out):
      #      self.location.msg_contents(string, exclude=(self,out[0]), mapping=mapping)
      #  else:
      #      self.location.msg_contents(string, exclude=(self, ), mapping=mapping)

    def announce_move_to(self, source_location, msg=None, mapping=None):
        """
        Called after the move if the move was not quiet. At this point
        we are standing in the new location.
        Args:
            source_location (Object): The place we came from
            msg (str, optional): the replacement message if location.
            mapping (dict, optional): additional mapping objects.
        You can override this method and call its parent with a
        message to simply change the default message.  In the string,
        you can use the following as mappings (between braces):
            object: the object which is moving.
            exit: the exit from which the object is moving (if found).
            origin: the location of the object before the move.
            destination: the location of the object after moving.
        """

        if not source_location and self.location.has_account:
            # This was created from nowhere and added to an account's
            # inventory; it's probably the result of a create command.
            string = "You now have %s in your possession." % self.get_display_name(self.location)
            self.location.msg(string)
            return

        if source_location:
            if msg:
                string = msg
            else:
                string = "{object} arrives to {destination} from {origin}."
        else:
            string = "{object} arrives to {destination}."

        origin = source_location
        destination = self.location
        exits = []
        if origin:
            exits = [o for o in destination.contents if o.location is destination and o.destination is origin]

        if not mapping:
            mapping = {}

        mapping.update({
                "object": self,
                "exit": exits[0] if exits else "somewhere",
                "origin": origin or "nowhere",
                "destination": destination or "nowhere",
        })
        out = []
        for objects in self.location.contents:
            if(objects.db.conscious == 0 or objects.db.alive == 0) or (objects.db.freeze == 1 and self.caller.db.present == 0):
                out.append(objects)
        out.append(self)
        self.location.msg_contents(string, exclude=out, mapping=mapping)
