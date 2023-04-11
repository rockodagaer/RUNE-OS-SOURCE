import random
import json
import os
import math
import time

# inventory is, 0: amount in inventory, 1: buy price, 2: sell price

skills = {"fishing": {"lvl": 1, "xp": 0, "needed": 100}, "prayer": {"lvl": 1, "xp": 0, "needed": 100}, "cooking": {"lvl": 1, "xp": 0, "needed": 100}, "mining": {"lvl": 1, "xp": 0, "needed": 100}}

# attack is the chance of hitting, strength is the damage, defence is the chance of dodging
combat = {"attack": {"lvl": 1, "xp": 0, "needed": 100}, "strength": {"lvl": 1, "xp": 0, "needed": 100}, "defense": {"lvl": 1, "xp": 0, "needed": 100}, "magic": {"lvl": 1, "xp": 0, "needed": 100}}

needs = {"health": 100, "hunger": 1000, "reputation": 50}
offline_variables = {"kills": {"plant": 0, "chicken": 0, "pig": 0, "cow": 0, "woman": 0, "melee goblin": 0, "man": 0, "farmer": 0, "scarr's minion": 0, "scarr's weak bodyguard (BOSS)": 0,
                               "bloodthirsty rabbit": 0, "tree goblin": 0, "wolf cub": 0, "Scarr's fast minion": 0, "fox": 0, "weak goblin giant (MINI-BOSS)": 0, "wolf": 0, "big fox": 0, "goblin giant (BOSS)": 0}, "mission": {"lvl": 0},

                                "difficulty": {"exponent": 1.5, "growth": 1.1, "lvl": 1}, "mail": {"error": False, "lvl": 0} }
max_lvl = 100
money = 50

equipped_weapon = "nothing"
# 0 = name, 1 = attack+, 2 = strength+, 3 = defense+, 4 = health+
weapons = [["nothing", 0, 0, 0], ["broken wood dagger", 1, 1, 0], ["broken bronze dagger", 3, 2, 1], ["broken silver dagger", 4, 3, 1], ["broken gold dagger", 3, 4, 2], ["broken rune dagger", 5, 4, 3],
           ["wood dagger", 10, 1, 5], ["bronze dagger", 10, 2, 5], ["silver dagger", 10, 3, 5], ["gold dagger", 10, 4, 5], ["rune dagger", 10, 5, 5]]

# Define a function that calculates the XP needed for the next level
def xp_for_next_level(level):
    base = 100 # The minimum XP needed for level 1
    exponent = offline_variables["difficulty"]["exponent"] # The constant that determines how fast the XP curve increases
    growth = offline_variables["difficulty"]["growth"] # The factor that adjusts the XP curve

    # Use the formula to calculate the XP
    xp = base * (level ** exponent) * growth
    # Round up the XP to the nearest integer
    xp = math.ceil(xp)
    # Return the XP value
    return xp

# set inventory to inventory.json
inventory = {}
with open("inventory.json", "r") as f:
    inventory = json.load(f)

print("WARNING: THIS IS HEAVILY INSPIRED BY RUNESCAPE.")
print("THIS IS MADE AS A FAN PROJECT AND WILL PROBABLY SUCK.")
input("Press Enter to continue...")
os.system("cls")

