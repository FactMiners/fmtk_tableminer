# Factminers Toolkit - TableMiner Tool
#
# Copyright 2023 Jim Salmons on behalf of the FactMiners.org
# Digital Humanities project focused on the development of a
# Ground-Truth Storage format providing an integrated complex
# document structure and content depiction model for print era
# commercial magazines.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http: // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language
# governing permissions and limitations under the License.
#

import wx
import json
import yaml
import xmltodict as xtd
from pathlib import Path
import os
import copy
from PIL import Image, ImageDraw, ImageFont
import fmtk_rubberband_panel as rbp
from fmtk_tableminer_gui import FmtkTableMinerFrame
from fmtk_tableminer_gui import FmtkTableMinerProjectDialog
from fmtk_tablegrid import FmtkTableGrid

import wx.lib.inspection

from fmtk_tableminer_gui import tb_TBL_BBOX, tb_ROW_SEP, tb_COL_SEP, tb_DEL_SEP, tb_SEL_CELL, ocr_TEXT_EDIT


# Class FmtkTableMinerApp
class FmtkTableMinerApp(wx.App):
    def OnInit(self):
        if 'wxMac' in wx.PlatformInfo:
            self.max_height = wx.GetDisplaySize().Height  # - 100
        else:
            self.max_height = wx.GetDisplaySize().Height - 50
        self.frame = FmtkTableMinerGui(None)
        self.SetTopWindow(self.frame)
        self.frame.app = self

        self.frame.Show()
        if wx.MessageBox("Do you want to load an existing project?",
                         "TableMiner Launch",
                         wx.YES_NO | wx.NO_DEFAULT) == wx.YES:
            self.frame.load_project_spec()

        return True


