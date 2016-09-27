#------------------------------------------------------------------------------
#
#   PyGUI - GLContext - Win32
#
#------------------------------------------------------------------------------

import OpenGL as gl
from OpenGL import WGL as wgl
from GUI.GGLContexts import GLContext as GGLContext
import threading

class GLContext(GGLContext):
    #  _win_dc       Device context
    #  _win_context  WGL context
    #  _win_dblbuf   Is double buffered

    def __init__(self, share_group, config, hdc, mode):
        #print "GLContext: mode =", mode ###
        GGLContext.__init__(self, share_group)
        self._config = config
        self._mode = mode
        self._win_contexts = {}

        self._win_contxt = None
        self._win_context = self._get_cur_win_context(hdc)
        self._win_dblbuf = True#actpf.dwFlags & wgl.PFD_DOUBLEBUFFER != 0

    def destroy(self):
        wgl.wglDeleteContext(self._win_context)

    def _get_cur_win_context(self, hdc):
        if threading.current_thread() in self._win_contexts:
            return self._win_contexts[threading.current_thread()]

        if hasattr(self, '_win_context'):
            shared_context = self._win_context
        else:
            shared_context = None
        ipf, actpf = self._config._win_supported_pixelformat(hdc, self._mode)
        self._config._check_win_pixelformat(actpf, self._mode)
        #print "GLContext: Setting pixel format", ipf, "for hdc", hdc ###
        wgl.SetPixelFormat(hdc, ipf, actpf)
        #print "GLContext: Creating context for hdc", hdc ###
        ctx = wgl.wglCreateContext(hdc)
        if shared_context:
            wgl.wglShareLists(shared_context, ctx)

        self._win_contexts[threading.current_thread()] = ctx
        return ctx


    def _with_context(self, hdc, proc, flush = False):
        old_hdc = wgl.wglGetCurrentDC()
        old_ctx = wgl.wglGetCurrentContext()
        result = wgl.wglMakeCurrent(hdc, self._get_cur_win_context(hdc))
        try:
            self._with_share_group(proc)
            if flush:
                if self._win_dblbuf:
                    wgl.SwapBuffers(hdc)
                else:
                    gl.glFlush()
        finally:
            wgl.wglMakeCurrent(old_hdc, old_ctx)