def menu():
    global skills, combat, needs, money, inventory, offline_variables
    print("NEW save or OLD save?")
    choice = input("keywoard>> ")

    if choice.lower() == "new":
        print
        choice = input("ARE YOU REALLY SURE YOU WANT TO CREATE A NEW SAVE? (y/n)")
        if choice.lower() == "y":
            print("LOADING INVENTORY...")
            # set everything in the inventory to 0
            for i in inventory:
                inventory[i][0] = 0
                print(str(i) + ": " + str(inventory[i][0]))
            print("SAVING INVENTORY...")
            with open("inventory.json", "w") as f:
                json.dump(inventory, f, indent=4)
            save_all_items = {"skills": skills, "combat": combat, "needs": needs, "money": money, "offline": offline_variables}
            with open("skills.json", "w") as f:
                json.dump(save_all_items, f, indent=4)
            os.system("cls")

        if choice.lower() == "n":
            print("LOADING INVENTORY...")
            load_all_items = {}
            with open("skills.json", "r") as f:
                load_all_items = json.load(f)
            skills = load_all_items["skills"]
            combat = load_all_items["combat"]
            needs = load_all_items["needs"]
            money = load_all_items["money"]
            offline_variables = load_all_items["offline"]
            os.system("cls")
    else:
        print("LOADING INVENTORY...")
        load_all_items = {}
        with open("skills.json", "r") as f:
            load_all_items = json.load(f)
        skills = load_all_items["skills"]
        combat = load_all_items["combat"]
        needs = load_all_items["needs"]
        money = load_all_items["money"]
        offline_variables = load_all_items["offline"]
        os.system("cls")

    os.system("cls")
    print("Do you want to play the tutorial? (y/n)")
    choice = input(">> ")
    if choice.lower() == "y":
        os.system("cls")
        print("These are the SUPER basics of the game.")
        print("This game can look difficult on the surface but it isnt. The hardest thing in here is remembering that you need to eat.")
        print("So anyways the gravitational pull of the sun is 9.8 m/s^2. This means that if you jump off a cliff you will die.")
        print("Nah im just f*cking with you, this tutorial wont go over all that stuff because that isnt even in the game.")
        print("This tutorial will first go over how to navigate the menus, then well go over the basics of skills and then well go over hunger and money management.")
        input("Press Enter to continue...")
        print("First well go over how to navigate the menus. Its quite simple actually.")
        print("In the first menu you will see a list of thing you can do on the top of the screen. These things you can type as commands to do them.")
        print("For example you can type \"skills\" to see a list of skills and their levels. Then when you get back to the main menu you can type the name of one of those skills to do it.")
        print("But when your outside of a menu youll be mostly typing NUMBERS to do things. For example you will see a list of numbers with things like [0] or [1] in front of them.")
        print("You can type the number in front of the thing you want to do to do it without the name of the thing. For example if you see \"[0] EXIT\" and you want to exit, then you need to type the number 0.")
        print("Besides the main menu you will only be using numbers to navigate or atleast in the beginning of the game's development.")
        input("Press Enter to continue...")
        os.system("cls")
        print("Now lets go over the basics of skills. Skills are the main way to progress in the game. You can level up skills by doing them.")
        print("For example if you want to level up your mining skill you need to mine ore, different ores give different amounts of xp. Mining rune essence gives you almoast no xp but mining other things may give you more xp.")
        print("If your ex is higher than your needed xp you level up, makes sense right? Well other skills may work differently.")
        print("For example the combat skill is actually 3 skills, attack, defence and strength. You can level up these skills by doing combat but you need to learn them separately.")
        print("You can switch between leveling different skills in the combat menu by going to change attack mode and picking one, and you will train the skill you picked.")
        print("But theres also another cool thing with the combat system which is, for example if you pick strength as your attack mode, you will have more strength for that battle.")
        print("And this works for all of the combat skills, you can also choose another attack mode like defense which will make your chance of blocking higher for that battle!")
        input("Press Enter to continue...")
        os.system("cls")
        print("Now lets go over hunger and money management. Hunger is a very important thing in this game. If you dont eat you wont be able to do anything. Money also has this but with not being able to buy things.")
        print("You can cook by going the the combat skills and picking the EAT option. A lot of actions require you to have at least a certain amount of hunger and drain your hunger.")
        print("For example fishing takes away 0.25 hunger for every in-game minute you fish. And it may sound like you want to keep your hunger low but actually you want to keep it high.")
        print("This is because hunger is reversed in this game and is actually how full you are. And you have a max of 1000 hunger so you dont have to worry too much about it.")
        print("You can get food by buying it, fishing or killing enemies like cows or chickens.")
        print("And for money its quite simple, you dont have a max amount of money and you start out with 50$ as a kind of fail safe for if you accidentally run out of food.")
        print("You can buy or sell items by going to the shop, you can buy items by spending money in the BUY tab or you can sell items by going to the SELL tab.")
        print("In both of these tabs you have a lot of options to buy or sell items but you cant buy and sell ALL items. And you cant duplicate money by buying and selling the same item, the selling price is always lower than the buying price.")
        input("Press Enter to continue...")
        os.system("cls")
    else:
        print("Ssuuuurreeee")
        input("Press Enter to continue... Or not idc")
        os.system("cls")

    print("Early access version 0.05: Weapons!")
    print("Welcome to RUNE OS")
    while True:
        print("You have " + str(needs["health"]) + " health, " + str(int(needs["hunger"])) + f" hunger and {money} money.")
        print("TYPE \"SKILLS\" FOR A LIST OF ALL THE SKILLS AND YOUR LEVEL")
        print("TYPE \"SAVE\" TO SAVE")
        print("TYPE \"HELP\" FOR OTHER COMMANDS")
        print("TYPE \"SHOP\" TO OPEN THE SHOP")
        print("TYPE \"TUTORIAL\" TO PICK A TUTORIAL")
        print("TYPE \"MISSIONS\" TO GO TO THE MISSIONS MENU")
        print("TYPE \"SETTINGS\" TO CHANGE YOUR SETTINGS")
        print("TYPE THE SKILL YOU WISH TO TRAIN")

        with open("inventory.json", "w") as f:
            json.dump(inventory, f, indent=4)
        save_all_items = {"skills": skills, "combat": combat, "needs": needs, "money": money, "offline": offline_variables}
        with open("skills.json", "w") as f:
            json.dump(save_all_items, f, indent=4)

        choice = input(">> ")
        os.system("cls")
        if choice.lower() == "help":
            print("[1] TYPE \"INVENTORY\" TO OPEN INVENTORY")
        
        if choice.lower() == "settings" or choice.lower() == "settings":
            print("Welcome to the settings menu.")
            print("[0] EXIT")
            print("[1] Change difficulty")
            print("[2] Show advanced developer settings")
            print("[3] Speed test")
            choice = input("NUMBER>> ")
            if choice.lower() == "0": pass



            if choice.lower() == "3":
                os.system("cls")
                testing = True
                time_start = time.time()
                num0 = 0
                while testing:
                    num0 += 1
                    if num0 == 100000*100:
                        testing = False
                        time_end = time.time()
                        print("It took", time_end - time_start, "seconds to count to 100000X100")
                        # now say if thats good or bad
                        if time_end - time_start < 1:
                            print("Good loop speed! This is the optimal speed for the game to run at. You shouldnt have any problems with the game running slow.")
                        if time_end - time_start < 4 and time_end - time_start > 1:
                            print("Ok loop speed, this might affect the speed of combat or loading times while fighting high-level enemies or big loading screens.")
                        input("Press Enter to continue...")
                        os.system("cls")
                testing = True
                time_start = time.time()
                num0 = 0
                while testing:
                    num0 += 1
                    print("Printing test.")
                    if num0 == 10000:
                        testing = False
                        print("Done testing printing speed.")
                        print("It took", time.time() - time_start, "seconds to print 100000X100")
                        if time.time() - time_start < 6:
                            print("This is a fantastic speed! You shouldnt have to wait a second for the game to load/calculate.")
                        if time.time() - time_start < 10 and time.time() - time_start > 6:
                            print("Very good speed, you might have little drops but nothing too bad.")
                        if time.time() - time_start < 20 and time.time() - time_start > 10:
                            print("Less then optimal speed, you might have to wait a few seconds for the game to load/calculate.")
                        input("Press Enter to continue...")
                        os.system("cls")



            if choice.lower() == "1":
                print("Change difficulty to: ")
                print("[0] EXIT")
                print("[1] EASY, for people who want a relaxing experience")
                print("[2] NORMAL, for people who want to play the game in the way it was meant to be played.")
                print("[3] HARD, for people who want a challenge")
                print("[4] EXTREME, for people who want to put a lot of time in beating a boss.")
                print("[5] IMPOSSIBLE, FOR PEOPLE WHO WANT TO SACRAFICE THEIR LIFE TO THE GAME")
                print("[6] GOD, FOR PEOPLE WHO WANT TO BE SACRAFICED TO THE GAME AND SUFFER IN HELL FOREVER")
                print("[7] SATAN, Ok so listen up right? Imagine every enemy you come across is a supernova. You got it? Good. Because now every enemy you see is a supernova, with a blackhole in the middle, with the heat of 5 billion suns and so big that you can fit a lot of galaxy's inside of it. And you need to fight it naked.")
                choice = input("NUMBER>> ")
                if choice.lower() == "0": pass
                if choice.lower() == "1": offline_variables["difficulty"]["exponent"] = 1.25; offline_variables["difficulty"]["growth"] = 1.1; print("Enemy's will enjoy sacrafising themselfes to you."); offline_variables["difficulty"]["lvl"] = 0; max_lvl = 75
                if choice.lower() == "2": offline_variables["difficulty"]["exponent"] = 1.5; offline_variables["difficulty"]["growth"] = 1.1; print("Enemy's will enjoy being your practice dummy."); offline_variables["difficulty"]["lvl"] = 1; max_lvl = 100
                if choice.lower() == "3": offline_variables["difficulty"]["exponent"] = 1.75; offline_variables["difficulty"]["growth"] = 1.25; print("Enemy's will enjoy drinking your little bit of blood."); offline_variables["difficulty"]["lvl"] = 2; max_lvl = 125
                if choice.lower() == "4": offline_variables["difficulty"]["exponent"] = 2; offline_variables["difficulty"]["growth"] = 1.5; print("Enemy's will enjoy your suffering."); offline_variables["difficulty"]["lvl"] = 3; max_lvl = 150
                if choice.lower() == "5": offline_variables["difficulty"]["exponent"] = 2.25; offline_variables["difficulty"]["growth"] = 1.75; print("ENEMY's SHALL NOW FEAST ON YOUR SOUL!"); offline_variables["difficulty"]["lvl"] = 4; max_lvl = 175
                if choice.lower() == "6": offline_variables["difficulty"]["exponent"] = 2.75; offline_variables["difficulty"]["growth"] = 2.25; print("Enemy's will enjoy your suffering in hell."); offline_variables["difficulty"]["lvl"] = 5; max_lvl = 225
                if choice.lower() == "7": offline_variables["difficulty"]["exponent"] = 4; offline_variables["difficulty"]["growth"] = 4; print("Enemy's will enjoy your suffering."); offline_variables["difficulty"]["lvl"] = 6; max_lvl = 300
                choice = ""
            if choice.lower() == "2":
                print("[0] EXIT")
                print("[1] Show skills")
                print("[2] Show combat")
                print("[3] Show needs")
                print("[4] Show offline_variables")
                print("[5] Show inventory")
                print("[6] Show XP growth")
                choice = input("NUMBER>> ")
                os.system("cls")
                if choice.lower() == "0": pass
                if choice.lower() == "1": print(skills)
                if choice.lower() == "2": print(combat)
                if choice.lower() == "3": print(needs)
                if choice.lower() == "4": print(offline_variables)
                if choice.lower() == "5": print(inventory)
                if choice.lower() == "6":
                    for i in range(1, max_lvl):
                        print(str(xp_for_next_level(i)))
                input("Press Enter to continue...")

        if choice.lower() == "skills":
            print("Type the name of the skill you which you want to train in the main menu.")
            print("What do you want to know more about? Because you need some lecturing.")
            print("[0] EXIT")
            print("[1] COMBAT")
            print("[2] FISHING")
            print("[3] PRAYER")
            print("[4] COOKING")
            print("[5] MINING")
            choice = input("NUMBER>> ")
            if choice.lower() == "0": pass
            if choice.lower() == "1":
                print("All your combat skills are:")
                print(f"Attack level: {combat['attack']['lvl']}. Attack XP: {combat['attack']['xp']}. Needed xp: {combat['attack']['needed']}")
                print(f"Strength level: {combat['strength']['lvl']}. Strength XP: {combat['strength']['xp']}. Needed xp: {combat['strength']['needed']}")
                print(f"Defence level: {combat['defense']['lvl']}. Defence XP: {combat['defense']['xp']}. Needed xp: {combat['defense']['needed']}")
            if choice.lower() == "2":
                print(f"Fishing level: {skills['fishing']['lvl']}. Fishing XP: {skills['fishing']['xp']}. Needed xp: {skills['fishing']['needed']}")
            if choice.lower() == "3":
                print(f"Prayer level: {skills['prayer']['lvl']}. Prayer XP: {skills['prayer']['xp']}. Needed xp: {skills['prayer']['needed']}")
            if choice.lower() == "4":
                print(f"Cooking level: {skills['cooking']['lvl']}. Cooking XP: {skills['cooking']['xp']}. Needed xp: {skills['cooking']['needed']}")

        if choice.lower() == "fishing" or choice.lower() == "fish": fishing()
        
        if choice.lower() == "combat" or choice.lower() == "fight": fight()

        if choice.lower() == "shop" or choice.lower() == "store": shop()

        if choice.lower() == "tutorial" or choice.lower() == "tutor": tutorial()

        if choice.lower() == "cooking" or choice.lower() == "cook": cooking()

        if choice.lower() == "mining" or choice.lower() == "mine": mining()
        
        if choice.lower() == "missions" or choice.lower() == "mission": missions()



