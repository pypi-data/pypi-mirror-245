# v. 7.2.0 231117

import logging
import matplotlib.pyplot as plt
from grid_iterator import GridIterator
from config_util import get_common_plots_params, get_1tab_ui_plots_params, get_mtab_ui_plots_params
import math
from config_util import get_emptysubplots_params
from plot_util import hide_empty_subplots

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def eval_tab_layout(mt_max_rows, mt_max_cols, max_plotspertab):
    logger = logging.getLogger(__name__)
    wnd_panel_rows = mt_max_rows # also good 2 rows 1 col and max 2 plots x tab
    wnd_panel_cols = mt_max_cols
    max_plots_x_tab = max_plotspertab
    tab_grid_spec = 100 * wnd_panel_rows + 10 * wnd_panel_cols # 310
    max_th_grid = (tab_grid_spec // 100) * ((tab_grid_spec % 100) // 10)
    if (max_plots_x_tab > max_th_grid):
        max_plots_x_tab = max_th_grid
    logger.debug('max_plots_x_tab reassessed: ' + str(max_plots_x_tab))
    return wnd_panel_rows, wnd_panel_cols, max_plots_x_tab, tab_grid_spec

class PlotWindowWrapper:

    #def __init__(self, multitab_mode, config, downsampled, num_time_samples_pre, num_time_samples, num_freqs, num_subplots, source_info):
    def __init__(self, multitab_mode, config, num_subplots, source_info):
        logger = logging.getLogger(__name__)
        self.config_hnd = config

        #common params
        window_title, bgcolor = get_common_plots_params(self.config_hnd)

        #params for old ui
        max_rows, max_cols, h_cell_span, w_cell_span, figsz_w, figsz_h, gridspec_hs, gridspec_ws = get_1tab_ui_plots_params(self.config_hnd)
        #params for new multitab ui
        anonym_tab_pfix, mt_max_rows, mt_max_cols, max_plotsxtab, expand, tab_expand, fill, tab_fill, tab_side, tab_dpi, mt_figsz_w, mt_figsz_h, mt_gridspec_hs = get_mtab_ui_plots_params(self.config_hnd)

        self.tab_count = 0
        main_wnd_title = '[' + source_info + '] ' + window_title

        #common_tprefix = window_head + ' [' + source_info + ', data points (t/f): '
        #common_tpostfix = '/' + str(num_freqs) + ']'
        #if (downsampled):
        #    self.p_subtitle = common_tprefix + str(num_time_samples_pre) + ' -> ' + str(num_time_samples) + common_tpostfix
        #else:
        #    self.p_subtitle = common_tprefix + str(num_time_samples) + common_tpostfix

        self.multitab_on = multitab_mode
        if (self.multitab_on):
            self.tkroot = tk.Tk()
            self.anonym_tab_prefix = anonym_tab_pfix #'plots-'
            #root.geometry('800x600') 
            self.mt_expand = expand #1
            self.mt_fill = fill #'both'
            self.tab_figsize = (mt_figsz_w, mt_figsz_h)
            self.tab_dpi = tab_dpi #180
            self.tab_expand = tab_expand #1
            self.tab_bgcolor = bgcolor
            self.tab_fill = tab_fill #tk.BOTH
            self.tab_side = tab_side #tk.TOP
            self.tab_plots_hspace = mt_gridspec_hs #0.8
            #self.tab_plots_wspace = None
            #self.num_total_tabbed_plots = 0
            self.wnd_panel_rows, self.wnd_panel_cols, self.max_plots_x_tab, self.tab_grid_spec = eval_tab_layout(mt_max_rows, mt_max_cols, max_plotsxtab)
            self.curr_tab_figure = None
            self.num_plots_in_curr_tab = 0
            self.tkroot.title(main_wnd_title)
            self.notebook = ttk.Notebook(self.tkroot)

            # Bind the window closing event to the on_closing function
            self.tkroot.protocol('WM_DELETE_WINDOW', self.on_ui_closing)
            #logger.warning('PlotWindowWrapper.init - TBI print somewhere the downdampled subtitle: ' + self.p_subtitle)

            #def add_title_above(notebook, title):
            #    title_label = tk.Label(root, text=title, font=("Helvetica", 16, "bold"))
            #    title_label.pack(pady=10)
            # Add Title Above the Notebook
            #add_title_above(notebook, "Main Title")

        else:
            self.plt = plt
            max_subplots = max_rows * max_cols
            temp_cols = math.ceil(num_subplots / max_rows)
            #self.wnd_panel_cols = temp_cols
            self.wnd_panel_cols = max_cols if (temp_cols > max_cols) else temp_cols
            self.wnd_panel_rows = max_rows if (num_subplots > max_rows) else num_subplots
            #self.wnd_panel_rows = 5 ##################################################################
            #self.wnd_panel_rows = 2 * self.wnd_panel_rows
            logger.info('Plot window layout: {max cols: ' + str(self.wnd_panel_cols) + ', max rows: ' + str(self.wnd_panel_rows) + '}')
            if (num_subplots > max_subplots):
                exc_plots = num_subplots - max_subplots
                logger.warning('Not enough room for all the plots (' + str(num_subplots) + ') with the selected layout (cols: ' + str(self.wnd_panel_cols) + ', rows: ' + str(self.wnd_panel_rows) + '), exceeding plots (' + str(exc_plots) + ') are being DISCARDED')

            #self.wnd_panel_rows = num_subplots
            #self.wnd_panel_cols = 1
            self.wndPlotSpotsIterator = GridIterator(self.wnd_panel_rows, self.wnd_panel_cols)
            logger.debug('Window Plot spots iterator built')

            c_height_ratios = [h_cell_span] * self.wnd_panel_rows #all elements are 1 - [1, 1, 1, ..., 1]
            #c_height_ratios = [2, 1, 1] ############################################################
            c_width_ratios = [w_cell_span] * self.wnd_panel_cols #all elements are 1 - [1, 1, 1, ..., 1]
            #c_height_ratios = [1] * (num_subplots - 1) + [2] #all elements are 1, except the last element, which is 2
            #constrained_layout=True, 
            self.fig, self.axes = self.plt.subplots(self.wnd_panel_rows, self.wnd_panel_cols, num=main_wnd_title, figsize=(float(figsz_w), float(figsz_h)),
                                  gridspec_kw={'height_ratios': c_height_ratios, 'width_ratios': c_width_ratios, 'hspace': float(gridspec_hs), 'wspace': float(gridspec_ws)})
            #fig, axes = self.plt.subplots(num_subplots, 1, num='[' + source_info + '] ' + window_title, figsize=(float(figsz_w), float(figsz_h)), gridspec_kw={'hspace': float(gridspec_hs)})
            self.fig.set_facecolor(bgcolor)  # Use a color code or name
            # or axes[0].get_figure().patch.set_facecolor(bgcolor)  # Use a color code or name
            logger.debug('Subplots areas created')

            # Adjust layout
            #self.plt.suptitle(self.p_subtitle)
            self.plt.tight_layout()
            self.tab_count = 1
            logger.debug('Layout adjusted')

    # Function to handle window closing event
    def on_ui_closing(self):
        logger = logging.getLogger(__name__)
        logger.debug('Quitting tkroot ...')
        self.tkroot.quit()
        logger.debug('Destroying tkroot ...')
        self.tkroot.destroy()

    #def currsubplot_axes(self):
    #    logger = logging.getLogger(__name__)
    #    if (self.multitab_on):
    #        ....
    #    else:
    #        row, col = self.wndPlotSpotsIterator.get_cell()
    #        logger.debug('plotWndWrap.curr(): returning axes')
    #        return self.return_axes(row, col)

    #for multitab only
    #def add_tabbed_subplot(self, title):
    #    return self.add_tabbed_subplot(title, False)

    #for multitab only
    def add_tabbed_subplot(self, title, is3D, is_tab_dedicated):
        ax = None
        if (is_tab_dedicated):
            tab_title = title
            #wnd_panel_rows, wnd_panel_cols are the two neglected outputs.
            _, _, max_plots_x_tab, tab_grid_specs = eval_tab_layout(1, 1, 1)
            self.num_plots_in_curr_tab = 0
            self.curr_tab_figure = self.add_tab(tab_title)
        else:
            tab_grid_specs = self.tab_grid_spec
            max_plots_x_tab = self.max_plots_x_tab
            if (self.curr_tab_figure is None) or (self.num_plots_in_curr_tab == max_plots_x_tab):
                tab_title = title if (max_plots_x_tab == 1) else None
                self.curr_tab_figure = self.add_tab(tab_title)
                self.num_plots_in_curr_tab = 0


        #(111) equivalent to figure.add_suXbplot(1, 1, 1), and you are creating a single subplot in a 1x1 grid.
        #If you wanted a 2x2 grid, you could use figure.add_suXbplot(2, 2, 1) to create the first subplot in a 2x2 grid.
        #The index can range from 1 to the total number of subplots in the grid.
        ax_compact_idx = tab_grid_specs + self.num_plots_in_curr_tab + 1

        ax = self.curr_tab_figure.add_subplot(ax_compact_idx, projection=('3d' if is3D else None)) # rows cols, nbr in total
        if (is_tab_dedicated):
            self.curr_tab_figure = None # so that ALSO on next call of 'add_tabbed_subplot', a tab is added!!

        self.num_plots_in_curr_tab = self.num_plots_in_curr_tab + 1
        return ax

    #for multitab only
    def add_tab(self, title):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=(title if title else (self.anonym_tab_prefix + str(self.tab_count + 1))))
        #screen_width, screen_height = get_screen_dimensions(root)
        # Calculate proportional figsize (adjust the multiplier as needed)
        #figsize_multiplier = 0.4
        #figsizex = (screen_width * figsize_multiplier, screen_height * figsize_multiplier)
        #figure = Figure(constrained_layout=True, figsize=self.taXb_figsize, dpi=self.tab_dpi)
        figure = Figure(figsize=self.tab_figsize, dpi=self.tab_dpi) #, gridspec_kw=cust_gridspec
        figure.subplots_adjust(hspace=self.tab_plots_hspace)
        figure.patch.set_facecolor(self.tab_bgcolor)
        canvas = FigureCanvasTkAgg(figure, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(side=self.tab_side, fill=self.tab_fill, expand=self.tab_expand)
        self.tab_count = self.tab_count + 1
        return figure

    def nextsubplot_axes(self, title, is3D=False, isDedicatedTab=False):
        logger = logging.getLogger(__name__)
        if (self.multitab_on):
            #figure = self.add_Xtab(title)
            #ax = figure.add_suXbplot(111) # rows cols, nbr in total
            ax = self.add_tabbed_subplot(title, is3D, isDedicatedTab)

            return ax
        else:
            next_avail = self.wndPlotSpotsIterator.next()
            if (next_avail is None):
                logger.debug('plotWndWrap.next() returning None')
                return None
            else:
                row, col = next_avail[0], next_avail[1]
                logger.debug('plotWndWrap.next() returning axes')
                return self.return_axes(row, col, is3D)

    # only for NON-multitab
    #def prevsubplot_axes(self):
    #    logger = logging.getLogger(__name__)
    #    prev_avail = self.wndPlotSpotsIterator.previous()
    #    if (prev_avail is None):
    #        logger.debug('plotWndWrap.prev() returning None')
    #        return None
    #    else:
    #        row, col = prev_avail[0], prev_avail[1]
    #        logger.debug('plotWndWrap.prev() returning axes')
    #        return self.return_axes(row, col)

    def convert_ax_2_3D(self, ax):
        proj_3d = '3d'
        ax.set_xticks([])
        ax.set_yticks([])
        #ax.set_zticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')
        #ax.set_zlabel('')
        #ax.outline_patch.set_visible(False)
        ax.set_frame_on(False)
        ax3d = self.fig.add_subplot(ax.get_subplotspec(), projection=proj_3d)
        return ax3d

    # only for NON-multitab
    def return_axes(self, row, col, is3D):
        logger = logging.getLogger(__name__)
        if (self.wnd_panel_cols > 1):
            if (self.wnd_panel_rows > 1):
                logger.debug('    plotWndWrap.return_axes(): (row: ' + str(row) + ', col: ' + str(col) + ')')
                if (is3D):
                       self.axes[row][col] = self.convert_ax_2_3D(self.axes[row][col])
                return self.axes[row][col]
            else:
                logger.debug('    plotWndWrap.return_axes(): (col: ' + str(col) + ')')
                if (is3D):
                       self.axes[col] = self.convert_ax_2_3D(self.axes[col])
                return self.axes[col]
        else:
            if (self.wnd_panel_rows > 1):
                logger.debug('    plotWndWrap.return_axes(): (row: ' + str(row) + ')')
                if (is3D):
                       self.axes[row] = self.convert_ax_2_3D(self.axes[row])
                return self.axes[row]
            else:
                logger.debug('    plotWndWrap.return_axes(): no indexes')
                if (is3D):
                       self.axes = self.convert_ax_2_3D(self.axes)
                return self.axes

    #def get_window(self):
    #    return self.axes

    def showPlots(self):
        logger = logging.getLogger(__name__)
        if (self.multitab_on):
            logger.debug('plotWndWrap: entering UI main loop')
            self.tkroot.mainloop()
        else:
            logger.debug('plotWndWrap: showing UI')
            self.plt.show()

    def prepareForDisplay(self):
        logger = logging.getLogger(__name__)
        if (self.multitab_on):
            logger.debug('plotWndWrap: packing the notebook')
            self.notebook.pack(expand=self.mt_expand, fill=self.mt_fill)
        else:
            logger.debug('plotWndWrap: cleaning up empty subplots')
            #clean up empty subplots
            # not happy about this: the hide_empty_subplots had to work fine against the ROOT panel, finding by 
            # itself the unused subplots, but it does not work or I am missing something
            #hide_empty_subplots(self.plt_hnd, axes, empty_wspace, empty_hspace) # needed, or ticks would be visible also on empty spots!
            # so I wrote the empty_unused_subplots, in this file, which is a workaround
            empty_wspace, empty_hspace = get_emptysubplots_params(self.config_hnd)
            targetAxes = self.nextsubplot_axes(None)
            while (not (targetAxes is None)):
                #print(counter)
                hide_empty_subplots(self.plt, targetAxes, empty_wspace, empty_hspace) # needed, or ticks would be visible also on empty spots!
                targetAxes = self.nextsubplot_axes(None)
