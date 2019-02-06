import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from PartitionsScreen import PartitionsScreen
from FilesScreen import FilesScreen

screen_manager = ScreenManager()
screen_manager.add_widget(PartitionsScreen(name="partitions"))
screen_manager.add_widget(FilesScreen(name="files"))

class DiskCleanerApp(App):
    def build(self):
        return screen_manager

if __name__ == '__main__':
    DiskCleanerApp().run()
