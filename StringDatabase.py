import random

class StringDatabase:
    def __init__(self, file_path="four_letters.txt"):
        # Load all valid 4-letter words from the provided file
        self.words = []
        with open(file_path, "r") as file:
            for line in file:
                # Split each line into individual words (in case they’re space-separated)
                for raw_word in line.strip().split():
                    candidate = raw_word.lower()
                    if len(candidate) == 4:
                        self.words.append(candidate)

    def get_random_word(self):
        # Pick a random 4-letter word from the loaded list
        return random.choice(self.words)