def tutorial():
    while True:
        print("Welcome to the RUNE OS TUTORIAL. Becuase you look like you need to do some learning.")
        print("You can learn about specific things over here by typing the number in front of a line of text.")
        print("[0] EXIT")
        print("[1] Skills and economy tutorial (Recommended for new players)")
        print("[2] Combat tutorial (Recommended for new players)")
        print("[3] Food tutorial (Small tutorial about how food works)")
        choice = input("NUMBER>> ")
        if choice.lower() == "0": break
        if choice.lower() == "1":
            print("Welcome to the RUNE OS TUTORIAL about skills and economy.")
            print("Rune OS is a runescape inspired game, which in this case means that you can train skills and get money in the same way you do in runescape.")
            input("Press Enter to continue...")
            print("The game sometimes looks complex but its actually really simple and fun. \nYou have skills you can train like combat and fishing.")
            print("Most skills have 1 thing to train but some of them have multiple things to train inside of it.")
            input("Press Enter to continue...")
            print("You need xp to level your skills and the higher your skill level is for a specific skill, the better you get at it.")
            print("For example when your level is extremely low in combat, you will have a very low chance actually hitting your target.")
            print("While if your skill level is extremely high, you will have a very high chance actually hitting your target and do a lot of damage.")
            input("Press Enter to continue...")
            print("Money is also gained from killing enemeys, selling items and doing other things.")
            print("You can sell most things you find in the game and if you cant find a specific item, you can buy it.")
            input("Press Enter to continue...")
            print("Theres also hunger, if your hunger is low you will die. Hunger is only spent while doing things like fishing.")
            print("You can replenish your hunger by eating stuff like shrimp and steak, you can eat by going to your combat skill, picking an area and enemy and then choosing EAT.")
            print("From there you can eat anything you have in your inventory.")
            input("Press Enter to continue...")
            print("Theres also an invisible stat called reputation, your reputation is affected by killing certain enemys, selling items and all that stuff.")
            print("When your reputation gets very low, some items might get a higher buying price and a lower selling profit. When nutral nothing will be affected.")
            print("But when your reputation gets very high, some items might get lower prices and higher selling profits.")
            input("Press Enter to continue...")
            print("But if you make too much use of the high reputation, your reputation will drop because of selfishness.")
            input("Press Enter to continue...")
            print("And thats the end of the tutorial about skills and economy!")
        if choice.lower() == "2":
            print("Welcome to the RUNE OS TUTORIAL about combat.")
            print("Because RUNE OS is inspired by runescape, the combat will be largely the same but you will still need to learn some quirks to know how it works.")
            input("Press Enter to continue...")
            print("The combat skill is a more unique skill that takes the training of 3 seperate skills all mashed up into one skill.")
            print("The skills are attack, strength and defense. You need to train them separately by going to the combat skill, picking an area and enemy and then going to the CHANGE ATTACK MODE tab.")
            print("The default mode is attack and you can only train 1 mode at a time. The attack skill is the chance of hitting the target. The strength skill is how much damage you do.")
            print("And the defense skill is the chance of only getting 50% damage done to you.")
            print("When you choose a specific skill to train you will also get a boost on that skill. This basically adds invisible levels to you while under level 60.")
            input("Press Enter to continue...")
            print("The enemy also has these skills. You cant see the enemys skills so when you pick an area, the top enemy you see in the list will be the easiest and the bottom enemy will be the hardest.")
            print("The combat system is turn based but you cant interact with the combat. When you start a fight, the game will play out a battle and only show you who won and your HP.")
            print("Your health can be replenished by going to an enemy and choosing EAT. From there you can see food you have and eat it to replenish your health.")
            print("When you kill enemys you also have a 1 in 5 chance that the enemy will drop an item based on what the enemy is. A chicken can drop chicken and a human can drop bones etc...")
            input("Press Enter to continue...")
            print("You are now done with the basics of the combat system.")
        if choice.lower() == "3":
            print("Welcome to the RUNE OS TUTORIAL about the basics of food.")
            print("The food system is extrememly simple and easy to understand.")
            print("First of all, if you want to eat something you need to go to the combat skill, pick an area and enemy and then choose EAT.")
            print("From there you can see what food you have and eat it to replenish your hunger.")
            input("Press Enter to continue...")
            print("At the menu screen you can see your hunger, it sounds like your hunger needs to be low but you actually need to keep it high.")
            print("Hunger in this term is reversed, high hunger means you are full and low hunger means you are starving.")
            print("Your hunger is 1 in 1000 and you lose hunger by doing things like fishing and cooking. For example every minute of fishing is about -0.5 hunger and every minute of cooking is -3 hunger.")
            input("Press Enter to continue...")
            print("Having low hunger will stop you from doing actions that take hunger away.")
            input("Press Enter to continue...")
            print("And thats the end of the tutorial about food!")

