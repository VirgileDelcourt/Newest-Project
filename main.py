from Scripts.Character import Player, Slime
from time import sleep


def turn(characters: list):
    return sorted(characters, key=lambda char: char.get_speed())

if __name__ == '__main__':
    time = 0
    actiontime = 12

    print("Hello world.")
    name = input("Enter the name of your hero : ")
    player = Player(name)

    while 1 > 0:  # game loop
        while time < 24:  # battles loop
            print("A fucking slime appeared !")
            slime = Slime()
            print(" ")
            while slime.get_hp() > 0 and player.get_hp() > 0:
                choice = input("What do you do ? Attack, heal or defend ? ")
                if choice.lower() == "attack":
                    act = player.cast_attack
                elif choice.lower() == "heal":
                    act = player.cast_heal
                elif choice.lower() == "defend":
                    act = player.cast_defend
                else:
                    act = None
                    print("I don't understand what you're talking about, please try again.")

                if act is not None:
                    for char in turn([player, slime]):
                        if char == player:
                            act(slime)
                        else:
                            char.turn(player)
                        sleep(1)
                        print(" ")
                time += actiontime
        print("This was a long day.")
        print("You set up a campfire and rest for the night.")
        player.rest()  # level up
        sleep(3)
        print(" ")

        time -= 24
        if actiontime != 1:  # increases days duration
            actiontime -= 1
