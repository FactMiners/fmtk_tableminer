# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.0-4761b0c)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from fmtk_rubberband_panel import RubberbandPanel
import wx
import wx.xrc
import wx.grid

tb_TBL_BBOX = 1000
tb_ROW_SEP = 1001
tb_COL_SEP = 1002
tb_DEL_SEP = 1003
tb_SEL_CELL = 1004
tb_IMG_PREV = 1005
tb_IMG_NEXT = 1006
tb_SETTINGS_DLG = 1007
ocr_TEXT_EDIT = 1008
nlpx_TEXT_EDIT = 1009

###########################################################################
## Class FmtkTableMinerFrame
###########################################################################

class FmtkTableMinerFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FMTK TableMiner", pos = wx.DefaultPosition, size = wx.Size( 1000,1100 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

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

		self.toolbar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TB_HORIZONTAL|wx.TAB_TRAVERSAL )
		self.toolbar.SetToolBitmapSize( wx.Size( 40,40 ) )
		self.toolbar.SetToolSeparation( 10 )
		self.toolbar.SetMargins( wx.Size( 0,-20 ) )
		self.tbar_table = self.toolbar.AddTool( tb_TBL_BBOX, u"Set Table BoundingBox", wx.Bitmap( u"resources/tbl_tbar_table_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Set Table BoundingBox", wx.EmptyString, None )

		self.tbar_row_sep = self.toolbar.AddTool( tb_ROW_SEP, u"Row Separator", wx.Bitmap( u"resources/tbl_tbar_row-sep_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Row Separator", wx.EmptyString, None )

		self.tbar_col_sep = self.toolbar.AddTool( tb_COL_SEP, u"Column Separator", wx.Bitmap( u"resources/tbl_tbar_col-sep_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Column Separator", wx.EmptyString, None )

		self.tbar_del_sep = self.toolbar.AddTool( tb_DEL_SEP, u"Delete Separator", wx.Bitmap( u"resources/tbl_tbar_del-sep_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Delete Separator", wx.EmptyString, None )

		self.tbar_sel_cell = self.toolbar.AddTool( tb_SEL_CELL, u"Select Cell", wx.Bitmap( u"resources/tbl_tbar_cell_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Select Cell at Row/Col click", wx.EmptyString, None )

		self.toolbar.AddSeparator()

		self.tbar_image_prev = self.toolbar.AddTool( tb_IMG_PREV, u"Previous Image", wx.Bitmap( u"resources/tbl_tbar_img-prev_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Previous Image", wx.EmptyString, None )

		self.tbar_image_next = self.toolbar.AddTool( tb_IMG_NEXT, u"Next Image", wx.Bitmap( u"resources/tbl_tbar_img-next_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Next Image", wx.EmptyString, None )

		self.toolbar.AddSeparator()

		self.tbar_zoom_label = wx.StaticText( self.toolbar, wx.ID_ANY, u"Zoom", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tbar_zoom_label.Wrap( -1 )

		self.toolbar.AddControl( self.tbar_zoom_label )
		tbar_zoom_sizeChoices = [ u"10%", u"25%", u"50%", u"75%", u"100%", u"150%", u"200%", u"400%", wx.EmptyString, wx.EmptyString ]
		self.tbar_zoom_size = wx.Choice( self.toolbar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, tbar_zoom_sizeChoices, 0 )
		self.tbar_zoom_size.SetSelection( 4 )
		self.toolbar.AddControl( self.tbar_zoom_size )
		self.toolbar.AddSeparator()

		self.tbar_settings_dlg = self.toolbar.AddTool( tb_SETTINGS_DLG, u"Settings Dialog", wx.Bitmap( u"resources/tbl_tbar_settings_40px.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Open Settings Dialog", wx.EmptyString, None )

		self.toolbar.AddSeparator()

		self.tbar_lock_bbox = wx.CheckBox( self.toolbar, wx.ID_ANY, u"Lock Table Bbox", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tbar_lock_bbox.SetToolTip( u"Lock the bounding box of the table" )

		self.toolbar.AddControl( self.tbar_lock_bbox )
		self.toolbar.AddSeparator()

		self.toolbar.Realize()

		topWin_sizer.Add( self.toolbar, 0, wx.EXPAND, 0 )

		self.image_panel = RubberbandPanel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.image_panel.SetScrollRate( 5, 5 )
		topWin_sizer.Add( self.image_panel, 1, wx.EXPAND |wx.ALL, 5 )

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

		self.ocr_text_edit = wx.TextCtrl( self, ocr_TEXT_EDIT, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_WORDWRAP )
		self.ocr_text_edit.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
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

		self.nlpx_text_edit = wx.TextCtrl( self, nlpx_TEXT_EDIT, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_WORDWRAP|wx.HSCROLL|wx.VSCROLL )
		self.nlpx_text_edit.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
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
		self.Bind( wx.EVT_MENU, self.on_project_settings_click, id = self.mnui_settings.GetId() )
		self.Bind( wx.EVT_MENU, self.on_set_image_directory, id = self.mnui_imgdir.GetId() )
		self.Bind( wx.EVT_MENU, self.on_set_data_directory, id = self.mnui_datadir.GetId() )
		self.Bind( wx.EVT_MENU, self.on_quit_app, id = self.mnui_quit.GetId() )
		self.toolbar.Bind( wx.EVT_ENTER_WINDOW, self.on_tbar_hover_enter )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_table.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_row_sep.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_col_sep.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_del_sep.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_tbar_tool_change, id = self.tbar_sel_cell.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_image_prev, id = self.tbar_image_prev.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_image_next, id = self.tbar_image_next.GetId() )
		self.tbar_zoom_size.Bind( wx.EVT_CHOICE, self.on_scale_change )
		self.Bind( wx.EVT_TOOL, self.on_project_settings_click, id = self.tbar_settings_dlg.GetId() )
		self.ocr_reread_btn.Bind( wx.EVT_BUTTON, self.on_reread_ocr )
		self.ocr_lock_text.Bind( wx.EVT_CHECKBOX, self.on_lock_ocr_text )
		self.nlpx_copy_ocr_text_btn.Bind( wx.EVT_BUTTON, self.on_copy_ocr_text_to_nlpx )
		self.nlpx_lock_text.Bind( wx.EVT_CHECKBOX, self.on_lock_nlpx_text )
		self.nlpx_tag.Bind( wx.EVT_CHOICE, self.on_insert_nlpx_tag )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_project_settings_click( self, event ):
		event.Skip()

	def on_set_image_directory( self, event ):
		event.Skip()

	def on_set_data_directory( self, event ):
		event.Skip()

	def on_quit_app( self, event ):
		event.Skip()

	def on_tbar_hover_enter( self, event ):
		event.Skip()

	def on_tbar_tool_change( self, event ):
		event.Skip()





	def on_image_prev( self, event ):
		event.Skip()

	def on_image_next( self, event ):
		event.Skip()

	def on_scale_change( self, event ):
		event.Skip()


	def on_reread_ocr( self, event ):
		event.Skip()

	def on_lock_ocr_text( self, event ):
		event.Skip()

	def on_copy_ocr_text_to_nlpx( self, event ):
		event.Skip()

	def on_lock_nlpx_text( self, event ):
		event.Skip()

	def on_insert_nlpx_tag( self, event ):
		event.Skip()


###########################################################################
## Class FmtkTableMinerProjectDialog
###########################################################################

class FmtkTableMinerProjectDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"FmtkTableMiner Project Setup", pos = wx.DefaultPosition, size = wx.Size( 460,820 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		main_sizer = wx.BoxSizer( wx.VERTICAL )

		self.szr_help = wx.CollapsiblePane( self, wx.ID_ANY, u"Project Setup Help", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.ALWAYS_SHOW_SB )
		self.szr_help.Collapse( True )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText11 = wx.StaticText( self.szr_help.GetPane(), wx.ID_ANY, u"Scroll for more...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		self.m_staticText11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer11.Add( self.m_staticText11, 0, wx.ALL, 5 )

		self.metadlg_desc = wx.TextCtrl( self.szr_help.GetPane(), wx.ID_ANY, u"Use this dialog to set up your TableMiner project. The standard use case is to gather the document page images containing the table structure of interest to be text- and data-mined. For eample, a project might consist of a collection of magazine pages with the mastheads of a serially-published magazine containing a borderless table of staff positions and person names fulfilling those roles.\n\nTo set up your project, provide a project title and brief desciption. The the directories for the source page images and output data. You may also set the column headers for you table and provide a semicolon-spearated list of tags that can be used to annotate your mined data to enhance the ground truth OCR text on export to JSON files in the data output directory.", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		bSizer11.Add( self.metadlg_desc, 1, wx.ALL|wx.EXPAND, 5 )


		self.szr_help.GetPane().SetSizer( bSizer11 )
		self.szr_help.GetPane().Layout()
		bSizer11.Fit( self.szr_help.GetPane() )
		main_sizer.Add( self.szr_help, 0, wx.ALL|wx.EXPAND, 5 )

		szr_proj_title_desc = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Project Title and Description" ), wx.VERTICAL )

		self.project_title = wx.TextCtrl( szr_proj_title_desc.GetStaticBox(), wx.ID_ANY, u"Title", wx.DefaultPosition, wx.Size( -1,-1 ), 0|wx.TAB_TRAVERSAL )
		szr_proj_title_desc.Add( self.project_title, 0, wx.ALL|wx.EXPAND, 5 )

		self.project_description = wx.TextCtrl( szr_proj_title_desc.GetStaticBox(), wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_WORDWRAP|wx.TAB_TRAVERSAL|wx.WANTS_CHARS )
		self.project_description.SetMinSize( wx.Size( -1,40 ) )

		szr_proj_title_desc.Add( self.project_description, 0, wx.ALL|wx.EXPAND, 5 )


		main_sizer.Add( szr_proj_title_desc, 0, wx.EXPAND, 5 )

		szr_project_directories = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Project Directories" ), wx.VERTICAL )

		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

		self.project_image_dir = wx.TextCtrl( szr_project_directories.GetStaticBox(), wx.ID_ANY, u"Set image directory...", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )
		bSizer18.Add( self.project_image_dir, 1, wx.ALL|wx.EXPAND, 5 )

		self.image_dir_btn = wx.Button( szr_project_directories.GetStaticBox(), wx.ID_ANY, u"Select...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.image_dir_btn, 0, wx.ALL, 5 )


		szr_project_directories.Add( bSizer18, 1, wx.EXPAND, 5 )

		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

		self.st_img_tally_label = wx.StaticText( szr_project_directories.GetStaticBox(), wx.ID_ANY, u"Image Tally (total/done)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_img_tally_label.Wrap( -1 )

		self.st_img_tally_label.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer17.Add( self.st_img_tally_label, 0, wx.ALL, 5 )

		self.project_images_processed = wx.TextCtrl( szr_project_directories.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER|wx.TE_READONLY )
		bSizer17.Add( self.project_images_processed, 1, wx.ALL|wx.EXPAND, 5 )


		szr_project_directories.Add( bSizer17, 1, wx.EXPAND, 5 )

		bSizer181 = wx.BoxSizer( wx.HORIZONTAL )

		self.project_data_dir = wx.TextCtrl( szr_project_directories.GetStaticBox(), wx.ID_ANY, u"Set data directory...", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )
		bSizer181.Add( self.project_data_dir, 1, wx.ALL|wx.EXPAND, 5 )

		self.data_dir_btn = wx.Button( szr_project_directories.GetStaticBox(), wx.ID_ANY, u"Select...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer181.Add( self.data_dir_btn, 0, wx.ALL, 5 )


		szr_project_directories.Add( bSizer181, 1, wx.EXPAND, 5 )


		main_sizer.Add( szr_project_directories, 0, wx.EXPAND, 5 )

		szr_table_cols_tags = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Table Column Labels and NLP Tags" ), wx.VERTICAL )

		szr_col_labels = wx.BoxSizer( wx.VERTICAL )

		bSizer27 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer31 = wx.BoxSizer( wx.VERTICAL )

		self.project_column_labels = wx.grid.Grid( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )

		# Grid
		self.project_column_labels.CreateGrid( 3, 1 )
		self.project_column_labels.EnableEditing( True )
		self.project_column_labels.EnableGridLines( True )
		self.project_column_labels.EnableDragGridSize( False )
		self.project_column_labels.SetMargins( 0, 0 )

		# Columns
		self.project_column_labels.SetColSize( 0, 120 )
		self.project_column_labels.EnableDragColMove( False )
		self.project_column_labels.EnableDragColSize( True )
		self.project_column_labels.SetColLabelValue( 0, u"Column label" )
		self.project_column_labels.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.project_column_labels.AutoSizeRows()
		self.project_column_labels.EnableDragRowSize( True )
		self.project_column_labels.SetRowLabelSize( 0 )
		self.project_column_labels.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.project_column_labels.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer31.Add( self.project_column_labels, 0, wx.ALL, 5 )

		bSizer32 = wx.BoxSizer( wx.HORIZONTAL )

		self.add_label_btn = wx.Button( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, u"+", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.add_label_btn.SetToolTip( u"Add column label after selected..." )
		self.add_label_btn.SetMaxSize( wx.Size( 20,-1 ) )

		bSizer32.Add( self.add_label_btn, 0, wx.ALL, 5 )

		self.delete_label_btn = wx.Button( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.delete_label_btn.SetToolTip( u"Delete selected column label." )
		self.delete_label_btn.SetMaxSize( wx.Size( 20,-1 ) )

		bSizer32.Add( self.delete_label_btn, 0, wx.ALL, 5 )


		bSizer31.Add( bSizer32, 1, wx.EXPAND, 5 )


		bSizer27.Add( bSizer31, 0, wx.EXPAND, 5 )

		self.dlg_desc2 = wx.TextCtrl( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, u"Column names are set left-to-right, and used for structuring export data file formats.", wx.DefaultPosition, wx.Size( -1,90 ), wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		bSizer27.Add( self.dlg_desc2, 1, wx.ALL, 5 )


		szr_col_labels.Add( bSizer27, 1, wx.EXPAND, 5 )

		self.project_show_column_labels = wx.CheckBox( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, u"Show column labels while editing?", wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		self.project_show_column_labels.SetValue(True)
		szr_col_labels.Add( self.project_show_column_labels, 0, wx.ALL, 5 )

		szr_nlpx_tags = wx.BoxSizer( wx.HORIZONTAL )

		bSizer36 = wx.BoxSizer( wx.VERTICAL )

		self.project_nlp_tags = wx.grid.Grid( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )

		# Grid
		self.project_nlp_tags.CreateGrid( 3, 1 )
		self.project_nlp_tags.EnableEditing( True )
		self.project_nlp_tags.EnableGridLines( True )
		self.project_nlp_tags.EnableDragGridSize( False )
		self.project_nlp_tags.SetMargins( 0, 0 )

		# Columns
		self.project_nlp_tags.SetColSize( 0, 120 )
		self.project_nlp_tags.EnableDragColMove( False )
		self.project_nlp_tags.EnableDragColSize( True )
		self.project_nlp_tags.SetColLabelValue( 0, u"NLP Tags" )
		self.project_nlp_tags.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.project_nlp_tags.AutoSizeRows()
		self.project_nlp_tags.EnableDragRowSize( True )
		self.project_nlp_tags.SetRowLabelSize( 0 )
		self.project_nlp_tags.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.project_nlp_tags.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer36.Add( self.project_nlp_tags, 0, wx.ALL, 5 )

		bSizer321 = wx.BoxSizer( wx.HORIZONTAL )

		self.add_tag_btn = wx.Button( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, u"+", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.add_tag_btn.SetToolTip( u"Add column label after selected..." )
		self.add_tag_btn.SetMaxSize( wx.Size( 20,-1 ) )

		bSizer321.Add( self.add_tag_btn, 0, wx.ALL, 5 )

		self.delete_tag_btn = wx.Button( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.delete_tag_btn.SetToolTip( u"Delete selected column label." )
		self.delete_tag_btn.SetMaxSize( wx.Size( 20,-1 ) )

		bSizer321.Add( self.delete_tag_btn, 0, wx.ALL, 5 )


		bSizer36.Add( bSizer321, 1, wx.EXPAND, 5 )


		szr_nlpx_tags.Add( bSizer36, 0, wx.EXPAND, 5 )

		self.dlg_desc21 = wx.TextCtrl( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, u"NLP Tags are used for fine-grained data-mining of OCR text.", wx.DefaultPosition, wx.Size( -1,90 ), wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		szr_nlpx_tags.Add( self.dlg_desc21, 1, wx.ALL, 5 )


		szr_col_labels.Add( szr_nlpx_tags, 1, wx.EXPAND, 5 )

		self.project_semicolon_delimiters = wx.CheckBox( szr_table_cols_tags.GetStaticBox(), wx.ID_ANY, u"Process semicolons as item separator.", wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		szr_col_labels.Add( self.project_semicolon_delimiters, 0, wx.ALL, 5 )


		szr_table_cols_tags.Add( szr_col_labels, 1, wx.EXPAND, 5 )


		main_sizer.Add( szr_table_cols_tags, 0, wx.EXPAND, 5 )

		szr_export_formats = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Export Data Files" ), wx.VERTICAL )

		self.st_export_files_desc = wx.StaticText( szr_export_formats.GetStaticBox(), wx.ID_ANY, u"Select one or more data file export formats.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_export_files_desc.Wrap( -1 )

		szr_export_formats.Add( self.st_export_files_desc, 0, wx.ALL, 5 )

		gSizer1 = wx.GridSizer( 2, 2, 0, 0 )

		self.project_json_export = wx.CheckBox( szr_export_formats.GetStaticBox(), wx.ID_ANY, u"JSON", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.project_json_export, 0, wx.ALL, 5 )

		self.project_xml_export = wx.CheckBox( szr_export_formats.GetStaticBox(), wx.ID_ANY, u"XML", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.project_xml_export, 0, wx.ALL, 5 )

		self.project_html_export = wx.CheckBox( szr_export_formats.GetStaticBox(), wx.ID_ANY, u"HTML", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.project_html_export, 0, wx.ALL, 5 )

		self.project_csv_export = wx.CheckBox( szr_export_formats.GetStaticBox(), wx.ID_ANY, u"CSV", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.project_csv_export, 0, wx.ALL, 5 )


		szr_export_formats.Add( gSizer1, 1, wx.EXPAND, 5 )


		main_sizer.Add( szr_export_formats, 1, wx.EXPAND, 5 )

		szr_dlg_actions = wx.BoxSizer( wx.HORIZONTAL )

		self.dlg_cancel_btn = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		szr_dlg_actions.Add( self.dlg_cancel_btn, 0, wx.ALL, 5 )

		self.dlg_save_btn = wx.Button( self, wx.ID_OK, u"Save", wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		szr_dlg_actions.Add( self.dlg_save_btn, 0, wx.ALL, 5 )


		main_sizer.Add( szr_dlg_actions, 0, wx.EXPAND, 5 )


		self.SetSizer( main_sizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.image_dir_btn.Bind( wx.EVT_BUTTON, self.on_set_image_directory )
		self.data_dir_btn.Bind( wx.EVT_BUTTON, self.on_set_data_directory )
		self.project_column_labels.Bind( wx.EVT_SIZE, self.on_resize_adjust_column_label )
		self.add_label_btn.Bind( wx.EVT_BUTTON, self.on_add_label_click )
		self.delete_label_btn.Bind( wx.EVT_BUTTON, self.on_delete_label_click )
		self.project_nlp_tags.Bind( wx.EVT_SIZE, self.on_resize_adjust_column_label )
		self.add_tag_btn.Bind( wx.EVT_BUTTON, self.on_add_tag_click )
		self.delete_tag_btn.Bind( wx.EVT_BUTTON, self.on_delete_tag_click )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_set_image_directory( self, event ):
		event.Skip()

	def on_set_data_directory( self, event ):
		event.Skip()

	def on_resize_adjust_column_label( self, event ):
		event.Skip()

	def on_add_label_click( self, event ):
		event.Skip()

	def on_delete_label_click( self, event ):
		event.Skip()


	def on_add_tag_click( self, event ):
		event.Skip()

	def on_delete_tag_click( self, event ):
		event.Skip()


