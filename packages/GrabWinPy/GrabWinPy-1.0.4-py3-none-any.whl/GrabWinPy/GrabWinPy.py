import pygetwindow as winget
import pyautogui
from tkinter import filedialog



class WinGrabber:
    def __init__(self):
        self.windows = []
        self._window = None
        self.target_window = None

    def show_available_windows(self) -> list:
        '''
        Returns a list of all available windows that can be grabbed.
        '''
        self.windows = winget.getAllTitles()
        self.valid_windows = []
        for window in self.windows:
            if window != '':
                self.valid_windows.append(window)
        for i, valid_window in enumerate(self.valid_windows):
            print(f'{i}. {valid_window}')
        return self.valid_windows


    def grab_window(self, save_path, window_name=None, window_index=None):
        '''
        Grabs a screenshot of a specified window.
        '''
        if window_index == None:
            if window_name != '':
                self._window = winget.getWindowsWithTitle(window_name)
            else:
                print('Window name not valid')  
        else:
            window_name = self.valid_windows[window_index]
            self._window = winget.getWindowsWithTitle(window_name)

        if self._window:
            self._window = self._window[0]
            left, top, width, height = self._window.left, self._window.top, self._window.width, self._window.height

            # Capture the specified window region
            screenshot = pyautogui.screenshot(region=(left, top, width, height))

            # Save the captured image
            screenshot.save(save_path)
        else:
            print('Could not find window')


    def help(self):
        '''
        Prints an example of how to use the library.
        '''
        print(f"from GrabWinPy import WinGrabber\n\ngrabber = WinGrabber()\nwindow = grabber.show_available_windows()[0]\ngrabber.grab_window(window, 'image.png')")



    def set_save_path(self):
        '''
        Opens a window that allows user to specify save location
        '''
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        return file_path





if __name__ == '__main__':
    grabber = WinGrabber()
    grabber.show_available_windows()
    grabber.grab_window('./save.png', window_index=0)