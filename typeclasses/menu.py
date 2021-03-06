from evennia.utils.evmenu import EvMenu
from evennia.contrib.dice import roll_dice
from evennia.utils.create import create_object
from evennia import default_cmds, utils
from evennia import create_script
from timeit import default_timer as timer

damage = 0
# Menu implementing the dialogue tree
def exit_combat(caller):
    caller.execute_cmd('Exit')

def attack_node(caller):
   
    caller.ndb.timebug = 1
    healthbar = "|/|X|[wHealth:"
    total = caller.db.lethal + caller.db.bashing

    diff = 8 - caller.db.lethal

    if caller.db.bashing > diff:
        caller.db.lethal += caller.db.bashing - diff
        caller.db.bashing -= caller.db.bashing - diff
    for i in range(0,8):
        if i < caller.db.lethal:
            healthbar += " X"
        elif i < total:
            healthbar += " /"
        else:
            healthbar += " 0"
    healthbar += "|/"
    caller.msg(prompt=healthbar)
    if(total>=8):
        caller.db.conscious = 0
    if(caller.db.lethal>=8):
        caller.db.alive = 0
        caller.locks.add("view:attr(alive, 0)")
    if(total<8):
        caller.db.conscious = 1
    caller.db.start_time = timer()

    attack_script = create_script("typeclasses.attackwait.AttackTime", obj=caller)
    attack_script.attacker(caller)
    attack_script.target(caller.db.target)

    text = ""
    if caller.db.form == "human":
        options = ({"key": "|ypunch",
            "desc": "Punch %s" % caller.db.target,
            "goto": "wait",
            "exec": "punch"},
            {"key": "|ykick",
            "desc": "Kick %s" % caller.db.target,
            "goto": "wait",
            "exec": "kick"},
            {"key": "|ywield",
            "desc": "Wield a weapon",
            "goto": "wield",
            "exec": "wield"},
            {"key": "|yskip",
            "desc": "Do nothing",
            "goto": "skip_attack"},)
        if caller.db.martialarts > 0:
            options += ({"key": "|ystrike",
                      "desc": "martial arts",
                      "goto": "wait",
                      "exec": "lethalpunch"},)
        if caller.db.attack_not:
            caller.db.mercy = 1
            options += ({"key": "|ymercy",
                      "desc": "Beg for mercy",
                      "goto": "wait",
                      "exec": "mercy_attack"},)
        options += ({"key": "|yflee",
                  "desc": "Flee from combat.",
                  "goto": "wait",
                  "exec": "flee_attack"},)

        for each in caller.contents:
               
            if caller.db.selected_weapon.lower() == each.key.lower():
                if(each.db.weapon == 2):
                    options += ({"key": "|y" + each.key,
                        "desc": "A knife.",
                        "goto": "wait",
                        "exec": "knife"},)
                if(each.db.weapon == 1):
                    options += ({"key": "|y" + each.key,
                        "desc": "An Axe.",
                        "goto": "wait",
                        "exec": "axe"},)
                if(each.db.weapon == 3):
                    options += ({"key": "|y" + each.key,
                        "desc": "A baseball bat.",
                        "goto": "wait",
                        "exec": "bat"},)
                if(each.db.weapon == 4):
                    options += ({"key": "|y" + each.key,
                        "desc": "A staff.",
                        "goto": "wait",
                        "exec": "staff"},)
                if(each.db.weapon == 5):
                    options += ({"key": "|y" + each.key,
                        "desc": "A sword.",
                        "goto": "wait",
                        "exec": "katana"},)
                if(each.db.weapon == 6):
                    options += ({"key": "|y" + each.key,
                        "desc": "A pistol.",
                        "goto": "auto",
                        "exec": "pistol"},)

        if(caller.db.conscious == 0 and caller.db.alive == 1):
            options = ({"key": "_default",
                "goto": "skip_attack"})

        if(caller.db.move_speed == "freeze"  and caller.db.alive == 1):
            options = ({"key": "_default",
            "goto": "skip_attack"})

        if(caller.db.attacking == 0):
            pain = (caller.db.bashing + caller.db.wits) / 2
            init_a = caller.db.wits + caller.db.intimidation + caller.db.stamina
            init_b = caller.db.target.db.intimidation + pain
            init_a = init_a + roll_dice(1,10)
            init_b = init_b + roll_dice(1,10)
            if(init_a  < init_b and caller.db.conscious and caller.db.target.db.conscious):
                caller.db.target.msg("|/|r%s is too afraid to fight" % caller.name)
                accounts = [con for con in caller.location.contents if con.has_account]
                for account in accounts:
                    if not account.ndb.end_combat:
                        account.msg("%s is too afraid to fight." % caller.name)
                text = ("|rYou are too afraid to fight")

                caller.db.intimidated = 1
                options = ({"key": "_default",
                "goto": "skip_attack"})

    if caller.db.form == "cat":
        options = ({"key": "|yclaw",
            "desc": "Claw %s" % caller.db.target,
            "goto": "wait",
            "exec": "claw"},
            {"key": "|ybite",
            "desc": "Bite %s" % caller.db.target,
            "goto": "wait",
            "exec": "bite"},
            {"key": "|yskip",
            "desc": "Do nothing",
            "goto": "skip_attack"},)
        if caller.db.attack_not:
            caller.db.mercy = 1
            options += ({"key": "|ymercy",
                      "desc": "Beg for mercy",
                      "goto": "wait",
                      "exec": "mercy_attack"},)
        options += ({"key": "|yflee",
                  "desc": "Flee from combat.",
                  "goto": "wait",
                  "exec": "flee_attack"},)


        if(caller.db.conscious == 0 and caller.db.alive == 1):
            options = ({"key": "_default",
                "goto": "skip_attack"})

        if(caller.db.move_speed == "freeze"  and caller.db.alive == 1):
            options = ({"key": "_default",
            "goto": "skip_attack"})

        if(caller.db.attacking == 0):
            pain = (caller.db.bashing + caller.db.wits) / 2
            init_a = caller.db.wits + caller.db.intimidation + caller.db.stamina
            init_b = caller.db.target.db.intimidation + pain
            init_a = init_a + roll_dice(1,10)
            init_b = init_b + roll_dice(1,10)
            if(init_a  < init_b and caller.db.conscious and caller.db.target.db.conscious):
                caller.db.target.msg("|/|r%s is too afraid to fight" % caller.name)
                accounts = [con for con in caller.location.contents if con.has_account]
                for account in accounts:
                    if not account.ndb.end_combat:
                        account.msg("%s is too afraid to fight." % caller.name)
                text = ("|rYou are too afraid to fight")

                caller.db.intimidated = 1
                options = ({"key": "_default",
                "goto": "skip_attack"})

    if caller.db.form == "dog":
        options = ({"key": "|ybite",
            "desc": "Bite %s" % caller.db.target,
            "goto": "wait",
            "exec": "bite"},
            {"key": "|yskip",
            "desc": "Do nothing",
            "goto": "skip_attack"},)
        if caller.db.attack_not:
            caller.db.mercy = 1
            options += ({"key": "|ymercy",
                      "desc": "Beg for mercy",
                      "goto": "wait",
                      "exec": "mercy_attack"},)
        options += ({"key": "|yflee",
                  "desc": "Flee from combat.",
                  "goto": "wait",
                  "exec": "flee_attack"},)


        if(caller.db.conscious == 0 and caller.db.alive == 1):
            options = ({"key": "_default",
                "goto": "skip_attack"})

        if(caller.db.move_speed == "freeze"  and caller.db.alive == 1):
            options = ({"key": "_default",
            "goto": "skip_attack"})

        if(caller.db.attacking == 0):
            pain = (caller.db.bashing + caller.db.wits) / 2
            init_a = caller.db.wits + caller.db.intimidation + caller.db.stamina
            init_b = caller.db.target.db.intimidation + pain
            init_a = init_a + roll_dice(1,10)
            init_b = init_b + roll_dice(1,10)
            if(init_a  < init_b and caller.db.conscious and caller.db.target.db.conscious):
                caller.db.target.msg("|/|r%s is too afraid to fight" % caller.name)
                accounts = [con for con in caller.location.contents if con.has_account]
                for account in accounts:
                    if not account.ndb.end_combat:
                        account.msg("%s is too afraid to fight." % caller.name)
                text = ("|rYou are too afraid to fight")

                caller.db.intimidated = 1
                options = ({"key": "_default",
                "goto": "skip_attack"})
    
    return text, options


