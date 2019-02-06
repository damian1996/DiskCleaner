import threading
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.splitter import Splitter
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, NumericProperty

from DirectoryTree import DirectoryTree
from LoadingWidget import LoadingWidget
from PlotWidget import PlotWidget
from Utils import get_human_readable_size

class FileTreeViewLabel(BoxLayout, TreeViewNode):
    file_name = StringProperty()
    file_size = StringProperty()
    file_size_percent = NumericProperty()

    def __init__(self, dir, tree, treeview, remove_node_callback, **kwargs):
        super().__init__()
        self.dir = dir
        self.tree = tree
        self.treeview = treeview
        self.remove_node_callback = remove_node_callback
        self.file_name = dir.get_name()
        self.file_size = get_human_readable_size(dir)
        self.file_size_percent = self.dir.get_size()/self.dir.get_size_parent_directory()

    def get_dir(self):
        return self.dir
    
    def on_delete_button_press(self):
        self.tree.remove_tree_node(self.dir.get_path())
        self.on_remove_node()
        self.treeview.remove_node(self)
    
    def on_remove_node(self):
        self.file_size = get_human_readable_size(self.dir)
        self.file_size_percent = self.dir.get_size()/self.dir.get_size_parent_directory()
        if self.parent_node and isinstance(self.parent_node, FileTreeViewLabel):
            self.parent_node.on_remove_node()
        self.remove_node_callback

class FilesTreeWidget(BoxLayout):
    def __init__(self, tree, remove_node_callback, **kwargs):
        super(FilesTreeWidget, self).__init__(**kwargs)
        self.tree = tree
        self.remove_node_callback = remove_node_callback
        self.tv = TreeView(load_func=self.load_func, root_options={'text': tree.root.get_name()})
        self.tv.size_hint = 1, None
        self.tv.bind(minimum_height = self.tv.setter('height'))
        scroll_view = ScrollView()
        scroll_view.add_widget(self.tv)
        self.add_widget(scroll_view)
    
    def load_func(self, tv, node):
        if node is None or not isinstance(node, FileTreeViewLabel):
            dir = self.tree.root
        else:
            dir = node.get_dir()
        for child in dir.get_children():
            label = FileTreeViewLabel(child, self.tree, self.tv, self.remove_node_callback, text=child.get_name())
            label.is_leaf = child.if_is_file()
            yield label


class FilesScreen(Screen):
    def __init__(self, **kwargs):
        super(FilesScreen, self).__init__(**kwargs)
        self.loading = LoadingWidget()
        self.add_widget(self.loading)
    
    def start_file_search(self, path):
        self.path = path
        threading.Thread(target=self._start_file_search).start()
    
    def _start_file_search(self):
        tree = DirectoryTree(self.path)
        self.build_screen(tree)
    
    @mainthread
    def build_screen(self, tree):
        self.remove_widget(self.loading)
        box_layout = BoxLayout(orientation="horizontal")
        splitter = Splitter(sizable_from="right")
        plot_widget = PlotWidget(tree.root)
        splitter.add_widget(FilesTreeWidget(tree, plot_widget.draw))
        box_layout.add_widget(splitter)
        box_layout.add_widget(plot_widget)
        self.add_widget(box_layout)

