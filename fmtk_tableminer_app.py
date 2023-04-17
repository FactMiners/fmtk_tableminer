# Factminers Toolkit - Table Bounding Box Tool

import wx
import json
from pathlib import Path
import os
import copy
from PIL import Image, ImageDraw, ImageFont
import fmtk_rubberband_panel as rbp
# from wx.lib.scrolledpanel import ScrolledPanel
from fmtk_tbl_bboxxer_gui import Fmtk_tbl_bboxerGUI
from fmtk_tbl_bboxxer_gui import Fmtk_tbl_grid_col_label_dlg
from fmtk_tablegrid import Fmtk_TableGrid  # , BoundingBox

import wx.lib.inspection

from fmtk_tbl_bboxxer_gui import tb_TBL_BBOX, tb_ROW_SEP, tb_COL_SEP, tb_DEL_SEP, tb_SEL_CELL, ocr_TEXT_EDIT


# Class Fmtk_tbl_bboxerApp
class Fmtk_tbl_bboxerApp(wx.App):
    def OnInit(self):
        if 'wxMac' in wx.PlatformInfo:
            self.max_height = wx.GetDisplaySize().Height  # - 100
        else:
            self.max_height = wx.GetDisplaySize().Height - 50
        self.frame = Fmtk_tbl_bboxerAppGUI(None)
        # Add the rubberband panel
        main_sizer = self.frame.appWin_toolbar.GetContainingSizer()
        self.frame.appWin_image = rbp.RubberbandPanel(
            self.frame, self, wx.ID_ANY)
        main_sizer.Insert(1, self.frame.appWin_image, 1, wx.EXPAND | wx.LEFT)
        self.frame.appWin_image.task_profile = "no_task"
        # Set a large but arbitary max_pixel size for the panel's image
        # self.frame.appWin_image.max_pixels = 2000000
        self.frame.appWin_image.max_pixels = 0
        self.frame.appWin_image.img_scale = 1.0

        self.frame.scale_dict = {
            "10%": 0.1,
            "25%": 0.25,
            "50%": 0.5,
            "75%": 0.75,
            "100%": 1.0,
            "150%": 1.5,
            "200%": 2.0,
            "400%": 4.0,
        }
        # The app needs to know which directories to use to find document images
        # and to save the output/export JSON files
        self.frame.imagedir = Path(os.getcwd())
        self.frame.datadir = Path(os.getcwd())
        self.frame.image_list = []
        self.frame.current_image_index = None

        # TODO: This (temp?) test image is in the base project directory...
        self.src_image = Image.open('softalkv2n07mar1982_0004.jpg')
        self.frame.appWin_image.src_image = self.src_image.copy()
        self.frame.appWin_image.prep_gui()

        ####
        # Create a TableGrid object
        self.tbl_grid = Fmtk_TableGrid(self.frame.appWin_image.src_image, None)
        self.tbl_grid.draw_grid()

        self.frame.Show()
        return True


