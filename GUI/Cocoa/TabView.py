#------------------------------------------------------------------------------
#
#   Python GUI - TabViews - PyObjC version
#
#------------------------------------------------------------------------------

from Foundation import NSMutableDictionary, NSAttributedString
from AppKit import NSMutableParagraphStyle, NSFontAttributeName, \
    NSForegroundColorAttributeName, NSParagraphStyleAttributeName, \
    NSTabView, NSTabViewItem
from GUI.Utils import NSMultiClass, PyGUI_NS_EventHandler, \
    ns_set_action, ns_size_to_fit
from GUI import Control
from GUI.StdColors import black
from GUI.GTabViews import TabView as GTabView
from GUI import export
from GUI.StdFonts import system_font
#------------------------------------------------------------------------------

class TabView(GTabView):

    _ns_handle_mouse = True

    def _create_ns_tabview(self, font, padding = (0, 0)):
        ns_tabview = PyGUI_NSTabView.alloc().init()
        ns_tabview.pygui_component = self
        ns_tabview.setFont_(font._ns_font)
        ns_tabview.setDelegate_(self)
        
        return ns_tabview

    def __init__(self, font = system_font, **kwds):
        _ns_tabview = self._create_ns_tabview(font, padding = (10, 2))
        GTabView.__init__(self, _ns_view = _ns_tabview, **kwds)

    def _create_ns_tabview_item(self, v, title):
        _ns_tabview = self._ns_view

        count = _ns_tabview.numberOfTabViewItems()
        
        _ns_tabview_item = NSTabViewItem.alloc().initWithIdentifier_('item_count_%d' % count)
        _ns_tabview_item.set_view_(v._ns_view)
        _ns_tabview_item.set_label_(title if title is not None else 'item %d' % (count + 1))

        return _ns_tabview_item
        
    def add_item(self, v, title = None):
        _ns_tabview = self._ns_view

        _ns_tabview_item = self._create_ns_tabview_item(v, title)
        
        _ns_tabview.addTabViewItem_(_ns_tabview_item)

    def remove_item(self, v):
        _ns_tabview = self._ns_view
        for item in _ns_tabview.tabViewItems():
            if item.view() == v._ns_view:
                _ns_tabview.removeTabViewItem_(item)
                break

    def insert_item_at(self, v, i, title = None):
        _ns_tabview = self._ns_view

        _ns_tabview_item = self._create_ns_tabview_item(v, title)
        
        _ns_tabview.insertTabViewItem_atIndex_(_ns_tabview_item, i)

    def remove_item_at(self, i):
        _ns_tabview = self._ns_view

        count = _ns_tabview.numberOfTabViewItems()

        if i >= count or i < 0:
            return

        _ns_tabview.removeTabViewItem_(_ns_tabview.tabViewItems()[i])

    def tabView_didSelectTabViewItem_(self, tabview, item):
        GTabView.tab_changed(self, tabview.indexOfTabViewItem_(item))
        
#------------------------------------------------------------------------------

class PyGUI_NSTabView(NSTabView, PyGUI_NS_EventHandler):
    __metaclass__ = NSMultiClass
    __slots__ = ['pygui_component']

export(TabView)