def shop():
    global money
    global inventory
    os.system("cls")
    while True:
        print("You wander into a shop, your wondering you should buy something or sell something...")
        print("[0] EXIT")
        print("[1] BUY")
        print("[2] SELL")
        choice = input("NUMBER>> ")
        os.system("cls")
        if choice.lower() == "0": print("Nevermind i have better things to do."); break
        if choice.lower() == "1":
            while True:
                print("You're looking to buy something, you look around and try to remember what you wanted to buy.")
                print("[0] EXIT")
                print("[1] FOOD")
                choice = input("NUMBER>> ")
                if choice.lower() == "0":print("You dont need any of this so you go away."); break
                if choice.lower() == "1":
                    os.system("cls")
                    print("You look around and see a bunch of food, you look at all of the food and see if something suits you.")
                    buy_options = ["shrimp", "pork", "chicken", "steak"]
                    print ("You have " + str(money) + " money. (0 for exit)")
                    print("[1] shrimp $2 [2] pork $10 [3] chicken $20 [4] steak $30")
                    choice = input("NUMBER>> ")
                    if choice == "0": print("Nope, you dont want any of this food."); break
                    if money >= inventory[buy_options[int(choice)-1]][1]:
                        inventory[buy_options[int(choice)-1]][0] += 1
                        money -= inventory[buy_options[int(choice)-1]][1]
                        print("Aha! This one looks good!")
                        print("You bought " + buy_options[int(choice)-1] + " for $" + str(inventory[buy_options[int(choice)-1]][1]) + ".")
                        print("You have $" + str(money) + " left."); print()
                    else: print("You dont have enough money to buy that! Get money by selling stuff idiot."); print()

        if choice.lower() == "2":
            while True:
                print("You're looking to sell something, you start thinking about what you want to sell.")
                print("[0] EXIT")
                print("[1] FOOD")
                print("[2] JUNK")
                choice = input("NUMBER>> ")
                if choice.lower() == "0": break
                if choice.lower() == "1":
                    os.system("cls")
                    sell_options = ["shrimp", "salmon", "light fish", "heavy fish", "pork", "chicken", "steak"]
                    print("You have some food left you could sell so you think about what food you want to sell.")
                    print ("You have " + str(money) + " money. (0 for exit)")
                    print(f"[1] shrimp $1 ({inventory[sell_options[0]][0]}) [2] pork $5 ({inventory[sell_options[4]][0]}) [3] chicken $10 ({inventory[sell_options[5]][0]}) [4] steak $20 ({inventory[sell_options[6]][0]})")
                    print(f"[5] salmon $2 ({inventory[sell_options[1]][0]}) [6] light fish $3 ({inventory[sell_options[2]][0]}) [7] heavy fish $5 ({inventory[sell_options[3]][0]})")
                    choice = input("NUMBER>> ")
                    if choice == "0": break
                    if inventory[sell_options[int(choice)-1]][0] >= 1:
                        inventory[sell_options[int(choice)-1]][0] -= 1
                        money += inventory[sell_options[int(choice)-1]][2]
                        print("I wasnt gonna eat this anyways.")
                        print("You sold " + sell_options[int(choice)-1] + " for $" + str(inventory[sell_options[int(choice)-1]][2]) + ". Thats a lot of money! Or not..")
                        print("You have $" + str(money) + " now."); print()
                    else: print("You don't have any " + sell_options[int(choice)-1] + " to sell! THEN WHY ARE YOU TRYING TO SELL IT!?"); print()
                if choice.lower() == "2":
                    os.system("cls")
                    sell_options = ["junk", "silver coin", "gold coin", "broken bronze dagger"]
                    print("You have some junk left to sell so you think about what junk you want to sell.")
                    print("You have " + str(money) + " money. (0 for exit)")
                    print(f"[1] junk $5 ({inventory[sell_options[0]][0]}) [2] silver coin $15 ({inventory[sell_options[1]][0]}) [3] gold coin $50 ({inventory[sell_options[2]][0]}) [4] broken bronze dagger $10 ({inventory[sell_options[3]][0]})")
                    choice = input("NUMBER>> ")
                    if choice == "0": break
                    if inventory[sell_options[int(choice)-1]][0] >= 1:
                        inventory[sell_options[int(choice)-1]][0] -= 1
                        money += inventory[sell_options[int(choice)-1]][2]
                        print("I wasnt gonna use this anyways.")
                        print("You sold " + sell_options[int(choice)-1] + " for $" + str(inventory[sell_options[int(choice)-1]][2]) + ". Thats a lot of money! Or not..")
                        print("You have $" + str(money) + " now."); print()

def fishing():
    global skills
    global max_lvl
    global inventory
    all_fish = [["junk", 1, 2], ["shrimp", 1, 5], ["salmon", 1, 10], ["light fish", 1, 10], ["heavy fish", 3, 20]]
    # name, needed level, xp
    while True:
        print("You're in the mood to go fishing so you wander to the nearby lake.")
        print("[0] EXIT")
        print("[1] FISH")
        choice = input("NUMBER>> ")
        os.system("cls")
        if choice.lower() == "0": print("You know what? This is boring, you go do something else."); break
        if choice.lower() == "1":
            print("Ahh yes, some good old fishing.")
            print("You wonder how long you should fish. (minutes)")
            minutes = int(input("MINUTES>> "))
            if minutes/4 < needs["hunger"]:
                needs["hunger"] -= minutes/4
                lvl = skills["fishing"]["lvl"]
                # loop the same amount of times as minutes
                caught = False
                caught_ever = False
                for i in range(0, minutes):
                    number = random.randint(0+lvl, max_lvl)
                    if lvl == number:
                        caught_ever = True
                        caught = True
                        perfect = True

                        while perfect == True:
                            number2 = random.randint(0, len(all_fish)-1)
                            caught_fish = all_fish[number2][0]
                            if lvl >= all_fish[number2][1] or random.randint(0, 100) <= 2:
                                perfect = False
                        if caught:
                            print("You caught " + caught_fish + " with " + str(minutes-i) + " minutes to spare!")
                            inventory[caught_fish][0] += 1
                            # 3rd number is the xp
                            skills["fishing"]["xp"] += all_fish[number2][2]
                            if skills["fishing"]["xp"] > skills["fishing"]["needed"]:
                                skills["fishing"]["needed"] = xp_for_next_level(skills["fishing"]["lvl"])
                                skills["fishing"]["lvl"] += 1
                                skills["fishing"]["xp"] -= skills["fishing"]["needed"]
                    if i == minutes: break
                if not caught_ever:
                    print("You didn't catch anything. The higher the level, the higher the chance of catching something!"); print("Thats what people say atleast..."); print()
            else: print("You need more hunger for that amount of time! Every minute is about -0.5 hunger. \nReplenish your hunger by eating at the combat skill! You should know this but i still said it. Be happy.")

