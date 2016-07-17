#coding=utf-8
import logging
import os
import select
import socket
import sys
import time
import traceback
import string

from GUI import Application, ScrollableView, Document, Window, Cursor, rgb, View, TabView
from GUI import application, Button
from GUI.Files import FileType
from GUI.Geometry import pt_in_rect, offset_rect, rects_intersect
from GUI.StdColors import black, red, blue
from GUI.StdFonts import application_font
from GUI.Colors import rgb

class TabViewPyGUIApp(Application):
    def __init__(self):
        Application.__init__(self)

    def make_window(self, document):
        self.tabview = view = TabView()

        win = Window(size = (600, 400), document = document)

        self.view1 = Button(title='Item 1', action=self.item1Action)
        view.add_item(self.view1)

        self.view2 = Button(title='Item 2', action=self.item2Action)
        view.add_item(self.view2)

        win.place(view, left = 0, top = 0, right = 0, bottom = 0, sticky = 'nsew')

        win.show()

    def make_document(self, fileref):
        doc = Document()

        return doc
    
    def open_app(self):
        self.new_cmd()

    def item1Action(self):
        self.tabview.remove_item_at(1)

    def item2Action(self):
        self.tabview.remove_item(self.view1)
        
if __name__ == '__main__':
    TabViewPyGUIApp().run()
