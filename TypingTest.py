import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    """
    Displays the welcome screen and waits for a key press to start the game.
    """
    stdscr.clear()  # Clear the screen
    stdscr.addstr("Welcome to the Typing Test!")  # Display welcome message
    stdscr.addstr("\nPress any key to begin!")  # Prompt user to start
    stdscr.refresh()  # Refresh the screen to show the changes
    stdscr.getkey()  # Wait for any key press

def display_text(stdscr, target, current, wpm=0):
    """
    Displays the target text and the current text typed by the user.
    Highlights correctly and incorrectly typed characters.
    
    Args:
        stdscr: The standard screen object.
        target: The text to be typed.
        current: The text typed by the user.
        wpm: Words per minute calculated so far.
    """
    stdscr.addstr(target)  # Display the target text
    stdscr.addstr(1, 0, f"WPM: {wpm}")  # Display the WPM at the second line
    
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)  # Default color (correct character)
        if char != correct_char:
            color = curses.color_pair(2)  # Color for incorrect characters
            
        stdscr.addstr(0, i, char, color)  # Display the current text with appropriate color

def load_text():
    """
    Loads and returns a random line from 'text.txt'.
    """
    with open("text.txt", "r") as f:
        lines = f.readlines()  # Read all lines from the file
        return random.choice(lines).strip()  # Select a random line and strip extra whitespace

def wpm_test(stdscr):
    """
    Conducts the typing test where the user types the target text.
    Measures and updates the WPM as the user types.
    
    Args:
        stdscr: The standard screen object.
    """
    target_text = load_text()  # Load the target text
    current_text = []  # List to keep track of typed characters
    wpm = 0  # Initialize words per minute
    start_time = time.time()  # Record the start time of the test
    stdscr.nodelay(True)  # Set the screen to non-blocking mode
    
    while True:
        time_elapsed = max(time.time() - start_time, 1)  # Calculate time elapsed, ensure it's at least 1 second
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)  # Calculate WPM
        
        stdscr.clear()  # Clear the screen
        display_text(stdscr, target_text, current_text, wpm)  # Update the display with current text and WPM
        stdscr.refresh()  # Refresh the screen to show changes
        
        if "".join(current_text) == target_text or len(current_text) > len(target_text):
            # End the test if the text is completed or over-typed
            stdscr.nodelay(False)  # Set the screen back to blocking mode
            break
        
        try:
            key = stdscr.getkey()  # Get the next key pressed
        except:
            continue
        
        if ord(key) == 27:  # Escape key (ASCII 27) to exit the test
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):  # Handle backspace key
            if len(current_text) > 0:
                current_text.pop()  # Remove the last character
        elif len(current_text) < len(target_text):
            current_text.append(key)  # Append the new character

def main(stdscr):
    """
    Main function to initialize colors, run the start screen, and handle the typing test loop.
    
    Args:
        stdscr: The standard screen object.
    """
    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct characters in green
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Incorrect characters in red
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # (Unused) Default text color
    
    start_screen(stdscr)  # Show the start screen
    
    while True:
        wpm_test(stdscr)  # Run the typing test
        
        # Display message after completing the text
        stdscr.addstr(2, 0, "You completed the text! Press any key to play again...")
        stdscr.refresh()  # Refresh the screen to show the message
        key = stdscr.getkey()  # Wait for user input to start again
        
        if ord(key) == 27:  # Escape key to exit the game
            break
        
# Run the main function with curses wrapper
wrapper(main)
