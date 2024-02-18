from Scripts.Character import Player, Slime


def turn(characters: list):
    return sorted(characters, key=lambda char: char.get_speed())

if __name__ == '__main__':
    time = 0
    actiontime = 12

    print("Hello world.")
    name = input("Enter the name of your hero : ")
    player = Player(name)

    while 1 > 0:
        while time < 24:
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

                if act != None:
                    for char in turn([player, slime]):
                        if char == player:
                            act(slime)
                        else:
                            char.turn(player)
                        print(" ")
                print(" ")
                time += actiontime
        print("This was a long day.")
        print("You set up a campfire and rest for the night.")
        player.rest()
        print(" ")

        time -= 24
        if actiontime != 1:
            actiontime -= 1
