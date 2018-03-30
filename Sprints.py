"""
Program: Sprint Generator
Author: Collin Sherman
"""

import random

NUMSPRINTS = 8

class SprintGenerator():
    """Generates specified number of sprints according to percentiles."""
    def run(self):
        reps = NUMSPRINTS
        count = 1
        noCount = 0
        shortCount = 0
        medCount = 0
        longCount = 0
        hugeCount = 0
        total = 0
        print("Sprint Generator will print", reps, "sprints randomly. "\
              "Get ready to work!\n")
        while reps != 0:
            num = random.randint(1, 100)
            if 1 <= num <= 5:
                num = self.noGain()
                noCount += 1
            elif 6 <= num <= 55:
                num = self.shortGain()
                shortCount += 1
            elif 56 <= num <= 75:
                num = self.mediumGain()
                medCount += 1
            elif 76 <= num <= 90:
                num = self.longGain()
                longCount += 1
            else:
                num = self.hugeGain()
                hugeCount += 1
            print(str(count) + ".", str(num))
            count += 1
            reps -= 1
            total += num
        print("\nNo Gain:", str(noCount), "\nShort Gain:",
              str(shortCount), "\nMedium Gain:", str(medCount),
              "\nLong Gain:", str(longCount), "\nHuge Gain:",
              str(hugeCount), "\n\nTotal Yards:", str(total))
            
    def noGain(self):
        """Gain of zero; 5% chance"""
        return 0

    def shortGain(self):
        """Gain of 5, 10, 15, or 20; 50% chance"""
        num = random.randint(1, 4)
        if num == 1: return 5
        if num == 2: return 10
        if num == 3: return 15
        if num == 4: return 20

    def mediumGain(self):
        """Gain of 30 or 40; 20% chance"""
        num = random.randint(1, 2)
        if num == 1: return 30
        if num == 2: return 40

    def longGain(self):
        """Gain of 50 or 60; 15% chance"""
        num = random.randint(1, 2)
        if num == 1: return 50
        if num == 2: return 60

    def hugeGain(self):
        """Gain of 70, 80, 90, or 100; 10% chance"""
        num = random.randint(1, 4)
        if num == 1: return 70
        if num == 2: return 80
        if num == 3: return 90
        if num == 4: return 100


def main():
    generator = SprintGenerator()
    generator.run()

if __name__ == "__main__":
    main()






        