class Fmtk_tbl_bboxerAppGUI(Fmtk_tbl_bboxerGUI):

    # Toolbar Event handlers when the user clicks on a toolbar button
    def start_table_bbox_mode(self, event):
        print("start_table_bbox_mode clicked")
        self.appWin_image.task_profile = "rubberband_on"
        wx.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.when_entering_tbl_bbox_mode(event)
        event.Skip()

    def start_row_sep_mode(self, event):
        self.when_leaving_task(self.appWin_image.task_profile)
        # if self.appWin_image.task_profile == "rubberband_on":
        #     self.when_leaving_tbl_bbox_mode(event)
        print("start_row_sep_mode clicked")
        self.appWin_image.task_profile = "row_sep"
        cursor_image = wx.Image("resources/row-sep_cursor.png",
                                wx.BITMAP_TYPE_ANY)
        cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 11)
        cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 20)
        cursor = wx.Cursor(cursor_image)
        wx.SetCursor(cursor)
        self.when_entering_any_sep_mode(event)
        event.Skip()

    def start_col_sep_mode(self, event):
        self.when_leaving_task(self.appWin_image.task_profile)
        print("start_col_sep_mode clicked")
        self.appWin_image.task_profile = "col_sep"
        cursor_image = wx.Image("resources/col-sep_cursor.png",
                                wx.BITMAP_TYPE_ANY)
        cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 0)
        cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 11)
        cursor = wx.Cursor(cursor_image)
        wx.SetCursor(cursor)
        self.when_entering_any_sep_mode(event)
        event.Skip()

    def start_del_sep_mode(self, event):
        self.when_leaving_task(self.appWin_image.task_profile)
        print("start_del_sep_mode clicked")
        self.appWin_image.task_profile = "del_sep"
        # TODO: Set cursor to a crosshair
        wx.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.when_entering_any_sep_mode(event)
        event.Skip()

    def start_sel_cell_mode(self, event):
        self.when_leaving_task(self.appWin_image.task_profile)
        print("start_sel_cell_mode clicked")
        self.appWin_image.task_profile = "sel_cell"
        self.ocr_edit_ui("on")
        self.nlpx_edit_ui("on")
        self.Layout()
        wx.SetCursor(wx.Cursor(wx.CURSOR_QUESTION_ARROW))
        self.when_entering_any_sep_mode(event)
        event.Skip()

    # When the user changes the zoom level scale factor
    def on_scale_change(self, event):
        print("Scale_changed: ", self.tbar_zoom_size.GetStringSelection())
        current_scale = self.appWin_image.img_scale
        # First, get the current bounding box from either the rubberband or
        # the table grid, and scale it to the scr_image size
        if self.appWin_image.task_profile == "rubberband_on":
            src_bbox = self.appWin_image.src_scale_bbox(
                self.appWin_image.rubberband.bounding_box)
        elif self.appWin_image.task_profile != "rubberband_on":
            src_bbox = self.appWin_image.scale_bbox(
                self.appWin_image.app.tbl_grid.get_bbox())
        else:
            # This should not happen...
            print("ERROR: on_scale_change: No bounding box found")
            src_bbox = None
        print("Source bbox: ", src_bbox)
        # Then, load the image at the new scale
        self.appWin_image.img_scale = self.scale_dict[
            self.tbar_zoom_size.GetStringSelection()]
        self.appWin_image.load_image()
        # Then, scale the bounding box back to the new image
        # size and set it as the new bounding box
        if src_bbox != None:
            scaled_bbox = self.appWin_image.scale_bbox(src_bbox)
            if self.appWin_image.task_profile == "rubberband_on":
                self.appWin_image.rubberband.bounding_box = scaled_bbox
        # Finally, redraw the image
        if self.appWin_image.task_profile == "rubberband_on":
            print("Scaled bbox: ", scaled_bbox)
            # self.appWin_image.rubberband.bounding_box = scaled_bbox
            dc = wx.BufferedDC(None, self.appWin_image.buffer)
            self.appWin_image.rubberband.clear_canvas_and_draw(dc)
        else:
            self.appWin_image.load_image()
            self.appWin_image.app.tbl_grid.draw_grid()
            self.appWin_image.Refresh()
        event.Skip()

    # Event handler helpers for the RubberbandPanel to
    # handle behavior differences between the different
    # toolbar modes
    def on_tbar_tool_change(self, event):
        print("on_tbar_tool_changed")
        if event.GetId() == tb_TBL_BBOX and self.appWin_image.task_profile != "rubberband_on":
            self.start_table_bbox_mode(event)
        elif event.GetId() == tb_ROW_SEP and self.appWin_image.task_profile != "row_sep":
            self.start_row_sep_mode(event)
        elif event.GetId() == tb_COL_SEP and self.appWin_image.task_profile != "col_sep":
            self.start_col_sep_mode(event)
        elif event.GetId() == tb_DEL_SEP and self.appWin_image.task_profile != "del_sep":
            self.start_del_sep_mode(event)
        elif event.GetId() == tb_SEL_CELL and self.appWin_image.task_profile != "sel_cell":
            self.start_sel_cell_mode(event)
        event.Skip()

    def when_leaving_tbl_bbox_mode(self, event):
        # Transfer the bounding box to the table grid
        src_scaled_bbox = self.appWin_image.src_scale_bbox(
            self.appWin_image.rubberband.bounding_box)
        self.appWin_image.app.tbl_grid.set_bbox(src_scaled_bbox)
        # If the rubberband bounding box is different from the
        # bbox_checkpoint, then the user has changed the bounding
        # box, so we need to invalidate the table grid row and
        # column lines so that they will be recalculated.
        if src_scaled_bbox != self.appWin_image.bbox_checkpoint:
            self.appWin_image.app.tbl_grid.invalidate_row_lines()
            self.appWin_image.app.tbl_grid.invalidate_column_lines()

    def when_entering_tbl_bbox_mode(self, event):
        # Transfer the bounding box to the table grid to
        # initialize the rubberband bounding_box
        self.appWin_image.src_image = self.appWin_image.app.src_image.copy()
        self.appWin_image.load_image()
        self.appWin_image.bbox_checkpoint = self.appWin_image.app.tbl_grid.get_bbox()
        scaled_bbox = self.appWin_image.scale_bbox(
            self.appWin_image.bbox_checkpoint)
        rb_rect = scaled_bbox
        self.appWin_image.rubberband.bounding_box = rb_rect
        dc = wx.BufferedDC(None, self.appWin_image.buffer)
        self.appWin_image.rubberband.clear_canvas_and_draw(dc)
        event.Skip()

    def when_entering_any_sep_mode(self, event):
        if self.appWin_image.task_profile != "rubberband_on":
            self.appWin_image.src_image = self.appWin_image.app.src_image.copy()
            self.appWin_image.load_image()
            self.appWin_image.app.tbl_grid.draw_grid()
            self.appWin_image.src_image = self.appWin_image.app.tbl_grid.return_image()
            self.appWin_image.load_image()
            self.appWin_image.app.tbl_grid.draw_grid()
            self.appWin_image.Refresh()
        event.Skip()

    def when_leaving_task(self, task_profile):
        if task_profile == "rubberband_on":
            # Transfer the bounding box to the table grid
            src_scaled_bbox = self.appWin_image.src_scale_bbox(
                self.appWin_image.rubberband.bounding_box)
            self.appWin_image.app.tbl_grid.set_bbox(src_scaled_bbox)
            # If the rubberband bounding box is different from the
            # bbox_checkpoint, then the user has changed the bounding
            # box, so we need to invalidate the table grid row and
            # column lines so that they will be recalculated.
            if src_scaled_bbox != self.appWin_image.bbox_checkpoint:
                self.appWin_image.app.tbl_grid.invalidate_row_lines()
                self.appWin_image.app.tbl_grid.invalidate_column_lines()
        elif task_profile == "row_sep":
            pass
        elif task_profile == "col_sep":
            pass
        elif task_profile == "del_sep":
            pass
        elif task_profile == "sel_cell":
            self.ocr_edit_ui("off")
            self.nlpx_edit_ui("off")

    def on_left_mouse_event(self, event):
        # Handle left click events in the RubberbandPanel when
        # the app is in any mode other than "rubberband_on"
        if event.LeftDClick():
            self.ocr_lock_text.SetValue(True)
            self.on_lock_ocr_text(event)
        elif event.LeftDown():
            evt_x, evt_y = evt_pos = self.appWin_image.rubberband.convert_event_coords(
                event)
            unscaled_pt = self.appWin_image.scale_point(wx.Point(evt_pos))
            if not self.appWin_image.app.tbl_grid.is_point_in_bbox(unscaled_pt):
                pass
            elif self.appWin_image.task_profile == "row_sep":
                offset = self.appWin_image.app.tbl_grid.img_point_to_table_offset(
                    unscaled_pt, "row")
                self.appWin_image.app.tbl_grid.add_row_offset(offset)
            elif self.appWin_image.task_profile == "col_sep":
                offset = self.appWin_image.app.tbl_grid.img_point_to_table_offset(
                    unscaled_pt, "col")
                self.appWin_image.app.tbl_grid.add_column_offset(offset)
            elif self.appWin_image.task_profile == "del_sep":
                self.appWin_image.app.tbl_grid.delete_near_row_or_column_sep(
                    unscaled_pt)
            elif self.appWin_image.task_profile == "sel_cell":
                # If the ocrgt text is modified, then save it
                # if self.ocr_text_edit.IsModified():
                #     self.ocr_lock_text.SetValue(True)
                #     self.on_lock_ocr_text(event)
                #     self.ocr_text_edit.SetModified(False)
                self.appWin_image.app.tbl_grid.compute_cell_bboxes()
                row_col = self.appWin_image.app.tbl_grid.select_cell_at_point(
                    unscaled_pt)
                if row_col is not False:
                    self.refresh_text_edit_panels(row_col)
            # Finally, redraw the image
            self.appWin_image.app.tbl_grid.draw_grid()
            self.appWin_image.src_image = self.appWin_image.app.tbl_grid.return_image()
            self.appWin_image.load_image()
            self.appWin_image.Refresh()
        event.Skip()

    def refresh_text_edit_panels(self, row_col):
        ocrgt_text, ocrgt_lock = self.appWin_image.app.tbl_grid.get_cell_ocrgt_text(
            row_col[0], row_col[1])
        if ocrgt_lock:
            self.ocr_lock_text.SetValue(ocrgt_lock)
            self.ocr_text_edit.SetValue(ocrgt_text)
            self.ocr_text_edit.Disable()
            if not self.nlpx_lock_text:
                self.nlpx_text_edit.SetValue(ocrgt_text)
                self.nlpx_lock_text.SetValue(ocrgt_lock)
                self.nlpx_text_edit.Disable()
        elif ocrgt_text not in [None, ""]:
            self.ocr_lock_text.SetValue(ocrgt_lock)
            self.ocr_text_edit.SetValue(ocrgt_text)
            self.ocr_text_edit.Enable()
            self.ocr_text_edit.SetFocus()
        else:
            self.ocr_lock_text.SetValue(ocrgt_lock)
            self.ocr_text_edit.SetValue("")
            self.ocr_text_edit.Enable()
            self.ocr_text_edit.SetFocus()
        # Handle similarly the nlpx panel
        nlpx_text, nlpx_lock = self.appWin_image.app.tbl_grid.get_cell_nlpx_text(
            row_col[0], row_col[1])
        if nlpx_lock:
            self.nlpx_lock_text.SetValue(nlpx_lock)
            self.nlpx_text_edit.SetValue(nlpx_text)
            self.nlpx_text_edit.Disable()
        elif nlpx_text not in [None, ""]:
            self.nlpx_lock_text.SetValue(nlpx_lock)
            self.nlpx_text_edit.SetValue(nlpx_text)
            self.nlpx_text_edit.Enable()
            self.nlpx_text_edit.SetFocus()
        else:
            self.nlpx_lock_text.SetValue(nlpx_lock)
            self.nlpx_text_edit.SetValue("")
            self.nlpx_text_edit.Enable()
            self.nlpx_text_edit.SetFocus()

    def on_column_labels_click(self, event):
        print("on_column_labels_click")
        dlg = Tbl_grid_column_dlg(self)
        if dlg.ShowModal() == wx.ID_OK:
            # Transfer the column labels to the table grid
            dlg.on_save_column_labels_dlg(event)
            # Finally, redraw the image
            self.appWin_image.app.tbl_grid.draw_grid()
            self.appWin_image.src_image = self.appWin_image.app.tbl_grid.return_image()
            self.appWin_image.load_image()
            self.appWin_image.Refresh()
        event.Skip()

    def ocr_edit_ui(self, onoff):
        if onoff == "on":
            self.ocr_edit_label.Show()
            # self.ocr_reread_btn.Show()
            self.ocr_lock_text.Show()
            self.ocr_text_edit.Show()
            self.ocr_edit_tip.Show()
        elif onoff == "off":
            self.ocr_edit_label.Hide()
            # self.ocr_reread_btn.Hide()
            self.ocr_lock_text.Hide()
            self.ocr_text_edit.Hide()
            self.ocr_edit_tip.Hide()
        self.Layout()

    def nlpx_edit_ui(self, onoff):
        if onoff == "on":
            self.nlpx_edit_label.Show()
            self.nlpx_copy_ocr_text_btn.Show()
            self.nlpx_lock_text.Show()
            self.nlpx_text_edit.Show()
            self.nlpx_tag.Show()
        elif onoff == "off":
            self.nlpx_edit_label.Hide()
            self.nlpx_copy_ocr_text_btn.Hide()
            self.nlpx_lock_text.Hide()
            self.nlpx_text_edit.Hide()
            self.nlpx_tag.Hide()
        self.Layout()

    def on_open_nlpx_editor(self, event):
        if self.nlpx_text_edit.IsShown():
            self.nlpx_edit_ui("off")
        else:
            self.nlpx_edit_ui("on")
            self.nlpx_text_edit.SetValue("")
            row_num, col_num = self.appWin_image.app.tbl_grid.cell_to_highlight
            nlpx_text, nlpx_lock = self.appWin_image.app.tbl_grid.get_cell_nlpx_text(
                row_num, col_num)
            self.nlpx_lock_text.SetValue(nlpx_lock)
            self.nlpx_text_edit.SetValue(nlpx_text)
            self.nlpx_text_edit.SetFocus()
        event.Skip()

    def on_copy_ocr_text_to_nlpx(self, event):
        if not self.nlpx_lock_text.GetValue():
            self.nlpx_text_edit.SetValue(self.ocr_text_edit.GetValue())
            self.Refresh()
        event.Skip()

    def on_lock_ocr_text(self, event):
        lock_state = self.ocr_lock_text.GetValue()
        self.appWin_image.app.tbl_grid.set_cell_ocrgt_lock(lock_state)
        row_num = self.appWin_image.app.tbl_grid.cell_to_highlight[0]
        col_num = self.appWin_image.app.tbl_grid.cell_to_highlight[1]
        if lock_state:
            self.appWin_image.app.tbl_grid.cells_edited = True
            self.appWin_image.app.tbl_grid.cell_ocrgt_texts[row_num][col_num] = self.ocr_text_edit.GetValue(
            )
            self.ocr_text_edit.Disable()
            self.appWin_image.app.tbl_grid.set_cell_nlpx_lock(lock_state)
            self.appWin_image.app.tbl_grid.cell_nlpx_texts[row_num][col_num] = self.nlpx_text_edit.GetValue(
            )
            self.nlpx_lock_text.SetValue(True)
            self.nlpx_text_edit.Disable()
        else:
            self.ocr_reread_btn.Show()
            self.Layout()
            self.ocr_text_edit.Enable()
            self.ocr_text_edit.SetFocus()
        event.Skip()

    def on_lock_nlpx_text(self, event):
        lock_state = self.nlpx_lock_text.GetValue()
        self.appWin_image.app.tbl_grid.set_cell_nlpx_lock(lock_state)
        row_num = self.appWin_image.app.tbl_grid.cell_to_highlight[0]
        col_num = self.appWin_image.app.tbl_grid.cell_to_highlight[1]
        if lock_state:
            self.appWin_image.app.tbl_grid.cells_edited = True
            self.appWin_image.app.tbl_grid.cell_nlpx_texts[row_num][col_num] = self.nlpx_text_edit.GetValue(
            )
            self.nlpx_text_edit.Disable()
        else:
            self.nlpx_text_edit.Enable()
            self.nlpx_text_edit.SetFocus()
        event.Skip()

    def on_insert_nlpx_tag(self, event):
        if self.nlpx_text_edit.Enabled:
            sel_index = self.nlpx_tag.GetSelection()
            tag = event.GetEventObject().GetString(sel_index)
            start_tag = "<" + tag + ">"
            end_tag = "</" + tag + ">"
            sel_text = self.nlpx_text_edit.GetStringSelection()
            start, end = self.nlpx_text_edit.GetSelection()
            if sel_text:
                self.nlpx_text_edit.Replace(
                    start, end, start_tag + sel_text + end_tag)
            else:
                self.nlpx_text_edit.WriteText(start_tag + end_tag)
            self.nlpx_text_edit.SetFocus()
        event.Skip()

    def on_lock_ocr_when_edited(self, event):
        self.ocr_lock_text.SetValue(True)
        self.on_lock_ocr_text(event)
        event.Skip()

    def on_lock_nlpx_when_edited(self, event):
        self.nlpx_lock_text.SetValue(True)
        self.on_lock_nlpx_text(event)
        event.Skip()

    def on_text_edited(self, event):
        event.EventObject.MarkDirty()
        event.Skip()

    def on_reread_ocr(self, event):
        row_col = self.appWin_image.app.tbl_grid.cell_to_highlight
        if row_col is not False:
            self.refresh_text_edit_panels(row_col)
        event.Skip()

    def on_menu_settings(self, event):
        event.Skip()

    def on_set_image_directory(self, event):
        dlg = wx.DirDialog(self, message="Choose a Document Image folder")
        if dlg.ShowModal() == wx.ID_OK:
            self.imagedir = dlg.GetPath()
        dlg.Destroy()
        print(self.imagedir)
        image_files = sorted(os.listdir(self.imagedir))
        for file in image_files:
            if os.path.splitext(file)[1].lower() in ['.jpg', '.jpeg', '.png', '.tif', '.tiff']:
                self.image_list.append(file)
        # print(self.image_list)
        self.current_image_index = 0
        current_image = self.imagedir + "/" + self.image_list[self.current_image_index]
        print(current_image)
        self.appWin_image.src_image = Image.open(current_image)
        self.appWin_image.image = self.appWin_image.src_image
        self.appWin_image.load_image()
        event.Skip()

    def on_set_data_directory(self, event):
        dlg = wx.DirDialog(self, message="Choose a Data Export folder")
        if dlg.ShowModal() == wx.ID_OK:
            self.datadir = dlg.GetPath()
        dlg.Destroy()
        print(self.datadir)
        event.Skip()

    def on_quit_app(self, event):
        event.Skip()


