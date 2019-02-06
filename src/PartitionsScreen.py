from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from DirectoryTree import DirectoryTree
from Disks import Disks
from Utils import get_files_and_dirs_to_delete
from dateutil.relativedelta import relativedelta

class PartitionWidget(GridLayout):
    partition = StringProperty()
    mountpoint = StringProperty()
    used = StringProperty()
    free = StringProperty()

    def __init__(self, partition, **kwargs):
        super().__init__()
        self.partition = partition.get_name()
        self.mountpoint = partition.get_mountpoint()
        self.used = "{} bytes ({}%)".format(partition.get_used_memory(), partition.get_used_memory_in_percents())
        self.free = "{} bytes".format(partition.get_free_memory())

class PartitionsScreen(Screen):
    def __init__(self, **kwargs):
        super(PartitionsScreen, self).__init__(**kwargs)
        Builder.load_file('partitions.kv')
        box_layout = BoxLayout()
        partitions_box_layout = BoxLayout(padding=50, orientation="vertical")
        disks = Disks()
        for partition in disks.get_partitions():
            partitions_box_layout.add_widget(PartitionWidget(partition))
        box_layout.add_widget(partitions_box_layout)
        file_chooser_layout = BoxLayout(orientation="vertical")
        self.file_chooser = FileChooserListView()
        file_chooser_layout.add_widget(self.file_chooser)
        buttons_box_layout = BoxLayout()
        buttons_box_layout.add_widget(Button(text="Run cleaner on selected directory", on_press=self.on_run_btn_press))
        buttons_box_layout.add_widget(Button(text="Give me some propositions", on_press=self.give_propositions))
        file_chooser_layout.add_widget(buttons_box_layout)
        box_layout.add_widget(file_chooser_layout)
        self.add_widget(box_layout)
    
    def on_run_btn_press(self, btn):
        self.manager.current = 'files'
        self.manager.current_screen.start_file_search(self.file_chooser.path)
    
    def give_propositions(self, btn):
        bx = BoxLayout(orientation="vertical")
        tree = DirectoryTree(self.file_chooser.path)
        propositions = get_files_and_dirs_to_delete(tree.root, 5, relativedelta(days=-20))
        bx.add_widget(Label(text="Found the following files:\n{}".format('\n'.join([file.get_path() for file in propositions]))))
        buttons = BoxLayout()
        popup = None
        buttons.add_widget(Button(text="Cancel", on_press=lambda btn: popup.dismiss()))
        def on_delete_btn_press(btn):
            tree.remove_tree_nodes(propositions)
            popup.dismiss()
        buttons.add_widget(Button(text="Delete them!", on_press=on_delete_btn_press))
        bx.add_widget(buttons)
        popup = Popup(title='Propositions', content=bx)
        popup.open()
        
