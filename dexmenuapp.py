import threading
import time

import rumps
from pydexcom import Dexcom
import dotenv
import os

dotenv.load_dotenv('.env')

rumps.debug_mode(True)

username = os.getenv('username')
password = os.getenv('password')

dexcom = Dexcom(username, password)  # add ous=True if outside of US


def egv_str():
    return(str(dexcom.get_current_glucose_reading().value) + dexcom.get_current_glucose_reading().trend_arrow)


class DexMenuApp(rumps.App):
    def __init__(self, name, *args, **kwargs):
        super(DexMenuApp, self).__init__(name, *args, **kwargs)

        self.notification_menu = rumps.MenuItem(
            "Click to Disable Notifications", callback=self.notificationToggle)
        self.threshold_menu = rumps.MenuItem("Adjust Thresholds")
        self.high_threshold_menu = rumps.MenuItem(
            "High Threshold", callback=self.change_high_threshold)
        self.low_threshold_menu = rumps.MenuItem(
            "Low Threshold", callback=self.change_low_threshold)

        self.timeout_menu = rumps.MenuItem("Adjust Timeout")
        self.high_timeout_menu = rumps.MenuItem(
            "High Timeout", callback=self.change_high_timeout)
        self.low_timeout_menu = rumps.MenuItem(
            "Low Timeout", callback=self.change_low_timeout)

        self.menu.add(self.notification_menu)
        self.menu.add(self.threshold_menu)
        self.threshold_menu.add(self.high_threshold_menu)
        self.threshold_menu.add(self.low_threshold_menu)

        self.menu.add(self.timeout_menu)
        self.timeout_menu.add(self.high_timeout_menu)
        self.timeout_menu.add(self.low_timeout_menu)

        self.high_number = 150
        self.low_number = 100
        self.high_timeout = 20
        self.low_timeout = 10
        self.notifications = True
        self.last_high_time = 0
        self.last_low_time = 0
        self.update()

    def change_high_threshold(self, _):
        self.adjustThreshold("High")

    def change_low_threshold(self, _):
        self.adjustThreshold("Low")

    def change_high_timeout(self, _):
        self.adjustTimeout("High")

    def change_low_timeout(self, _):
        self.adjustTimeout("Low")

    def notificationToggle(self, _):
        if self.notifications == True:
            self.notifications = False
            self.notification_menu.title = "Click to Enable Notifications"
        elif self.notifications == False:
            self.notifications = True
            self.notification_menu.title = "Click to Disable Notifications"

    def adjustThreshold(self, hilow):
        window = rumps.Window(
            'Change your ' + hilow.lower() + ' notification threshold.')
        window.title = hilow + ' Threshold'
        if hilow is "High":
            window.default_text = self.high_number
            self.high_number = int(window.run().text)
        elif hilow is "Low":
            window.default_text = self.low_number
            self.low_number = int(window.run().text)

    def adjustTimeout(self, hilow):
        window = rumps.Window(
            'Change your ' + hilow.lower() + ' notification timeout in minutes.')
        window.title = hilow + ' Timeout'
        if hilow is "High":
            window.default_text = self.high_timeout
            self.high_timeout = int(window.run().text)
        elif hilow is "Low":
            window.default_text = self.low_timeout
            self.low_timeout = int(window.run().text)

    def update(self):
        threading.Timer(30.0, self.update).start()

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
