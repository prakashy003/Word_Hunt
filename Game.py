class Game:
    def __init__(self, word):
        # The actual word the player needs to guess
        self.word = word

        # Outcome of the game: "Success", "Failed", or "Gave up"
        self.status = ""

        # Number of times the player guessed the full word incorrectly
        self.bad_guesses = 0

        # List of letters the player tried using the 'l' option
        self.guessed_letters = []

        # The masked version of the word shown to the player (e.g., ['a', '-', '-', '-'])
        self.displayed_word = ["-"] * 4

        # Final score for this round (calculated at the end)
        self.score = 0.0

    def set_result(self, status, bad_guesses, current_display, guessed_letters):
        # Update the game state with final outcome details
        self.status = status
        self.bad_guesses = bad_guesses
        self.displayed_word = current_display
        self.guessed_letters = guessed_letters

    def missed_letters(self):
        # Count how many letters the player guessed that were *not* in the word
        return sum(1 for letter in self.guessed_letters if letter not in self.word)
