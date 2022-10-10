import threading
import time
import multiprocessing

import rumps
from pydexcom import Dexcom
import os
import dotenv

dotenv.load_dotenv('.env')

rumps.debug_mode(True)

USERNAME = os.getenv('username')
PASSWORD = os.getenv('password')

dexcom = Dexcom(USERNAME, PASSWORD)  # add ous=True if outside of US


def egv_str():
    return(str(dexcom.get_current_glucose_reading().value) + dexcom.get_current_glucose_reading().trend_arrow)


class DexMenuApp(rumps.App):
    def __init__(self, name, *args, **kwargs):
        super(DexMenuApp, self).__init__(name, *args, **kwargs)

        self.notification_menu = rumps.MenuItem(
            "Click to Disable Notifications", callback=self.notificationToggle)
        self.settings_menu = rumps.MenuItem(
            "Settings", callback=self.openSettingsWindow)

        self.menu.add(self.notification_menu)
        self.menu.add(self.settings_menu)

        self.high_number = 150
        self.low_number = 100
        self.high_timeout = 20
        self.low_timeout = 10
        self.notifications = True
        self.last_high_time = 0
        self.last_low_time = 0
        self.update()

    def loadSettings(self):
        pass

    def saveSettings(self):
        pass

    def openSettingsWindow(self, event):
        print("opening settings")
        mythread = threading.Thread(target=self.settingsThread)
        mythread.start()
        mythread.join()
        print("thread finished")

    def settingsThread(self):
        import settingsWindow
        settingsWindow.startSettings()

    def notificationToggle(self, _):
        if self.notifications == True:
            self.notifications = False
            self.notification_menu.title = "Click to Enable Notifications"
        elif self.notifications == False:
            self.notifications = True
            self.notification_menu.title = "Click to Disable Notifications"

    def update(self):
        #threading.Timer(30.0, self.update).start()

        if dexcom.get_current_glucose_reading() is None:
            self.title = "No Data"
        else:
            self.title = egv_str()
            if self.notifications == True:
                self.notify(dexcom.get_current_glucose_reading().value)

    def notify(self, number):
        if number > self.high_number and (time.time() - self.last_high_time >= (self.high_timeout * 60)):
            rumps.notification("Dex-Menu-App", "High Alert!",
                               egv_str())
            self.last_high_time = time.time()
        elif number < self.low_number and (time.time() - self.last_low_time >= (self.low_timeout * 60)):
            rumps.notification("Dex-Menu-App", "Low Alert!",
                               egv_str())
            self.last_low_time = time.time()


if __name__ == "__main__":
    DexMenuApp("DexMenuApp").run()
