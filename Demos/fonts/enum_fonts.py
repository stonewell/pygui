# -*- coding: utf-8 -*-

import win32con as wc, win32ui as ui, win32gui as gui, win32api as api
import GUI.Font
from GUI.StdFonts import application_font
import GUI.GDIPlus as gdip

win_none = ui.CreateFrame()
win_none.CreateWindow(None, "", 0, (0, 0, 10, 10))

def enum_fonts(logfont, *largs):
    try:
        _gui_font = ui.CreateFont({'name':logfont.lfFaceName, 'height':-17, 'weight':400})
        _gui_font2 = GUI.Font(family=logfont.lfFaceName, size=17)
        _font = gui.CreateFontIndirect(logfont)
        hdc = win_none.GetDC().GetSafeHdc()
        gui.SelectObject(hdc, _font)
        print '1.------'
        print ''.join(['[', logfont.lfFaceName, ']']), gui.GetTextExtentPoint32(hdc, '12345'), logfont
        gui.SelectObject(hdc, _gui_font.GetSafeHandle())
        logfont.lfHeight = 17
        _gdip_font2 = gdip.Font.from_logfont(hdc, logfont)
        _gui_font2._win_gdip_font = _gdip_font2
        print _gui_font, (logfont.lfHeight,
                          logfont.lfWidth,
                          logfont.lfEscapement,
                          logfont.lfOrientation,
                          logfont.lfWeight,
                          logfont.lfItalic,
                          logfont.lfUnderline,
                          logfont.lfStrikeOut,
                          logfont.lfCharSet,
                          logfont.lfOutPrecision,
                          logfont.lfClipPrecision,
                          logfont.lfQuality,
                          logfont.lfPitchAndFamily), gui.GetTextExtentPoint32(hdc, '12345'), _gui_font2.width('12345')
        _gdip_font2 = gdip.Font.from_logfont(hdc, logfont)
        print '2.------', _gdip_font2.ptr
    except:
        import traceback
        traceback.print_exc()

    return True

try:
    gui.EnumFontFamilies(win_none.GetDC().GetSafeHdc(),
                     None,
                     enum_fonts,
                     None)
    _gui_font2 = GUI.Font(family=u'文泉驿等宽微米黑', size=17)
    _gui_font3 = GUI.Font(family='Noto Sans Mono CJK SC Regular', size=17)
    _gui_font4 = ui.CreateFont({'name':'Noto Sans Mono CJK SC Regular', 'height':-17, 'weight':400})
    print _gui_font2.width(u'12345文'), _gui_font3.width(u'12345文')
    hdc = win_none.GetDC().GetSafeHdc()
    gui.SelectObject(hdc, _gui_font4.GetSafeHandle())
    print gui.GetTextExtentPoint32(hdc, u'12345文文')
    gui.SelectObject(hdc, _gui_font3._win_font.GetSafeHandle())
    print gui.GetTextExtentPoint32(hdc, u'12345文')
    print _gui_font3._win_gdip_font.ptr,  _gui_font2._win_gdip_font.ptr
    print _gui_font2.width(u'文泉驿等宽微米黑'), _gui_font2.width(u'文'), _gui_font3.width(u'12345文')
except:
    import traceback
    traceback.print_exc()

