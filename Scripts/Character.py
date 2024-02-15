from random import random, choice


class Entity:
    def __init__(self, name, hp, _str, _def, mag):
        self.name = name

        self.maxhp = hp
        self.hurt = 0  # how much damage the entity has taken (maxhp - hurt = current hp)
        self.strength = _str
        self.magic = mag
        self.defence = _def

        self.status = []  # list of str that represent the status inflicted on target (like defdown, burn, shield, etc.)

        # three lists containing lambda functions that take user, target as arguments
        # represent the actions the entity can take during a turn
        self.attack = [lambda user, target: target.damage(user.strength)]
        self.heal = [lambda user, target: user.recover(user.magic)]
        self.defend = [lambda user, target: user.add(("shield", (user.defence // 10) + 1))]

    def get_hp(self):
        """return entity's current hp"""
        return self.maxhp - self.hurt

    def alive(self):
        """return True if entity is alive, False if they're dead"""
        return self.get_hp() > 0

    def damage(self, damage):
        """takes in an int damage and adds it to the entity's hurt (they lose hp)
        damage is lowered by target's defence and the 'shield' status block a hit"""
        if self.check("shield"):  # we check for shield
            self.remove("shield")
            print(self.name + " had a shield.")
            return False
        if damage - self.defence <= 0:  # we check for negative damage (bad)
            print(self.name + " received " + str(0) + " damage")
            return False
        self.hurt += damage - self.defence
        print(self.name + " received " + str(damage - self.defence) + " damage")
        return True

    def recover(self, strength):
        """takes in an int strength and lowers the entity's hurt by that amount (they heal hp)"""
        self.hurt -= strength
        if self.hurt < 0:
            self.hurt = 0
        print(self.name + " recovered " + str(strength) + " health")

    def add(self, *args):
        """takes in a list of str that represent the status to add to entity's status
        instead of str, can also have tuple like : (str, int)
        where str is the status to add and int is the number of status to add"""
        for s in args:
            if type(s) == str:
                self.status.append(s)
            elif type(s) == tuple:
                try:
                    for _ in range(s[1]):
                        self.status.append(s[0])
                except:
                    raise RuntimeError("arg was not (str, int), instead : " + str(s))
        return True

    def check(self, item):
        """takes in a str item and check if it is in entity's status
        return the number of time item appears in entity's status"""
        return self.status.count(item)

    def remove(self, item):
        """takes in a str item and removes it from entity's status
        return True if it removed it, an error if not"""
        if self.check(item):
            try:
                self.status.remove(item)
            except:  # might be a bit redundant but you never know
                raise RuntimeError("something append during the removal of " + item + " on " + self.name)
            else:
                return True
        else:
            raise RuntimeError("tried to remove unexisting " + item + " on " + self.name)

    def cast_attack(self, target):
        """takes in an entity target and will pass it in every function in entity's attack list
        return True if it all worked well, False if entity's dead, an error otherwise"""
        if not self.alive():
            print(self.name + " tried to attack, even thought he was dead.")
            return False
        print(self.name + " attacked")
        try:
            for act in self.attack:
                act(self, target)
        except:
            raise RuntimeError("something happened during " + self.name + "'s attack")
        else:
            return self.end_turn("attack")

    def cast_heal(self, target):
        """takes in an entity target and will pass it in every function in entity's heal list
        return True if it all worked well, False if entity's dead, an error otherwise"""
        if not self.alive():
            print(self.name + " tried to use magic, even thought he was dead.")
            return False
        print(self.name + " used magic")
        try:
            for act in self.heal:
                act(self, target)
        except:
            raise RuntimeError("something happened during " + self.name + "'s heal")
        else:
            return self.end_turn("heal")

    def cast_defend(self, target):
        """takes in an entity target and will pass it in every function in entity's defend list
        return True if it all worked well, False if entity's dead, an error otherwise"""
        if not self.alive():
            print(self.name + " tried to defend, even thought he was dead.")
            return False
        print(self.name + " raised their guard")
        try:
            for act in self.defend:
                act(self, target)
        except:
            raise RuntimeError("something happened during " + self.name + "'s defend")
        else:
            return self.end_turn("defend")

    def turn(self, target):
        """takes in an entity target and user will take its turn automically
        available actions are : attacking target, healing themselves, defending themselves
        target can also be a list of targets and a random one will be chosen"""
        total = self.strength + self.magic + self.defence
        attack_cap = self.strength / total  # probability for entity to attack
        heal_cap = (self.magic / total) + attack_cap  # probability for entity to heal
        defend_cap = (self.defence / total) + heal_cap  # probability for entity to defend
        ans = random()
        if ans <= attack_cap:
            if type(target) == list:
                target = choice(target)
            self.cast_attack(target)
            return True
        elif ans <= heal_cap:
            self.cast_heal(self)
            return True
        elif ans <= defend_cap:
            self.cast_defend(self)
            return True
        else:  # yes I know, this isn't supposed to happen, ever, since attack_cap + heal_cap + defend_cap = 1
            # and random() gives a float between 0 and 1, but hey, ya never knwo
            raise RuntimeError("What")

    def end_turn(self, action):
        """handles end of turn logic (like DoT effects and lowering buffs duration)
        takes in a str action representing the action done during this turn"""
        if action != "defend" and self.check("shield"):  # lower buffs (and debuffs when I'll add those)
            if self.check("sturdy"):  # sturdy will allow you to keep shields for longer
                self.remove("sturdy")
            else:
                self.remove("shield")
            # Maybe I should add a debuff list to know which to lower and automatically do it

        if self.check("burn"):  # burn logic
            damage = self.check("burn")
            if self.check("wet"):
                damage *= 2
                print(self.name + " evaporates")
                self.remove("wet")
            self.hurt += damage
            print(self.name + " took " + str(damage) + " damage from burn")
            self.remove("burn")
        return True


class Player(Entity):
    def __init__(self, name):
        super().__init__(name, 20, 6, 3, 3)
        self.attack.append(lambda user, target: target.add("burn"))


class Slime(Entity):
    def __init__(self):
        super().__init__("Slime", 10, 4, 1, 2)
        self.add(("wet", 999))
