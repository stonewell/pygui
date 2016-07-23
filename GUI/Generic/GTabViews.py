#
#   Python GUI - TabViews - Generic
#

from GUI.Properties import overridable_property
from GUI.Geometry import add_pt, sub_pt, rect_sized
from GUI import Component, Container

class TabView(Component):
    """ A tabview."""
    
    selected_index = overridable_property('selected_index',
        "selected tab item")
    items = overridable_property('items', "tab view items")

    def __init__(self, **kwargs):
        Component.__init__(self, **kwargs)

        self._contents = []
        
    def add_item(self, v, title = None):
        self._contents.append(v)

    def remove_item(self, v):
        self._contents.remove(v)

    def insert_item_at(self, v, i, title = None):
        self._contents.insert(i, v)

    def remove_item_at(self, i):
        self._contents.remove(self_items[i])

    def tab_changed(self, tab_index):
        pass

    def get_items(self):
        return self._contents

    def get_selected_index(self):
        raise NotImplementedError

    def set_selected_index(self, index):
        raise NotImplementedError

    def _resized(self, delta):
        self.resized(delta)

    def resized(self, delta):
        pass
        
