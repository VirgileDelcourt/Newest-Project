class LevelUp:
    def __init__(self, text, **kwargs):
        self.text = text
        self.attack = []
        self.heal = []
        self.defend = []
        if "attack" in kwargs:
            self.attack = kwargs["attack"]
        if "heal" in kwargs:
            self.heal = kwargs["heal"]
        if "defend" in kwargs:
            self.defend = kwargs["defend"]

    def apply(self, character):
        """takes in an Entity and gives it the corresponding upgrades
        also notifies the player with a (cryptic) message"""
        print(self.text)
        character.attack.extend(self.attack)
        character.heal.extend(self.heal)
        character.defend.extend(self.defend)

# those dicts have the level up requirement as keys and the level up effects (a LevelUp object) as value
fire = {1: LevelUp("The warmth of the campfire kept you company.", attack=[lambda user, target: target.add("burn")])}
nature = {1: LevelUp("You heard the sounds of animals all night long.", heal=[lambda user, target: user.recover(10)])}
earth = {1: LevelUp("You found a pebble in your shoe.", defend=[lambda user, target: user.add("shield")])}
water = {1: LevelUp("You woke up thirsty in the middle of the night", heal=[lambda user, target: target.damage(10)])}