class Tbl_grid_column_dlg(Fmtk_tbl_grid_col_label_dlg):
    def __init__(self, parent):
        Fmtk_tbl_grid_col_label_dlg.__init__(self, parent)
        self.parent = parent
        self.app = self.parent.appWin_image.app

    # Virtual event handlers
    def on_save_column_labels_dlg(self, event):
        # Transfer the column labels to the table grid
        num_columns = self.app.tbl_grid.get_number_of_columns()
        for i in range(num_columns):
            self.app.tbl_grid.set_column_label(
                i + 1, self.tbl_grid_props.GetCellValue(i, 0))
        self.app.tbl_grid.show_labels = self.chk_show_labels.GetValue()
        self.Close()
        event.Skip()

    def on_column_label_dlg_init(self, event):
        num_columns = self.app.tbl_grid.get_number_of_columns()
        self.tbl_grid_props.InsertRows(numRows=num_columns)
        for i in range(num_columns):
            col_num = i + 1
            col_label = self.app.tbl_grid.get_column_label(col_num)
            self.tbl_grid_props.SetCellValue(i, 0, col_label)
        self.on_resize_adjust_column_label(event)
        self.tbl_grid_props.SetFocus()
        self.chk_show_labels.SetValue(self.app.tbl_grid.show_labels)
        event.Skip()

    def on_resize_adjust_column_label(self, event):
        self.tbl_grid_props.SetColSize(0, self.GetSize()[0] - 40)
        event.Skip()

    def on_cancel_column_labels_dlg(self, event):
        self.Close()
        event.Skip()


# Main
if __name__ == "__main__":
    app = Fmtk_tbl_bboxerApp(0)
    # app.SetAppName("Fmtk TableMiner")
    # wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()
