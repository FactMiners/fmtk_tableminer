#
# The Rubberband Panel is part of the FactMiners Toolkit. It features
#  non-flickering selection rectangle click-drag on a scrolling bitmap
#  (larger than the display panel), returns an image-global bounding-box
#  location that is a consistent bbox rectangle regardless of the
#  (quadrant) direction of the user's drag interaction.
#

import wx
import math
import copy
import html
from PIL import Image
import fmtk_rubberband_rect as rb_rect

standalone = False


class RubberbandPanel(wx.ScrolledWindow):

    def __init__(self, parent, any_id):
        wx.ScrolledWindow.__init__(self, parent, any_id, wx.DefaultPosition,
                                   wx.DefaultSize, wx.SUNKEN_BORDER |
                                   wx.HSCROLL | wx.VSCROLL, 'ID_RBPANEL')
        self.frame = parent
        # self.app = an_app
        # The use_case attribute distinguished beteen the "ml_tim" and
        # "scale_resizable" use cases.  The "ml_tim" use case is for the
        # creating resized images and bounding box dimensions of images
        # scaled to the lachine-learning maximum pixel reqirement.
        # The "scale_resizable" use case is for use by apps and tools
        # that need to resize the image to fit the panel, but also
        # need to maintain the original image dimensions for
        # subsequent processing.
        self.use_case = "scale_resizable"

        # TODO: Default to rubberband off for now...
        self.task_profile = "rubberband_on"
        self.task_limbo = ""
        # If True, the panel is instantiated w/ its own menu and statusbars.
        self.standalone = standalone
        # Properties and related whatnot...
        # Default is to not resize the image, but to scroll the panel
        self.max_pixels = 0
        # self.max_pixels = 1000000
        # self.max_pixels = 300000
        self.resize_dimensions = (0, 0)
        self.img_scale = 1.0
        # If a user wants to check the change in the bounding box dimensions.
        self.bbox_checkpoint = wx.Rect(0, 0, 0, 0)
        # if self.standalone:
            #  TODO: Image height offset is hard-coded, needs dynamic fix or
            #   user setting
        if 'wxMac' in wx.PlatformInfo:
            self.max_height = wx.GetDisplaySize().Height # - 100
        else:
            self.max_height = wx.GetDisplaySize().Height - 50
        # else:
        #     # Use the hosting app's max_height...
        #     self.max_height = an_app.max_height

        self.src_image = Image.new('RGB', (100, 100))
        self.scaled_img2buffer = wx.Image(self.src_image.width,
                                          self.src_image.height)
        # This image is to be sized according to the 'ml_tim' max_pixels limit
        self.scaled_image = self.src_image.copy()
        # This buffer is refreshed with the task profile appropriate bitmap
        self.buffer = wx.Bitmap(self.src_image.width, self.src_image.height)
        self.rubberband = rb_rect.RubberbandRect(self)

        # Register event handlers for mouse to be handled by the RubberbandPanel
        self.Bind(wx.EVT_LEFT_DCLICK, self.rubberband.on_left_mouse_event)
        self.Bind(wx.EVT_LEFT_DOWN, self.rubberband.on_left_mouse_event)
        self.Bind(wx.EVT_LEFT_UP, self.rubberband.on_left_mouse_event)
        self.Bind(wx.EVT_MOTION, self.rubberband.on_left_mouse_event)
        self.Bind(wx.EVT_TIMER, self.rubberband.mouse_down)
        self.Bind(wx.EVT_PAINT, self.on_paint)

        self.prep_gui()
        dc = wx.BufferedDC(None, self.buffer)
        self.rubberband.clear_canvas_and_draw(dc)

        if self.standalone:
            self.frame.CreateStatusBar(2)
            self.frame.SetStatusWidths([10, -1])
            self.frame.SetStatusText(
                "Click and drag to set a rubberband rectangle.", 1)
    # end __init__

    def prep_gui(self):
        if self.standalone:
            menu_bar = wx.MenuBar()
            file_menu = wx.Menu()
            exit_item = file_menu.Append(wx.ID_EXIT, "&Quit\tCtrl+Q",
                                         "Close the program")
            menu_bar.Append(file_menu, "&File")
            self.frame.SetMenuBar(menu_bar)
            self.frame.Bind(wx.EVT_MENU, self.quit_program, exit_item)

        try:
            self.load_image()
        except Exception as exc:
            dlg = wx.MessageDialog(self, str(exc.args), "Error message", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            pass
    # end prep_gui

    def load_image(self):
        if self.standalone:
            # TODO: This (temp?) test image is in the base project directory...
            self.scaled_image = Image.open('softalkv2n07mar1982_0004.jpg')
        else:
            self.scaled_image = self.src_image.copy()

        # First, do the full-page image scaled to ML model image max_pixels...
        self.resize_dimensions = self.cap_dimensions(self.scaled_image.size[0],
                                                     self.scaled_image.size[1])
        # Resize the scaled_image to the constraint of the maximum number of
        #  pixels desired in the training images. This is the non-spotted
        #  'ml_tim' max_pixels compliant page image to be written to the
        #  model training dataset.
        self.scaled_image = self.scaled_image.resize(self.resize_dimensions,
                                                    #  Image.Resampling.BICUBIC)
                                                     Image.BICUBIC)
        self.scaled_img2buffer = wx.Image(self.scaled_image.size[0],
                                          self.scaled_image.size[1])
        self.scaled_img2buffer.SetData(
            self.scaled_image.convert("RGB").tobytes())
        try:
            self.buffer = self.scaled_img2buffer.ConvertToBitmap()
        except KeyError:
            print('Could not convert PIL image to bitmap...')
        if self.standalone:
            # TODO: Multiply system-reported scrollbar size due to OS
            #  resolution adjustment on 4K. May need user setting.
            sb_size = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_ARROW_X)
            if hasattr(self.app, 'widgetbar'):
                # TODO: Adding 10 for 2 times the SizerItem Border...
                #  how to calc this!?
                sb_size = sb_size + self.app.widgetbar.GetSize().GetWidth()
            self.frame.SetSize((self.resize_dimensions[0] + sb_size,
                                self.max_height))
        # Keep the scrolling frame's virtual size the same as the
        #  max_pixel-sized bitmap.
        self.SetVirtualSize(self.resize_dimensions[0],
                            self.resize_dimensions[1])
        self.SetScrollRate(10, 10)
    # end load_image

    def set_max_pixels(self, max_pixels):
        self.max_pixels = max_pixels
    # end set_max_pixels

    def cap_dimensions(self, width, height):
        pixels = width * height
        if self.use_case == 'ml_tim':
            if self.max_pixels == 0 or pixels <= self.max_pixels:
                self.img_scale = 1.0
                return wx.Size(width, height)
        elif self.use_case == 'scale_resizable':
            return self.scale_by_img_scale()
        else:
            # Cap dimensions to max_pixels for ML training image model
            self.wh_ratio = float(width) / height
            self.img_scale = math.sqrt(float(pixels) / self.max_pixels)
            height2 = int(float(height) / self.img_scale)
            width2 = int(self.wh_ratio * height / self.img_scale)
            # print('Output2, x: ', str(width2), ' h: ', str(height2))
            return wx.Size(width2, height2)
    # end cap_dimensions

    def scale_by_img_scale(self):
        return wx.Size(math.ceil(self.src_image.size[0] * self.img_scale),
                       math.ceil(self.src_image.size[1] * self.img_scale))

    def unscale_dimensions(self, width, height):
        return wx.Size(math.ceil(width * self.img_scale),
                       math.ceil(height * self.img_scale))
    # end unscale_dimensions

    def unscale_position(self, x, y):
        return wx.Point(math.floor(x * self.img_scale),
                        math.floor(y * self.img_scale))
    # end unscale_position

    def unscale_point(self, point):
        return wx.Point(math.floor(point.x * self.img_scale),
                        math.floor(point.y * self.img_scale))
    # end unscale_position

    def scale_point(self, point):
        return wx.Point(math.floor(point.x / self.img_scale),
                        math.floor(point.y / self.img_scale))
    # end scale_position

    def scale_bbox(self, bbox):
        return wx.Rect(math.floor(bbox.x * self.img_scale),
                       math.floor(bbox.y * self.img_scale),
                       math.ceil(bbox.width * self.img_scale),
                       math.ceil(bbox.height * self.img_scale))
    # end scale_bbox

    def src_scale_bbox(self, bbox):
        return wx.Rect(math.floor(bbox.x / self.img_scale),
                       math.floor(bbox.y / self.img_scale),
                       math.ceil(bbox.width / self.img_scale),
                       math.ceil(bbox.height / self.img_scale))
    # end src_scale_bbox

    def quit_program(self, event):
        # TODO: ??? Throws a runtime exception on close in a paint event
        #  (where we work around this)
        if event:
            wx.CallAfter(self.frame.Close)
            event.Skip()
    # end quit_program

    def tell_pos(self, event):
        # start_pos = event.GetPosition()
        status_msg = 'Out rect (x, y, w, h): ' + \
                     str(self.rubberband.bounding_box)
        status_msg += " Bitmap position " + \
            str(event.GetEventObject().Position)
        # status_msg += " Image dimensions " + str(event.GetEventObject().Size)
        status_msg += " Image dimensions " + str(self.resize_dimensions)
        self.frame.SetStatusText(status_msg, 1)
    # end tell_pos

    def on_paint(self, event):
        """set up the device context (DC) for painting"""
        if event:
            wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
    # end on_paint
# end of class RubberbandPanel


if standalone:
    if __name__ == '__main__':
        app = wx.App()
        frame = wx.Frame(None, -1, "FMTK Rubberband Panel Test", (1024, 768))
        rbp = RubberbandPanel(frame, wx.ID_ANY)
        rbp.task_profile = 'standalone'
        app.SetTopWindow(frame)
        frame.Centre()
        frame.Show()

        # import wx.lib.inspection
        # wx.lib.inspection.InspectionTool().Show()

        app.MainLoop()