def select_weapon(caller, input):
    caller.db.start_time = timer()
    caller.db.selected_weapon = input
    caller.db.target.msg("|/|g%s wields his %s." % (caller.name, caller.db.selected_weapon))
    accounts = [con for con in caller.location.contents if con.has_account]
    for account in accounts:
        if not account.ndb.end_combat:
            account.msg("%s wield his %s." % (caller.name, caller.db.selected_weapon))
    text = ("|/|gYou wield the %s" % input)
    EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node",auto_quit=False, cmd_on_exit=None)

    options = ({"key": "_default", 
        "goto": "skip_attack"})
    return text, options

def remove_weapon(caller, input):
        caller.db.start_time = timer()
        caller.db.target.msg("|/|g%s puts his %s away." % (caller.name, caller.db.selected_weapon))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s puts away his %s." % (caller.name, caller.db.selected_weapon))
        text = ("|/|gYou put your %s away" % caller.db.selected_weapon)
        caller.db.selected_weapon = "None"
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node",auto_quit=False, cmd_on_exit=None)

        options = ({"key": "_default", 
                "goto": "skip_attack"})
        return text, options

def wield(caller):
    caller.db.start_time = timer() - 7
    text = ""
    options = ()
    for each in caller.contents:
        options += ({"key": "|y" + each.name,
            "desc": "appearances",
            "goto": "select_weapon"},)
    options += ({"key": "|y remove",
                "desc": "remove weapons",
                "goto": "remove_weapon"},
                {"key": "_default",
        "goto": "skip_attack"},)

    return text, options

def punch(caller):
    caller.db.weapon = 0
    caller.db.attack_not = 0
    test = caller.db.dexterity + caller.db.brawl +caller.db.blessed
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 6):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints
    hit = caller.db.strength
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou punch %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to punch you with %i succesful rolls." % (caller, attackpoints))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s punches %s." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s punches, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
        "goto": "skip_attack"})
    return text, options

def lethalpunch(caller):
    caller.db.weapon = 1
    caller.db.attack_not = 0
    test = caller.db.dexterity + caller.db.martialarts +caller.db.blessed
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 6):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints
    hit = caller.db.strength
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou execute a lethal punch on %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attacks with a lethal punch, using %i succesful rolls." % (caller, attackpoints))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s strikes %s." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s punches, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
        "goto": "skip_attack"})
    return text, options


def claw(caller):
    caller.db.weapon = 0
    caller.db.attack_not = 0
    test = caller.db.dexterity + caller.db.brawl +caller.db.blessed
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 6):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints
    hit = caller.db.strength
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou claw %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to claw you with %i succesful rolls." % (caller, attackpoints))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s claws %s." % (caller, caller.db.target))

        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s claws, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
        "goto": "skip_attack"})
    return text, options

def bite(caller):
    caller.db.weapon = 0
    caller.db.attack_not = 0
    test = caller.db.dexterity + caller.db.brawl +caller.db.blessed
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 6):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints
    hit = caller.db.strength
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou bite %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to bite you with %i succesful rolls." % (caller, attackpoints))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s bites %s." % (caller, caller.db.target))

        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s claws, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s claws %s." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
        "goto": "skip_attack"})
    return text, options



def kick(caller):
    caller.db.attack_not = 0
    caller.db.weapon = 0
    test = caller.db.dexterity + caller.db.brawl + caller.db.blessed
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 7):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints

    hit = caller.db.strength + 1
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou kick %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to kick you with %i succesful rolls." % (caller, attackpoints))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s kicks %s." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s kicks, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s kicks %s." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
        "goto": "skip_attack"})
    return text, options

def axe(caller):
    caller.db.attack_not = 0
    caller.db.weapon = 1
    axe = caller.search("axe", candidates=caller.contents)
    if axe.db.enchant:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed + axe.db.enchant
    else:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed 

    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 7):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints

    hit = caller.db.strength+3
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou strike %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to strike you with %i succesful rolls." % (caller, attackpoints))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s hits %s with his axe." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s strikes, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s. with his axe" % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
                "goto": "skip_attack"})
    return text, options

