from gask.screenshots import login_screenshot
from guiask import TerminalScreen, TKeys
from gask import session_manager
import sys


def main():
    def default_input_handler(**kwargs):
        if 'char' not in kwargs:
            return
        ch = kwargs['char']

        if ch == TKeys.CTRL_C:
            print("Killed By User")
            sys.exit()

        if ch == TKeys.CTRL_E:
            screen.gorightfocus()

    screen = TerminalScreen(input_handler=default_input_handler)

    session_manager.start_connection()
    screenshot = login_screenshot()
    screen.load(screenshot)
    screen.loop()


if __name__ == '__main__':
    main()