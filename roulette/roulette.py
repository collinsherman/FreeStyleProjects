import random
import time
import sys

RED = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
BLACK = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
GREEN = [0, 37]     # 37 stands in for 00

FIR_COL = [1,4,7,10,13,16,19,22,25,28,31,34]
SEC_COL = [2,5,8,11,14,17,20,23,26,29,32,35]
THR_COL = [3,6,9,12,15,18,21,24,27,30,33,36]

CHOICES = ['red', 'black', 'green', 'even', 'odd', 'low', 'high', '1col', '2col', '3col', '1doz', '2doz', '3doz', '00']
for x in range(37):
    CHOICES.append(str(x))

PAY_DICT = {'Red':1, 'Black':1, 'Green':17, 'Even':1, 'Odd':1, 'First Column':2, 'Second Column':2,
                'Third Column':2, 'First Dozen':2, 'Second Dozen':2, 'Third Dozen':2, 'Low':1, 'High':1}

class RouletteTable:
    def __init__(self, wager, purse, min_bet, bet):
        self.wager = None
        self.purse = 100
        self.min_bet = 15
        self.bet = []

    def start(self):
        print("\n\nWelcome to our casino!  Join us at the roulette table!")
        play = True
        replay = False
        while play == True:
            print("Looks like you have $%s. The minimum bet is currently $%s." %(self.purse, self.min_bet))
            
            # Create wager
            security = 0
            while True:
                try:
                    self.wager = int(input("\nWhat would you like to wager per chip? $"))
                    if self.wager >= self.min_bet and self.wager <= self.purse:
                        break
                    else:
                        self.wager = int("break")
                except ValueError:
                    if security == 4:
                        self.security()
                    print("Please, enter a positive integer less than your current purse of $%s and more than the minimum bet of $%s." %(self.purse, self.min_bet))
                    security += 1
                    
            num_bets = self.purse // self.wager
            if num_bets == 1:
                print("Great! $%s for a single chip.\n" %self.wager)
            else:
                print("Great! $%s per chip it is. You can place a maximum of %s bets.\n" %(self.wager, num_bets))
            
            print("_/\_"*28)
            time.sleep(1)
            
            self.bet.clear()
            print("\nWhat would you like to bet on?")
            print("\tYour choices are red, black, green (0 and 00), even, odd, low, or high.") 
            print("\tYou can also choose the first, second, or third column or dozen (type '1col', '2col', etc.") 
            print("\tor '3doz', etc.). Or you can pick and choose specific numbers 0-36 or 00.  Up to you!\n")    
            
            print("_/\_"*28)
            time.sleep(1)
            
            fin = False
            while fin != True:
                security = 0
                while True:
                    choice = input("\nSo, what will it be? One at at time, please (type your choice as specified above or 'help' for rules): ").lower().strip().replace(" ", "")
                    if choice == "help":
                        self.help()
                    elif choice in CHOICES:
                        self.bet.append(choice)
                        break
                    elif security == 4:
                        self.security()
                    else:
                        print("Invalid choice. Please choose one of the listed choices above.")
                        security += 1
                        
                num_bets -= 1
                print("Great! You bet on %s." %choice)
                if num_bets == 0:
                    print("\nLooks like that's the most chips you can put down this hand.")
                    fin = True
                else:
                    security = 0
                    while True:
                        more = input("\nChips left: %s. Anything else (y/n)? " %num_bets).lower().strip()
                        if more == "n":
                            fin = True
                            break
                        elif more == "y":
                            break
                        elif security == 4:
                            self.security()
                        else:
                            print("Please use either 'y' or 'n'.")
                            security += 1
                            
            result = self.roll()
            mult = len(self.bet)
            deficit = mult*self.wager
            self.purse -= deficit  
            
            print("\nRisking $%s! Here we go!" %deficit)
            
            result = self.roll()
            fate = self.win_lose(result, self.bet)
            
            timer = 0
            print("Spinning", end="", flush=True)
            while timer < 4:
                time.sleep(1)
                print(".", end="", flush=True)
                timer += 1
                
            if result == 37:
                print(" and... it's 00!\n")
            else:
                print(" and... it's %s!\n" %result)
            
            time.sleep(1)
            
            if len(fate) > 0:
                if len(fate) == 1:
                    print("Congratulations! Your bet on %s won!" %fate[0])
                    self.purse += (self.payouts(fate[0]) + self.wager)
                    print("And even better, you won $%s and now have $%s! Wow!" %(self.payouts(fate[0]), self.purse))
                else:
                    print("Congratulations! You won on these bets:")
                    takings = 0
                    for x in fate:
                        print(x)
                        self.purse += self.wager
                        takings += self.payouts(x)
                    self.purse += takings
                    print("And even better, you won $%s and now have $%s! Wow!" %(takings, self.purse))
                
            else:
                print("Sorry, you weren't so lucky this time. You lost $%s and now have $%s." %(deficit, self.purse))
                
            if self.purse < self.min_bet:
                play = False
                if self.purse == 0:
                        print("The house always wins...")
            else:    
                security = 0
                while True:
                    restart = input("\nWould you like to keep playing (y/n)? ").lower().strip()
                    if restart == "n":
                        play = False
                        print("\n\nSorry to see you go! You ended up with $%s! Not too shabby! Come back any time.\n" %self.purse)
                        break
                    elif restart == "y":
                        print("Awesome!\n")
                        replay = True
                        print("_/\_"*28)
                        print()
                        break
                    elif security == 4:
                        self.security()
                    else:
                        print("Please use either 'y' or 'n'.")
                        security += 1
        
    def wage(self):
        security = 0
        while True:
            try:
                self.wager = int(input("\nWhat would you like to wager per chip? $"))
                if self.wager >= 1 and self.wager <= self.purse:
                    break
                else:
                    self.wager = int("break")
            except ValueError:
                if security == 4:
                    self.security()
                print("Please, enter a positive number less than your current purse of $%s and more than the minimum bet of $%s." %(self.purse, self.min_bet))
                security += 1        
                
    def place_bet(self, bets):
        print("\nWhat would you like to bet on?")
        print("\tYour choices are red, black, green (0 and 00), even, odd, low, or high.") 
        print("\tYou can also choose the first, second, or third column or dozen (type '1col', '2col', etc.") 
        print("\tor '3doz', etc.). Or you can pick and choose specific numbers 0-36 or 00.  Up to you!\n")
        fin = False
        while fin != True:
            security = 0
            while True:
                choice = input("\nSo, what will it be? One at at time, please (type your choice as specified above or 'help' for rules): ").lower().strip().replace(" ", "")
                if choice == "help":
                    self.help()
                elif choice in CHOICES:
                    self.bet.append(choice)
                    break
                elif security == 4:
                    self.security()
                else:
                    print("Invalid choice. Please choose one of the listed choices above.")
                    security += 1
                    
            bets -= 1
            print("Great! You bet on %s." %choice)
            if bets == 0:
                print("\nLooks like that's the most chips you can put down this hand.")
                fin = True
            else:
                security = 0
                while True:
                    more = input("\nChips left: %s. Anything else (y/n)? " %bets).lower().strip()
                    if more == "n":
                        fin = True
                        return
                    elif more == "y":
                        break
                    elif security == 4:
                        self.security()
                    else:
                        print("Please use either 'y' or 'n'.")
                        security += 1
        
    def roll(self):
        result = random.randint(0, 37)
        return result
        
    def win_lose(self, result, bet):
        winner = []
        for x in bet:
            if len(x) > 2:
                if x == "red":
                    if result in RED:
                        winner.append("Red")
                elif x == "black":
                    if result in BLACK:
                        winner.append("Black")
                elif x == "green":
                    if result in GREEN:
                        winner.append("Green")
                elif x == "even":
                    if (result  % 2) == 0:
                        winner.append("Even")
                elif x == "odd":
                    if result  % 2 != 0:
                        winner.append("Odd")
                elif x == "1col":
                    if result in FIR_COL:
                        winner.append("First Column")
                elif x == "2col":
                    if result in SEC_COL:
                        winner.append("Second Column")
                elif x == "3col":
                    if result in THR_COL:
                        winner.append("Third Column")
                elif x == "1doz":
                    if 0 < result < 13:
                        winner.append("First Dozen")
                elif x == "2doz":
                    if 12 < result < 25:
                        winner.append("Second Dozen")
                elif x == "3doz":
                    if 24 < result < 37:
                        winner.append("Third Dozen")
                elif x == "low":
                    if 0 < result < 19:
                        winner.append("Low")
                else:
                    if 18 < result < 37:
                        winner.append("High")
                
            else:
                if (x == "00" and result == 37) or int(x) == result:
                    winner.append(x)

        return winner
    
    def payouts(self, bet):
        pay = 0
        if bet in PAY_DICT:
            pay += (self.wager * PAY_DICT[bet])
        else:
            pay += (self.wager * 35)
        return pay
        
    def help(self):
        f = open('help.txt', "r")
        print(f.read())
        f.close()

    def security(self):
        sys.exit("\nSecurity! Escort this person out please! They can't seem to follow the rules...")

def main():
    roulette = RouletteTable(None, None, None, None)
    roulette.start()
    
if __name__ == "__main__":
    main()
    