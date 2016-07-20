#
#   Python GUI - Buttons - Gtk version
#

import gtk
from GUI import export
from GUI.StdFonts import system_font
from GUI.GTabViews import TabView as GTabView

_gtk_extra_hpad = 5   # Amount to add to default width at each end
_gtk_icon_spacing = 2  # Space to leave between icon and label

class TabView(GTabView):

    def __init__(self, font = system_font, **kwds):
        gtk_notebook = gtk.Notebook()
        gtk_notebook.show_all()
        self._gtk_connect(gtk_notebook, 'switch-page', self._gtk_notebook_switch_page_signal)
        GTabView.__init__(self, _gtk_outer = gtk_notebook,
            **kwds)
    
    def add_item(self, v, title = None):
        _gtk_notebook = self._gtk_inner_widget

        _tab_label = None
        if title:
            _tab_label = gtk.Label(title)
            _tab_label.show()

        v._gtk_inner_widget.show()
        _gtk_notebook.append_page(v._gtk_inner_widget, tab_label = _tab_label)

    def remove_item(self, v):
        _gtk_notebook = self._gtk_inner_widget

        page_num = _gtk_notebook.page_num(v._gtk_inner_widget)

        if page_num >= 0:
            _gtk_notebook.remove_page(page_num)

    def insert_item_at(self, v, i, title = None):
        _gtk_notebook = self._gtk_inner_widget
        _tab_label = None
        if title:
            _tab_label = gtk.Label(title)

        _gtk_notebook.insert_page(v._gtk_inner_widget, tab_label=_tab_label, position=i)

    def remove_item_at(self, i):
        _gtk_notebook = self._gtk_inner_widget

        _gtk_notebook.remove_page(i)

    def _gtk_notebook_switch_page_signal(self, page, page_num, *largs):
        self.tab_changed(page_num)
        
export(TabView)