def fight():
    os.system("cls")
    print("Loading areas...")
    areas = []
    with open("combat.json", "r") as f:
        areas = json.load(f)
    print("setting variables...")
    area = []
    global combat, skills, needs, max_level, equipped_weapon, weapons, inventory
    enemy = []
    choice = ""
    running = True
    attack_mode = 0
    attack_modes = ["attack", "strength", "defense"]
    os.system("cls")

    while running:
        print("You wander around looking for where you want to go but eventually pick...")
        print("[0] village")
        if combat["attack"]["lvl"] >= 6 and combat["strength"]["lvl"] >= 5 and combat["defense"]["lvl"] >= 2: print("[1] forrest")
        else: print("[1] Forrest (Unlocked at ATK 6, STR 5, DEF 2)")
        choice = input("Number>> ")

        if choice == "0":
            print("Loading area... if im in the mood to.")
            area = areas[0]
            running = False
            os.system("cls")
        if choice == "1" and combat["attack"]["lvl"] >= 6 and combat["strength"]["lvl"] >= 5 and combat["defense"]["lvl"] >= 2:
            print("Loading area... if im in the mood to.")
            area = areas[1]
            running = False
            os.system("cls")
    running = True
    while running:
        print("You look around for an enemy to attack and eventually land on...")
        for i in range(0, len(area)):
            print("[" + str(i+1) + "] " + area[i]["name"])
        
        choice = input("Number>> ")

        if int(choice)-1 <= len(area):
            print("Loading enemy... or not.")
            # attack strength defense health
            enemy = area[int(choice)-1]
            enemy_health = enemy["health"]
            enemy["attack"] = enemy["attack"] * 1.6
            enemy["strength"] = enemy["strength"] * 2
            running = False
            os.system("cls")
    running = True
    while running:
        input("Press enter to continue...")
        os.system("cls")
        print("You see an enemy and decide to attack it!")
        print("You have: " + equipped_weapon + " equipped.")
        print("[0] EXIT")
        print("[1] ATTACK")
        print("[2] CHANGE ATTACK MODE")
        print("[3] EAT")
        print("[4] BURRY BONES")
        print("[5] CHANGE WEAPON")
        choice = input("Number>> ")
        os.system("cls")



        if choice == "0": print("You decide to stop fighting."); running = False
        if choice == "5":
            # show all weapons in inventory
            print("You look at your weapons and decide to change to...")
            print("[0] EXIT")
            num = 0
            for i in range(0, len(weapons)):
                if weapons[i][0] != "nothing":
                    if inventory[weapons[i][0]][0] >= 1:
                        print(f"[{i+1}] {weapons[i][0]} ATK {weapons[i][1]} DMG {weapons[i][2]} DEF {weapons[i][3]}", end=" ")
                        num += 1
                        if num % 3 == 0: print()
            if num <= 2: print("")
            choice = input("Number>> ")
            if choice == "0": print("You decide to keep your weapon."); break
            if int(choice)-1 <= len(weapons) and inventory[weapons[int(choice)-1][0]][0] >= 1:
                equipped_weapon = weapons[int(choice)-1][0]
                print(f"You changed your weapon to {equipped_weapon}.")
        if choice == "4":
            print("You decide to bury some of your bones, but which one?")
            print(f"[1] You have {inventory['bone'][0]} bone(s).")
            print(f"[2] You have {inventory['big bone'][0]} big bone(s).")
            print(f"[3] You have {inventory['large bone'][0]} large bone(s).")
                
            choice = input("Number>> ")
            if choice == "0": print("You dont want to bury any bones right now."); break
            if choice == "1":
                print("You think about how many you would like to burry...")
                choice = input("NUMBER>> ")
                if int(choice) > 0:
                    if int(choice) <= inventory["bone"][0]:
                        inventory["bone"][0] -= int(choice)
                        skills["prayer"]["xp"] += int(int(choice) * 2)
                        if skills["prayer"]["xp"] > skills["prayer"]["needed"]:
                            skills["prayer"]["xp"] -= skills["prayer"]["needed"]
                            skills["prayer"]["needed"] = xp_for_next_level(skills["prayer"]["lvl"])
                            skills["prayer"]["lvl"] += 1
                            print("You leveled up your prayer!")
                        print("You burried " + str(int(choice)) + " bone(s).")
                    else: print("You don't have that many bone(s) to burry! Go get some!")
            if choice == "2":
                print("You think about how many you would like to burry...")
                choice = input("NUMBER>> ")
                if int(choice) > 0:
                    if int(choice) <= inventory["big bone"][0]:
                        inventory["big bone"][0] -= int(choice)
                        skills["prayer"]["xp"] += int(int(choice) * 4)
                        if skills["prayer"]["xp"] > skills["prayer"]["needed"]:
                            skills["prayer"]["xp"] -= skills["prayer"]["needed"]
                            skills["prayer"]["needed"] = xp_for_next_level(skills["prayer"]["lvl"])
                            skills["prayer"]["lvl"] += 1
                            print("You leveled up your prayer!")
                        print("You burried " + str(int(choice)) + " big bone(s).")
                    else: print("You don't have that many big bone(s) to burry! Go get some!")
            if choice == "3":
                print("You think about how many you would like to burry...")
                choice = input("NUMBER>> ")
                if int(choice) > 0:
                    if int(choice) <= inventory["large bone"][0]:
                        inventory["large bone"][0] -= int(choice)
                        skills["prayer"]["xp"] += int(int(choice) * 10)
                        if skills["prayer"]["xp"] > skills["prayer"]["needed"]:
                            skills["prayer"]["xp"] -= skills["prayer"]["needed"]
                            skills["prayer"]["needed"] = xp_for_next_level(skills["prayer"]["lvl"])
                            skills["prayer"]["lvl"] += 1
                            print("You leveled up your prayer!")
                        print("You burried " + str(int(choice)) + " large bone(s).")
                    else: print("You don't have that many large bone(s) to burry! Go get some!")



        if choice == "3":
            all_food = {"shrimp": 5, "salmon": 8, "light fish": 8, "heavy fish": 10,
                         "pork": 10, "chicken": 15, "steak": 20,
                         "cooked shrimp": 8, "cooked salmon": 12, "cooked light fish": 14, "cooked heavy fish": 18,
                         "cooked pork": 15, "cooked chicken": 20, "cooked steak": 25}
            position = 0
            position_invisible = 0
            for item in all_food.items():
                if inventory[item[0]][0] >= 1:
                    print(f"[{position_invisible}] {item[0]} ({inventory[item[0]][0]})", end=" ")
                    position += 1
                position_invisible += 1
                if position % 4 == 0:
                    print()
            if position < 4:
                print()

            choice = int(input("Number>> "))
            name = list(all_food.keys())[int(choice)]
            if 0 <= choice < len(all_food) and inventory[name][0] >= 1:
                # Get the item and price from the list using the user input as the index
                extra_health = list(all_food.values())[choice]
                inventory[name][0] -= 1
                needs["health"] += extra_health
                print("You earned " + str(extra_health) + " extra health and " + str(int(extra_health*2)) + " hunger.")
                if needs["health"] > 100: needs["health"] = 100
                needs["hunger"] += int(extra_health*2)
                if needs["hunger"] > 1000: needs["hunger"] = 1000
                print("You now have " + str(needs["health"]) + " health. Good job!")

        if choice == "2":
            print("You decide to change your approach to combat.")
            print("[0] ATTACK/Chance to hit")
            print("[1] STRENGTH/Damage done")
            print("[2] BLOCK/Chance to block")
            if choice == "0": attack_mode = 0; print("Your attack mode is changed to ATTACK!")
            if choice == "1": attack_mode = 1; print("Your attack mode is changed to STRENGTH!")
            if choice == "2": attack_mode = 2; print("Your attack mode is changed to BLOCK!")



        if choice == "1":
            os.system("cls")
            enemy["health"] = enemy_health
            enemy["health"] = enemy_health * 2

            if offline_variables["difficulty"]["lvl"] == 0: enemy["health"] = int(enemy["health"] / 1.5); enemy["attack"] = int(enemy["attack"] / 1.5); enemy["strength"] = int(enemy["strength"] / 1.5); enemy["defense"] = int(enemy["defense"] / 1.5); enemy["xp"] = int(enemy["xp"] * 1.5)
            if offline_variables["difficulty"]["lvl"] == 2: enemy["health"] = int(enemy["health"] * 1.5); enemy["attack"] = int(enemy["attack"] * 1.5); enemy["strength"] = int(enemy["strength"] * 1.5); enemy["defense"] = int(enemy["defense"] * 1.5); enemy["xp"] = int(enemy["xp"] * 1.1)
            if offline_variables["difficulty"]["lvl"] == 3: enemy["health"] = int(enemy["health"] * 2); enemy["attack"] = int(enemy["attack"] * 2); enemy["strength"] = int(enemy["strength"] * 2); enemy["defense"] = int(enemy["defense"] * 2); enemy["xp"] = int(enemy["xp"] * 1.2)
            if offline_variables["difficulty"]["lvl"] == 4: enemy["health"] = int(enemy["health"] * 3); enemy["attack"] = int(enemy["attack"] * 3); enemy["strength"] = int(enemy["strength"] * 3); enemy["defense"] = int(enemy["defense"] * 3); enemy["xp"] = int(enemy["xp"] * 1.3)
            if offline_variables["difficulty"]["lvl"] == 5: enemy["health"] = int(enemy["health"] * 3.5); enemy["attack"] = int(enemy["attack"] * 3.5); enemy["strength"] = int(enemy["strength"] * 3.5); enemy["defense"] = int(enemy["defense"] * 3.5); enemy["xp"] = int(enemy["xp"] * 1.4)
            if offline_variables["difficulty"]["lvl"] == 6: enemy["health"] = int(enemy["health"] * 6); enemy["attack"] = int(enemy["attack"] * 6); enemy["strength"] = int(enemy["strength"] * 6); enemy["defense"] = int(enemy["defense"] * 6); enemy["xp"] = int(enemy["xp"] * 1.5)

            chances = {"attack": 0, "block": 0, "strength": 0}
            if attack_mode == 0:
                number0 = 20 - (combat["attack"]["lvl"] / 2)
                if number0 < 0: number0 = 0
                number = int( combat["attack"]["needed"] + number0 )
                chances["attack"] = number
            else:
                # the same but now the number is lower
                number0 = 10 - (combat["attack"]["lvl"] / 2)
                if number0 < 0: number0 = 0
                number = int( combat["attack"]["needed"] + number0 )
                chances["attack"] = number
            
            if attack_mode == 1:
                number0 = 20 - (combat["strength"]["lvl"] / 2)
                if number0 < 0: number0 = 0
                number = int( combat["strength"]["needed"] + number0 )
                chances["strength"] = number
            else:
                number0 = 10 - (combat["strength"]["lvl"] / 2)
                if number0 < 0: number0 = 0
                number = int( combat["strength"]["needed"] + number0 )
                chances["strength"] = number
            
            if attack_mode == 2:
                # now do block which is the 1 in 100 chance to not get hit by an enemy
                number0 = 6 - (combat["defense"]["lvl"] / 2)
                if number0 < 0: number0 = 0
                number = int( combat["defense"]["needed"] + number0 )
                chances["block"] = number
            else:
                number0 = 4 - (combat["defense"]["lvl"] / 2)
                if number0 < 0: number0 = 0
                number = int( combat["defense"]["needed"] + number0 )
                chances["block"] = number

            num = 0
            for i in range(0, len(weapons)):
                if weapons[i][0] == equipped_weapon:
                    num = i
            chances["attack"] += weapons[num][1]
            chances["strength"] += weapons[num][2]
            chances["block"] += weapons[num][3]



            num0 = random.randint(0, 3)
            if num0 == 0:
                print("Another man shows up and asks you to take a gamble for a powerup!")
                print("Do you want to make a gamble for a powerup?")
                print("How about...")
                chance = random.randint(0, 2)
                if chance == 0:
                    print("A 50 50 procent chance that your attack level will get increased by 10 for this battle.")
                    print("But if you lose, i will make your block chance 0%! Y/N?")
                    if input("Y/N>> ").lower() == "y":
                        chance = random.randint(0, 1)
                        if chance == 0:
                            print("Congratulations! Your attack level will get increased by 10 for this battle! Good for you..")
                            chances["attack"] += 10
                        else:
                            print("You lose! Your block chance is now 0%! HA!!")
                            chances["block"] = 0
                    else: print("Fine... ILL GET YOU NEXT TIME!!!")
                if chance == 1:
                    print("A 50 50 procent chance that your block level will get increased by 10 for this battle.")
                    print("But if you lose, i will make your block chance 0%! Y/N?")
                    if input("Y/N>> ").lower() == "y":
                        chance = random.randint(0, 1)
                        if chance == 0:
                            print("Congratulations! Your block level will get increased by 10 for this battle! Good for you..")
                            chances["block"] += 10
                        else:
                            print("You lose! Your block chance is now 0%! HA!!")
                            chances["block"] = 0
                    else: print("Fine... ILL GET YOU NEXT TIME!!!")
                if chance == 2:
                    print("A 50 50 procent chance that your strength level will get increased by 10 for this battle!")
                    print("But if you lose, i will make your block chance 0%! Y/N?")
                    if input("Y/N>> ").lower() == "y":
                        chance = random.randint(0, 1)
                        if chance == 0:
                            print("Congratulations! Your strength level will get increased by 10 for this battle! Good for you..")
                            chances["strength"] += 10
                        else:
                            print("You lose! Your block chance is now 0%! HA!!")
                            chances["block"] = 0
                    else: print("Fine... ILL GET YOU NEXT TIME!!!")
                input("Press enter to continue...")
            if num0 == 1:
                print("Another man shows up and asks you to take a gamble for a powerup!")
                print("He asks you to guess a number between 1 and 100 in 5 tries. He gives you 1 hint every time you guess wrong.")
                print("If you guess the number, you will get an extra 30% attack chance!")
                print("If you lose, you will get a 0% block chance!")
                print("Do you want to take the gamble?")
                if input("Y/N>> ").lower() == "y":
                    # make the minigame
                    number = random.randint(1, 100)
                    tries = 0
                    while tries < 5:
                        tries += 1
                        guess = int(input("Guess a number between 1 and 100>> "))
                        if guess == number:
                            print("Congratulations! You guessed the number! You will get an extra 30% attack chance!")
                            chances["attack"] += 30
                            break
                        else:
                            if guess > number:
                                print("The number is lower than that!")
                            else:
                                print("The number is higher than that!")
                        if tries == 5 and guess != number:
                            print("You lost! You will now get a 0% block chance!")
                            chances["block"] = 0
                else: print("Fine...")




            
            dead = True
            while dead:
                # enemy hits you first
                number = random.randint(0 + (int(enemy["attack"] / 4)), max_lvl + enemy["attack"])
                damage_done = 0
                if number <= enemy["attack"]:
                    # the enemy managed to hit you and will now choose how much damage you took
                    number = random.randint(0, max_lvl)
                    if number <= 30:
                        number1 = random.randint(int(enemy["strength"] / 4) + 1, enemy["strength"])
                        damage_done = number1
                    else:
                        number1 = random.randint(1, int(enemy["strength"] / 2) + 1)
                        damage_done = number1
                    # check if the player blocked the enemy
                    number = random.randint(0, max_lvl+50)
                    if number <= chances["block"]:
                        # only do 50% of the damage to the enemy
                        needs["health"] -= number1 / 2
                        damage_done = number1 / 2
                        if needs["health"] <= 0: dead = False
                if damage_done > 0:
                    print("The enemy hit you for " + str(damage_done) + " damage!")
                else:
                    print("The enemy missed you!")
                damage_done = 0
                # player hits enemy
                number = random.randint(0, max_lvl)
                if number <= chances["attack"]:
                    # the player managed to hit enemy and will now choose how much damage you took
                    number = random.randint(0, max_lvl)
                    if number <= 30:
                        number1 = random.randint(int(chances["strength"] / 2)+1, chances["strength"])
                        damage_done = number1
                    else:
                        number1 = random.randint(1, int(chances["strength"] / 2)+1)
                        damage_done = number1
                    # check if the enemy blocked you
                    number = random.randint(0, max_lvl+50)
                    if number <= chances["block"]:
                        # only do 50% of the damage to the enemy
                        enemy["health"] -= number1 / 2
                        damage_done = number1 / 2
                        if enemy["health"] <= 0: dead = False
                    else:
                        enemy["health"] -= number1 / 2
                        damage_done = number1 / 2
                        if enemy["health"] <= 0: dead = False
                if damage_done > 0:
                    print("You hit the enemy for " + str(damage_done) + " damage!")
                else:
                    print("You missed the enemy!")
            os.system("cls")
            print("")
            if enemy["health"] <= 0:
                print("You won! No sh*t...")
                print("You had " + str(needs["health"]) + " HP left! Very nice.")
                item_gained = ""
                if len(enemy["drops"]) > 0:
                    if random.randint(0, 1) == 0:
                        item_gained = enemy["drops"][random.randint(0, len(enemy["drops"])-1)]
                if not item_gained == "": print("The enemy dropped " + item_gained + "!")
                if not item_gained == "": inventory[item_gained][0] += 1
                offline_variables["kills"][enemy["name"]] += 1
                # add xp
                combat[attack_modes[attack_mode]]["xp"] += enemy["xp"]
                if combat[attack_modes[attack_mode]]["xp"] > combat[attack_modes[attack_mode]]["needed"]:
                    combat[attack_modes[attack_mode]]["xp"] -= combat[attack_modes[attack_mode]]["needed"]
                    combat[attack_modes[attack_mode]]["needed"] = xp_for_next_level(combat[attack_modes[attack_mode]]["lvl"])
                    combat[attack_modes[attack_mode]]["lvl"] += 1
                    print("You leveled up!")
            else:
                print("You lost!")
                print("The enemy had " + str(enemy["health"]) + " HP left! Wow.. ur really bad at this arent you?")
                needs["health"] = 5






