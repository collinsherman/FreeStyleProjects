"""
Program: Sprint Generator
Author: Collin Sherman
"""

import random

# Choose desired number of sprints
NUMSPRINTS = 16

class SprintGenerator():
    """Generates specified number of sprints according to percentiles."""


    def run(self):
        """Initializes counters and runs loop, calling methods based on randomly drawn number to return sprint lengths"""

        count = 1
        noCount = 0
        shortCount = 0
        medCount = 0
        longCount = 0
        hugeCount = 0
        total = 0

        print("Sprint Generator will print", NUMSPRINTS, "sprints randomly. "\
              "Get ready to work!\n")

        while NUMSPRINTS >= count:
            randomNum = random.randint(1, 100)
            if 1 <= randomNum <= 5:
                length = self.noGain()
                noCount += 1
            elif 6 <= randomNum <= 55:
                length = self.shortGain(randomNum)
                shortCount += 1
            elif 56 <= randomNum <= 85:
                length = self.mediumGain(randomNum)
                medCount += 1
            elif 86 <= randomNum <= 95:
                length = self.longGain(randomNum)
                longCount += 1
            else:
                length = self.hugeGain(randomNum)
                hugeCount += 1

            print("%d. %d" %(count, length))
            count += 1
            total += length

        print("\nNo Gain: %d\nShort Gain: %d\nMedium Gain: %d\nLong Gain: %d\nHuge Gain: %d" %(noCount, shortCount, medCount, longCount, hugeCount))

        return total
            
    def noGain(self):
        """Gain of zero; 5% chance"""

        return 0

    def shortGain(self, num):
        """Gain of 5, 10, 15, or 20; 50% chance"""
        
        if 6 <= num <= 17: return 5
        elif 18 <= num <= 29: return 10
        elif 30 <= num <= 42: return 15
        else: return 20 

    def mediumGain(self, num):
        """Gain of 30 or 40; 30% chance"""

        if 56 <= num <= 70: return 30
        else: return 40

    def longGain(self, num):
        """Gain of 50 or 60; 10% chance"""

        if 86 <= num <= 90: return 50
        else: return 60

    def hugeGain(self, num):
        """Gain of 70, 80, 90, or 100; 5% chance"""

        if num == 96: return 70
        elif num == 97: return 80
        elif num == 98: return 90
        else: return 100

def main():
    generator = SprintGenerator()
    generator.run()

if __name__ == "__main__":
    main()
    