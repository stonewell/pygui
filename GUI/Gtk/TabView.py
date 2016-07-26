#
#   Python GUI - Buttons - Gtk version
#

import gtk
from GUI import export
from GUI.StdFonts import system_font
from GUI.GTabViews import TabView as GTabView
from GUI.GContainers import Container as GContainer

class TabView(GTabView):

    def __init__(self, font = system_font, **kwds):
        gtk_notebook = gtk.Notebook()
        gtk_notebook.show_all()
        self._gtk_connect(gtk_notebook, 'switch-page', self._gtk_notebook_switch_page_signal)
        GTabView.__init__(self, _gtk_outer = gtk_notebook,
            **kwds)

    def add_item(self, v, title = None):
        GTabView.add_item(self, v, title)
        _gtk_notebook = self._gtk_inner_widget

        _tab_label = None
        if title:
            _tab_label = gtk.Label(title)
            _tab_label.show()

        index = _gtk_notebook.append_page(v._gtk_inner_widget, tab_label = _tab_label)

    def remove_item(self, v):
        GTabView.remove_item(self, v)
        _gtk_notebook = self._gtk_inner_widget

        page_num = _gtk_notebook.page_num(v._gtk_inner_widget)

        if page_num >= 0:
            _gtk_notebook.remove_page(page_num)

    def insert_item_at(self, v, i, title = None):
        GTabView.insert_item_at(self, v, i, title)
        _gtk_notebook = self._gtk_inner_widget
        _tab_label = None
        if title:
            _tab_label = gtk.Label(title)

        _gtk_notebook.insert_page(v._gtk_inner_widget, tab_label=_tab_label, position=i)

    def remove_item_at(self, i):
        GTabView.remove_item_at(self, i)
        _gtk_notebook = self._gtk_inner_widget

        _gtk_notebook.remove_page(i)

    def _gtk_notebook_switch_page_signal(self, page, page_num, *largs):
        self.tab_changed(page_num)

    def get_selected_index(self):
        _gtk_notebook = self._gtk_inner_widget

        return _gtk_notebook.get_current_page()

    def set_selected_index(self, index):
        _gtk_notebook = self._gtk_inner_widget

        _gtk_notebook.set_current_page(index)

    def _add(self, comp):
        GContainer._add(self, comp)

    def _remove(self, comp):
        GContainer._remove(self, comp)
export(TabView)