def cooking():
    global skills
    os.system("cls")
    all_items = ["shrimp", "salmon", "light fish", "heavy fish", "pork", "chicken", "steak"] # all cookable items
    while True:
        print("You want to do some cooking right now so you do that.")
        print("[0] EXIT")
        print("[1] Cook")
        print("[2] Cookable items in inventory")
        choice = input("NUMBER>> ")
        if choice == "0": print("You leave because you got bored of cooking."); break
        if choice == "2":
            # show all items in inventory that can be cooked in rows of 3 items every row
            os.system("cls")
            print("Cookable items in inventory:")
            for item in all_items:
                if inventory[item][0] > 0:
                    print(item + " x" + str(inventory[item][0]))
            input("Press enter to continue... or dont idc.")
            os.system("cls")
        
        if choice == "1":
            os.system("cls")
            all_items_cooked = ["cooked shrimp", "cooked salmon", "cooked pork", "cooked light fish", "cooked heavy fish", "cooked chicken", "cooked steak"] # all cooked items
            print("You go to your kitchen and start cooking. But what do you want to cook?")
            print("[0] EXIT")
            for i in range(len(all_items)):
                if inventory[all_items[i]][0] > 0:
                    print("[" + str(i+1) + "] " + all_items[i] + " x" + str(inventory[all_items[i]][0]))
            choice = input("NUMBER>> ")
            if choice == "0": pass
            elif inventory[all_items[int(choice)-1]][0] > 0:
                if needs["hunger"] > 3:
                    needs["hunger"] -= 3
                    # make a random number between 0 and 100 and use that as a chance to be successfull in cooking the item based on the player level
                    chance = random.randint(0, 100)
                    cooking_chance = 0 # the number that the chance needs to be lower then to be successfull
                    # Add invisible levels to the cooking chance to make it easyer to cook items on lower levels and make the invisible level lower based on the height of the cooking level
                    cooking_chance = skills["cooking"]["lvl"]
                    if not (30 - (skills["cooking"]["lvl"] / 2)) < 0:
                        cooking_chance += int(30 - (skills["cooking"]["lvl"] / 2))
                    if chance <= cooking_chance:
                        print("You cooked the " + all_items[int(choice)-1] + "!")
                        inventory[all_items[int(choice)-1]][0] -= 1
                        inventory[all_items_cooked[int(choice)-1]][0] += 1
                        skills["cooking"]["xp"] += 5
                        if skills["cooking"]["xp"] >= skills["cooking"]["needed"]:
                            skills["cooking"]["xp"] -= skills["cooking"]["needed"]
                            skills["cooking"]["lvl"] += 1
                            skills["cooking"]["needed"] = xp_for_next_level(skills["cooking"]["lvl"])
                    else:
                        print("You failed to cook the " + all_items[int(choice)-1] + ", you burned it! Go try again, you can do it!")
                        inventory[all_items[int(choice)-1]][0] -= 1
                else: print("You need at least 3 hunger to cook something! Go eat!")
            else: print("You dont have any " + all_items[int(choice)-1] + " in your inventory! Go get some!")