def knife(caller):
    caller.db.attack_not = 0
    caller.db.weapon = 1

    knife = caller.search("knife", candidates=caller.contents)
    if knife.db.enchant:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed + knife.db.enchant
    else:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed      

    caller.msg(knife.db.enchant)
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 4):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints

    hit = caller.db.strength+1
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 +  1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou strike %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to strike you with %i succesful rolls." % (caller, attackpoints))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s cuts %s with his knife." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s strikes, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s with his knife." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
                "goto": "skip_attack"})
    return text, options

def bat(caller):
    caller.db.attack_not = 0
    caller.db.weapon = 0

    bat = caller.search("bat", candidates=caller.contents)
    if bat.db.enchant:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed + bat.db.enchant
    else:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed 

    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 5):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints

    hit = caller.db.strength+2
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou strike %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to strike you with %i succesful rolls." % (caller, attackpoints))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s hits %s with his baseball bat." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s strikes, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s with his baseball bat." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
                "goto": "skip_attack"})
    return text, options

def staff(caller):
    caller.db.attack_not = 0
    caller.db.weapon = 0

    staff = caller.search("staff", candidates=caller.contents)
    if staff.db.enchant:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed + staff.db.enchant
    else:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed 
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 6):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints

    hit = caller.db.strength+1
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou strike %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to strike you with %i succesful rolls." % (caller, attackpoints))
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s hits %s with his staff." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s strikes, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s with his staff." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
                "goto": "skip_attack"})
    return text, options

def katana(caller):
    caller.db.attack_not = 0
    caller.db.weapon = 1

    sword = caller.search("sword", candidates=caller.contents)
    if sword.db.enchant:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed + sword.db.enchant
    else:
        test = caller.db.dexterity + caller.db.melee + caller.db.blessed 
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 6):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage
    damage = attackpoints

    hit = caller.db.strength+3
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1

    global damage2
    damage2 = attackpoints2 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou strike %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to strike you with %i succesful rolls." % (caller, attackpoints))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s attacks %s with his katana." % (caller, caller.db.target))
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s strikes, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s with his katana." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
                "goto": "skip_attack"})
    return text, options

def single(caller):
    caller.db.attack_not = 0
    caller.db.weapon = 2

    pistol = caller.search("pistol", candidates=caller.contents)
    if pistol.db.enchant:
        test = caller.db.dexterity + caller.db.firearms + caller.db.blessed + pistol.db.enchant
    else:
        test = caller.db.dexterity + caller.db.firearms+ caller.db.blessed 
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 6):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage    
    damage = attackpoints

    hit = caller.db.strength+3
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1
            
    global damage2
    damage2 = 4 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou shoot %s with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to shoot you with %i succesful rolls." % (caller, attackpoints))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s shoots %s with his pistol." % (caller, caller.db.target))
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s shoots, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s with his pistol." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
                "goto": "skip_attack"})
    return text, options

def double(caller):	
    caller.db.attack_not = 0
    caller.db.weapon = 3

    pistol = caller.search("pistol", candidates=caller.contents)
    if pistol.db.enchant:
        test = caller.db.dexterity + caller.db.firearms + caller.db.blessed + pistol.db.enchant
    else:
        test = caller.db.dexterity + caller.db.firearms+ caller.db.blessed 
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 6):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage    
    damage = attackpoints

    hit = caller.db.strength+3
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1
            
    global damage2
    damage2 = 4 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou shoot %s twice with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to shoot you twice with %i succesful rolls." % (caller, attackpoints))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s shoots %s twice with his pistol." % (caller, caller.db.target))
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s shoots, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s with his pistol." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
                "goto": "skip_attack"})
    return text, options

