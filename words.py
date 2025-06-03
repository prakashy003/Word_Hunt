import sys
from Guess import Guess

def main():
    # Check if the mode argument is correctly provided
    if len(sys.argv) != 2 or sys.argv[1] not in ["play", "test"]:
        print("Usage: python3 words.py [play|test]")
        sys.exit(1)

    # Either 'play' (normal mode) or 'test' (shows the word for debugging)
    mode_selected = sys.argv[1]

    # Create a new guessing game session
    game_runner = Guess(mode_selected)

    # Start the game loop
    game_runner.play_game()

# This ensures main() runs only when this file is executed directly
if __name__ == "__main__":
    main()
