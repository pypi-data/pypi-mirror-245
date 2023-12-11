# v. 2.6.0 231104

import logging

class GridIterator:
    def __init__(self, rows, columns):
        self.max_row_index = rows - 1
        self.max_col_index = columns - 1
        self.current_row = 0
        self.current_column = 0
        self.next_never_called = True

    def get_cell(self):
        return self.current_row, self.current_column

    def next(self):
        moved = False
        cell_to_ret = None
        if (self.next_never_called):
            self.current_row = 0
            self.current_column = 0
            cell_to_ret = self.get_cell()
            self.next_never_called = False
            moved = True
        else:
            if (self.current_row < self.max_row_index):
                self.current_row += 1
                moved = True
            else:
                if (self.current_column < self.max_col_index):
                    self.current_row = 0
                    self.current_column += 1
                    moved = True

        if (moved):
            cell_to_ret = self.get_cell()
        return cell_to_ret

    #def previous(self):
    #    moved = False
    #    cell_to_ret = None
    #    if (self.current_row > 0):
    #        self.current_row -= 1
    #        moved = True
    #    else:
    #        if (self.current_column > 0):
    #            self.current_row = self.max_row_index
    #            self.current_column = 0
    #            moved = True
    #    if (moved):
    #        cell_to_ret = self.get_cell()
    #    return cell_to_ret

# Example usage:
#grid_iterator = GridIterator(2, 2)
#print(grid_iterator.next())  # Output: (0, 1)
#print(grid_iterator.next())  # Output: (1, 0)
##print(grid_iterator.previous())  # Output: (0, 1)