def mining():
    global needs, inventory
    while True:
        if skills["mining"]["xp"] >= skills["mining"]["needed"]:
            skills["mining"]["xp"] -= skills["mining"]["needed"]
            skills["mining"]["lvl"] += 1
            skills["mining"]["needed"] = xp_for_next_level(skills["mining"]["lvl"])
            
        print("You go do some mining and pick what your looking for.")
        print("[0] EXIT")
        print("[1] Rune essence")
        choice = input("NUMBER>> ")
        if choice == "0": print("Nevermind..."); break
        if choice == "1":
            print("You want to mine this for... (5 minutes per 1 rune essence)")
            print("You have " + str(needs["hunger"]) + " hunger left. That should be enough right?")
            choice = input("MINUTES>> ")
            if int(choice) <= needs["hunger"] and int(choice) >= 5:
                needs["hunger"] -= int(choice)
                # every 10 minutes you mine you get 1 rune essence
                inventory["rune essence"][0] += int(int(choice) / 5)
                print("You mined " + str(int(int(choice) / 5)) + " rune essence! Nice job! Its not like its the easyest thing to mine or anything..")
                # add xp and level up if needed
                skills["mining"]["xp"] += int(int(choice) / 5) * 4

def missions():
    while True:
        print("You go do some missions.")
        print("[0] EXIT")
        print("[1] View missions")
        print("[2] What is this?")
        choice = input("NUMBER>> ")
        if choice == "0": break
        if choice == "2":
            os.system("cls")
            print("Missions are not like quests but more like list of things you can do to get rewards.")
            print("Missions are not needed to be done but they can give you rewards.")
            print("Missions are added to add a goal to the game because the game is a bit boring without it.")
        if choice == "1":
            os.system("cls")
            print("Missions:")
            print("[0] EXIT")
            print("[1] Level 1 to 10 missions")
            if offline_variables["mission"]["lvl"] >= 10 and False: print("[2] Level 10 to 20 missions")
            choice = input("NUMBER>> ")
            if choice == "0": pass



            if choice == "1":
                # missions for level 1 to 10
                os.system("cls")
                if offline_variables["mission"]["lvl"] == 0: print("[1] Collect 10 shrimp, gives 50 coins")
                if offline_variables["mission"]["lvl"] == 1: print("[1] Kill 5 chickens, gives 100 cooking XP")
                if offline_variables["mission"]["lvl"] == 2: print("[1] Have 200 coins in your inventory, gives 200 attack XP")
                if offline_variables["mission"]["lvl"] == 3: print("[1] Kill 3 men, gives 200 defense XP")
                if offline_variables["mission"]["lvl"] == 4: print("[1] Kill 1 of scarr's minions, gives 200 strength XP")
                if offline_variables["mission"]["lvl"] == 5: print("[1] Kill 4 of scarr's minions, gives 400 defense XP")
                if offline_variables["mission"]["lvl"] == 6: print("[1] Collect 2 heavy fish, gives 200 fishing XP")
                if offline_variables["mission"]["lvl"] == 7: print("[1] Kill 1 of scarr's weak bodyguards, gives 1000 attack XP")
                if offline_variables["mission"]["lvl"] == 8: print("[1] Kill a fox, gives 1 silver dagger")
                if offline_variables["mission"]["lvl"] == 9: print("[1] Kill 8 foxes, gives 400 defense XP, 400 strength XP and 400 attack XP")
                choice = input("NUMBER>> ")
                if choice == "1" and offline_variables["mission"]["lvl"] == 0:
                    if inventory["shrimp"][0] >= 10: money += 50; offline_variables["mission"]["lvl"] += 1; print("You got your reward! Just like promised.")
                    else: print("You dont have 10 shrimp in your inventory!")
                if choice == "1" and offline_variables["mission"]["lvl"] == 1:
                    if offline_variables["kills"]["chicken"] >= 5: skills["cooking"]["xp"] += 100; offline_variables["mission"]["lvl"] += 1; print("You got your reward! You happy now?")
                    else: print("You havent killed 5 chickens! What are you doing?? Go kill some!")
                if choice == "1" and offline_variables["mission"]["lvl"] == 2:
                    if inventory["coins"][0] >= 200: combat["attack"]["xp"] += 200; offline_variables["mission"]["lvl"] += 1; print("You got your reward! You should be happy now.")
                    else: print("You dont have 200 coins in your inventory! Go get some!")
                if choice == "1" and offline_variables["mission"]["lvl"] == 3:
                    if offline_variables["kills"]["man"] >= 3: skills["defense"]["xp"] += 200; offline_variables["mission"]["lvl"] += 1; print("You got your reward! Be happy about it.")
                    else: print("You havent killed 3 men! Serious? Go kill some!")
                if choice == "1" and offline_variables["mission"]["lvl"] == 4:
                    if offline_variables["kills"]["scarr's minion"] >= 1: combat["strength"]["xp"] += 200; offline_variables["mission"]["lvl"] += 1; print("You got your reward! You get the drill..")
                    else: print("You havent killed 1 of scarr's minions! Booooo!")
                if choice == "1" and offline_variables["mission"]["lvl"] == 5:
                    if offline_variables["kills"]["scarr's minion"] >= 4: combat["defense"]["xp"] += 400; offline_variables["mission"]["lvl"] += 1; print("You got your reward! You get the drill..")
                    else: print("You havent killed 4 of scarr's minions! Booooo!")
                if choice == "1" and offline_variables["mission"]["lvl"] == 6:
                    if inventory["heavy fish"][0] >= 2: skills["fishing"]["xp"] += 200; offline_variables["mission"]["lvl"] += 1; print("You got your reward! You get the drill..")
                    else: print("You dont have 2 heavy fish in your inventory! Go get some!")
                if choice == "1" and offline_variables["mission"]["lvl"] == 7:
                    if offline_variables["kills"]["scarr's weak bodyguard"] >= 1: combat["attack"]["xp"] += 1000; offline_variables["mission"]["lvl"] += 1; print("You got your reward! You get the drill..")
                    else: print("You havent killed 1 of scarr's weak bodyguards! Booooo!")
                if choice == "1" and offline_variables["mission"]["lvl"] == 8:
                    if offline_variables["kills"]["fox"] >= 1: inventory["silver dagger"][0] += 1; offline_variables["mission"]["lvl"] += 1; print("You got your reward! You get the drill..")
                    else: print("You havent killed a fox! Booooo!")
                if choice == "1" and offline_variables["mission"]["lvl"] == 9:
                    if offline_variables["kills"]["fox"] >= 8: combat["defense"]["xp"] += 400; combat["strength"]["xp"] += 400; combat["attack"]["xp"] += 400; offline_variables["mission"]["lvl"] += 1; print("You got your reward! You get the drill..")
                    else: print("You havent killed 8 foxes! Booooo!")
            
            if choice == "2":
                # missions for 11 to 20
                pass

def prayer():
    print("Welcome to the prayer menu.")
    while True:
        print("[0] EXIT")
        choice = input("NUMBER>> ")
        if choice == "0": break

menu()