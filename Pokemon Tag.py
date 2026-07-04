import os
import random


# Below is the data of the pokemons and there stats
pokemon_stats = [
    { "Pokemon" : "Pikachu" , "HP" : 70 , "Attack": 31 , "Defense": 10, "Heal": 22, "Max_heals": 1, "Speed": 95 , "Moves" : "THUNDER BOLT ⚡"} ,
    { "Pokemon" : "Charmander" , "HP" : 80 , "Attack": 27 , "Defense": 13, "Heal": 26, "Max_heals": 3, "Speed": 70, "Moves": "EMBER 🔥"} ,
    { "Pokemon" : "Bulbasaur" , "HP" : 95 , "Attack": 20 ,"Defense": 18, "Heal": 32, "Max_heals":3, "Speed": 45, "Moves": "RAZOR LEAF 🍃"} , 
    
 ]
def main():

    print("\n========================")
    print("  ⚔️  POKÉMON BATTLE ⚔️")
    print("========================\n")

# Step 1: Decide player's pokemon
    player_list = choose_pokemon(pokemon_stats)
    
# Step 2: Deiced computer's pokemon != players pokemon
    while True:
        comp_list = random.choice([pokemon_stats[0], pokemon_stats[1], pokemon_stats[2], pokemon_stats[3]])

        if comp_list != player_list:
            break

# Step 3: When pokemon's are selected, clear the terminal and print "BATTLE START"
    os.system('cls' if os.name == 'nt' else 'clear')

    battle_start(player_list, comp_list)

    round_number = 1
    player_hp = player_list["HP"]
    comp_hp = comp_list["HP"]
    
    player_heals = player_list["Max_heals"]
    comp_heals = comp_list["Max_heals"]

# Step 4: Speed decides who will take the first
    while player_hp > 0 and comp_hp > 0:

        next_Round(player_list, comp_list, player_hp, comp_hp, round_number)

# If player's pokemon speed higher: loop follows below
        if player_list["Speed"] >= comp_list["Speed"]:

# The return value from the player's turn is a list, which may contain comp_hp or players_hp, so first its checked which value is in it, then stored accordingly.
            hp = player_turn(player_list , player_hp, player_heals, comp_list , comp_hp) # Player turn first
            player_heals = hp[2]

            if hp[1]:
                player_hp = hp[0]
            else:
                comp_hp = hp[0]
            
            input() # Press Enter to proceed

            if comp_hp <=0:
                break

# The return value from the computer's turn is a list, which may contain comp_hp or players_hp, so first its checked which value is in it, then stored accordingly.
            hp = comp_turn(comp_list, comp_hp, comp_heals, player_list, player_hp, ) # computer turn after
            comp_heals = hp[2]

            if hp[1]:
                player_hp = hp[0]
            else:
                comp_hp = hp[0]
            
# If computer's pokemon speed higher: loop follows below
        else:
            hp = comp_turn(comp_list, comp_hp, comp_heals, player_list, player_hp, ) # Computer Turn first
            comp_heals = hp[2]

            if hp[1]:
                player_hp = hp[0]
            else:
                comp_hp = hp[0]

            input() # Press Enter to proceed

            if player_hp <=0:
                break

            hp = player_turn(player_list , player_hp, player_heals, comp_list , comp_hp) # Player turn after
            player_heals = hp[2]

            if hp[1]:
                player_hp = hp[0]
            else:
                comp_hp = hp[0]

# Step 5: Round ends here
        if comp_hp > 0 and player_hp > 0:

            round_number += 1             
            input("Ready for the next round?? ")
            os.system('cls' if os.name == 'nt' else 'clear')


# Step 6: When one pokemon faints, Game Over
    if comp_hp <= 0 :
        print("\n\n#################################")
        print(f"\n💥💥 !!! {player_list["Pokemon"]} wins !!!💥💥\n")
        print("#################################\n")

    elif player_hp <= 0:
        print("\n\n#################################")
        print(f"\n💥💥 !!! {comp_list["Pokemon"]} wins !!!💥💥\n")
        print("#################################\n")

def player_turn(player, player_hp, player_heals, comp , comp_hp):
        
# Player's move is decided here and the hp's change accordingly
        move = choose_move(player, player_hp, player_heals)
        match move:
            case "Attack":
                damage = damage_calculator(player, comp)
                comp_hp -= damage[0]

                if comp_hp < 0:
                    comp_hp = 0 # removes negative HP

                side_effect(player, player_hp, player_heals, comp, comp_hp, move, damage) # The result of player's move is printed here

                return [comp_hp , False , player_heals]

            case "Heal":
                player_hp = min(player["HP"], player_hp + player["Heal"])
                player_heals -= 1
                side_effect(player, player_hp, player_heals, comp, comp_hp, move, 0) # The result of player's move is printed here

                return [player_hp , True , player_heals]


