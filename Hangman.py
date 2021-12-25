import random
from phases import hang_phases


class HangManData:
    def __init__(self, word):
        self.word = word
        self.guesses = []
        self._hits = []
        self._misses = []
        self._appearances = 0

    def add_guess(self, letter):
        if letter in self.guesses:
            return False
        else:
            self.guesses.append(letter)
            self._appearances = self.word.count(letter)

            xs = self._hits if self.appearances > 0 else self._misses
            xs.append(letter)
            xs.sort()
            return True

    @property
    def is_invalid(self):
        return self.word == ""

    @property
    def appearances(self):
        return self._appearances

    @property
    def hits(self):
        return self._hits

    @property
    def misses(self):
        return self._misses

    @property
    def remaining_chances(self):
        return 9 - len(self._misses)

    @property
    def is_dead(self):
        return self.remaining_chances <= 0

    @property
    def is_solved(self):
        return all(letter in self._hits for letter in self.word)

    @property
    def diagram(self):
        return hang_phases[self.remaining_chances]

    @property
    def display_word(self):
        return ' '.join(
            letter if letter in self._hits else '_'
            for letter in self.word
        )


class UI:
    def __init__(self):
        self.word_list = open('Words').read().split("\n")
        self.word = random.choice(self.word_list).upper()

    @staticmethod
    def display(hm):
        # print(hm.word)
        print(hm.diagram)
        print(hm.display_word)
        print(f"Incorrect Letters Guessed {hm.misses}")

    def generate_word(self):
        return self.word

    def play(self):
        hm = HangManData(self.generate_word())
        while True:
            self.display(hm)
            if hm.is_invalid:
                print("Invalid Word Was Generated")
                break
            elif hm.is_solved:
                print("Congrats!")
                break
            elif hm.is_dead:
                print(f"The Word Was {hm.word}")
                break
            else:
                guessed_letter = input("Guess A Letter: ").upper()
                if guessed_letter == hm.word:
                    print("Congrats!")
                    break
                else:
                    check_added = hm.add_guess(guessed_letter)
                    if guessed_letter == "QUIT":
                        print(f"The Word Was {hm.word}")
                        break
                    elif not check_added:
                        print("You Already Guessed This Letter")
                    else:
                        if hm.appearances == 1:
                            print(f"{guessed_letter} Appears Once In The Word")
                        else:
                            print(f"{guessed_letter} Appears {hm.appearances} Times In The Word")


def main():
    play = True
    while play:
        u = UI()
        u.play()
        while True:
            print("Play Again?")
            play_again = input("Y/n > ").upper()
            if play_again == "Y":
                print("Setting Up...")
                break
            elif play_again == "N":
                print("Goodbye")
                play = False
                break
            else:
                print("Invalid Input")


if __name__ == "__main__":
    main()
