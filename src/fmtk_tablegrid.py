#
# Factminers Toolkit - TableGrid Class
#

import json
from pathlib import Path
import os
import copy
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import wx


# Class FmtkTableGrid
class FmtkTableGrid(object):
    def __init__(self, image: Image.Image, table_spec=None):
        self.src_image = image
        self.image = copy.deepcopy(self.src_image)
        if isinstance(table_spec, str):
            if not os.path.isfile(table_spec):
                raise FileNotFoundError(f"Table spec file {table_spec} not found")
            self.load_spec_from_json(table_spec)
        elif isinstance(table_spec, dict):
            self.load_spec_from_dict(table_spec)
        else:
            self.x = 0
            self.y = 0
            self.width = 0
            self.height = 0
            # self.width = self.image.width
            # self.height = self.image.height
            self.row_offsets = []
            self.column_offsets = []
        # How near must a point be to either side
        # of a row or column separator
        self.near_threshold = 2
        self.row_lines = {}
        self.column_lines = {}
        self.cell_bboxes = {}
        self.cell_ocrgt_texts = {}
        self.cell_nlpx_texts = {}
        self.cell_ocrgt_locks = {}
        self.cell_nlpx_locks = {}
        if not hasattr(self, "column_labels"):
            self.column_labels = {}  # {column_number: label}
        if 'wxMac' in wx.PlatformInfo:
            labelfont = "Arial.ttf"
        else:
            labelfont = "arial.ttf"
        self.column_label_font = ImageFont.truetype(labelfont, 24)
        self.show_labels = False
        self.cell_to_highlight = None
        self.cells_edited = False

    # Load the table specification from a dictionary
    def load_spec_from_dict(self, table_spec):
        self.x = table_spec["table_bbox"][0]
        self.y = table_spec["table_bbox"][1]
        self.width = table_spec["table_bbox"][2]
        self.height = table_spec["table_bbox"][3]
        self.row_offsets = table_spec["row_offsets"]
        self.column_offsets = table_spec["column_offsets"]
        if "column_labels" in table_spec:
            self.column_labels = table_spec["column_labels"]
        else:
            self.column_labels = {}
        self.cell_ocrgt_texts = table_spec["cell_ocrgt_texts"]
        self.cell_nlpx_texts = table_spec["cell_nlpx_texts"]
        self.cell_ocrgt_locks = table_spec["cell_ocrgt_locks"]
        self.cell_nlpx_locks = table_spec["cell_nlpx_locks"]

    # Load the table specification from a json file
    def load_spec_from_json(self, filename):
        table_spec = json.loads(open(filename).read())
        self.x = table_spec["x"]
        self.y = table_spec["y"]
        self.width = table_spec["width"]
        self.height = table_spec["height"]
        self.points = table_spec["points"]
        self.center = table_spec["center"]
        self.label = table_spec["label"]
        self.row_offsets = table_spec["row_offsets"]
        self.row_offsets.sort()
        self.column_offsets = table_spec["column_offsets"]
        self.column_offsets.sort()
        if "column_labels" in table_spec:
            self.column_labels = table_spec["column_labels"]
        else:
            self.column_labels = {}
        self.cell_ocrgt_texts = table_spec["cell_ocrgt_texts"]
        self.cell_nlpx_texts = table_spec["cell_nlpx_texts"]
        self.cell_ocrgt_locks = table_spec["cell_ocrgt_locks"]
        self.cell_nlpx_locks = table_spec["cell_nlpx_locks"]

    def clear_grid(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.row_offsets = []
        self.column_offsets = []
        self.row_lines = {}
        self.column_lines = {}
        self.cell_bboxes = {}
        self.cell_ocrgt_texts = {}
        self.cell_nlpx_texts = {}
        self.cell_ocrgt_locks = {}
        self.cell_nlpx_locks = {}
        self.cells_edited = False
        self.cell_to_highlight = None

    def load_image(self, image: Image.Image):
        # If image is a filename then open it
        # if isinstance(image, str) and os.path.isfile(image):
        #     self.src_image = Image.open(image)
        #     self.image = copy.deepcopy(self.src_image)
        # else:
        self.src_image = image
        self.image = copy.deepcopy(self.src_image)

    # Manage the table_spec by providing methods to get, set, and delete
    # row and column separators.
    def get_row_offsets(self):
        return self.row_offsets

    def get_column_offsets(self):
        return self.column_offsets

    def set_row_offsets(self, row_offsets):
        self.row_offsets = row_offsets

    def set_column_offsets(self, column_offsets):
        self.column_offsets = column_offsets

    # Manage the table_spec by providing methods to get, set, and delete
    # the x, y, width, and height of the table.
    def get_x(self):
        return float(self.x)

    def get_y(self):
        return float(self.y)

    def get_width(self):
        return float(self.width)

    def get_height(self):
        return float(self.height)

    def get_bbox(self):
        return wx.Rect(self.x, self.y, self.width, self.height)

    def get_bbox_tuple(self):
        return (self.x, self.y, self.width, self.height)

    def get_number_of_rows(self):
        return len(self.row_offsets) + 1

    def get_number_of_columns(self):
        return len(self.column_offsets) + 1

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_bbox(self, bbox):
        self.x = bbox.x
        self.y = bbox.y
        self.width = bbox.width
        self.height = bbox.height

    def get_column_label(self, column_number):
        if column_number in self.column_labels:
            return self.column_labels[column_number]
        else:
            return ""

    def set_column_label(self, column_number, label):
        self.column_labels[column_number] = label

    # Add and delete row and column separators
    def add_row_offset(self, row_offset):
        current_row_offsets = self.row_offsets.copy()
        self.row_offsets.append(row_offset)
        self.row_offsets.sort()
        if self.cells_edited:
            new_offset_index = self.row_offsets.index(row_offset)
            if new_offset_index < len(self.row_offsets) + 1:
                # The row offset index is one less than the row number
                self.adjust_added_row_offsets(new_offset_index + 1)

    def adjust_added_row_offsets(self, new_row_num):
        adjust_locks = self.confirm_row_lock_ajustment()
        for old_row_num in reversed(range(new_row_num, len(self.row_offsets) + 1)):
            if str(old_row_num) in self.cell_ocrgt_texts.keys():
                self.cell_ocrgt_texts[str(old_row_num +
                                      1)] = self.cell_ocrgt_texts[str(old_row_num)]
                if adjust_locks:
                    unlocks = {}
                    for key in self.cell_ocrgt_locks[str(old_row_num)].keys():
                        unlocks[key] = False
                    self.cell_ocrgt_locks[str(old_row_num + 1)] = unlocks
                    self.cell_nlpx_texts[str(old_row_num +
                                         1)] = self.cell_nlpx_texts[str(old_row_num)]
                    self.cell_nlpx_locks[str(old_row_num + 1)] = unlocks
                else:
                    self.cell_ocrgt_locks[str(old_row_num +
                                          1)] = self.cell_ocrgt_locks[str(old_row_num)]
                    self.cell_nlpx_texts[str(old_row_num +
                                         1)] = self.cell_nlpx_texts[str(old_row_num)]
                    self.cell_nlpx_locks[str(old_row_num +
                                         1)] = self.cell_nlpx_locks[str(old_row_num)]
                self.cell_bboxes[str(old_row_num +
                                 1)] = self.cell_bboxes[str(old_row_num)]
        self.cell_ocrgt_texts[str(new_row_num)] = {}
        self.cell_ocrgt_locks[str(new_row_num)] = {}
        self.cell_nlpx_texts[str(new_row_num)] = {}
        self.cell_nlpx_locks[str(new_row_num)] = {}

    def confirm_row_lock_ajustment(self):
        dlg = wx.MessageDialog(None, caption="Confirm Row Lock Adjustment?",
                               message="Yes to unlock affected rows, no to keep locks.\n In either case, double-check your cell edits.", style=wx.YES_NO | wx.ICON_WARNING)
        if dlg.ShowModal() == wx.ID_OK:
            return True
        else:
            return False

    def add_column_offset(self, column_offset):
        self.column_offsets.append(column_offset)
        self.column_offsets.sort()

    def delete_row_offset(self, row_offset):
        current_row_offsets = self.row_offsets.copy()
        self.row_offsets.remove(row_offset)
        self.row_lines.pop(row_offset)
        # Sort not needed as offsets were sorted before the delete
        # self.row_offsets.sort()
        if self.cells_edited:
            deleted_offset_index = current_row_offsets.index(row_offset)
            # The deleted row offset index is one less than the row number
            self.adjust_deleted_row_offsets(deleted_offset_index + 1)

    def adjust_deleted_row_offsets(self, deleted_row_num):
        adjust_locks = self.confirm_row_lock_ajustment()
        # Deleted row_col text is merged with the row above
        for column_num in range(1, len(self.column_offsets) + 2):
            if str(column_num) in self.cell_ocrgt_texts[str(deleted_row_num)].keys():
                self.cell_ocrgt_texts[str(deleted_row_num)][str(column_num)] = \
                    self.cell_ocrgt_texts[str(deleted_row_num)][str(column_num)] + \
                    '\n' + \
                    self.cell_ocrgt_texts[str(deleted_row_num + 1)][str(column_num)]
            if str(column_num) in self.cell_nlpx_texts[str(deleted_row_num)].keys():
                self.cell_nlpx_texts[str(deleted_row_num)][str(column_num)] = \
                    self.cell_nlpx_texts[str(deleted_row_num)][str(column_num)] + \
                    '\n' + \
                    self.cell_nlpx_texts[str(deleted_row_num + 1)][str(column_num)]
            if adjust_locks:
                self.cell_ocrgt_locks[str(deleted_row_num)][str(column_num)] = False
                self.cell_nlpx_locks[str(deleted_row_num)][str(column_num)] = False
        # self.cell_ocrgt_texts[deleted_row_num - 1] = \
        #     self.cell_ocrgt_texts[deleted_row_num - 1] + \
        #     '\n' + self.cell_ocrgt_texts[deleted_row_num]
        for row_num in range(deleted_row_num + 1, len(self.cell_ocrgt_texts)):
            if str(row_num) in self.cell_ocrgt_texts.keys():
                self.cell_ocrgt_texts[str(row_num)] = self.cell_ocrgt_texts[str(row_num + 1)]
                if adjust_locks:
                    unlocks = {}
                    for key in self.cell_ocrgt_locks[str(row_num + 1)].keys():
                        unlocks[str(key)] = False
                    self.cell_ocrgt_locks[str(row_num)] = unlocks
                    self.cell_nlpx_texts[str(row_num)] = self.cell_nlpx_texts[str(row_num + 1)]
                    self.cell_nlpx_locks[str(row_num)] = unlocks
                else:
                    self.cell_ocrgt_locks[str(row_num)] = self.cell_ocrgt_locks[str(row_num + 1)]
                    self.cell_nlpx_texts[str(row_num)] = self.cell_nlpx_texts[str(row_num + 1)]
                    self.cell_nlpx_locks[str(row_num)] = self.cell_nlpx_locks[str(row_num + 1)]
        # The last row is a dummy row for now
        self.cell_ocrgt_texts.pop(len(self.row_offsets) + 2)
        self.cell_ocrgt_locks.pop(len(self.row_offsets) + 2)
        self.cell_nlpx_texts.pop(len(self.row_offsets) + 2)
        self.cell_nlpx_locks.pop(len(self.row_offsets) + 2)
        self.compute_cell_bboxes()
        self.cell_to_highlight = None

    def delete_column_offset(self, column_offset):
        self.column_offsets.remove(column_offset)
        self.column_lines.pop(column_offset)

    # Compute bounding boxes for the row/column cells in a TableGrid
    def compute_cell_bboxes(self):
        self.cell_bboxes = {}
        # Create a local list of row and column offsets that include
        # the TableGrid height and width as the last element in
        # their respective lists.
        row_offsets = [0]
        row_offsets.extend(self.row_offsets)
        row_offsets.append(self.height)
        column_offsets = [0]
        column_offsets.extend(self.column_offsets)
        column_offsets.append(self.width)
        # Compute the bounding boxes for each cell in the table
        for row_num, row_offset in enumerate(row_offsets, 1):
            if row_offsets.index(row_offset) == len(row_offsets) - 1:
                break   # We've reached the end of the list
            columns = {}
            for col_num, column_offset in enumerate(column_offsets, 1):
                if column_offsets.index(column_offset) == len(column_offsets) - 1:
                    break   # We've reached the end of the list
                cell_bbox = wx.Rect(self.x + column_offset, self.y + row_offset,
                                        column_offsets[column_offsets.index(
                                            column_offset) + 1] - column_offset,
                                        row_offsets[row_offsets.index(row_offset) + 1] - row_offset)
                columns[str(col_num)] = cell_bbox
            self.cell_bboxes[str(row_num)] = columns
        return self.cell_bboxes

    def get_cell_bbox(self, row_num, col_num):
        return self.cell_bboxes[str(row_num)][str(col_num)]

    def get_cell_bboxes(self):
        return self.cell_bboxes

    # Get the text from a cell in the table
    def get_cell_ocrgt_text(self, row_num, col_num):
        if str(row_num) not in self.cell_ocrgt_texts.keys():
            self.cell_ocrgt_texts[str(row_num)] = {}
        if str(col_num) not in self.cell_ocrgt_texts[str(row_num)].keys():
            self.cell_ocrgt_texts[str(row_num)][str(col_num)] = None
        # print("Text is: " , self.cell_ocrgt_texts[row_num][col_num])
        self.cell_to_highlight = (str(row_num), str(col_num))
        if self.ocrgt_cell_lock(str(row_num), str(col_num)) == False:
            self.cell_ocrgt_texts[str(row_num)][str(col_num)] = self.extract_cell_text(
                row_num, col_num)
        return (self.cell_ocrgt_texts[str(row_num)][str(col_num)], 
                self.cell_ocrgt_locks[str(row_num)][str(col_num)])

    def get_cell_nlpx_text(self, row_num, col_num):
        if str(row_num) not in self.cell_nlpx_texts.keys():
            self.cell_nlpx_texts[str(row_num)] = {}
        if str(col_num) not in self.cell_nlpx_texts[str(row_num)].keys():
            self.cell_nlpx_texts[str(row_num)][str(col_num)] = None
        self.cell_to_highlight = (str(row_num), str(col_num))
        if self.nlpx_cell_lock(str(row_num), str(col_num)) == False:
            self.cell_nlpx_texts[str(row_num)][str(col_num)] = self.extract_cell_text(
                row_num, col_num).replace("\n", " ")
        return (self.cell_nlpx_texts[str(row_num)][str(col_num)], 
                self.cell_nlpx_locks[str(row_num)][str(col_num)])

    def ocrgt_cell_lock(self, row_num, col_num):
        if row_num not in self.cell_ocrgt_locks:
            self.cell_ocrgt_locks[row_num] = {}
        if col_num not in self.cell_ocrgt_locks[row_num]:
            self.cell_ocrgt_locks[row_num][col_num] = False
        return self.cell_ocrgt_locks[row_num][col_num]

    def nlpx_cell_lock(self, row_num, col_num):
        if str(row_num) not in self.cell_nlpx_locks.keys():
            self.cell_nlpx_locks[str(row_num)] = {}
        if str(col_num) not in self.cell_nlpx_locks[str(row_num)].keys():
            self.cell_nlpx_locks[str(row_num)][str(col_num)] = False
        return self.cell_nlpx_locks[str(row_num)][str(col_num)]

    # Extract the text from a cell in the table
    def extract_cell_text(self, row_num, col_num):
        cell_image = self.crop_cell_image(row_num, col_num)
        cell_text = pytesseract.image_to_string(cell_image)
        # Trim cell_text to remove trailing whitespace
        cell_text = cell_text.rstrip()
        return cell_text

    def set_cell_ocrgt_lock(self, state):
        if self.cell_to_highlight is not None:
            row_num = self.cell_to_highlight[0]
            col_num = self.cell_to_highlight[1]
            self.cell_ocrgt_locks[str(row_num)][str(col_num)] = state

    def get_cell_ocrgt_lock(self, row_col):
        if str(row_col[0]) not in self.cell_ocrgt_locks.keys():
            self.cell_ocrgt_locks[str(row_col[0])] = {}
        if str(row_col[1]) not in self.cell_ocrgt_locks[str(row_col[0])].keys():
            self.cell_ocrgt_locks[str(row_col[0])][str(row_col[1])] = False
        return self.cell_ocrgt_locks[str(row_col[0])][str(row_col[1])]

    def set_cell_nlpx_lock(self, state):
        if self.cell_to_highlight is not None:
            row_num = self.cell_to_highlight[0]
            col_num = self.cell_to_highlight[1]
            self.cell_nlpx_locks[str(row_num)][str(col_num)] = state

    def get_cell_nlpx_lock(self, row_col):
        if str(row_col[0]) not in self.cell_nlpx_locks.keys():
            self.cell_nlpx_locks[str(row_col[0])] = {}
        if str(row_col[1]) not in self.cell_nlpx_locks[str(row_col[0])].keys():
            self.cell_nlpx_locks[str(row_col[0])][str(row_col[1])] = False
        return self.cell_nlpx_locks[str(row_col[0])][str(row_col[1])]

    # Crop the image of a cell in the table
    def crop_cell_image(self, row_num, col_num):
        cell_bbox = self.get_cell_bbox(row_num, col_num)
        cell_image = self.src_image.crop(
            (cell_bbox.x - 2, cell_bbox.y - 2, cell_bbox.x + cell_bbox.width + 2, cell_bbox.y + cell_bbox.height + 2))
        buffer = wx.Bitmap(cell_image.width, cell_image.height)
        img2buffer = wx.Image(
            cell_image.size[0], cell_image.size[1])
        img2buffer.SetData(cell_image.convert("RGB").tobytes())
        try:
            buffer = img2buffer.ConvertToBitmap()
        except KeyError:
            print('Could not convert PIL image to bitmap...')
        return cell_image

    def is_point_in_bbox(self, point):
        if self.x <= point[0] <= self.x + self.width and self.y <= point[1] <= self.y + self.height:
            return True
        else:
            return False

    def is_point_in_cell(self, point, cell_bbox):
        if cell_bbox.x <= point[0] <= cell_bbox.x + cell_bbox.width and cell_bbox.y <= point[1] <= cell_bbox.y + cell_bbox.height:
            return True
        else:
            return False

    def select_cell_at_point(self, point):
        if self.is_point_in_bbox(point) is False:
            return False
        for row_num, row in self.cell_bboxes.items():
            for col_num, cell_bbox in row.items():
                if self.is_point_in_cell(point, cell_bbox):
                    return [row_num, col_num]
        return False

    def img_point_to_table_offset(self, point, row_or_col):
        if self.is_point_in_bbox(point) is False:
            return False
        elif row_or_col == "col":
            offset = point[0] - self.x
        else:
            offset = point[1] - self.y
        return offset

    def table_offset_to_img_point(self, offset, row_or_col):
        if row_or_col == "row":
            point = (self.x + offset, self.y)
        else:
            point = (self.x, self.y + offset)
        return point

    # Is the point on a row or column separator?
    def is_on_row_or_column(self, point):
        for row_offset in self.row_offsets:
            if point[1] == self.y + row_offset:
                return ["row", row_offset]
        for column_offset in self.column_offsets:
            if point[0] == self.x + column_offset:
                return ["column", column_offset]
        return [False, False]

    # Is the point near a row or column separator?
    # Note: This will return near row separators
    # before near column separators.
    def is_near_row_or_column_sep(self, point):
        for row_offset in self.row_offsets:
            near_min = self.y + row_offset - self.near_threshold
            near_max = self.y + row_offset + self.near_threshold
            if near_min <= point.y <= near_max:
                return ["row", row_offset]
        for column_offset in self.column_offsets:
            near_min = self.x + column_offset - self.near_threshold
            near_max = self.x + column_offset + self.near_threshold
            if near_min <= point.x <= near_max:
                return ["column", column_offset]
        return False

    def delete_near_row_or_column_sep(self, point):
        target_sep = self.is_near_row_or_column_sep(point)
        if target_sep:
            row_or_col, offset = target_sep
            if row_or_col == "row":
                self.delete_row_offset(offset)
            elif row_or_col == "column":
                self.delete_column_offset(offset)

    # Return the image
    def return_image(self):
        return self.image

    def save_spec_to_json(self, filename):
        table_spec = {}
        table_spec["label"] = self.label
        table_spec["x"] = self.x
        table_spec["y"] = self.y
        table_spec["width"] = self.width
        table_spec["height"] = self.height
        table_spec["row_offsets"] = self.row_offsets
        table_spec["column_offsets"] = self.column_offsets
        table_spec["points"] = self.points
        table_spec["center"] = self.center
        with open(filename, "w") as f:
            f.write(json.dumps(table_spec, indent=4))

    def move_tbl_bbox(self, x, y):
        dif_x = x - self.x
        dif_y = y - self.y
        self.x = x
        self.y = y
        self.points = [(self.x, self.y),
                       (self.x + self.width, self.y),
                       (self.x + self.width, self.y + self.height),
                       (self.x, self.y + self.height)]
        self.center = (self.x + self.width / 2, self.y + self.height / 2)
        for row_offset in self.row_offsets:
            self.row_lines[row_offset] = [(self.x, self.y + row_offset),
                                          (self.x + self.width, self.y + row_offset)]
        for col_offset in self.column_offsets:
            self.column_lines[col_offset] = [(self.x + col_offset, self.y),
                                             (self.x + col_offset, self.y + self.height)]

    def move_tbl_bbox_by_offset(self, x, y):
        self.move_tbl_bbox(self.x + x, self.y + y)

    def invalidate_row_lines(self):
        self.row_lines = {}

    def invalidate_column_lines(self):
        self.column_lines = {}

    # Draw methods
    #
    def draw_grid(self):
        self.image = self.src_image.copy()
        # If grid height or width is 0, then don't draw the grid
        if self.height == 0 or self.width == 0:
            return self.image
        # Before drawing the grid, get a copy of the src_image.
        # This is so we can draw the grid on top of the image
        self.draw_bbox()
        self.draw_row_lines()
        self.draw_col_lines()
        self.draw_column_labels()
        self.draw_highlight_cell()
        return self.image

    # Draw the table grid on the image
    def draw_bbox(self):
        # draw the test table's bbox rectangle on the image
        img1 = ImageDraw.Draw(self.image)
        xy = (self.get_x(), self.get_y())
        hw = (self.get_width(), self.get_height())
        bbox = (xy, hw)
        img1.rectangle(bbox, fill=None, outline="blue", width=5)

    def draw_row_lines(self):
        # draw the test table's row lines on the image
        img1 = ImageDraw.Draw(self.image)
        for row_offset in self.row_offsets:
            if not self.row_lines.get(row_offset):
                self.row_lines[row_offset] = [(self.x, self.y + row_offset),
                                              (self.x + self.width, self.y + row_offset)]
            img1.line(self.row_lines[row_offset], fill="blue", width=3)

    def draw_col_lines(self):
        # draw the test table's column lines on the image
        img1 = ImageDraw.Draw(self.image)
        for col_offset in self.column_offsets:
            if not self.column_lines.get(col_offset):
                self.column_lines[col_offset] = [(self.x + col_offset, self.y),
                                                 (self.x + col_offset, self.y + self.height)]
            img1.line(self.column_lines[col_offset], fill="blue", width=3)

    def draw_column_labels(self):
        if not self.column_labels or self.show_labels == False:
            return
        elif len(self.column_labels) != len(self.column_offsets) + 1:
            return
        # draw the test table's column labels on the image
        img1 = ImageDraw.Draw(self.image)
        for col_num, col_name in enumerate(self.column_labels, 1):
            if col_num == 1:
                x = self.x
            else:
                x = self.x + self.column_offsets[col_num - 2]
            position = (x + 5, self.y - 28)
            l, t, r, b = bbox = img1.textbbox(position, col_name,
                                              font=self.column_label_font)
            img1.rectangle((l - 5, t - 5, r + 5, b + 5),
                           fill="yellow", outline="blue", width=1)
            img1.text(position, col_name,
                      font=self.column_label_font, fill="blue")

    def draw_highlight_cell(self):
        if self.cell_to_highlight is not None:
            row_num = self.cell_to_highlight[0]
            col_num = self.cell_to_highlight[1]
            # draw the test table's row lines on the image
            img1 = ImageDraw.Draw(self.image)
            
            xy = (self.cell_bboxes[row_num][col_num].get_x(), self.cell_bboxes[row_num][col_num].get_y())
            hw = (self.cell_bboxes[row_num][col_num].get_width(), 
                  self.cell_bboxes[row_num][col_num].get_height())
            bbox = (xy, hw)
            img1.rectangle(bbox, outline="green", width=5)
            # TODO: May not be right to do this here
            # self.cell_to_highlight = None

    def show(self):
        self.image.show()

    def save_image(self, filename):
        self.image.save(filename)

    def run_tests(self):
        self.draw_grid()
        # self.show()
        self.save_image("./tblgrid_test_results/tbl_test0.png")
        print(self.compute_cell_bboxes())
        self.highlight_cell = (4, 4)
        self.draw_grid
        # self.show()
        self.set_column_label(1, "Role")
        self.set_column_label(2, "Name")
        self.set_column_label(3, "Email")
        self.draw_column_labels()
        self.show()
        self.add_row_offset(100)
        self.add_column_offset(200)
        self.draw_grid()
        # self.show()
        self.save_image("./tblgrid_test_results/tbl_test1.png")
        self.save_spec_to_json("./tblgrid_test_results/tbl_test1.json")
        self.delete_row_offset(100)
        self.delete_column_offset(200)
        self.draw_grid()
        # self.show()
        self.save_image("./tblgrid_test_results/tbl_test2.png")
        self.save_spec_to_json("./tblgrid_test_results/tbl_test2.json")
        self.move_tbl_bbox(120, 240)
        self.draw_grid()
        # self.show()
        self.save_image("./tblgrid_test_results/tbl_test3.png")
        self.save_spec_to_json("./tblgrid_test_results/tbl_test3.json")
        self.move_tbl_bbox_by_offset(-40, -60)
        self.draw_grid()
        # self.show()
        self.save_image("./tblgrid_test_results/tbl_test4.png")
        test_pt = (250, 450)
        print("row offest is", self.img_point_to_table_offset(test_pt, "row"))
        print("col offset is", self.img_point_to_table_offset(test_pt, "col"))


####
# Create an Fmtk_TableGrid object and test it
####
if __name__ == "__main__":
    # Create a table grid object
    starter_image = Image.open("fmtk_tableminer_test-image.png")
    tbl_grid = FmtkTableGrid(starter_image,
                             "fmtk_tableminer_test-image.json")
    tbl_grid.run_tests()

# End of file