class FmtkTableMinerGui(FmtkTableMinerFrame):
    def __init__(self, parent):
        FmtkTableMinerFrame.__init__(self, parent)
        self.app = parent
        self.project_spec_file = ""
        self.project_spec = {}
        self.project_spec["title"] = "Untitled"
        self.project_spec["description"] = ""
        self.project_spec["image_dir"] = Path(os.getcwd())
        self.project_spec["data_dir"] = Path(os.getcwd())
        self.project_spec["column_labels"] = []
        self.project_spec["show_column_labels"] = True
        self.project_spec["nlp_tags"] = []
        self.project_spec["semicolon_delimiters"] = False
        self.project_spec["export_formats"] = ["json", "xml"]
        self.project_spec["image_list"] = []
        self.project_spec["current_image_index"] = None
        self.project_spec["done_image_list"] = []

        self.scale_dict = {
            "10%": 0.1,
            "25%": 0.25,
            "50%": 0.5,
            "75%": 0.75,
            "100%": 1.0,
            "150%": 1.5,
            "200%": 2.0,
            "400%": 4.0,
        }
        # Add the rubberband panel
        main_sizer = self.toolbar.GetContainingSizer()
        self.image_panel = rbp.RubberbandPanel(
            self, wx.ID_ANY)
        main_sizer.Insert(1, self.image_panel, 1, wx.EXPAND | wx.LEFT)
        self.image_panel.task_profile = "no_task"
        self.image_panel.Bind(wx.EVT_ENTER_WINDOW,
                              self.on_image_panel_hover_enter)
        self.tool_cursor = wx.Cursor(wx.CURSOR_ARROW)
        # Set a large but arbitary max_pixel size for the panel's image
        # self.image_panel.max_pixels = 2000000
        self.image_panel.max_pixels = 0
        self.image_panel.img_scale = 1.0
        # TODO: This (temp?) test image is in the base project directory...
        self.src_image = Image.open('softalkv2n07mar1982_0004.jpg')
        self.image_panel.src_image = self.src_image.copy()
        self.image_panel.prep_gui()

        ####
        # Create a TableGrid object
        self.tbl_grid = FmtkTableGrid(self.image_panel.src_image, None)
        self.tbl_grid.draw_grid()

    # Toolbar Event handlers when the user clicks on a toolbar button
    def start_table_bbox_mode(self, event):
        # print("start_table_bbox_mode clicked")
        self.when_leaving_task(self.image_panel.task_profile)
        self.image_panel.task_profile = "rubberband_on"
        wx.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.when_entering_tbl_bbox_mode(event)
        event.Skip()

    def start_row_sep_mode(self, event):
        self.when_leaving_task(self.image_panel.task_profile)
        # if self.image_panel.task_profile == "rubberband_on":
        #     self.when_leaving_tbl_bbox_mode(event)
        # print("start_row_sep_mode clicked")
        self.image_panel.task_profile = "row_sep"
        cursor_image = wx.Image("resources/row-sep_cursor.png",
                                wx.BITMAP_TYPE_ANY)
        cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 11)
        cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 20)
        cursor = wx.Cursor(cursor_image)
        wx.SetCursor(cursor)
        # self.tool_cursor = cursor
        self.when_entering_any_sep_mode(event)
        event.Skip()

    def start_col_sep_mode(self, event):
        self.when_leaving_task(self.image_panel.task_profile)
        # print("start_col_sep_mode clicked")
        self.image_panel.task_profile = "col_sep"
        cursor_image = wx.Image("resources/col-sep_cursor.png",
                                wx.BITMAP_TYPE_ANY)
        cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 0)
        cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 11)
        cursor = wx.Cursor(cursor_image)
        wx.SetCursor(cursor)
        # self.tool_cursor = cursor
        self.when_entering_any_sep_mode(event)
        event.Skip()

    def start_del_sep_mode(self, event):
        self.when_leaving_task(self.image_panel.task_profile)
        # print("start_del_sep_mode clicked")
        self.image_panel.task_profile = "del_sep"
        # TODO: Set cursor to a crosshair
        wx.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.when_entering_any_sep_mode(event)
        event.Skip()

    def start_sel_cell_mode(self, event):
        self.when_leaving_task(self.image_panel.task_profile)
        # print("start_sel_cell_mode clicked")
        self.image_panel.task_profile = "sel_cell"
        self.ocr_edit_ui("on")
        self.nlpx_edit_ui("on")
        self.Layout()
        wx.SetCursor(wx.Cursor(wx.CURSOR_QUESTION_ARROW))
        self.tool_cursor = wx.Cursor(wx.CURSOR_QUESTION_ARROW)
        self.when_entering_any_sep_mode(event)
        event.Skip()

    # When the user changes the zoom level scale factor
    def on_scale_change(self, event):
        # print("Scale_changed: ", self.tbar_zoom_size.GetStringSelection())
        current_scale = self.image_panel.img_scale
        # First, get the current bounding box from either the rubberband or
        # the table grid, and scale it to the scr_image size
        if self.image_panel.task_profile == "rubberband_on":
            src_bbox = self.image_panel.src_scale_bbox(
                self.image_panel.rubberband.bounding_box)
        elif self.image_panel.task_profile != "rubberband_on":
            src_bbox = self.image_panel.scale_bbox(
                self.tbl_grid.get_bbox())
        else:
            # This should not happen...
            print("ERROR: on_scale_change: No bounding box found")
            src_bbox = None
        print("Source bbox: ", src_bbox)
        # Then, load the image at the new scale
        self.image_panel.img_scale = self.scale_dict[
            self.tbar_zoom_size.GetStringSelection()]
        self.image_panel.load_image()
        # Then, scale the bounding box back to the new image
        # size and set it as the new bounding box
        if src_bbox != None:
            scaled_bbox = self.image_panel.scale_bbox(src_bbox)
            if self.image_panel.task_profile == "rubberband_on":
                self.image_panel.rubberband.bounding_box = scaled_bbox
        # Finally, redraw the image
        if self.image_panel.task_profile == "rubberband_on":
            print("Scaled bbox: ", scaled_bbox)
            # self.image_panel.rubberband.bounding_box = scaled_bbox
            dc = wx.BufferedDC(None, self.image_panel.buffer)
            self.image_panel.rubberband.clear_canvas_and_draw(dc)
        else:
            self.image_panel.load_image()
            self.tbl_grid.draw_grid()
            self.image_panel.Refresh()
        event.Skip()

    # Event handler helpers for the RubberbandPanel to
    # handle behavior differences between the different
    # toolbar modes
    def on_tbar_tool_change(self, event):
        print("on_tbar_tool_changed")
        if event.GetId() == tb_TBL_BBOX and self.image_panel.task_profile != "rubberband_on":
            self.start_table_bbox_mode(event)
        elif event.GetId() == tb_ROW_SEP and self.image_panel.task_profile != "row_sep":
            self.start_row_sep_mode(event)
        elif event.GetId() == tb_COL_SEP and self.image_panel.task_profile != "col_sep":
            self.start_col_sep_mode(event)
        elif event.GetId() == tb_DEL_SEP and self.image_panel.task_profile != "del_sep":
            self.start_del_sep_mode(event)
        elif event.GetId() == tb_SEL_CELL and self.image_panel.task_profile != "sel_cell":
            self.start_sel_cell_mode(event)
        event.Skip()

    def on_tbar_hover_enter(self, event):
        self.image_panel.task_limbo = self.image_panel.task_profile
        # self.tool_cursor = self.GetCursor()
        wx.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        event.Skip()

    def on_image_panel_hover_enter(self, event):
        match self.image_panel.task_profile:
            case "rubberband_on":
                wx.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
            case "row_sep":
                cursor_image = wx.Image("resources/row-sep_cursor.png",
                                        wx.BITMAP_TYPE_ANY)
                cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 11)
                cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 20)
                cursor = wx.Cursor(cursor_image)
                wx.SetCursor(cursor)
            case "col_sep":
                cursor_image = wx.Image("resources/col-sep_cursor.png",
                                        wx.BITMAP_TYPE_ANY)
                cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 0)
                cursor_image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 11)
                cursor = wx.Cursor(cursor_image)
                wx.SetCursor(cursor)
            case "del_sep":
                wx.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
            case "sel_cell":
                wx.SetCursor(wx.Cursor(wx.CURSOR_QUESTION_ARROW))
            case _:
                wx.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        event.Skip()

    def when_leaving_tbl_bbox_mode(self, event):
        # Transfer the bounding box to the table grid
        src_scaled_bbox = self.image_panel.src_scale_bbox(
            self.image_panel.rubberband.bounding_box)
        self.tbl_grid.set_bbox(src_scaled_bbox)
        # If the rubberband bounding box is different from the
        # bbox_checkpoint, then the user has changed the bounding
        # box, so we need to invalidate the table grid row and
        # column lines so that they will be recalculated.
        if src_scaled_bbox != self.image_panel.bbox_checkpoint:
            self.tbl_grid.invalidate_row_lines()
            self.tbl_grid.invalidate_column_lines()

    def when_entering_tbl_bbox_mode(self, event):
        # Transfer the bounding box to the table grid to
        # initialize the rubberband bounding_box
        self.image_panel.src_image = self.src_image.copy()
        self.image_panel.load_image()
        self.image_panel.bbox_checkpoint = self.tbl_grid.get_bbox()
        scaled_bbox = self.image_panel.scale_bbox(
            self.image_panel.bbox_checkpoint)
        rb_rect = scaled_bbox
        self.image_panel.rubberband.bounding_box = rb_rect
        dc = wx.BufferedDC(None, self.image_panel.buffer)
        self.image_panel.rubberband.clear_canvas_and_draw(dc)
        event.Skip()

    def when_entering_any_sep_mode(self, event):
        if self.image_panel.task_profile != "rubberband_on":
            self.image_panel.src_image = self.src_image.copy()
            self.image_panel.load_image()
            self.tbl_grid.draw_grid()
            self.image_panel.src_image = self.tbl_grid.return_image()
            self.image_panel.load_image()
            self.tbl_grid.draw_grid()
            self.image_panel.Refresh()
        event.Skip()

    def when_leaving_task(self, task_profile):
        if task_profile == "rubberband_on":
            # Transfer the bounding box to the table grid
            src_scaled_bbox = self.image_panel.src_scale_bbox(
                self.image_panel.rubberband.bounding_box)
            self.tbl_grid.set_bbox(src_scaled_bbox)
            # If the rubberband bounding box is different from the
            # bbox_checkpoint, then the user has changed the bounding
            # box, so we need to invalidate the table grid row and
            # column lines so that they will be recalculated.
            if src_scaled_bbox != self.image_panel.bbox_checkpoint:
                self.tbl_grid.invalidate_row_lines()
                self.tbl_grid.invalidate_column_lines()
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
            evt_x, evt_y = evt_pos = \
                self.image_panel.rubberband.convert_event_coords(event)
            unscaled_pt = self.image_panel.scale_point(wx.Point(evt_pos))
            if not self.tbl_grid.is_point_in_bbox(unscaled_pt):
                pass
            elif self.image_panel.task_profile == "row_sep":
                offset = self.tbl_grid.img_point_to_table_offset(
                    unscaled_pt, "row")
                self.tbl_grid.add_row_offset(offset)
            elif self.image_panel.task_profile == "col_sep":
                offset = self.tbl_grid.img_point_to_table_offset(
                    unscaled_pt, "col")
                self.tbl_grid.add_column_offset(offset)
            elif self.image_panel.task_profile == "del_sep":
                self.tbl_grid.delete_near_row_or_column_sep(unscaled_pt)
            elif self.image_panel.task_profile == "sel_cell":
                # If the ocrgt text is modified, then save it
                # if self.ocr_text_edit.IsModified():
                #     self.ocr_lock_text.SetValue(True)
                #     self.on_lock_ocr_text(event)
                #     self.ocr_text_edit.SetModified(False)
                self.tbl_grid.compute_cell_bboxes()
                row_col = self.tbl_grid.select_cell_at_point(
                    unscaled_pt)
                if row_col is not False:
                    self.refresh_text_edit_panels(row_col)
            # Finally, redraw the image
            self.tbl_grid.draw_grid()
            self.image_panel.src_image = self.tbl_grid.return_image()
            self.image_panel.load_image()
            self.image_panel.Refresh()
        event.Skip()

    def refresh_text_edit_panels(self, row_col):
        ocrgt_text, ocrgt_lock = self.tbl_grid.get_cell_ocrgt_text(
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
        nlpx_text, nlpx_lock = self.tbl_grid.get_cell_nlpx_text(
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
            self.ocr_text_edit.SetValue("")
            self.ocr_lock_text.SetValue(False)
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
            self.nlpx_lock_text.SetValue(False)
            self.nlpx_text_edit.SetValue("")
            self.nlpx_text_edit.Hide()
            self.nlpx_tag.Hide()
        self.Layout()

    def on_open_nlpx_editor(self, event):
        if self.nlpx_text_edit.IsShown():
            self.nlpx_edit_ui("off")
        else:
            self.nlpx_edit_ui("on")
            self.nlpx_text_edit.SetValue("")
            row_num, col_num = self.tbl_grid.cell_to_highlight
            nlpx_text, nlpx_lock = self.tbl_grid.get_cell_nlpx_text(
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
        self.tbl_grid.set_cell_ocrgt_lock(lock_state)
        row_num = self.tbl_grid.cell_to_highlight[0]
        col_num = self.tbl_grid.cell_to_highlight[1]
        if lock_state:
            self.tbl_grid.cells_edited = True
            self.tbl_grid.cell_ocrgt_texts[row_num][col_num] = \
                self.ocr_text_edit.GetValue()
            self.ocr_text_edit.Disable()
            self.tbl_grid.set_cell_nlpx_lock(lock_state)
            self.tbl_grid.cell_nlpx_texts[row_num][col_num] = \
                self.nlpx_text_edit.GetValue()
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
        self.tbl_grid.set_cell_nlpx_lock(lock_state)
        row_num = self.tbl_grid.cell_to_highlight[0]
        col_num = self.tbl_grid.cell_to_highlight[1]
        if lock_state:
            self.tbl_grid.cells_edited = True
            self.tbl_grid.cell_nlpx_texts[row_num][col_num] = \
                self.nlpx_text_edit.GetValue()
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
        row_col = self.tbl_grid.cell_to_highlight
        if row_col is not False:
            self.refresh_text_edit_panels(row_col)
        event.Skip()

    def on_menu_settings(self, event):
        event.Skip()

    # def on_set_image_directory(self, event):
    #     dlg = wx.DirDialog(self, message="Choose a Document Image folder")
    #     if dlg.ShowModal() == wx.ID_OK:
    #         self.imagedir = dlg.GetPath()
    #     dlg.Destroy()
    #     print(self.imagedir)
    #     image_files = sorted(os.listdir(self.imagedir))
    #     for file in image_files:
    #         if os.path.splitext(file)[1].lower() in ['.jpg', '.jpeg', '.png', '.tif', '.tiff']:
    #             self.image_list.append(file)
    #     # print(self.image_list)
    #     self.current_image_index = 0
    #     current_image = self.imagedir + "/" + \
    #         self.image_list[self.current_image_index]
    #     print(current_image)
    #     self.src_image = Image.open(current_image)
    #     self.image_panel.src_image = self.src_image.copy()
    #     # self.image_panel.image = self.image_panel.src_image
    #     self.image_panel.load_image()
    #     event.Skip()

    # def on_set_data_directory(self, event):
    #     dlg = wx.DirDialog(self, message="Choose a Data Export folder")
    #     if dlg.ShowModal() == wx.ID_OK:
    #         self.datadir = dlg.GetPath()
    #     dlg.Destroy()
    #     print(self.datadir)
    #     event.Skip()

    def on_prior_image(self, event):
        prior_index = self.project_spec['current_image_index'] - 1
        self.project_spec['current_image_index'] = prior_index
        self.load_current_image(event)

    def on_next_image(self, event):
        # Save the current table_spec before moving to the next image
        self.save_table_spec()
        self.tbl_grid.clear_grid()
        self.table_spec = {}
        next_index = self.project_spec['current_image_index'] + 1
        self.project_spec['current_image_index'] = next_index
        self.load_current_image(event)

    def load_current_image(self, event):
        current_image = self.project_spec['image_dir'] + "/" + \
            self.project_spec['image_list'][self.project_spec['current_image_index']]
        self.src_image = Image.open(current_image)
        self.image_panel.src_image = self.src_image.copy()
        self.image_panel.load_image()
        self.tbl_grid.load_image(self.src_image.copy())
        self.tbl_grid.draw_grid()
        self.image_panel.Refresh()
        event.Skip()

    def on_project_settings_click(self, event):
        dlg = FmtkTableMinerProjectDlg(self)
        if dlg.ShowModal() == wx.ID_OK:
            # Save the project settings to the self.project_spec,
            # and save the project_spec to a YAML file.
            self.project_spec['title'] = dlg.project_title.GetValue()
            self.project_spec['description'] = dlg.project_description.GetValue()
            self.project_spec['image_dir'] = dlg.project_image_dir.GetValue()
            self.project_spec['data_dir'] = dlg.project_data_dir.GetValue()
            self.project_spec['column_labels'] = self.gridcol2list(
                dlg.project_column_labels)
            self.project_spec['show_column_labels'] = dlg.project_show_column_labels.GetValue(
            )
            self.project_spec['nlp_tags'] = self.gridcol2list(
                dlg.project_nlp_tags)
            self.project_spec['semicolon_delimiters'] = dlg.project_semicolon_delimiters.GetValue(
            )
            self.project_spec['export_formats'] = self.gather_export_formats(
                dlg)
            self.project_spec['image_list'] = dlg.image_list
            self.project_spec['current_image_index'] = dlg.current_image_index
            self.project_spec['done_image_list'] = dlg.done_image_list
            self.save_project_spec()
            # TODO: Finally, redraw the image grid if exists.
            # self.tbl_grid.draw_grid()
            # self.image_panel.src_image = self.tbl_grid.return_image()
            if self.project_spec['show_column_labels']:
                self.tbl_grid.show_labels = True
            else:
                self.tbl_grid.show_labels = False
            self.tbl_grid.column_labels = self.project_spec['column_labels']
            current_image = self.project_spec['image_dir'] + "/" + \
                self.project_spec['image_list'][self.project_spec['current_image_index']]
            print(current_image)
            self.src_image = Image.open(current_image)
            self.image_panel.src_image = self.src_image.copy()
            self.image_panel.load_image()
            self.tbl_grid.load_image(self.src_image.copy())
            self.tbl_grid.draw_grid()
            self.image_panel.Refresh()
        dlg.Destroy()
        event.Skip()

    # Save the project_spec to a YAML file.
    def save_project_spec(self):
        with wx.FileDialog(self, "Project Spec filename ('.yml' ext to be added)",
                           defaultFile="project_spec.yml",
                           wildcard="Project YAML files (*.yml)|*.yml",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) \
                as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed mind
            # save the current contents in the file
            self.project_spec_file = fileDialog.GetPath()
            try:
                with open(self.project_spec_file, 'w') as outfile:
                    yaml.dump(self.project_spec, outfile,
                              default_flow_style=False)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'."
                            % self.project_spec_file)

    # Load the project_spec from a YAML file.
    def load_project_spec(self):
        with wx.FileDialog(self, "Open Project Spec file",
                           wildcard="Project YAML files (*.yml)|*.yml",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) \
                as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed mind
            # Proceed loading the file chosen by the user
            self.project_spec_file = fileDialog.GetPath()
            try:
                with open(self.project_spec_file, 'r') as infile:
                    self.project_spec = yaml.safe_load(infile)
            except IOError:
                wx.LogError("Cannot open file '%s'." % self.project_spec_file)
            # self.on_project_settings_click(None)

    def save_table_spec(self):
        # Output file name is scr_image filenane with 'json' extension
        # and saved to the data directory.
        tblspec_filename = self.project_spec['data_dir'] + "/" + \
            self.project_spec['image_list'][self.project_spec['current_image_index']].split(
                ".")[0]
        json_export_filename = tblspec_filename + ".json"
        xml_export_filename = tblspec_filename + ".xml"
        # Prepare the table spec for saving.
        table_spec = self.prepare_tablespec_for_save('json')
        # Save the table spec to a JSON file.
        try:
            with open(json_export_filename, 'w') as outfile:
                json.dump(table_spec, outfile, indent=4)
        except IOError:
            wx.LogError("Cannot save current data in file '%s'."
                        % json_export_filename)
        # Save the table spec to an XML file.
        table_spec = self.prepare_tablespec_for_save('xml')
        try:
            with open(xml_export_filename, 'w') as outfile:
                rooted_table_spec = {'table_spec': table_spec}
                xtd.unparse(rooted_table_spec, pretty=True, output=outfile)
        except IOError:
            wx.LogError("Cannot save current data in file '%s'."
                        % xml_export_filename)

    def adjust_text_dicts_for_xml_export(self, text_dict):
        # The keys of the text_dict dict are integers and need to be prefixed with 'r' for XML export.
        tweaked_text = {}
        for key in text_dict.keys():
            rkey = 'r' + str(key)
            # tweaked_text[rkey] = text_dict[key]
        # The keys of the text_dict values are integers and need to be prefixed with 'c' for XML export.
            tweaked_text[rkey] = {}
            for key2 in text_dict[key].keys():
                ckey = 'c' + str(key2)
                tweaked_text[rkey][ckey] = text_dict[key][key2]
        return tweaked_text

    def prepare_tablespec_for_save(self, export_type):
        # Table_spec Root
        # + Src_image filename
        # + Project_spec filename
        # + Image size
        # + Table bounding box
        # + Row offsets
        # + Column offsets
        # + OCR/GT text
        # + NLP tagged text
        table_spec = {}
        table_spec['src_image'] = self.project_spec['image_list'][self.project_spec['current_image_index']]
        table_spec['project_spec'] = self.project_spec_file
        if export_type == 'xml':
            table_spec['image_size'] = str(self.src_image.size)
            table_spec['table_bbox'] = str(self.tbl_grid.get_bbox_tuple())
            table_spec['row_offsets'] = str(self.tbl_grid.row_offsets)
            table_spec['column_offsets'] = str(self.tbl_grid.column_offsets)
        else:
            table_spec['image_size'] = self.src_image.size
            table_spec['table_bbox'] = self.tbl_grid.get_bbox_tuple()
            table_spec['row_offsets'] = self.tbl_grid.row_offsets
            table_spec['column_offsets'] = self.tbl_grid.column_offsets
        if export_type == 'xml':
            table_spec['ocr_text'] = self.adjust_text_dicts_for_xml_export(
                self.tbl_grid.cell_ocrgt_texts)
            table_spec['nlp_text'] = self.adjust_text_dicts_for_xml_export(
                self.tbl_grid.cell_nlpx_texts)
        else:
            table_spec['ocr_text'] = self.tbl_grid.cell_ocrgt_texts
            table_spec['nlp_text'] = self.tbl_grid.cell_nlpx_texts
        return table_spec

    def gridcol2list(self, grid):
        list = []
        for i in range(grid.GetNumberRows()):
            if grid.GetCellValue(i, 0) != '':
                list.append(grid.GetCellValue(i, 0))
        return list

    def gather_export_formats(self, dlg):
        formats = []
        if dlg.project_csv_export.GetValue():
            formats.append('csv')
        if dlg.project_json_export.GetValue():
            formats.append('json')
        if dlg.project_xml_export.GetValue():
            formats.append('xml')
        if dlg.project_html_export.GetValue():
            formats.append('html')
        return formats

    def on_quit_app(self, event):
        event.Skip()


class FmtkTableMinerProjectDlg(FmtkTableMinerProjectDialog):
    def __init__(self, parent):
        FmtkTableMinerProjectDialog.__init__(self, parent)
        # self.parent = parent
        # self.app = self.parent.image_panel.app
        self.image_list = []
        self.current_image_index = 0
        self.project_spec_file = parent.project_spec_file
        self.done_image_list = []
        if self.project_spec_file != '':
            self.project_title.SetValue(str(parent.project_spec['title']))
            self.project_description.SetValue(
                str(parent.project_spec['description']))
            self.project_image_dir.SetValue(
                str(parent.project_spec['image_dir']))
            self.project_data_dir.SetValue(
                str(parent.project_spec['data_dir']))
            self.project_semicolon_delimiters.SetValue(
                parent.project_spec['semicolon_delimiters'])
            self.project_show_column_labels.SetValue(
                parent.project_spec['show_column_labels'])
            self.project_csv_export.SetValue(
                'csv' in parent.project_spec['export_formats'])
            self.project_json_export.SetValue(
                'json' in parent.project_spec['export_formats'])
            self.project_xml_export.SetValue(
                'xml' in parent.project_spec['export_formats'])
            self.project_html_export.SetValue(
                'html' in parent.project_spec['export_formats'])
            for i in range(len(parent.project_spec['column_labels'])):
                self.project_column_labels.SetCellValue(
                    i, 0, parent.project_spec['column_labels'][i])
            for i in range(len(parent.project_spec['nlp_tags'])):
                self.project_nlp_tags.SetCellValue(
                    i, 0, parent.project_spec['nlp_tags'][i])
            self.image_list = parent.project_spec['image_list']
            self.done_image_list = parent.project_spec['done_image_list']
            self.update_image_process_tally()

    def on_set_image_directory(self, event):
        dlg = wx.DirDialog(self, message="Choose a Document Image folder")
        if dlg.ShowModal() == wx.ID_OK:
            self.project_image_dir.SetValue(str(dlg.GetPath()))
            self.image_list = []
        dlg.Destroy()
        print(self.project_image_dir.GetValue())
        image_files = sorted(os.listdir(self.project_image_dir.GetValue()))
        for file in image_files:
            if os.path.splitext(file)[1].lower() in \
                    ['.jpg', '.jpeg', '.png', '.tif', '.tiff']:
                self.image_list.append(file)
        # print(self.image_list)
        self.current_image_index = 0
        self.update_image_process_tally()
        event.Skip()

    def on_set_data_directory(self, event):
        dlg = wx.DirDialog(self, message="Choose a Data Export folder")
        if dlg.ShowModal() == wx.ID_OK:
            self.project_data_dir.SetValue(str(dlg.GetPath()))
        dlg.Destroy()
        print(self.project_data_dir.GetValue())
        event.Skip()

    def update_image_process_tally(self):
        self.project_images_processed.SetValue(
            str(len(self.done_image_list)) + " : " +
            str(len(self.image_list)))

    # Virtual event handlers
    def on_add_label_click(self, event):
        selected_row = self.tbl_grid_col_labels.GetGridCursorRow()
        if selected_row == -1:
            selected_row = self.tbl_grid_col_labels.GetNumberRows()
            self.tbl_grid_col_labels.AppendRows(numRows=1)
        else:
            selected_row += 1
            self.tbl_grid_col_labels.InsertRows(pos=selected_row, numRows=1)
        event.Skip()

    def on_delete_label_click(self, event):
        selected_row = self.tbl_grid_col_labels.GetGridCursorRow()
        if selected_row != -1:
            self.tbl_grid_col_labels.DeleteRows(pos=selected_row, numRows=1)
        event.Skip()

    def on_add_tag_click(self, event):
        selected_row = self.tbl_grid_nlp_tags.GetGridCursorRow()
        if selected_row == -1:
            selected_row = self.tbl_grid_nlp_tags.GetNumberRows()
            self.tbl_grid_nlp_tags.AppendRows(numRows=1)
        else:
            selected_row += 1
            self.tbl_grid_nlp_tags.InsertRows(pos=selected_row, numRows=1)
        event.Skip()

    def on_delete_tag_click(self, event):
        selected_row = self.tbl_grid_nlp_tags.GetGridCursorRow()
        if selected_row != -1:
            self.tbl_grid_nlp_tags.DeleteRows(pos=selected_row, numRows=1)
        event.Skip()


# Main
if __name__ == "__main__":
    app = FmtkTableMinerApp()
    # app.SetAppName("Fmtk TableMiner")
    # wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()