def comp_turn(comp, comp_hp, comp_heals, player, player_hp, ):
# Computer's move is decided here and the hp's change accordingly
        c_move = comp_move(comp, comp_hp, comp_heals, player, player_hp)
        input()

        match c_move:
            case "Attack":
                damage = damage_calculator(comp , player)
                player_hp -= damage[0]

                if player_hp < 0:
                    player_hp = 0 # Removes negative HP

                side_effect(comp, comp_hp, comp_heals, player, player_hp, c_move, damage) # The result of Comp's move is printed here

                return [player_hp , True, comp_heals]

            case "Heal":
                comp_hp = min(comp["HP"], comp_hp + comp["Heal"])
                comp_heals -= 1
                side_effect(comp, comp_hp, comp_heals, player, player_hp, c_move, 0) # The result of Comp's move is printed here

                return [comp_hp , False, comp_heals]


def side_effect(player, player_hp, player_heals, opponent, opponent_hp , move, damage):
    print("\n-----------------------------------")
    match move:
        case "Attack":
            print(f"{player["Pokemon"]} used {player["Moves"]} !!!\n")

            if damage[1] == "critical_true":
                print("--- !!! CRITICAL HIT !!! ---\n")

            print(f"damage dealt: - {damage[0]}")
            print(f"{opponent["Pokemon"]}'s HP:  {opponent_hp}\n")
        
        case "Heal":
            print(f"{player["Pokemon"]} used HEALING ➕ !!!   ")
            print(f"HP Healed: + {player["Heal"]}\n")

            print(f"{player["Pokemon"]}'s HP: {player_hp}\n")
            print(f"--- Heals left: {player_heals} ---")


def damage_calculator(attacker, defender):

    damage = max(1, attacker["Attack"] - defender["Defense"])
    damage += random.choice([2, 1, 0, -1, -2]) 

    critical = random.choice([False, False, False, False, False, False, False, False, False, True ]) # 10% Chance of critical hit

    if critical:
        return [damage * 2 , "critical_true"]
    else:
        return [damage , "critical_false"]

    
def choose_move(player, player_hp, heals):
    print("-----------------------------------")
    print("Your Turn !!!\n")
    print("1. Attack\n")
    print("2. Heal\n")
 
    while True:
        move = input("Choose your move: ")
        match move:
            case "1":
                return "Attack"
            
            case "2":
                if heals == 0:
                    print("\n--- No HEALS left ---\n")
                
                elif player_hp == player["HP"]:
                    print("\n-- Your HP is full --\n")

                else:
                    return "Heal"
                
            case _:
                print("The move isn't availiable\n")

def comp_move(comp, comp_hp, comp_heals, player, player_hp):
    print("-----------------------------------")
    print("Computer's Turn !!!\n")

    # Comp first calculate the damage of a mid critical hit by player, and then decides to heal if the damage will kill him
    # IF comp decided not to heal, comp can be killed if the player hits by a high critical attack probabilty: 3.33% (Only to reduce difficulty and give satisfaction to player)
    # If the player will be killed by computers worst attack, comp will not heal and instead attack

    if ( comp_hp - (player["Attack"] - comp["Defense"]) * 2 ) <= 0 and comp_heals != 0: 

        if (player_hp + player["Defense"] - comp["Attack"] - 2) <= 0: # comp can't itself determine the fluctuation in a move's damage,
            return "Attack"                                           #  so he uses this move only when it is certain
        else:
            return "Heal"
    
    else:
        return "Attack"


def choose_pokemon(pokemon_list):

    for pokemon_index in range(len(pokemon_list)):
        pokemon_dict = pokemon_list[pokemon_index]
        
        print(pokemon_index + 1, pokemon_dict["Pokemon"], sep = '. ')

    while True:
        n = input("\nChoose your pokemon: ")
        print()

        if n.isdigit and n in ["1", "2", "3", "4"]:
            n = int(n)

            for pokemon_index in range(len(pokemon_list)):

                if n == pokemon_index + 1:
                    return pokemon_list[pokemon_index]
                
        else:
            print("--- Enter the number of the pokemon, you wanna choose ---")
        
    


def next_Round(player, comp, player_hp, comp_hp, round_num):
    print()
    print("-----------------------------------")
    print(f"  ---((  --- ROUND - {round_num} ---  ))---")
    print("-----------------------------------")
    print(f"\n\n{player["Pokemon"]} HP: {player_hp}")
    print(f"{comp["Pokemon"]} HP: {comp_hp}" , end = '\n\n')
    

def battle_start(p_list , c_list):

    print("\n========================")
    print("  ⚔️  BATTLE START ⚔️")
    print("========================", end = '\n\n')

    print("Your pokemon: ", p_list["Pokemon"] , end = '\n')
    print("HP: ", p_list["HP"])
    
    print("\nEnemy: ", c_list["Pokemon"] , end ='\n')
    print("HP: ", c_list["HP"] , end = '\n\n')
    input("Are you ready (y/n) ??? ")

    # terminal is cleared to print the Round into the screen
    os.system('cls' if os.name == 'nt' else 'clear')

main()
