#
#   Python GUI - TabViews - Generic
#

from GUI.Properties import overridable_property
from GUI.Geometry import add_pt, sub_pt, rect_sized
from GUI import Component

class TabView(Component):
    """ A tabview."""
    
    selected_index = overridable_property('selected_index',
        "selected tab item")
    items = overridable_property('items', "tab view items")

    def __init__(self, **kwargs):
        Component.__init__(self, **kwargs)

        self._items = []
        
    def add_item(self, v, title = None):
        self._items.append(v)

    def remove_item(self, v):
        self._items.remove(v)

    def insert_item_at(self, v, i, title = None):
        self._items.insert(i, v)

    def remove_item_at(self, i):
        self._items.remove(self._items[i])

    def tab_changed(self, tab_index):
        pass

    def get_items(self):
        return self._items