def three(caller):	
    caller.db.attack_not = 0
    caller.db.weapon = 4

    pistol = caller.search("pistol", candidates=caller.contents)
    if pistol.db.enchant:
        test = caller.db.dexterity + caller.db.firearms + caller.db.blessed + pistol.db.enchant
    else:
        test = caller.db.dexterity + caller.db.firearms+ caller.db.blessed 
    counter = 0
    attackpoints = 0
    while(counter < test):
        counter = counter + 1
        roll = roll_dice(1,10)
        if(roll >= 6):
            attackpoints = attackpoints + 1
    if caller.db.autopoint:
        attackpoints +=1
        caller.db.autopoint = 0
    global damage    
    damage = attackpoints

    hit = caller.db.strength+3
    counter = 0
    attackpoints2 = 0
    while (counter < hit):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            attackpoints2 = attackpoints2 + 1
            
    global damage2
    damage2 = 4 + caller.db.blessed + caller.db.target.db.cursed
    caller.db.target.db.cursed = 0
    caller.db.start_time = timer()
    if (attackpoints > 0):
        caller.msg("|/|gYou shoot %s three times with %i success rolls. " % (caller.db.target, attackpoints))
        caller.db.target.msg("|/|g%s attempts to shoot you three times with %i succesful rolls." % (caller, attackpoints))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="defend_node", auto_quit=False, cmd_on_exit=None)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s shoots %s three times with his pistol." % (caller, caller.db.target))
    else:
        caller.msg("|/|gYou miss %s." % caller.db.target)
        caller.db.target.msg("|/|g%s shoots, but misses you." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s misses %s with his pistol." % (caller, caller.db.target))
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = ({"key": "skip",
                "goto": "skip_attack"})
    return text, options

def auto(caller):
    caller.db.start_time = timer()
    text = ""
    options = ({"key": "|ysingle",
            "desc": "Shoot once.",
            "goto": "wait",
            "exec": "single"},
            {"key": "|ytwice",
            "desc": "shoot twice",
            "goto": "wait",
            "exec": "double"},
            {"key": "|ythree",
            "desc": "shoot three times",
            "goto": "wait",
            "exec": "three"},)

    return text, options
    
def wait(caller):
    caller.db.start_time = timer()
    text = ""
    options = {"key": "_default",
               "goto": "wait"}
    return text, options

def finish(caller):
    caller.db.start_time = 99999999999999999999
    EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    text = ""
    options = {"key": "_default",
        "goto": "wait"}
    return text, options

def skip_attack(caller):
    
    caller.db.start_time = timer()
    text = " "
    if caller.db.intimidated:
        text = "|r You are too afraid to fight!"
        caller.db.target.msg("|/|r %s is too afraid to fight." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s cowers in fear." % caller.name)
    if(caller.db.move_speed == "freeze"):
        caller.msg("Time is moving too slow to react") 
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s is frozen still." % caller.name)
    if(caller.db.conscious == 0 and caller.db.alive ==1):
        text = "|r You are unconscious!"
        caller.db.target.msg("|/|r %s is unconscious."% caller)
        caller.location.log_action("%s is unconscious" % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
    if(caller.db.conscious == 1 or caller.db.alive == 0):
        if(caller.db.intimidated == 0):
            text = "|r You have skipped your turn!"

    EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node",auto_quit=False, cmd_on_exit=None)

    if(caller.db.alive == 0):
        caller.locks.add("view:attr(alive, 0)")
        caller.db.conscious = 1
        caller.msg("|/|rYou are dead!")
        caller.db.target.msg("|/|r%s is dead!"% caller)
        caller.location.log_action("%s is dead." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s is dead!." % caller.name)
                caller.location.log_action("%s is dead." % caller.name)
        caller.ndb._menutree.close_menu()
        caller.db.target.ndb._menutree.close_menu()
        corpse1 = create_object(key="Corpse", location = caller.location)
        print(caller.location)
        corpse1.attributes.add("target", caller.db.target)
        corpse1.attributes.add("lastname", caller)
        corpse1.db.description = "A bloody mess of flesh and broken bones."
        text = ""
        options = ()


    options = {"key": "_default",
               "goto": "wait"}
    return text, options

def skip_defend(caller):
    caller.db.start_time = timer()
    caller.msg("|/|rYou have been hit by %s.|/" % caller.db.target)
    accounts = [con for con in caller.location.contents if con.has_account]
    for account in accounts:
        if not account.ndb.end_combat:
            account.msg("%s has been hit by %s." % (caller.name, caller.db.target))
    if(caller.db.conscious == 0):
        caller.db.target.msg("|/|r%s is unconscious.|/" % caller)
        caller.location.log_action("%s is unconscious" % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
    if(caller.db.conscious == 1):
        caller.db.target.msg("|/|r%s has skipped his turn.|/" % caller)

    if(caller.db.conscious == 0 and caller.db.alive == 1):
        text = "|/|rYou are unconscious!"
    if(caller.db.conscious == 1 or caller.db.alive == 0):
        text = "|/|r You have skipped your turn!"
    EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node",auto_quit=False, cmd_on_exit=None)

    if(caller.db.alive == 0):
        caller.locks.add("view:attr(alive, 0)")
        caller.db.conscious = 1
        caller.msg("|rYou are dead!")
        caller.db.target.msg("|/|r%s is dead!"% caller)
        caller.location.log_action("%s is dead." % caller)
        caller.ndb._menutree.close_menu()
        caller.db.target.ndb._menutree.close_menu()
        corpse2 = create_object(key="Corpse", location = caller.location)
        corpse2.attributes.add("target", caller.db.target)
        corpse2.attributes.add("lastname", caller)
        corpse2.db.description = "A bloody mess of flesh and broken bones."
        print(caller.location)
        text = ""
        options = ()


    options = {"key": "_default",
               "goto": "wait"}
    return text, options

def defend_node(caller):
    if caller.ndb.ritual:
        caller.msg("You are forced to stop your ritual.")
        caller.ndb.ritual = 0
    healthbar = "|/|X|[wHealth:"
    total = caller.db.lethal + caller.db.bashing

    diff = 8 - caller.db.lethal

    if caller.db.bashing > diff:
        caller.db.lethal += caller.db.bashing - diff
        caller.db.bashing -= caller.db.bashing - diff
    for i in range(0,8):
        if i < caller.db.lethal:
            healthbar += " X"
        elif i < total:
            healthbar += " /"
        else:
            healthbar += " 0"
    healthbar += "|/"
    caller.msg(prompt=healthbar)
    if(total>=8):
        caller.db.conscious = 0
    if(caller.db.lethal>=8):
        caller.db.alive = 0
        caller.locks.add("view:attr(alive, 0)")
    if(total<8):
        caller.db.conscious = 1
    caller.db.start_time = timer()
    defend_script = create_script("typeclasses.defendwait.DefendTime", obj=caller)
    defend_script.attacker(caller.db.target)
    defend_script.target(caller)

    text = ""
    options = ({"key": "|ydodge",
        "desc": "Avoid the attack.",
        "goto": "wait",
        "exec": "dodge"},
        {"key": "|yblock",
        "desc": "Block the attack.",
        "goto": "wait",
        "exec": "block"},)

    if caller.db.attack_not:
        caller.db.mercy = 1
        options += ({"key": "|ymercy",
                  "desc": "Beg for mercy",
                  "goto": "wait",
                  "exec": "mercy"},)
    
    options += ({"key": "|yflee",
              "desc": "Run away.",
              "goto": "wait",
              "exec": "flee_attack"},)


    if(caller.db.alive == 0):
        caller.locks.add("view:attr(alive, 0)")
        caller.ndb.end_combat = 0
        caller.db.target.ndb.end_combat = 0
        caller.db.conscious = 1
        caller.msg("|rYou are dead!")
        caller.db.target.msg("|/|r%s is dead!"% caller)
        caller.location.log_action("%s is dead." % caller)
        caller.ndb._menutree.close_menu()
        caller.db.target.ndb._menutree.close_menu()
        corpse3 = create_object(key="Corpse", location = caller.location)
        corpse3.db.description = "A bloody mess of flesh and broken bones."
        corpse3.attributes.add("target", caller.db.target)
        corpse3.attributes.add("lastname", caller)
        print(caller.location)
        text = ""
        options = ()

    if(caller.db.conscious == 0 and caller.db.alive == 1):
        options = ({"key": "_default",
        "goto": "new_skip"})

    if(caller.db.move_speed == "freeze" and caller.db.alive == 1):
        options = ({"key": "_default",
        "goto": "new_skip"})
        
    return text, options

def dodge(caller):
    caller.ndb.action = 1
    test = caller.db.dexterity + caller.db.athletics + caller.db.blessed
    soak = caller.db.stamina + caller.db.blessed
    counter = 0
    defendpoints = 0
    while (counter < test):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            defendpoints = defendpoints + 1
    if caller.db.autopoint:
        defendpoints +=1
        caller.db.autopoint = 0
    counter = 0
    soakpoints = 0
    while (counter < soak):
        counter = counter + 1
        roll = roll_dice(1,10)
        if (roll >= 6):
            soakpoints = soakpoints + 1
    dmg = damage
    caller.db.start_time = timer()
    if (defendpoints > 0):
        tst = damage2
        dmg2 = damage
        cnt2 = 0
        while (cnt2 < tst):
            cnt2 = cnt2 + 1
            roll = roll_dice(1, 10)
            if (roll >= 6):
                dmg = dmg + 1
        cnt2 = 0
        bonusdmg = 0
        while(cnt2 < dmg2 - defendpoints - 1):
            cnt2 += 1
            roll = roll_dice(1,10)
            if (roll >= 6):
                bonusdmg = bonusdmg + 1

        reduced =  dmg - defendpoints
        if(reduced < 0):
            reduced = 0
        if(defendpoints >= dmg2):
            defendpoints = dmg2
            reduced = 0
        reduced = reduced + bonusdmg
        if(caller.db.target.db.weapon == 0):
            caller.msg("|/|gYou dodge %i out of %i of %s's attack points." % (defendpoints, dmg2, caller.db.target))
            if(caller.db.target.db.form == "cat"):
                if reduced > 3:
                    reduced = 3
            if(caller.db.target.db.form == "dog"):
                if reduced > 3:
                   reduced = 3
            caller.msg("|/|g%s causes %i points of damage to you." % (caller.db.target, reduced + bonusdmg))
            if (soakpoints > reduced):
                soakpoints = reduced
            if (soakpoints > 0):
                caller.msg("|/|gYou soak %i out of %i points of bashing damage." % (soakpoints, reduced + bonusdmg))
            if (reduced - soakpoints > 0):
                caller.msg("|/|gYou lose a total of %i health points." % (reduced+bonusdmg - soakpoints))
                caller.db.bashing = caller.db.bashing + (reduced - soakpoints)
            caller.db.target.msg("|/|g%s dodges %i points of your attack." % (caller, defendpoints))
            caller.db.target.msg("|/|gYou deal %i points of damage with your attack." % (reduced+bonusdmg))
    
            if(soakpoints>0):
                caller.db.target.msg("|/|g%s soaks %i points of damage from your attack." % (caller, soakpoints))
            if(reduced-soakpoints > 0):
                caller.db.target.msg("|/|g%s loses a total of %i hit points." % (caller, reduced+bonusdmg - soakpoints))

        if(caller.db.target.db.weapon == 1):
            caller.msg("|/|gYou dodge %i out of %i of %s's attack points." % (defendpoints, dmg2, caller.db.target))
            caller.msg("|/|g%s causes %i points of lethal damage to you." % (caller.db.target, reduced+bonusdmg))
            caller.db.lethal = caller.db.lethal + reduced
            caller.db.target.msg("|/|g%s dodges %i points of your attack." % (caller, defendpoints))
            caller.db.target.msg("|/|gYou deal %i points of lethal damage." % (reduced+bonusdmg))
            
        if(caller.db.target.db.weapon == 2):
        
            caller.msg("|/|gYou dodge %i out of %i of %s's attack points." % (defendpoints, dmg2, caller.db.target))
            caller.msg("|/|g%s causes %i points of lethal damage to you." % (caller.db.target, 4 + bonusdmg))
            caller.db.lethal = caller.db.lethal + 4 + bonusdmg
            caller.db.target.msg("|/|g%s dodges %i points of your attack." % (caller, defendpoints))
            caller.db.target.msg("|/|gYou deal %i points of lethal damage." % (4+bonusdmg))
            
        if(caller.db.target.db.weapon == 3):
            caller.msg("|/|gYou dodge %i out of i% of %s's attack." % (defendpoints, dmg2, caller.db.target))
            caller.msg("|/|g%s causes %i points of lethal damage to you." % (caller.db.target, 8 + bonusdmg))
            caller.db.lethal = caller.db.lethal + 8 + bonusdmg
            caller.db.target.msg("|/|g%s dodges %i points of your attack." % (caller, defendpoints))
            caller.db.target.msg("|/|gYou deal %i points of lethal damage." % (8+bonusdmg))
            
        if(caller.db.target.db.weapon == 4):
            caller.msg("|/|gYou dodge %i out of %i of %s's attack." % (defendpoints, dmg2, caller.db.target))
            caller.msg("|/|g%s causes %i points of lethal damage to you." % (caller.db.target, 12+bonusdmg))
            caller.db.lethal = caller.db.lethal + 12 + bonusdmg
            caller.db.target.msg("|/|g%s dodges %i points of your attack." % (caller, defendpoints))
            caller.db.target.msg("|/|gYou deal %i points of lethal damage." % (8 + bonusdmg))
            
    else:
        caller.msg("|/|rYou have been hit by %s." % caller.db.target)
        caller.db.target.msg("|/|r%s fails to dodge your attack." % caller)

        if(caller.db.target.db.weapon == 0):
            if(caller.db.target.db.form == "cat"):
                if dmg > 3:
                    dmg = 3
            caller.msg("|/|g%s causes %i points of damage to you." % (caller.db.target, dmg))
            caller.msg("|/|gYou soak %i out of %i points of bashing damage." % (soakpoints, dmg))
            caller.msg("|/|gYou lose a total of %i health points." % (dmg - soakpoints))
            caller.db.bashing = caller.db.bashing + (dmg - soakpoints)
            caller.db.target.msg("|/|gYou deal %i points of damage with your attack." % (dmg))
            caller.db.target.msg("|/|g%s soaks %i points of damage from your attack." % (caller, soakpoints))
            caller.db.target.msg("|/|g%s loses a total of %i hit points." % (caller, dmg - soakpoints))

        if(caller.db.target.db.weapon == 1):
            caller.msg("|/|g%s causes %i points of lethal damage to you." % (caller.db.target, dmg))
            caller.db.lethal = caller.db.lethal + dmg 
            caller.db.target.msg("|/|gYou deal %i points of lethal damage to %s." % (dmg, caller))
            caller.db.target.msg("|/|g%s loses a total of %i hit points." % (caller, dmg))

    if(caller.db.target.db.slowtime == 1):
        caller.msg("%s is moving too fast for you to react!" % caller.db.target)
        caller.db.target.msg("You move too fast for %s to react!" % caller)
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    else:
        EvMenu(caller, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)

    text = ""
    options = ({"key": "skip",
        "goto": "skip_attack"})
    
    if(caller.db.alive == 0 or caller.db.target.db.alive == 0):
        caller.ndb.end_combat = 0
        caller.db.target.ndb.end_combat = 0
        caller.db.conscious = 1
        caller.db.target.db.conscious = 1
        caller.msg("|rYou are dead!")
        caller.location.log_action("%s is dead." % caller.name)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account == caller:
                account.msg("|r%s is dead!" % caller.name)
        caller.locks.add("view:attr(alive, 0)")
        caller.db.target.ndb._menutree.close_menu()
        caller.ndb._menutree.close_menu()
        corpse5 = create_object(key="Corpse", location = caller.location)
        corpse5.attributes.add("target", caller.db.target)
        corpse5.attributes.add("lastname", caller)
        corpse5.db.description = "A bloody mess of flesh and broken bones."
        print(caller.location)
    text = ""
    options = ()

    return text, options


def block(caller):
    test = caller.db.dexterity + caller.db.brawl + caller.db.blessed
    soak = caller.db.stamina + caller.db.blessed
    counter = 0
    defendpoints = 0
    while (counter < test):
        counter = counter + 1
        roll = roll_dice(1, 10)
        if (roll >= 6):
            defendpoints = defendpoints + 1
    if caller.db.autopoint:
        defendpoints +=1
        caller.db.autopoint = 0
    counter = 0
    soakpoints = 0
    while (counter < soak):
        counter = counter + 1
        roll = roll_dice(1,10)
        if (roll >= 6):
            soakpoints = soakpoints + 1
    dmg = damage
    caller.db.start_time = timer()
    if (defendpoints > 0):
        tst = damage2
        dmg2 = damage
        cnt2 = 0
        while (cnt2 < tst):
            cnt2 = cnt2 + 1
            roll = roll_dice(1, 10)
            if (roll >= 6):
                dmg = dmg + 1

        reduced =  dmg - defendpoints
        if(reduced < 0):
            reduced = 0
        if(defendpoints >= dmg2):
            defendpoints = dmg2
            reduced = 0

        if(caller.db.target.db.weapon == 0):
            if(caller.db.target.db.form == "cat"):
                if reduced > 3:
                    reduced = 3
            if(caller.db.target.db.form == "dog"):
                if reduced > 3:
                   reduced = 3
            caller.msg("|/|gYou block %i out of %i of %s's attack points." % (defendpoints, dmg2, caller.db.target))
            caller.msg("|/|g%s causes %i points of damage to you." % (caller.db.target, reduced))
            if (soakpoints > reduced):
                soakpoints = reduced
            if (soakpoints > 0):
                caller.msg("|/|gYou soak %i out of %i points of bashing damage." % (soakpoints, reduced))
            if (reduced - soakpoints > 0):
                caller.msg("|/|gYou lose a total of %i health points." % (reduced - soakpoints))
                caller.db.bashing = caller.db.bashing + (reduced - soakpoints)
            caller.db.target.msg("|/|g%s blocks %i points of your attack." % (caller, defendpoints))
            caller.db.target.msg("|/|gYou deal %i points of damage with your attack." % (reduced))
    
            if(soakpoints>0):
                caller.db.target.msg("|/|g%s soaks %i points of damage from your attack." % (caller, soakpoints))
            if(reduced-soakpoints > 0):
                caller.db.target.msg("|/|g%s loses a total of %i hit points." % (caller, reduced - soakpoints))

        if(caller.db.target.db.weapon == 1):
            caller.msg("|/|gYou can't block %s's attack points." % (caller.db.target))
            caller.msg("|/|g%s causes %i points of lethal damage to you." % (caller.db.target, dmg))
            caller.db.lethal = caller.db.lethal + dmg
            caller.db.target.msg("|/|g%s fails to block your attack." % (caller))
            caller.db.target.msg("|/|gYou deal %i points of lethal damage." % (dmg))
            
        if(caller.db.target.db.weapon == 2):
            caller.msg("|/|gYou can't block %s's bullet." % (caller.db.target))
            caller.msg("|/|g%s causes 4 points of lethal damage to you." % caller.db.target)
            caller.db.lethal = caller.db.lethal + 4
            caller.db.target.msg("|/|g%s fails to block your attack." % caller)
            caller.db.target.msg("|/|gYou deal 4 points of lethal damage." % dmg)

        if(caller.db.target.db.weapon == 3):
            caller.msg("|/|gYou can't block %s's bullets." % (caller.db.target))
            caller.msg("|/|g%s causes 8 points of lethal damage to you." % caller.db.target)
            caller.db.lethal = caller.db.lethal + 8
            caller.db.target.msg("|/|g%s fails to block your attack." % caller)
            caller.db.target.msg("|/|gYou deal 8 points of lethal damage." % dmg) 
            
        if(caller.db.target.db.weapon == 4):
            caller.msg("|/|gYou can't block %s's bullets." % (caller.db.target))
            caller.msg("|/|g%s causes 12 points of lethal damage to you." % caller.db.target)
            caller.db.lethal = caller.db.lethal + 12
            caller.db.target.msg("|/|g%s fails to block your attack." % caller)
            caller.db.target.msg("|/|gYou deal 12 points of lethal damage." % dmg)
            
    else:
        caller.msg("|/|rYou have been hit by %s." % caller.db.target)
        caller.db.target.msg("|/|r%s fails to block your attack." % caller)

        if(caller.db.target.db.weapon == 0):
            if(caller.db.target.db.form == "cat"):
                if dmg > 3:
                    dmg = 3
            if(caller.db.target.db.form == "dog"):
                if reduced > 3:
                   reduced = 3
            caller.msg("|/|g%s causes %i points of damage to you." % (caller.db.target, dmg))
            caller.msg("|/|gYou soak %i out of %i points of bashing damage." % (soakpoints, dmg))
            caller.msg("|/|gYou lose a total of %i health points." % (dmg - soakpoints))
            caller.db.bashing = caller.db.bashing + (dmg - soakpoints)
            caller.db.target.msg("|/|gYou deal %i points of damage with your attack." % (dmg))
            caller.db.target.msg("|/|g%s soaks %i points of damage from your attack." % (caller, soakpoints))
            caller.db.target.msg("|/|g%s loses a total of %i hit points." % (caller, dmg - soakpoints))

        if(caller.db.target.db.weapon == 1):
            caller.msg("|/|g%s causes %i points of lethal damage to you." % (caller.db.target, dmg))
            caller.msg("|/|gYou lose a total of %i health points." % (dmg))
            caller.db.lethal = caller.db.lethal + dmg
            caller.db.target.msg("|/|gYou deal %i points of lethal damage with your attack." % (dmg))
            caller.db.target.msg("|/|g%s loses a total of %i hit points." % (caller, dmg))
    if(caller.db.target.db.slowtime == 1):
        caller.msg("%s is moving too fast for you to react!" % caller.db.target)
        caller.db.target.msg("You move too fast for %s to react!" % caller)
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
    else:
        EvMenu(caller, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)

    text = ""
    options = ({"key": "skip",
        "goto": "skip_attack"})
    

    if(caller.db.alive == 0 or caller.db.target.db.alive == 0):
            caller.ndb.end_combat = 0
            caller.db.target.ndb.end_combat = 0
            caller.db.conscious = 1
            caller.db.target.db.conscious = 1
            caller.msg("|rYou are dead!")
            caller.locks.add("view:attr(alive, 0)")
            accounts = [con for con in caller.location.contents if con.has_account]
            for account in accounts:
                 if not account == caller:
                    account.msg("|r%s is dead!" % caller.name)
            caller.location.log_action("%s is dead." % caller.name)
            caller.db.target.ndb._menutree.close_menu()
            caller.ndb._menutree.close_menu()
            corpse5 = create_object(key="Corpse", location = caller.location)
            corpse5.attributes.add("target", caller.db.target)
            corpse5.attributes.add("lastname", caller)
            corpse5.db.description = "A bloody mess of flesh and broken bones."
            print(caller.location)
            text = ""
            options = ()


    return text, options

def mercy_attack(caller):
   caller.db.start_time = timer()
   if caller.db.attack_not:
       init_a = caller.db.dexterity + caller.db.wits + caller.db.blessed + caller.db.charisma
       caller.db.target.msg("|/|y%s doesn't want to fight." % caller)
   else:
       init_a = caller.db.dexterity + caller.db.wits + caller.db.blessed
   init_b = caller.db.target.db.dexterity + caller.db.target.db.wits
   init_a = init_a + roll_dice(1,10) 
   init_b = init_b + roll_dice(1,10)
   if(init_a > init_b):
       caller.msg("|/|yYou beg %s for mercy|/|/" % caller.db.target)
       caller.db.target.msg("|/|y%s begs for mercy!|/|/" % caller)
       if(caller.ndb._menutree):
           caller.ndb._menutree.close_menu()
       if(caller.db.target.ndb._menutree):
           caller.db.target.ndb._menutree.close_menu()
       caller.ndb.end_combat = 0
       caller.db.target.ndb.end_combat = 0
   else:
       caller.msg("|/|yYou're cries for mercy go unheard.")
       caller.db.target.msg("|/|yYou ignore %s's cries for mercy " % caller)
       EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
       text = ""
       options = ({"key": "skip",
               "goto": "skip_attack"})
       return text, options

   text = ""
   options = ()
   return text, options

def mercy(caller):
    caller.db.start_time = timer()
    init_a = caller.db.dexterity + caller.db.wits + caller.db.blessed + caller.db.charisma
    caller.db.target.msg("|/|y%s doesn't want to fight." % caller)
    init_b = caller.db.target.db.dexterity + caller.db.target.db.wits
    init_a = init_a + roll_dice(1,10) 
    init_b = init_b + roll_dice(1,10)
    if(init_a > init_b):
        caller.msg("|/|yYou beg %s for mercy!|/|/" % caller.db.target)
        caller.db.target.msg("|/|y%s cries for mercy!|/|/" % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        caller.db.target.ndb._menutree.close_menu()
        caller.ndb._menutree.close_menu()
        caller.ndb.end_combat = 0
        caller.db.target.ndb.end_combat = 0
    else:
        caller.msg("|yYour cries for mercy go unheard.")
        caller.db.target.msg("|y%s's cries for mercy go unheard" % caller)
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)

    text = ""
    options = ()
    return text, options


def flee_attack(caller):
    caller.db.start_time = timer()
    if caller.db.attack_not:
        init_a = caller.db.dexterity + caller.db.wits + caller.db.blessed + caller.db.charisma+4
        caller.db.target.msg("|/|y%s doesn't want to fight." % caller)
    else:
        init_a = caller.db.dexterity + caller.db.wits + caller.db.blessed+4
    init_b = caller.db.target.db.dexterity + caller.db.target.db.wits
    init_a = init_a + roll_dice(1,10) 
    init_b = init_b + roll_dice(1,10)
    if caller.db.autopoint:
        init_a += roll_dice(1,10)
        caller.db.autopoint = 0
    if caller.db.target.db.conscious == 0:
        caller.msg("|/|yYou leave from combat!|/|/")
        caller.db.target.msg("|/|y%s leaves from combat!|/|/" % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s leaves from combat." % caller.name)
        caller.ndb._menutree.close_menu()
        if(caller.db.target.ndb._menutree):
            caller.db.target.ndb._menutree.close_menu()
        caller.ndb.end_combat = 0
        caller.db.target.ndb.end_combat = 0
        caller.execute_cmd('look')

    elif(init_a > init_b):
        caller.msg("|/|yYou flee from combat!|/|/")
        caller.db.target.msg("|/|y%s flees from combat!|/|/" % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s flees from combat." % caller.name)
        caller.ndb._menutree.close_menu()
        if(caller.db.target.ndb._menutree):
            caller.db.target.ndb._menutree.close_menu()
        caller.ndb.end_combat = 0
        caller.db.target.ndb.end_combat = 0
        caller.execute_cmd('look')
        caller.db.target.execute_cmd('look')
    else:
        caller.msg("|/|yYou couldn't flee")
        caller.db.target.msg("|/|y%s couldn't flee" % caller)
        EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
        text = ""
        options = ({"key": "skip",
                "goto": "skip_attack"})
        return text, options

    text = ""
    options = ()
    return text, options

def flee(caller):
    caller.db.start_time = timer()
    if caller.db.attack_not:
        init_a = caller.db.dexterity + caller.db.wits + caller.db.blessed + caller.db.charisma
        caller.db.target.msg("|/|y%s doesn't want to fight." % caller)
    else:
        init_a = caller.db.dexterity + caller.db.wits + caller.db.blessed
        init_b = caller.db.target.db.dexterity + caller.db.target.db.wits
        init_a = init_a + roll_dice(1,10) 
        init_b = init_b + roll_dice(1,10)
    if caller.db.autopoint:
        init_a +=1
        caller.db.autopoint = 0
    if(init_a > init_b or caller.db.target.db.conscious == 0 or caller.db.target.db.alive == 0):
        caller.msg("|/|yYou flee from combat!|/|/")
        caller.db.target.msg("|/|y%s flees from combat!|/|/" % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s flees from combat." % caller.name)
        caller.db.target.ndb._menutree.close_menu()
        caller.ndb._menutree.close_menu()
        caller.ndb.end_combat = 0
        caller.db.target.ndb.end_combat = 0
    else:
        caller.msg("|yYou fail to flee from combat")
        caller.db.target.msg("|y%s fails to flee from combat" % caller)
        if(caller.db.target.db.weapon == 1):
            caller.msg("|/|g%s causes %i points of lethal damage to you." % (caller.db.target, damage))
            caller.msg("|/|gYou lose a total of %i health points." % (damage))
            caller.db.lethal = caller.db.lethal + damage
            caller.db.target.msg("|/|gYou deal %i points of lethal damage with your attack." % (damage))
            caller.db.target.msg("|/|g%s loses a total of %i hit points." % (caller, damage))
        if(caller.db.target.db.weapon == 0):
            if(caller.db.target.db.form == "cat"):
                if damage > 3:
                    damage = 3
            if(caller.db.target.db.form == "dog"):
                if damage > 3:
                   damage = 3
            caller.msg("|/|g%s causes %i points of bashing damage to you." % (caller.db.target, damage))
            caller.msg("|/|gYou lose a total of %i health points." % (damage))
            caller.db.bashing = caller.db.bashing + damage
            caller.db.target.msg("|/|gYou deal %i points of bashing damage with your attack." % (damage))
            caller.db.target.msg("|/|g%s loses a total of %i hit points." % (caller, damage))
        EvMenu(caller, "typeclasses.menu", startnode="attack_node", auto_quit=False, cmd_on_exit=None)
        text = ""
        options = ({"key": "skip",
                "goto": "skip_attack"})
        
        if(caller.db.alive == 0 or caller.db.target.db.alive == 0):
                caller.ndb.end_combat = 0
                caller.db.target.ndb.end_combat = 0
                caller.db.conscious = 1
                caller.db.target.db.conscious = 1
                caller.msg("|rYou are dead!")
                caller.locks.add("view:attr(alive, 0)")

                accounts = [con for con in caller.location.contents if con.has_account]


                for account in accounts:
                     if not account == caller:
                        account.msg("|r%s is dead!" % caller.name)

                caller.location.log_action("%s is dead." % caller.name)
                caller.db.target.ndb._menutree.close_menu()
                caller.ndb._menutree.close_menu()
                corpse5 = create_object(key="Corpse", location = caller.location)
                corpse5.attributes.add("target", caller.db.target)
                corpse5.attributes.add("lastname", caller)
                corpse5.db.description = "A bloody mess of flesh and broken bones."
                print(caller.location)
                text = ""
                options = ()

        return text, options

def new_skip(caller):
    if(caller.db.move_speed == "freeze"): 
            caller.msg("Time is moving too slow to react") 
    caller.msg("|/|rYou have been hit by %s." % caller.db.target)
    caller.db.target.msg("|/|r%s fails to dodge your attack." % caller)

    if(caller.db.target.db.weapon == 0):
        if(caller.db.target.db.form == "cat"):
            if damage > 3:
                damage = 3
        caller.msg("|/|g%s causes %i points of damage to you." % (caller.db.target, damage))
        caller.msg("|/|gYou lose a total of %i health points." % damage)
        caller.db.bashing = caller.db.bashing + damage
        caller.db.target.msg("|/|gYou deal %i points of damage with your punch." % damage)
        caller.db.target.msg("|/|g%s loses a total of %i hit points." % (caller, damage))

    if(caller.db.conscious == 0 and caller.db.alive == 1):
        text = "|r You are unconscious."
        caller.db.target.msg("|/|r%s is unconscious. "% caller)
        caller.location.log_action("%s is unconscious." % caller)
        accounts = [con for con in caller.location.contents if con.has_account]
    if(caller.db.conscious == 1 or caller.db.alive == 0):
        text = "|r You have skipped your turn!"
    EvMenu(caller.db.target, "typeclasses.menu", startnode="attack_node",auto_quit=False, cmd_on_exit=None)

    if(caller.db.alive == 0):
        caller.db.conscious = 1
        caller.msg("|rYou are dead!")
        caller.locks.add("view:attr(alive, 0)")
        caller.db.target.msg("|/|r%s is dead!"% caller)
        accounts = [con for con in caller.location.contents if con.has_account]
        for account in accounts:
            if not account.ndb.end_combat:
                account.msg("%s is dead!." % caller.name)
        caller.location.log_action("%s is dead" % caller.name)
        caller.ndb._menutree.close_menu()
        caller.db.target.ndb._menutree.close_menu()
        corpse4 = create_object(key="Corpse", location = caller.location)
        corpse4.db.description = "A bloody mess of flesh and broken bones."
        corpse4.attributes.add("target", caller.db.target)
        corpse4.attributes.add("lastname", caller)
        print(caller.location)
        text = ""
        options = ()


    options = {"key": "_default",
        "goto": "wait"}
    return text, options


def END(caller):
    caller.msg("EXIT COMBAT")
    caller.db.target.msg("EXIT COMBAT")
    caller.ndb._menutree.close_menu()
    caller.db.target.ndb._menutree.close_menu()

    text = ""
    options = ()
    return text, options
