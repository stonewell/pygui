#--------------------------------------------------------------------
#
#   PyGUI - DrawableContainer - Win32
#
#--------------------------------------------------------------------

from GUI import export
from GUI import Canvas
from GUI.Geometry import rect_topleft, rect_size, offset_rect, empty_rect
from GUI.GDrawableContainers import DrawableContainer as GDrawableContainer
import GUI.GDIPlus as gdi
import win32gui as gui
import win32ui as ui
import win32con

class DrawableContainer(GDrawableContainer):

    _double_buffer = True
    _win_paint_broken = False

    def update(self):
        self._win.UpdateWindow()

    def with_canvas(self, body):
        win = self._win
        dc = win.GetDC()
        self._win_prepare_dc(dc)
        try:
            canvas = Canvas._from_win_dc(dc)
            body(canvas)
        finally:
            win.ReleaseDC(dc)

    def OnPaint(self):
        if not self._win_paint_broken:
            try:
                win = self._win
                dc, ps = win.BeginPaint()
                try:
                    win_update_rect = ps[2]
                    if not empty_rect(win_update_rect):
                        #print "DrawableContainer.OnPaint: win_update_rect =", win_update_rect ###
                        scroll_offset = self._win_scroll_offset()
                        view_update_rect = offset_rect(win_update_rect, scroll_offset)
                        if self._double_buffer:
                            dx, dy = rect_topleft(view_update_rect)
                            width, height = rect_size(view_update_rect)
                            #GDIPlus draw large image in very bad performance
                            #use GDI instead
                            #buffer = gdi.Bitmap(width, height)
                            #canvas = Canvas._from_win_image(buffer)
                            #canvas.translate(-dx, -dy)
                            #self.draw(canvas, view_update_rect)
                            #graphics = gdi.Graphics.from_dc(dc)
                            #src_rect = (0, 0, width, height)
                            #graphics.DrawImage_rr(buffer, win_update_rect, src_rect)

                            c_dc = dc.CreateCompatibleDC(dc)
                            c_dm = ui.CreateBitmap()
                            c_dm.CreateCompatibleBitmap(dc, width, height)
                            old = c_dc.SelectObject(c_dm)
                            c_dc.SetViewportOrg((-dx, -dy))
                            canvas = Canvas._from_win_dc(c_dc)

                            self.draw(canvas, view_update_rect)

                            l, t = rect_topleft(win_update_rect)
                            dc.BitBlt((l, t), (width, height), c_dc, (0, 0), win32con.SRCCOPY)
                            c_dc.SelectObject(old)
                        else:
                            self._win_prepare_dc(dc)
                            canvas = Canvas._from_win_dc(dc)
                            self.draw(canvas, view_update_rect)
                finally:
                    win.EndPaint(ps)
            except Exception:
                self._win_paint_broken = True
                raise

    def _win_prepare_dc(self, dc):
        dc.SetWindowOrg(self._win_scroll_offset())

    def _win_scroll_offset(self):
        return (0, 0)

export(DrawableContainer)
