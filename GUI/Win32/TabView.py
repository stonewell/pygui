#--------------------------------------------------------------------
#
#   PyGUI - TabView - Win32
#
#--------------------------------------------------------------------

from time import sleep
import win32con as wc, win32gui as gui, commctrl as cc, win32ui as ui
from GUI import export
from GUI.GTabViews import TabView as GTabView
from GUI.WinUtils import win_none
import ctypes, ctypes.wintypes
import struct

gui.InitCommonControls()

class TabView(GTabView):
    def __init__(self, **kwds):
        win = self._win_create_tabctrl()
        GTabView.__init__(self, _win = win, **kwds)

    def _win_create_tabctrl(self):
        _win = gui.CreateWindow(cc.WC_TABCONTROL,
                                '',
                                wc.WS_CHILD | wc.WS_CLIPSIBLINGS | wc.WS_VISIBLE,
                                0, 0, 1, 1,
                                win_none.GetSafeHwnd(),
                                0, 0, None)
        _pywin = ui.CreateWindowFromHandle(_win)

        _pywin.HookMessage(self._win_wm_notify, wc.WM_NOTIFY)

        return _pywin
    
    def add_item(self, v, title = None):
        i = len(self.items)

        self._insert_item_at(v, i, title)
        
        GTabView.add_item(self, v, title)
        
    def insert_item_at(self, v, i, title = None):
        self._insert_item_at(v, i, title)
        
        GTabView.insert_item_at(self, v, i, title)
        
    def _insert_item_at(self, v, i, title = None):
        _tab_ctrl = self._win
        
        if not title:
            title = 'Page %d' % (i)
        
        lbuf = gui.PyMakeBuffer(len(title)+1)
        address,l = gui.PyGetBufferAddressAndLen(lbuf)
        gui.PySetMemory(address, title)

        _format = "iiiPiii"
        buf = struct.pack(_format,
            cc.TCIF_TEXT, # mask
            0, # state
            0, # state mask
            address,
            0, #unused
            0, #image
            i #data
            )
        
        gui.SendMessage(_tab_ctrl.GetSafeHwnd(),
                        cc.TCM_INSERTITEM,
                        i,
                        buf)

        self._resize_children(v)

    def remove_item(self, v):
        i = self.items.index(v)
        _tab_ctrl = self._win
        
        GTabView.remove_item(self, v)
        
        gui.SendMessage(_tab_ctrl.GetSafeHwnd(),
                        cc.TCM_DELETEITEM,
                        i,
                        0)

    def remove_item_at(self, i):
        GTabView.remove_item_at(self, i)
        _tab_ctrl = self._win
        gui.SendMessage(_tab_ctrl.GetSafeHwnd(),
                        cc.TCM_DELETEITEM,
                        i,
                        0)

    def get_selected_index(self):
        _tab_ctrl = self._win
        return gui.SendMessage(_tab_ctrl.GetSafeHwnd(),
                        cc.TCM_GETCURSEL,
                        0,
                        0)

    def set_selected_index(self, index):
        _old_index = self.get_selected_index()

        if _old_index == index:
            return
        
        _tab_ctrl = self._win
        gui.SendMessage(_tab_ctrl.GetSafeHwnd(),
                        cc.TCM_SETCURSEL,
                        index,
                        0)

        self._tab_changed(index)

    def _tab_changed(self, index):
        for i in range(len(self.items)):
            if i == index:
                self.items[i]._win.ShowWindow(wc.SW_SHOW)
            else:
                self.items[i]._win.ShowWindow(wc.SW_HIDE)
                
        self.tab_changed(index)
        
    def _resize_children(self, child = None):
        _tab_ctrl = self._win
        l, t, r, b = self.bounds
        
        _rformat = 'iiii'
        _rect = struct.pack(_rformat,
                            l,
                            t,
                            r,
                            b)
        
        gui.SendMessage(_tab_ctrl.GetSafeHwnd(),
                        cc.TCM_ADJUSTRECT,
                        0,
                        _rect)

        l, t, r, b = struct.unpack(_rformat, _rect)

        if child:
            child.bounds = (l, t, r, b)
            child._win.MoveWindow((l, t, r, b))
            return
        
        for v in self.items:
            v.bounds = (l, t, r, b)
            v._win.MoveWindow((l, t, r, b))
        
    def _resized(self, delta):
        self._resize_children()
            
        GTabView._resized(self, delta)
        
    def _win_wm_notify(self, nm_item):
        TCN_SELCHANGE = -551

        if nm_item.code == TCN_SELCHANGE:
            self._tab_changed(self.get_selected_index())
        
export(TabView)
