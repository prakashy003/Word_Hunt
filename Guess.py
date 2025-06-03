import os
import random
from StringDatabase import StringDatabase
from Game import Game

# English letter frequency table — used for calculating scores
LETTER_FREQUENCY = {
    'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23,
    'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03,
    'm': 2.41, 'n': 6.75, 'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99,
    's': 6.33, 't': 9.06, 'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15,
    'y': 1.97, 'z': 0.07
}

class Guess:
    def __init__(self, mode):
        self.mode = mode  # Either 'play' or 'test' mode
        self.database = StringDatabase("four_letters.txt")  # Load words from file
        self.completed_games = []  # Keep track of all finished games

    def clear_screen(self):
        # Clear terminal screen (cross-platform)
        os.system('cls' if os.name == 'nt' else 'clear')

    def play_game(self):
        # This is the main game loop — player can play multiple rounds
        while True:
            selected_word = self.database.get_random_word()
            game_instance = Game(selected_word)
            did_play = self.run_single_game(game_instance)
            if did_play:
                self.completed_games.append(game_instance)
            if not self.prompt_continue():
                self.clear_screen()
                self.display_report()
                break

    def run_single_game(self, game):
        # One complete round of guessing for a single word
        current_guess = ["-"] * 4  # Displayed to the user
        attempted_letters = []     # All letters guessed so far
        wrong_word_guesses = 0     # Count of incorrect full word guesses
        user_made_move = False     # Tracks if user interacted at all

        while True:
            self.clear_screen()
            print("╔══════════════════════════════════════════════╗")
            print("║         🎯 THE GREAT GUESSING GAME 🎯        ║")
            print("╚══════════════════════════════════════════════╝\n")

            if self.mode == "test":
                print(f"🔍 [TEST MODE] Word to guess:  {game.word}\n")

            print("🧩 Current Guess : ", " ".join(current_guess))
            print("🔡 Letters Guessed: ", " ".join(attempted_letters) if attempted_letters else "(none)")
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

            print("🔘 Options:")
            print("   [g] Guess the full word")
            print("   [t] Give up and reveal the word")
            print("   [l] Guess a letter")
            print("   [q] Quit the game")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

            option = input("🔎 Enter Option: ").strip().lower()


            # Full word guess
            if option == 'g':
                full_word_guess = input("\nMake your guess: ").strip().lower()
                user_made_move = True
                if full_word_guess == game.word:
                    print("\n✅ Great job! You guessed the word correctly!")
                    game.set_result("Success", wrong_word_guesses, current_guess, attempted_letters)
                    game.score = self.calculate_score(game)
                    input("\nPress any key to continue...")
                    return True
                else:
                    print("\n❌ Incorrect guess. Try again!")
                    wrong_word_guesses += 1

            # Give up — player gives up immediately
            elif option == 't':
                user_made_move = True
                print("\n╔" + "═" * 50 + "╗")
                print("║{:^49}║".format("😞 You gave up..."))
                print("╚" + "═" * 50 + "╝")
                print(f"\n💡 The correct word was: '{game.word}'")

                game.set_result("Gave up", wrong_word_guesses, current_guess, attempted_letters)
                game.score = self.calculate_score(game)
                input("\nPress any key to continue...")
                return True

            # Guess a letter
            elif option == 'l':
                letter_input = input("\nEnter a letter: ").strip().lower()
                user_made_move = True
                if len(letter_input) != 1 or not letter_input.isalpha() or letter_input in attempted_letters:
                    print("\n⚠️ Invalid input!")
                    print("Please enter a **new** single alphabetic letter.")

                else:
                    attempted_letters.append(letter_input)
                    match_count = 0
                    for i, ch in enumerate(game.word):
                        if ch == letter_input:
                            current_guess[i] = ch
                            match_count += 1
                    if match_count > 0:
                        print("\n🎉 Correct!")
                        print(f"✔️  You found {match_count} matching letter(s)!")


                    else:
                        print("\n❌ Oops!")
                        print("That letter isn't in the word. Try again!")


                    # Word completely revealed — auto win
                    if "".join(current_guess) == game.word:
                        game.set_result("Success", wrong_word_guesses, current_guess, attempted_letters)
                        game.score = self.calculate_score(game)
                        input("\nPress any key to continue...")
                        return True

            # Quit mid-game — if user made a move, mark as failed
            elif option == 'q':
                if user_made_move:
                    game.set_result("Failed", wrong_word_guesses, current_guess, attempted_letters)
                    game.score = 0.00
                    return True
                return False

            else:
                print("\n🚫 Invalid Option Selected!")
                print("Please enter one of: [g], [t], [l], or [q]")



            input("\nPress any key to continue...")

    def calculate_score(self, game):
        # Score calculation is based on game outcome and user actions
        unrevealed_letters = [c for i, c in enumerate(game.word) if game.displayed_word[i] == '-']
        unrevealed_total = sum(LETTER_FREQUENCY[c] for c in unrevealed_letters)
        missed_letters = sum(1 for letter in game.guessed_letters if letter not in game.word)
        wrong_guesses = game.bad_guesses

        if game.status == "Success":
            if missed_letters == 0:
                # Perfect game — guessed directly without wrong letters
                penalty_factor = 1 - (0.1 * wrong_guesses)
                score = unrevealed_total * penalty_factor
                return round(max(0.0, score), 2)
            base_score = unrevealed_total / missed_letters
            penalty_factor = 1 - (0.1 * wrong_guesses)
            final_score = base_score * penalty_factor
            return round(max(0.0, final_score), 2)

        elif game.status == "Gave up":
            # Give up — lose points for remaining letters
            return round(-unrevealed_total, 2)

        return 0.0

    def prompt_continue(self):
        # Ask if user wants to play again
        print("\n🔄 Would you like to play another round?")
        user_input = input("➡️  Enter [y] for yes or [n] for no: ").strip().lower()

        return user_input == 'y'

    def display_report(self):
        # Nicely formatted game summary at the end
        print("╔══════════════════════════════════════╗")
        print("║            📝 GAME REPORT            ║")
        print("╚══════════════════════════════════════╝\n")

        print(f"{'Game':<6}{'Word':<10}{'Status':<12}{'Bad Guesses':<15}{'Missed Letters':<17}{'Score':<10}")
        print("-" * 70)

        total_score = 0
        for idx, game in enumerate(self.completed_games, 1):
            missed_count = game.missed_letters()
            print(f"{idx:<6}{game.word:<10}{game.status:<12}{game.bad_guesses:<15}{missed_count:<17}{game.score:.2f}")
            total_score += game.score
        print(f"\nFinal Score: {total_score:.2f}")
