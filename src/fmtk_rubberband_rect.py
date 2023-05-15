#
# The RubberbandRect is used by the RubberbandPanel as part of the
#  FactMiners Toolkit.
#

import wx
import copy


def point_in_rect(px, py, rx, ry, rw, rh):
    if rx <= px <= (rx + rw) and ry <= py <= (ry + rh):
        return True
    else:
        return False
# end point_in_rect


class RubberbandRect(wx.Object):

    def __init__(self, scrolled_window):
        wx.Object.__init__(self)

        self.scr_win = scrolled_window

        # To store bbox rectangle and a last-used cache of it...
        self.bounding_box = wx.Rect()
        self.last_used = wx.Rect()
        # Once a drag is initiated, we set an anchor until drag release.
        #  Zero is pre-drag.
        self.drag_quadrant = 0
        self.drag_anchor = wx.Point(0, 0)
        # To store rubberband anchor point. Here the rect class object is
        # used to store the distance in the x and y direction from the anchor
        # point to the top-left and the bottom-right corner relative to the
        # click point within the rubberband.
        self.anchor = wx.Rect()
        # Timer and delay for handling double-clicks
        self.timer = wx.Timer()
        self.dclick_delay = 500
        # Selection marker size
        self.sBlk = 6

        # FLAGS
        # Rect already present?
        self.active = False
        # TODO: May be unnecessary
        # Drag for rect resize in progress
        self.drag = False
        # Marker flags by positions
        self.TL = False
        self.TM = False
        self.TR = False
        self.LM = False
        self.RM = False
        self.BL = False
        self.BM = False
        self.BR = False
        # User double-clicked inside existing rubberband rect to drag move it
        self.hold = False
        # This is the rubberband's rect, defaults to zeroes
        self.bounding_box.SetTopLeft(wx.Point(0, 0))
        self.bounding_box.SetSize(wx.Size(0, 0))
    # end init

    """ 
    Here is the explanation for the on_left_mouse_event code:
    1. When the left mouse button is pressed down, the mouse_down() 
    method is called. This method sets the self.active flag to True and 
    captures the mouse. The mouse_down() method also sets the self.start_pos 
    attribute to the position of the mouse at the moment the left mouse 
    button was pressed. The self.start_pos attribute is a wx.Point object, 
    which contains an x and y coordinate. The mouse_move() method is called 
    when the mouse is moved while the left mouse button is pressed down. 
    The mouse_move() method sets the self.bounding_box attribute to a wx.Rect 
    object that is defined by the coordinates of self.start_pos and the 
    current position of the mouse. The mouse_move() method also sets the 
    self.hold attribute to True. The mouse_up() method is called when the 
    left mouse button is released. The mouse_up() method sets the self.active 
    flag to False and releases the mouse. The mouse_up() method also sets 
    the self.hold attribute to False.

    2. The mouse_down() method calls the self.scr_win.CaptureMouse() method. 
    This method is used to capture the mouse so that it can be used even when 
    the mouse is outside the window. The mouse_up() method releases the mouse 
    by calling the self.scr_win.ReleaseMouse() method.

    3. The mouse_move() method is called when the mouse is moved while the 
    left mouse button is pressed down. The mouse_move() method sets the 
    self.bounding_box attribute to a wx.Rect object that is defined by the 
    coordinates of self.start_pos and the current position of the mouse. 
    """

    def on_left_mouse_event(self, event):
        if self.scr_win.IsAutoScrolling():
            self.scr_win.StopAutoScrolling()

        if self.scr_win.task_profile in ['standalone', 'rubberband_on']:
            if event.LeftDown():
                self.scr_win.SetFocus()
                self.mouse_down(event)
                # self.scr_win.CaptureMouse()
            elif event.Dragging() and (self.active or self.hold):
                self.mouse_move(event)

            elif event.LeftUp() and self.active:
                self.mouse_up(event)
                # self.scr_win.ReleaseMouse()
                # Don't think we need this...
                if self.bounding_box.GetWidth() == 0 or \
                        self.bounding_box.GetHeight() == 0:
                    self.active = False
        # Else let the scr_win.app handle the event
        else:
            self.scr_win.frame.on_left_mouse_event(event)
        self.scr_win.Refresh(eraseBackground=False)
        self.scr_win.tell_pos(event)
    # end on_left_mouse_event

    def mouse_down(self, event):
        evt_x, evt_y = evt_pos = self.convert_event_coords(event)
        if self.active:
            # If rubberband is not yet stretched, the else condition starts
            #  things off. Otherwise, if a band is rendered, the down-click
            #  may be a resizing task initiated by the user in response to
            #  clicking on one of the eight resizer handles.
            if point_in_rect(
                    evt_x, evt_y, self.bounding_box.GetX() - self.sBlk,
                    self.bounding_box.GetY() - self.sBlk,  self.sBlk * 2,
                    self.sBlk * 2):
                self.TL = True
            elif point_in_rect(
                    evt_x, evt_y,
                    self.bounding_box.GetX() +
                    self.bounding_box.GetWidth() - self.sBlk,
                    self.bounding_box.GetY() - self.sBlk, self.sBlk * 2,
                    self.sBlk * 2):
                self.TR = True
            elif point_in_rect(
                    evt_x, evt_y,
                    self.bounding_box.GetX() - self.sBlk,
                    self.bounding_box.GetY() + self.bounding_box.GetHeight()
                    - self.sBlk, self.sBlk * 2, self.sBlk * 2):
                self.BL = True
            elif point_in_rect(
                    evt_x, evt_y,
                    self.bounding_box.GetX() + self.bounding_box.GetWidth() -
                    self.sBlk,
                    self.bounding_box.GetY() + self.bounding_box.GetHeight()
                    - self.sBlk, self.sBlk * 2, self.sBlk * 2):
                self.BR = True
            elif point_in_rect(
                    evt_x, evt_y,
                    self.bounding_box.GetX() + self.bounding_box.GetWidth() /
                    2 - self.sBlk, self.bounding_box.GetY() - self.sBlk,
                    self.sBlk * 2, self.sBlk * 2):
                self.TM = True
            elif point_in_rect(
                    evt_x, evt_y,
                    self.bounding_box.GetX() + self.bounding_box.GetWidth() /
                    2 - self.sBlk,
                    self.bounding_box.GetY() + self.bounding_box.GetHeight()
                    - self.sBlk, self.sBlk * 2, self.sBlk * 2):
                self.BM = True
            elif point_in_rect(
                    evt_x, evt_y, self.bounding_box.GetX() - self.sBlk,
                    self.bounding_box.GetY() + self.bounding_box.GetHeight()
                    / 2 - self.sBlk, self.sBlk * 2, self.sBlk * 2):
                self.LM = True
            elif point_in_rect(
                    evt_x, evt_y,
                    self.bounding_box.GetX() + self.bounding_box.GetWidth() -
                    self.sBlk,
                    self.bounding_box.GetY() + self.bounding_box.GetHeight()
                    / 2 - self.sBlk, self.sBlk * 2, self.sBlk * 2):
                self.RM = True
            # If the click down in inside the existing rubberband,
            #  the rubberband rect is being dragged.
            elif point_in_rect(
                    evt_x, evt_y, self.bounding_box.GetX(),
                    self.bounding_box.GetY(), self.bounding_box.GetWidth(),
                    self.bounding_box.GetHeight()):
                self.anchor.SetX(evt_x - self.bounding_box.GetX())
                self.anchor.SetWidth = \
                    self.bounding_box.GetWidth() - self.anchor.GetX()
                self.anchor.SetY(evt_y - self.bounding_box.GetY())
                self.anchor.SetHeight = \
                    self.bounding_box.GetHeight() - self.anchor.GetY()
                self.hold = True
            # If there is an existing rubberband, a click outside of it
            #  clears it and starts a new one.
            # TODO: Check if user wants to start a new rubberband to avoid
            #  an errant click 'overwriting' the active
            elif not self.bounding_box.Contains(evt_pos):
                self.bounding_box.SetX(evt_x)
                self.bounding_box.SetY(evt_y)
                self.bounding_box.SetSize(wx.Size(0, 0))
                self.drag = True
                self.active = True
        else:
            # This is the start of the rubberbanding stretch process.
            self.bounding_box.SetX(evt_x)
            self.bounding_box.SetY(evt_y)
            self.bounding_box.SetSize(wx.Size(0, 0))
            self.drag = True
            self.active = True
    # end mouse_down

    def mouse_move(self, event):
        # Get a fresh background bitmap in the buffer before drawing rubberband
        self.scr_win.buffer = self.scr_win.scaled_img2buffer.ConvertToBitmap()
        bdc = wx.BufferedDC(None, self.scr_win.buffer)
        e_x, e_y = evt_pos = self.convert_event_coords(event)

        # Once a rubberband drag is initiated, we restrict the stretch to that
        #  one of four directions...
        if self.drag and self.active:
            # And if we are moving top-left to lower-right...
            if e_x > self.bounding_box.GetX() \
                    and e_y > self.bounding_box.GetY() \
                    and self.drag_quadrant in [0, 1]:
                if self.drag_quadrant == 0:
                    self.drag_quadrant = 1
                    self.drag_anchor = wx.Point(e_x, e_y)
                self.bounding_box.SetWidth(e_x - self.bounding_box.GetX())
                self.bounding_box.SetHeight(e_y - self.bounding_box.GetY())
            # And if we are moving bottom-right to top-left...
            elif (e_x < self.bounding_box.GetX()
                  and e_y < self.bounding_box.GetY()
                  and self.drag_quadrant == 0) \
                    or self.drag_quadrant == 2:
                if self.drag_quadrant == 0:
                    self.drag_quadrant = 2
                    self.drag_anchor = wx.Point(e_x, e_y)
                width = (self.bounding_box.GetRight() + 1) - e_x
                height = (self.bounding_box.GetBottom() + 1) - e_y
                # TODO: WTF? Should not happen...
                if (width or height) < 0:
                    print('This should not happen...')
                    return
                self.bounding_box.SetWidth(
                    (self.bounding_box.GetRight() + 1) - e_x)
                self.bounding_box.SetHeight(
                    (self.bounding_box.GetBottom() + 1) - e_y)
                self.bounding_box.SetTopLeft(evt_pos)
            # And moving from bottom-left to top-right...
            elif (e_x > self.bounding_box.GetX()
                  and e_y < self.bounding_box.GetY()
                  and self.drag_quadrant == 0) \
                    or self.drag_quadrant == 3:
                self.drag_quadrant = 3
                o_left, o_bottom = self.drag_anchor = \
                    self.bounding_box.GetBottomLeft()
                width = e_x - o_left
                height = o_bottom - e_y + 1
                self.bounding_box = wx.Rect(wx.Point(o_left, e_y), wx.Size(
                    width, height))
            # And moving from top-right to bottom-left...
            elif (e_x < self.bounding_box.GetX()
                  and e_y > self.bounding_box.GetY()
                  and self.drag_quadrant == 0) \
                    or self.drag_quadrant == 4:
                self.drag_quadrant = 4
                o_right, o_top = self.drag_anchor = \
                    self.bounding_box.GetTopRight()
                width = o_right - e_x + 1
                height = e_y - o_top + 1
                self.bounding_box = wx.Rect(wx.Point(e_x, o_top), wx.Size(
                    width, height))
            self.clear_canvas_and_draw(bdc)
            return
            # endif

        # An existing rubberband has been clicked inside its bounding box
        #  and is being dragged to new location.
        if self.hold:
            self.bounding_box.SetX(e_x - self.anchor.GetX())
            self.bounding_box.SetY(e_y - self.anchor.GetY())
            self.clear_canvas_and_draw(bdc)
            return
        # endif

        # Computations for drags of resize knobs of existing rubberband rect.
        if self.TL:
            self.bounding_box.SetWidth(
                (self.bounding_box.GetX() + self.bounding_box.GetWidth()) - e_x)
            self.bounding_box.SetHeight(
                (self.bounding_box.GetY() + self.bounding_box.GetHeight()) -
                e_y)
            self.bounding_box.SetX(e_x)
            self.bounding_box.SetY(e_y)
        elif self.BR:
            self.bounding_box.SetWidth(e_x - self.bounding_box.GetX())
            self.bounding_box.SetHeight(e_y - self.bounding_box.GetY())
        elif self.TR:
            self.bounding_box.SetHeight((self.bounding_box.GetY() +
                                         self.bounding_box.GetHeight()) - e_y)
            self.bounding_box.SetY(e_y)
            self.bounding_box.SetWidth(e_x - self.bounding_box.GetX())
        elif self.BL:
            self.bounding_box.SetWidth((self.bounding_box.GetX() +
                                        self.bounding_box.GetWidth()) - e_x)
            self.bounding_box.SetX(e_x)
            self.bounding_box.SetHeight(e_y - self.bounding_box.GetY())
        elif self.TM:
            self.bounding_box.SetHeight((self.bounding_box.GetY() +
                                         self.bounding_box.GetHeight()) - e_y)
            self.bounding_box.SetY(e_y)
        elif self.BM:
            self.bounding_box.SetHeight(e_y - self.bounding_box.GetY())
        elif self.LM:
            self.bounding_box.SetWidth((self.bounding_box.GetX() +
                                        self.bounding_box.GetWidth()) - e_x)
            self.bounding_box.SetX(e_x)
        elif self.RM:
            self.bounding_box.SetWidth(e_x - self.bounding_box.GetX())
        # endif
        self.clear_canvas_and_draw(bdc)
    # end mouse_move

    def mouse_up(self, event):
        if event:
            self.drag = False
            self.reset_resize_knobs()
            self.drag_quadrant = 0
            self.drag_anchor = wx.Point(0, 0)
            # The rubberband rect has moved or been stretched,
            #  save its 'actual' entry...
            # spec_key = self.scr_win.app.adlistings_cbox.GetStringSelection()
            # self.scr_win.app.rubberband_on_rects[spec_key]['actual'] = \
            #     copy.deepcopy(self.bounding_box)
            # print("Actual updated: " + str(self.bounding_box))
        # end mouse_up

    def reset_resize_knobs(self):
        self.TL = self.TM = self.TR = False
        self.LM = self.RM = False
        self.BL = self.BM = self.BR = False
        self.hold = False
    # end reset_resize_knobs

    def clear_canvas_and_draw(self, bdc):
        if 'wxMac' not in wx.PlatformInfo:
            bdc = wx.GCDC(bdc)
        self.draw_rubberband_with_resize_knobs(bdc)
        del bdc
        self.scr_win.Refresh(eraseBackground=False)
        # self.scr_win.Update()
    # end clear_canvas_and_draw

    def draw_rubberband_with_resize_knobs(self, bdc):
        bdc.SetPen(wx.Pen("black", 2))
        bdc.SetBrush(wx.Brush(wx.Colour(0xC0, 0xC0, 0xC0, 0x80)))
        # Redraw the rubberband rect on the fresh page image bitmap...
        bdc.DrawRectangle(self.bounding_box)
        # If neither the width nor height is negative, draw all the knobs
        if not self.bounding_box.GetWidth() <= 0 and not \
                self.bounding_box.GetHeight() <= 0:
            # Top-Left
            bdc.DrawRectangle((int(self.bounding_box.GetX() - self.sBlk),
                               int(self.bounding_box.GetY() - self.sBlk)),
                              (self.sBlk * 2, self.sBlk * 2))
            # Top-Right
            bdc.DrawRectangle((int(self.bounding_box.GetX() +
                                   self.bounding_box.GetWidth() - self.sBlk),
                               int(self.bounding_box.GetY() - self.sBlk)),
                              (self.sBlk * 2, self.sBlk * 2))
            # Bottom-Left
            bdc.DrawRectangle((int(self.bounding_box.GetX() - self.sBlk),
                               int(self.bounding_box.GetY() +
                                   self.bounding_box.GetHeight() - self.sBlk)),
                              (self.sBlk * 2, self.sBlk * 2))
            # Bottom-Right
            bdc.DrawRectangle((int(self.bounding_box.GetX() +
                                   self.bounding_box.GetWidth() - self.sBlk),
                               int(self.bounding_box.GetY() +
                                   self.bounding_box.GetHeight() - self.sBlk)),
                              (self.sBlk * 2, self.sBlk * 2))
            # Top-Mid
            bdc.DrawRectangle((int(self.bounding_box.GetX() +
                                   self.bounding_box.GetWidth() / 2 -
                                   self.sBlk),
                               int(self.bounding_box.GetY() - self.sBlk)),
                              (self.sBlk * 2, self.sBlk * 2))
            # Bottom-Mid
            bdc.DrawRectangle((int(self.bounding_box.GetX() +
                                   self.bounding_box.GetWidth() / 2 -
                                   self.sBlk),
                               int(self.bounding_box.GetY() +
                                   self.bounding_box.GetHeight() - self.sBlk)),
                              (self.sBlk * 2, self.sBlk * 2))
            # Left-Mid
            bdc.DrawRectangle((int(self.bounding_box.GetX() - self.sBlk),
                               int(self.bounding_box.GetY() +
                                   self.bounding_box.GetHeight() / 2 -
                                   self.sBlk)), (self.sBlk * 2, self.sBlk * 2))
            # Right-Mid
            bdc.DrawRectangle((int(self.bounding_box.GetX() +
                                   self.bounding_box.GetWidth() - self.sBlk),
                               int(self.bounding_box.GetY() +
                                   self.bounding_box.GetHeight() / 2 -
                                   self.sBlk)), (self.sBlk * 2, self.sBlk * 2))
        # If either width or height is negative,
        #  just draw a knob at the anchor point
        elif self.drag_anchor.Get() != (0, 0):
            # Spot the drag_anchor
            bdc.DrawRectangle((int(self.drag_anchor.Get()[0] - self.sBlk),
                               int(self.drag_anchor.Get()[1] - self.sBlk)),
                              (self.sBlk * 2, self.sBlk * 2))
    # end draw_rubberband_with_resize_knobs

    def convert_event_coords(self, event):
        newpos = self.scr_win.CalcUnscrolledPosition(
            event.GetX(), event.GetY())
        return newpos
    # end convert_event_coords
# End RubberbandRect class
