# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.0-4761b0c)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

tb_TBL_BBOX = 1000
tb_ROW_SEP = 1001
tb_COL_SEP = 1002
tb_DEL_SEP = 1003
tb_SEL_CELL = 1004
ocr_TEXT_EDIT = 1005
nlpx_TEXT_EDIT = 1006

###########################################################################
## Class Fmtk_tbl_bboxerGUI
###########################################################################

class Fmtk_tbl_bboxerGUI ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FMTK Table Boxer Widget", pos = wx.DefaultPosition, size = wx.Size( 1000,1100 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.mnu_top = wx.Menu()
		self.mnui_settings = wx.MenuItem( self.mnu_top, wx.ID_ANY, u"Settings...", wx.EmptyString, wx.ITEM_NORMAL )
		self.mnu_top.Append( self.mnui_settings )

		self.mnui_imgdir = wx.MenuItem( self.mnu_top, wx.ID_ANY, u"Set Image Directory...", wx.EmptyString, wx.ITEM_NORMAL )
		self.mnu_top.Append( self.mnui_imgdir )

		self.mnui_datadir = wx.MenuItem( self.mnu_top, wx.ID_ANY, u"Select Data Directory...", wx.EmptyString, wx.ITEM_NORMAL )
		self.mnu_top.Append( self.mnui_datadir )

		self.mnu_top.AppendSeparator()

		self.mnui_quit = wx.MenuItem( self.mnu_top, wx.ID_ANY, u"Quit Fmtk_TableMiner", wx.EmptyString, wx.ITEM_NORMAL )
		self.mnu_top.Append( self.mnui_quit )

		self.m_menubar1.Append( self.mnu_top, u"File" )

		self.SetMenuBar( self.m_menubar1 )

		topWin_sizer = wx.BoxSizer( wx.VERTICAL )

		self.appWin_toolbar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TB_HORIZONTAL|wx.TAB_TRAVERSAL )
		self.appWin_toolbar.SetToolBitmapSize( wx.Size( 40,40 ) )
		self.appWin_toolbar.SetToolSeparation( 10 )
		self.appWin_toolbar.SetMargins( wx.Size( 0,-20 ) )
		self.tbar_table = self.appWin_toolbar.AddTool( tb_TBL_BBOX, u"Set Table BoundingBox", wx.Bitmap( u"resources/tbl_tbar_table_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Set Table BoundingBox", wx.EmptyString, None )

		self.tbar_row_sep = self.appWin_toolbar.AddTool( tb_ROW_SEP, u"Row Separator", wx.Bitmap( u"resources/tbl_tbar_row-sep_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Row Separator", wx.EmptyString, None )

		self.tbar_col_sep = self.appWin_toolbar.AddTool( tb_COL_SEP, u"Column Separator", wx.Bitmap( u"resources/tbl_tbar_col-sep_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Column Separator", wx.EmptyString, None )

		self.tbar_del_sep = self.appWin_toolbar.AddTool( tb_DEL_SEP, u"Delete Separator", wx.Bitmap( u"resources/tbl_tbar_del-sep_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Delete Separator", wx.EmptyString, None )

		self.tbar_sel_cell = self.appWin_toolbar.AddTool( tb_SEL_CELL, u"Select Cell", wx.Bitmap( u"resources/tbl_tbar_cell_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Select Cell at Row/Col click", wx.EmptyString, None )

		self.appWin_toolbar.AddSeparator()

		self.tbar_zoom_label = wx.StaticText( self.appWin_toolbar, wx.ID_ANY, u"Zoom", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tbar_zoom_label.Wrap( -1 )

		self.appWin_toolbar.AddControl( self.tbar_zoom_label )
		tbar_zoom_sizeChoices = [ u"10%", u"25%", u"50%", u"75%", u"100%", u"150%", u"200%", u"400%", wx.EmptyString, wx.EmptyString ]
		self.tbar_zoom_size = wx.Choice( self.appWin_toolbar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, tbar_zoom_sizeChoices, 0 )
		self.tbar_zoom_size.SetSelection( 4 )
		self.appWin_toolbar.AddControl( self.tbar_zoom_size )
		self.appWin_toolbar.AddSeparator()

		self.tbar_col_labels = wx.Button( self.appWin_toolbar, wx.ID_ANY, u"Column Labels", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.appWin_toolbar.AddControl( self.tbar_col_labels )
		self.appWin_toolbar.AddSeparator()

		self.tbar_lock_bbox = wx.CheckBox( self.appWin_toolbar, wx.ID_ANY, u"Lock Table Bbox", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tbar_lock_bbox.SetToolTip( u"Lock the bounding box of the table" )

		self.appWin_toolbar.AddControl( self.tbar_lock_bbox )
		self.appWin_toolbar.AddSeparator()

		self.tbar_img_sel_label = wx.StaticText( self.appWin_toolbar, wx.ID_ANY, u"Image selection:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tbar_img_sel_label.Wrap( -1 )

		self.appWin_toolbar.AddControl( self.tbar_img_sel_label )
		self.tbar_prior_image = wx.Button( self.appWin_toolbar, wx.ID_ANY, u"<", wx.DefaultPosition, wx.Size( 33,-1 ), 0 )
		self.tbar_prior_image.SetToolTip( u"Move to PRIOR image by filename in the Settings’ designated image directory." )

		self.appWin_toolbar.AddControl( self.tbar_prior_image )
		self.tbar_next_image_btn = wx.Button( self.appWin_toolbar, wx.ID_ANY, u">", wx.DefaultPosition, wx.Size( 33,-1 ), 0 )
		self.tbar_next_image_btn.SetToolTip( u"Move to NEXT image by filename in the Settings’ designated image directory." )

		self.appWin_toolbar.AddControl( self.tbar_next_image_btn )
		self.appWin_toolbar.Realize()

		topWin_sizer.Add( self.appWin_toolbar, 0, wx.EXPAND, 0 )

		ocr_CELLEDITOR = wx.BoxSizer( wx.VERTICAL )

		ocr_edit_label_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.ocr_edit_label = wx.StaticText( self, wx.ID_ANY, u"OCR/Ground-Truth Editor", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ocr_edit_label.Wrap( -1 )

		self.ocr_edit_label.Hide()

		ocr_edit_label_sizer.Add( self.ocr_edit_label, 0, wx.ALL, 5 )

		self.ocr_reread_btn = wx.Button( self, wx.ID_ANY, u"Re-read OCR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ocr_reread_btn.Hide()
		self.ocr_reread_btn.SetToolTip( u"Click to re-read the OCR text extraction." )

		ocr_edit_label_sizer.Add( self.ocr_reread_btn, 0, wx.ALL, 5 )

		self.ocr_lock_text = wx.CheckBox( self, wx.ID_ANY, u"Lock OCR/GT text", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ocr_lock_text.Hide()

		ocr_edit_label_sizer.Add( self.ocr_lock_text, 0, wx.ALL, 5 )

		self.ocr_edit_tip = wx.StaticText( self, wx.ID_ANY, u"Tip: Double-click cell to lock both OCR and NLP texts.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ocr_edit_tip.Wrap( -1 )

		self.ocr_edit_tip.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.ocr_edit_tip.Hide()

		ocr_edit_label_sizer.Add( self.ocr_edit_tip, 0, wx.ALL, 5 )


		ocr_CELLEDITOR.Add( ocr_edit_label_sizer, 1, wx.EXPAND, 5 )

		self.ocr_text_edit = wx.TextCtrl( self, ocr_TEXT_EDIT, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_WORDWRAP|wx.TAB_TRAVERSAL )
		self.ocr_text_edit.SetFont( wx.Font( 24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.ocr_text_edit.Hide()
		self.ocr_text_edit.SetMinSize( wx.Size( -1,80 ) )
		self.ocr_text_edit.SetMaxSize( wx.Size( -1,80 ) )

		ocr_CELLEDITOR.Add( self.ocr_text_edit, 0, wx.ALL|wx.EXPAND, 5 )

		nlpx_edit_label_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.nlpx_edit_label = wx.StaticText( self, wx.ID_ANY, u"NLP/Export Editor", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.nlpx_edit_label.Wrap( -1 )

		self.nlpx_edit_label.Hide()

		nlpx_edit_label_sizer.Add( self.nlpx_edit_label, 0, wx.ALL, 5 )

		self.nlpx_copy_ocr_text_btn = wx.Button( self, wx.ID_ANY, u"Copy OCR/GT Text", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.nlpx_copy_ocr_text_btn.Hide()

		nlpx_edit_label_sizer.Add( self.nlpx_copy_ocr_text_btn, 0, wx.ALL, 5 )

		self.nlpx_lock_text = wx.CheckBox( self, wx.ID_ANY, u"Lock NLP/Export text", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.nlpx_lock_text.Hide()

		nlpx_edit_label_sizer.Add( self.nlpx_lock_text, 0, wx.ALL, 5 )

		nlpx_tagChoices = [ u"_NLP/Export tag", u"Person", u"Role", u"Company", u"Software" ]
		self.nlpx_tag = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, nlpx_tagChoices, wx.CB_SORT )
		self.nlpx_tag.SetSelection( 0 )
		self.nlpx_tag.Hide()

		nlpx_edit_label_sizer.Add( self.nlpx_tag, 0, wx.ALL, 5 )


		ocr_CELLEDITOR.Add( nlpx_edit_label_sizer, 1, wx.EXPAND, 5 )

		self.nlpx_text_edit = wx.TextCtrl( self, nlpx_TEXT_EDIT, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_WORDWRAP|wx.HSCROLL|wx.TAB_TRAVERSAL|wx.VSCROLL )
		self.nlpx_text_edit.SetFont( wx.Font( 24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.nlpx_text_edit.Hide()
		self.nlpx_text_edit.SetMinSize( wx.Size( -1,80 ) )
		self.nlpx_text_edit.SetMaxSize( wx.Size( -1,80 ) )

		ocr_CELLEDITOR.Add( self.nlpx_text_edit, 0, wx.ALL|wx.EXPAND, 5 )


		topWin_sizer.Add( ocr_CELLEDITOR, 0, wx.EXPAND, 5 )


		self.SetSizer( topWin_sizer )
		self.Layout()
		self.appWin_statusBar = self.CreateStatusBar( 2, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.on_menu_settings, id = self.mnui_settings.GetId() )
		self.Bind( wx.EVT_MENU, self.on_set_image_directory, id = self.mnui_imgdir.GetId() )
		self.Bind( wx.EVT_MENU, self.on_set_data_directory, id = self.mnui_datadir.GetId() )
		self.Bind( wx.EVT_MENU, self.on_quit_app, id = self.mnui_quit.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_table.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_row_sep.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_col_sep.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_del_sep.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_sel_cell.GetId() )
		self.tbar_zoom_size.Bind( wx.EVT_CHOICE, self.on_scale_change )
		self.tbar_col_labels.Bind( wx.EVT_BUTTON, self.on_column_labels_click )
		self.tbar_prior_image.Bind( wx.EVT_BUTTON, self.on_prior_image )
		self.tbar_next_image_btn.Bind( wx.EVT_BUTTON, self.on_next_image )
		self.ocr_reread_btn.Bind( wx.EVT_BUTTON, self.on_reread_ocr )
		self.ocr_lock_text.Bind( wx.EVT_CHECKBOX, self.on_lock_ocr_text )
		self.ocr_text_edit.Bind( wx.EVT_KEY_DOWN, self.on_text_edited )
		self.nlpx_copy_ocr_text_btn.Bind( wx.EVT_BUTTON, self.on_copy_ocr_text_to_nlpx )
		self.nlpx_lock_text.Bind( wx.EVT_CHECKBOX, self.on_lock_nlpx_text )
		self.nlpx_tag.Bind( wx.EVT_CHOICE, self.on_insert_nlpx_tag )
		self.nlpx_text_edit.Bind( wx.EVT_KEY_DOWN, self.on_text_edited )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_menu_settings( self, event ):
		event.Skip()

	def on_set_image_directory( self, event ):
		event.Skip()

	def on_set_data_directory( self, event ):
		event.Skip()

	def on_quit_app( self, event ):
		event.Skip()

	def on_tbar_tool_change( self, event ):
		event.Skip()





	def on_scale_change( self, event ):
		event.Skip()

	def on_column_labels_click( self, event ):
		event.Skip()

	def on_prior_image( self, event ):
		event.Skip()

	def on_next_image( self, event ):
		event.Skip()

	def on_reread_ocr( self, event ):
		event.Skip()

	def on_lock_ocr_text( self, event ):
		event.Skip()

	def on_text_edited( self, event ):
		event.Skip()

	def on_copy_ocr_text_to_nlpx( self, event ):
		event.Skip()

	def on_lock_nlpx_text( self, event ):
		event.Skip()

	def on_insert_nlpx_tag( self, event ):
		event.Skip()



###########################################################################
## Class Fmtk_tbl_grid_col_label_dlg
###########################################################################

class Fmtk_tbl_grid_col_label_dlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Label Names", pos = wx.DefaultPosition, size = wx.Size( 314,301 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.dlg_desc2 = wx.TextCtrl( self, wx.ID_ANY, u"Column names are enumerated left-to-right and used for NLP/XML entity tagging for metadata and data export of OCR content.", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		bSizer2.Add( self.dlg_desc2, 0, wx.ALL|wx.EXPAND, 5 )

		self.tbl_grid_props = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )

		# Grid
		self.tbl_grid_props.CreateGrid( 0, 1 )
		self.tbl_grid_props.EnableEditing( True )
		self.tbl_grid_props.EnableGridLines( True )
		self.tbl_grid_props.EnableDragGridSize( False )
		self.tbl_grid_props.SetMargins( 0, 0 )

		# Columns
		self.tbl_grid_props.SetColSize( 0, 200 )
		self.tbl_grid_props.AutoSizeColumns()
		self.tbl_grid_props.EnableDragColMove( False )
		self.tbl_grid_props.EnableDragColSize( True )
		self.tbl_grid_props.SetColLabelValue( 0, u"Column label" )
		self.tbl_grid_props.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.tbl_grid_props.AutoSizeRows()
		self.tbl_grid_props.EnableDragRowSize( True )
		self.tbl_grid_props.SetRowLabelSize( 30 )
		self.tbl_grid_props.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.tbl_grid_props.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer2.Add( self.tbl_grid_props, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.chk_show_labels = wx.CheckBox( self, wx.ID_ANY, u"Show labels?", wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		self.chk_show_labels.SetValue(True)
		bSizer3.Add( self.chk_show_labels, 1, wx.ALL, 5 )

		self.dlg_cancel_btn = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		bSizer3.Add( self.dlg_cancel_btn, 0, wx.ALL, 5 )

		self.dlg_save_btn = wx.Button( self, wx.ID_OK, u"Save", wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		bSizer3.Add( self.dlg_save_btn, 0, wx.ALL, 5 )


		bSizer2.Add( bSizer3, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.on_column_label_dlg_init )
		self.tbl_grid_props.Bind( wx.EVT_SIZE, self.on_resize_adjust_column_label )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_column_label_dlg_init( self, event ):
		event.Skip()

	def on_resize_adjust_column_label( self, event ):
		event.Skip()


