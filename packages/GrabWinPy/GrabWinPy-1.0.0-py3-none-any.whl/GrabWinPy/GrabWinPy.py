import pygetwindow as winget
import pyautogui

class WinGrabber:
    def __init__(self):
        self.windows = []
        self.selected_window = None

    def show_available_windows(self) -> list:
        '''
        Returns a list of all available windows that can be grabbed.
        '''
        self.windows = [window.title for window in winget.getWindows()]
        return self.windows


    def grab_window(self, window_name, save_path):
        '''
        Grabs a screenshot of a specified window.
        '''
        self.selected_window = winget.getWindowsWithTitle(window_name)
        if self.selected_window:
            self.selected_window = self.selected_window[0]
            left, top, width, height = self.selected_window.left, self.selected_window.top, self.selected_window.width, self.selected_window.height

            # Capture the specified window region
            screenshot = pyautogui.screenshot(region=(left, top, width, height))

            # Save the captured image
            screenshot.save(save_path)
        else:
            print('Could not find window')

