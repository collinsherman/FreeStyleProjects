import random
import time
import sys
import getpass

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
    def __init__(self):
        self.wager = 0
        self.purse = 0
        self.starting = 0
        self.min_bet = 1
        self.bet = []
        self.automated = False
        self.num_automate = 100

    def start(self):
        if len(sys.argv) > 1:
            self.automate()
        print("\n\nWelcome to our casino!  Join us at the roulette table!")
        self.purse = self.set_purse()
        self.starting = self.purse
        play = True
        replay = False
        while play == True:
            if replay == True:
                print("You currently have $%s." %self.purse)
            self.wage()
            num_bets = self.purse // self.wager
            if num_bets == 1:
                print("Great! $%s for a single chip.\n" %self.wager)
            else:
                print("Great! $%s per chip it is. You can place a maximum of %s bets.\n" %(self.wager, num_bets))
            self.sleeper()
            
            if replay == True and len(self.bet) <= num_bets:
                self.same_bet(num_bets)
            else:
                self.bet.clear()
                self.place_bet(num_bets)

            result = self.roll()
            mult = len(self.bet)
            deficit = mult*self.wager
            self.purse -= deficit  
            
            if len(self.bet) > 1:
                print("\nRisking $%s with %s bets! Here we go!" %(deficit, len(self.bet)))
            else:
                print("\nRisking $%s with 1 bet! Here we go!" %deficit)
            fate = self.win_lose(result, self.bet)
            self.spin()
            if result == 37:
                print(" and... it's 00!\n")
            else:
                print(" and... it's %s!\n" %result)
            time.sleep(1)
            
            self.determine(fate, deficit)
            
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
        
    def set_purse(self):
        security = 0
        while True:
            try:
                purse = int(input("\nHow much money are you bringing to the table? $"))
                if purse >= 1:
                    break
                else:
                    self.wager = int("break")
            except ValueError:
                if security == 4:
                    self.security()
                print("Please, enter a positive integer more than the minimum chip value of $%s." %self.min_bet)
                security += 1 
        return purse
        
    def wage(self):
        security = 0
        while True:
            try:
                self.wager = int(input("\nWhat would you like to wager per chip? The minimum chip value is $%s: $" %self.min_bet))
                if self.wager == 1365:
                    self.automate()
                elif self.wager >= 1 and self.wager <= self.purse:
                    break
                else:
                    self.wager = int("break")
            except ValueError:
                if security == 4:
                    self.security()
                print("Please, enter a positive number less than your current purse of $%s and more than the minimum bet of $%s." %(self.purse, self.min_bet))
                security += 1        
                
    
    def same_bet(self, bets):
        security = 0
        while True:
            same = input("\nWould you like to place the same bet as your last hand (y/n)? ").lower().strip()
            if same == 'y':
                print()
                self.sleeper()
                break
            elif same == 'n':
                self.bet.clear()
                self.place_bet(bets)
                break
            elif security == 4:
                self.security()
            else:
                print("Invalid choice. Please choose one of the listed choices above.")
                security += 1
        
    def place_bet(self, bets):
        print("\nWhat would you like to bet on?")
        print("\tYour choices are red, black, green (0 and 00), even, odd, low, or high.") 
        print("\tYou can also choose the first, second, or third column or dozen (type '1col', '2col', etc.") 
        print("\tor '3doz', etc.). Or you can pick and choose specific numbers 0-36 or 00.  Up to you!\n")
        
        self.sleeper()
        
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
    
    def spin(self):
        timer = 0
        print("Spinning", end="", flush=True)
        while timer < 4:
            time.sleep(1)
            print(".", end="", flush=True)
            timer += 1
            
    def determine(self, fate, deficit):
        if self.automated == True:
            if len(fate) > 0:
                if len(fate) == 1:
                    self.purse += self.wager
                    deficit -= self.wager
                    takings = self.payouts(fate[0])
                else:
                    takings = 0
                    for x in fate:
                        self.purse += self.wager
                        deficit -= self.wager
                        takings += self.payouts(x)
                self.purse += takings
                print("Won $%s; Purse: $%s" %((takings - deficit), self.purse))
            else:
                print("\tLost $%s; Purse: $%s" %(deficit, self.purse))
        else:
            starting = self.purse + deficit
            if len(fate) > 0:
                if len(fate) == 1:
                    print("Congratulations! Your bet on %s won!" %fate[0])
                    self.purse += (self.payouts(fate[0]) + self.wager)
                else:
                    print("Congratulations! You won on these bets:")
                    takings = 0
                    for x in fate:
                        print(x)
                        self.purse += self.wager
                        takings += self.payouts(x)
                    self.purse += takings
                if starting > self.purse:
                    print("Unfortunately, you still lost $%s and now have $%s." %((starting - self.purse), self.purse))
                elif starting == self.purse:
                    print("You stayed even and now have $%s." %self.purse)
                else:
                    print("And even better, you won $%s and now have $%s! Wow!" %((self.purse - starting), self.purse))
                    
            else:
                print("Sorry, you weren't so lucky this time. You lost $%s and now have $%s." %(deficit, self.purse))

    
    def payouts(self, bet):
        pay = 0
        if bet in PAY_DICT:
            pay += (self.wager * PAY_DICT[bet])
        else:
            pay += (self.wager * 35)
        return pay

    def sleeper(self):
        print("_/\_"*28)
        time.sleep(1)
        
    def help(self):
        f = open('help.txt', "r")
        print(f.read())
        f.close()

    def security(self):
        sys.exit("\nSecurity! Escort this person out please! They can't seem to follow the rules...")

    def automate(self):
        # sentinel = getpass.getpass(prompt="Password: ")
        # if sentinel.lower().replace(" ", "") != "thisistheway":
        #     sys.exit("Intruder detected.")
        self.automated = True
        self.purse = int(sys.argv[1])
        self.starting = self.purse
        self.wager = int(sys.argv[2])
        num_bets = self.purse // self.wager
        self.bet.append(sys.argv[3])
        if len(sys.argv) > 4:
            for x in range(4, len(sys.argv)):
                self.bet.append(sys.argv[x])
        hands = self.num_automate
        max_winnings = 0
        while hands != 0:
            result = self.roll()
            mult = len(self.bet)
            deficit = mult*self.wager
            self.purse -= deficit 
            fate = self.win_lose(result, self.bet)
            self.determine(fate, deficit)
            if self.purse - self.starting > max_winnings:
                max_winnings = self.purse - self.starting
            hands -= 1
        
            
        aftermath = "\n\nBet %s on %s hands\n\tStarting: $%s\n\tFinal: $%s\n\tHighest winnings: $%s" %(self.bet, self.num_automate, self.starting, self.purse, max_winnings)
        f = open("automation.txt", "a")
        f.write(aftermath)
        f.close()
        sys.exit("\nWinnings after %s hands: $%s; highest winnings: $%s" %(self.num_automate, (self.purse - self.starting), max_winnings))


def main():
    roulette = RouletteTable()
    roulette.start()
    
if __name__ == "__main__":
    main()
    