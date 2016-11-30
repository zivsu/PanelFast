import sublime, sublime_plugin

COL_INDEX_LEFT = 0
ROW_INDEX_TOP = 1
COL_INDEX_RIGHT = 2
ROW_INDEX_BOTTOM =3

class PanelLayoutCommand(sublime_plugin.WindowCommand):
    def get_layout(self):
        """
        {
            'cols': [0.0,0.5,1.0],
            'rows': [0.0,0.5,1.0],
            'cells': [
                [0,0,1,1],
                [1,0,2,1],
                [0,1,1,2],
                [1,1,2,2]
            ]
        }
        """
        layout = self.window.layout()
        return layout["cells"], layout["rows"], layout["cols"]

    @property
    def cells(self):
        return self.get_layout()[0]

    @property
    def cols(self):
        return self.get_layout()[-1]

    @property
    def rows(self):
        return self.get_layout()[1]

    @property
    def row_num(self):
        return self.cells[-1][-1]

    @property
    def col_num(self):
        return self.cells[-1][-2]

    def get_active_cell(self):
        active_group_index = self.window.active_group()
        return self.cells[active_group_index]

    def set_layout(self, layout):
        active_group_index = self.window.active_group()
        self.window.set_layout(layout)
        self.window.focus_group(active_group_index)


class HorizontalExpandCommand(PanelLayoutCommand):
    """
    Take the left side of the panel as the operation target
    """
    def run(self, fraction):
        if self.col_num == 1: return
        current_cell = self.get_active_cell()
        cell_col_index_left = current_cell[COL_INDEX_LEFT]
        if cell_col_index_left == 0:
            # The active cell is the first column
            cell_col_index_left = current_cell[COL_INDEX_RIGHT]

        old_left_scale = self.cols[cell_col_index_left]
        new_left_scale = self.adjust_new_scale(old_left_scale, fraction)
        new_cols = self.cols
        new_cols[cell_col_index_left] = new_left_scale
        new_layout = {
           "cells": self.cells,
           "rows": self.rows,
           "cols": new_cols
        }
        self.set_layout(new_layout)

    def adjust_new_scale(self, old_scale, fraction):
        msg = "Function must be implemented by subclass: {!r}"
        raise NotImplementedError(msg.format(self.__class__.__name__))


class ExpandToLeftCommand(HorizontalExpandCommand):
    def adjust_new_scale(self, old_scale, fraction):
        return old_scale - fraction

    def run(self, fraction):
        super(ExpandToLeftCommand, self).run(fraction)


class ExpandToRightCommand(HorizontalExpandCommand):
    def adjust_new_scale(self, old_scale, fraction):
        return old_scale + fraction

    def run(self, fraction):
        super(ExpandToRightCommand, self).run(fraction)


class VerticalExpandCommand(PanelLayoutCommand):
    """
    Take the top side of the panel as the operation target
    """
    def run(self, fraction):
        if self.row_num == 1: return
        current_cell = self.get_active_cell()
        cell_row_index_top = current_cell[ROW_INDEX_TOP]
        if cell_row_index_top == 0:
            # The active cell is the first column
            cell_row_index_top = current_cell[ROW_INDEX_BOTTOM]

        old_top_scale = self.rows[cell_row_index_top]
        new_top_scale = self.adjust_new_scale(old_top_scale, fraction)
        new_rows = self.rows
        new_rows[cell_row_index_top] = new_top_scale
        new_layout = {
           "cells": self.cells,
           "rows": new_rows,
           "cols": self.cols
        }
        self.set_layout(new_layout)

    def adjust_new_scale(self, old_scale, fraction):
        msg = "Function must be implemented by subclass: {!r}"
        raise NotImplementedError(msg.format(self.__class__.__name__))


class ExpandToTopCommand(VerticalExpandCommand):
    def adjust_new_scale(self, old_scale, fraction):
        return old_scale - fraction

    def run(self, fraction):
        super(ExpandToTopCommand, self).run(fraction)

class ExpandToBottomCommand(VerticalExpandCommand):
    def adjust_new_scale(self, old_scale, fraction):
        return old_scale + fraction

    def run(self, fraction):
        super(ExpandToBottomCommand, self).run(fraction)