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

    def add_item(self, v, title = None):
        pass

    def remove_item(self, v):
        pass

    def insert_item_at(self, v, i, title = None):
        pass

    def remove_item_at(self, i):
        pass

