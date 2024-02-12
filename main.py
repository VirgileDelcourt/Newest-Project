from Scripts.Character import Player, Slime

if __name__ == '__main__':
    print("Hello world.")
    name = input("Enter the name of your hero : ")
    player = Player(name)
    print("A fucking slime appeared !")
    slime = Slime()
    while slime.get_hp() > 0 and player.get_hp() > 0:
        choice = input("What do you do ? Attack, heal or defend ? ")
        if choice.lower() == "attack":
            player.cast_attack(slime)
            slime.turn(player)
        elif choice.lower() == "heal":
            player.cast_heal(player)
            slime.turn(player)
        elif choice.lower() == "defend":
            player.cast_defend(player)
            slime.turn(player)
        else:
            print("I don't understand what you're talking about, please try again.")
