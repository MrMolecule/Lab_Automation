import wx
import wx.html2 as html2
import fitz
import wx.lib.pdfwin as pdfwin
import wx.lib.pdfviewer as pdfviewer
import wx.grid as gridlib
import wx.lib.mixins.listctrl as listmix
import wx.aui
import csv
import wx.dataview as dv
from datetime import datetime

# Define sample_data at the module level: this is just a sample data set, you would need to use a different initial code to grab the data from the SQL database

sample_data = [
    ("231107001-RAP", "STEC", "06:00"),
    ("231107001-RAP", "Salmonella", "06:00"),
    ("231107002-FE", "E.Coli", "09:23"),
    ("231107103-WM", "L.Mono", "12:34"),
    ("231107020-GJ", "Listeria", "14:45"),
    ("231108004-SSF", "Salmonella", "06:00"),
    ("231107005-FE", "E.Coli", "09:23"),
    ("231107006-RAP", "Salmonella", "06:00"),
    ("231107007-FE", "E.Coli", "09:23"),
    ("231107108-WM", "L.Mono", "12:34"),
    ("231107029-GJ", "Listeria", "14:45"),
    ("231108011-SSF", "Salmonella", "06:00"),
    ("231107012-FE", "E.Coli", "09:23"),
    ("231107113-WM", "L.Mono", "12:34"),
    ("231106014-GJ", "Listeria", "14:45"),
    ("231107015-RAP", "Salmonella", "06:00"),
    ("231107016-FE", "E.Coli", "09:23"),
    ("231107117-WM", "L.Mono", "12:34"),
    ("231107018-GJ", "Listeria", "14:45"),
    ("231107019-RAP", "Salmonella", "06:00"),
    ("231107020-FE", "STEC", "09:23"),
    ("231107121-WM", "L.Mono", "12:34"),
    ("231107022-GJ", "Listeria", "14:45"),
    ("231108023-SSF", "Salmonella", "06:00"),
    ("231107024-FE", "E.Coli", "09:23"),
    ("231107125-WM", "L.Mono", "12:34"),
    ("231106026-GJ", "Listeria", "14:45"),
    ("231107027-RAP", "Salmonella", "06:00"),
    ("231107028-FE", "E.Coli", "09:23"),
    ("231107129-WM", "E.Coli", "12:34"),
    ("231107030-GJ", "Listeria", "14:45"),
    ("231107031-RAP", "STEC", "06:00"),
    ("231107032-FE", "E.Coli", "09:23"),
    ("231107133-WM", "L.Mono", "12:34"),
    ("231107034-GJ", "Listeria", "14:45"),
    ("231108035-SSF", "Salmonella", "06:00"),
    ("231107036-FE", "STEC", "09:23"),
    ("231107137-WM", "L.Mono", "12:34"),
    ("231109038-GJ", "Listeria", "14:45"),
    ("231107039-RAP", "Salmonella", "06:00"),
    ("231107040-FE", "E.Coli", "09:23"),
    ("231107041-WM", "L.Mono", "12:34"),
    ("231108042-SSF", "Salmonella", "06:00"),
    ("231107043-FE", "E.Coli", "09:23"),
    ("231107145-WM", "L.Mono", "12:34"),
    ("231106046-GJ", "Listeria", "14:45"),
    ("231107047-RAP", "Salmonella", "06:00"),
    ("231107048-FE", "E.Coli", "09:23"),
    ("231107149-WM", "E.Coli", "12:34"),
    ("231107050-GJ", "Listeria", "14:45"),
    ("231107051-RAP", "STEC", "06:00"),
    ("231107052-FE", "E.Coli", "09:23"),
    ("231107153-WM", "L.Mono", "12:34"),
    ("231107054-GJ", "Listeria", "14:45"),
    ("231108055-SSF", "Salmonella", "06:00"),
    ("231107056-FE", "STEC", "09:23"),
    ("231107157-WM", "L.Mono", "12:34"),
    ("231109058-GJ", "Listeria", "14:45"),
    ("231107059-RAP", "Salmonella", "06:00"),
    ("231107060-FE", "E.Coli", "09:23"),
    ("231107061-WM", "L.Mono", "12:34"),
]

class MainWindow(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)

        self.SetSize((550, 250))    
        self.panel = wx.Panel(self)

        main_panel = wx.GridBagSizer(vgap=10, hgap=10)

        # Group 1: Gene UP and BAX
        group1_label = wx.StaticText(self.panel, label="PCR Methods:")
        group1_label.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        main_panel.Add(group1_label, pos=(0, 0), span=(1, 2), flag=wx.EXPAND | wx.ALIGN_CENTER)

        GeneUP_button = wx.Button(self.panel, label="Gene UP")
        BAX_button = wx.Button(self.panel, label="BAX")
        main_panel.Add(GeneUP_button, pos=(1, 0), flag=wx.EXPAND)
        main_panel.Add(BAX_button, pos=(1, 1), flag=wx.EXPAND)

        # Group 2: VIDAS and Romer
        group2_label = wx.StaticText(self.panel, label="ELISA Methods:")
        group2_label.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        main_panel.Add(group2_label, pos=(2, 0), span=(1, 2), flag=wx.EXPAND | wx.ALIGN_CENTER)

        VIDAS_button = wx.Button(self.panel, label="VIDAS")
        Romer_button = wx.Button(self.panel, label="Romer")
        main_panel.Add(VIDAS_button, pos=(3, 0), flag=wx.EXPAND)
        main_panel.Add(Romer_button, pos=(3, 1), flag=wx.EXPAND)

        # Group 3: Pour Plates and PetriFilm
        group3_label = wx.StaticText(self.panel, label="Cultured Colonies:")
        total_samples = len(sample_data[0])
        group3b_label =wx.StaticText(self.panel, label=f"Total Samples: {total_samples}")
        group3_label.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        main_panel.Add(group3_label, pos=(4, 0), span=(1, 2), flag=wx.EXPAND | wx.ALIGN_CENTER)
        group3b_label.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        main_panel.Add(group3b_label, pos=(7, 0), span=(1, 2), flag=wx.EXPAND | wx.ALIGN_CENTER)
        
        Plates_button = wx.Button(self.panel, label="Pour Plates and Petrifilms")
        main_panel.Add(Plates_button, pos=(5, 0), span=(1, 2), flag=wx.EXPAND)

        # Add an extra row with a vertical gap
        main_panel.Add((0, 0), pos=(6, 0), span=(1, 2))

        main_panel.AddGrowableCol(0)
        main_panel.AddGrowableCol(1)
        main_panel.AddGrowableRow(0)
        main_panel.AddGrowableRow(1)
        main_panel.AddGrowableRow(2)
        main_panel.AddGrowableRow(3)
        main_panel.AddGrowableRow(4)

        self.panel.SetSizer(main_panel)

        self.Show()
        
        # Bind buttons to the on_button_click method
        GeneUP_button.Bind(wx.EVT_BUTTON, self.on_button_click)
        BAX_button.Bind(wx.EVT_BUTTON, self.on_button_click)
        VIDAS_button.Bind(wx.EVT_BUTTON, self.on_button_click)
        Romer_button.Bind(wx.EVT_BUTTON, self.on_button_click)

        
    def on_button_click(self, event):
        button_label = event.GetEventObject().GetLabel()

        if button_label== "Gene UP":
            # Open a new window with the GU from Element samples
            app = wx.GetApp()
            app.second_frame = GeneUP_Frame(None, title="Sample Selection Window for Gene Up")
            app.second_frame.Show()

        elif button_label == "BAX":
            # Open a new window for BAX button
            app = wx.GetApp()
            app.bax_frame = BAX_Frame(None, title="Sample Selection Window for BAX")
            app.bax_frame.Show()
        elif button_label == "VIDAS":
            # Open a new window for VIDAS button
            app = wx.GetApp()
            app.vidas_frame = VIDAS_Frame(None, title="Sample Selection Window for VIDAS")
            app.vidas_frame.Show()
        elif button_label == "Romer":
            # Open a new window for Romer button
            app = wx.GetApp()
            app.romer_frame = Romer_Frame(None, title="Sample Selection Window for Romer")
            app.romer_frame.Show()
            
                        
class GeneUP_Frame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1000, 400))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.selected_samples = []


         # Create the menu bar
        status = self.CreateStatusBar()
        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        editButton = wx.Menu()
        crButton = wx.Menu()
        fileButton.Append(wx.NewId(), "Exit", "Exit")
        editButton.Append(wx.NewId(), "Sort", "Sort")
        crButton.Append(wx.NewId(), "Automatic Select", "Automatic Select")
        crButton.Append(wx.NewId(), "Manual Select", "Manual Select")
        menuBar.Append(fileButton, "File")
        menuBar.Append(editButton, "Edit")
        menuBar.Append(crButton, "Create Run")
        self.SetMenuBar(menuBar)
        
        
        # Create a panel to contain the list
        self.panel = wx.Panel(self)  # Define panel as self.panel
        current_font = self.panel.GetFont()
        current_font.SetPointSize(16)
        self.panel.SetFont(current_font)
        
        
        # Create a DataViewListCtrl widget for displaying the sample list
        self.dvlc = dv.DataViewListCtrl(self.panel, style= wx.dataview.DV_MULTIPLE)
        self.dvlc.AppendTextColumn('Sample ID', width=150)
        self.dvlc.AppendTextColumn('Test Name', width=200)
        self.dvlc.AppendTextColumn('Incubation Time Achieved At (hours)', width=200)

        # Populate the DataViewListCtrl with sample data
        for data in sample_data:
            self.dvlc.AppendItem(data)
            
        self.sizer.Add(self.dvlc, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(self.sizer)
        

        # Create a "Select Samples" button
        select_button = wx.Button(self.panel, label="Select Samples")
        select_button.Bind(wx.EVT_BUTTON, self.OnSelectSamples)
        self.sizer.Add(select_button, 0, wx.ALL | wx.EXPAND, 5)      
        

        # Bind the DataViewListCtrl column click event to the sorting method
        self.dvlc.Bind(dv.EVT_DATAVIEW_COLUMN_HEADER_CLICK, self.OnColumnHeaderClick)

    def OnColumnHeaderClick(self, event):
        col = event.GetColumn()
        # Assuming sorting based on the first column (change logic as needed)
        self.SortByColumn(col)

    def SortByColumn(self, col):
        items = [
            (
            self.dvlc.GetTextValue(row, 0),  # Get Sample IDs
            self.dvlc.GetTextValue(row, 1),
            self.dvlc.GetTextValue(row, 2)
        )
        for row in range(self.dvlc.GetItemCount())
    ]
        sorted_items = sorted(items, key=lambda x: x[col])
        self.dvlc.DeleteAllItems()
        for item in sorted_items:
            self.dvlc.AppendItem(item)

        # Bind the Sort menu item to the sorting method
        self.Bind(wx.EVT_MENU, lambda event, data=sample_data: self.OnSort(event, data=data), id=wx.ID_ANY)


    def OnSort(self, event, data):
        
         # Now the OnSort method has access to the 'data' variable passed from SortByColumn
        sorted_data = sorted(data, key=lambda x: self.to_datetime(x[2]))  # assuming third column (index 2) is for time

        # Update the ListCtrl with sorted data
        self.UpdateListCtrl(sorted_data)

    def GetListCtrlData(self):
        data = []
        for index in range(self.dvlc.GetItemCount()):
            item = [
                self.dvlc.GetTextValue(index, col)
                for col in range(self.dvlc.GetColumnCount())
            ]
            data.append(item)
        return data

    @staticmethod
    def to_datetime(time_str):
        try:
            return datetime.strptime(time_str, "%H:%M")
        except ValueError:
            return datetime.strptime("00:00", "%H:%M")  # Default value for incorrect data    


    def GetIndexFromDataViewItem(self, item):
        for index in range(self.dvlc.GetItemCount()):
            if self.dvlc.GetStore().GetItem(index) == item:
                return index
        raise ValueError("Item index not found")

    def OnSelectSamples(self, event):
        
        #Clear selected_samples before populating it again
        self.selected_samples.clear()
        #print("selected samples", self)
        
        selected_items =self.dvlc.GetSelections()
        #print("total selected:", len(selected_items)) #print total count
        
        for item in selected_items:
            try:
                item_index = self.GetIndexFromDataViewItem(item)
                item_data = [
                    self.dvlc.GetTextValue(item_index, col)
                    for col in range(self.dvlc.GetColumnCount())
                ]
                #print("Item Data:", item_data)
                self.selected_samples.append(item_data)
            except Exception as e:
                #print(f"Error retrieving data for index {item_index}::{e}")
                
                   
                #print("Item Data:", item_data)  # Check if item data is retrieved correctly

                self.selected_samples.append(item_data)
        
                    
        #print("Selected Samples:", self.selected_samples)  # Check the content of selected samples
        #call a method or perform actions with selected_samples here or trigger another function
        self.ProcessSelectedSamples()
    
    # Inside ProcessSelectedSamples
    def ProcessSelectedSamples(self):
        selected_samples = self.selected_samples  # Your selected samples list
        #print("Processing Selected Samples:", selected_samples)  # Check if data is received here correctly
        if selected_samples:
            self.OpenSecondWindow(selected_samples)
        else:
            pass

    def TransformSamples(self, samples):
        # Perform transformation of selected samples into the format accepted by UpdateListCtrl
        transformed_data = []
        for sample in samples:
            # Convert the DataViewListCtrl format (sample data) to the expected format for UpdateListCtrl
            transformed_item = [value for value in sample]
            transformed_data.append(transformed_item)
        return transformed_data
        print("transformed data", transformed_data)
    

    def OpenSecondWindow(self, selected_samples):
        #print("Opening Second Window with Samples:", selected_samples)  # Check if data is received here correctly
        if selected_samples is not None:
            
            app = wx.GetApp()  # Get the wx.App instance
            app.frame2 = GeneUP_SecondWindow(None, title="Create Gene Up Run", selected_samples=selected_samples)
            #app.frame2.UpdateData(selected_samples)
            app.frame2.Show()
        else:
            print("No Samples selected.")


class BAX_Frame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1000, 400))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.selected_samples = []


         # Create the menu bar
        status = self.CreateStatusBar()
        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        editButton = wx.Menu()
        crButton = wx.Menu()
        fileButton.Append(wx.NewId(), "Exit", "Exit")
        editButton.Append(wx.NewId(), "Sort", "Sort")
        crButton.Append(wx.NewId(), "Automatic Select", "Automatic Select")
        crButton.Append(wx.NewId(), "Manual Select", "Manual Select")
        menuBar.Append(fileButton, "File")
        menuBar.Append(editButton, "Edit")
        menuBar.Append(crButton, "Create Run")
        self.SetMenuBar(menuBar)
        
        
        # Create a panel to contain the list
        self.panel = wx.Panel(self)  # Define panel as self.panel
        current_font = self.panel.GetFont()
        current_font.SetPointSize(16)
        self.panel.SetFont(current_font)
        
        
        # Create a DataViewListCtrl widget for displaying the sample list
        self.dvlc = dv.DataViewListCtrl(self.panel, style= wx.dataview.DV_MULTIPLE)
        self.dvlc.AppendTextColumn('Sample ID', width=150)
        self.dvlc.AppendTextColumn('Test Name', width=200)
        self.dvlc.AppendTextColumn('Incubation Time Achieved At (hours)', width=200)

        # Populate the DataViewListCtrl with sample data
        for data in sample_data:
            self.dvlc.AppendItem(data)
            
        self.sizer.Add(self.dvlc, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(self.sizer)
        

        # Create a "Select Samples" button
        select_button = wx.Button(self.panel, label="Select Samples")
        select_button.Bind(wx.EVT_BUTTON, self.OnSelectSamples)
        self.sizer.Add(select_button, 0, wx.ALL | wx.EXPAND, 5)      
        

        # Bind the DataViewListCtrl column click event to the sorting method
        self.dvlc.Bind(dv.EVT_DATAVIEW_COLUMN_HEADER_CLICK, self.OnColumnHeaderClick)

    def OnColumnHeaderClick(self, event):
        col = event.GetColumn()
        # Assuming sorting based on the first column (change logic as needed)
        self.SortByColumn(col)

    def SortByColumn(self, col):
        items = [
            (
            self.dvlc.GetTextValue(row, 0),  # Get Sample IDs
            self.dvlc.GetTextValue(row, 1),
            self.dvlc.GetTextValue(row, 2)
        )
        for row in range(self.dvlc.GetItemCount())
    ]
        sorted_items = sorted(items, key=lambda x: x[col])
        self.dvlc.DeleteAllItems()
        for item in sorted_items:
            self.dvlc.AppendItem(item)

        # Bind the Sort menu item to the sorting method
        self.Bind(wx.EVT_MENU, lambda event, data=sample_data: self.OnSort(event, data=data), id=wx.ID_ANY)


    def OnSort(self, event, data):
        
         # Now the OnSort method has access to the 'data' variable passed from SortByColumn
        sorted_data = sorted(data, key=lambda x: self.to_datetime(x[2]))  # assuming third column (index 2) is for time

        # Update the ListCtrl with sorted data
        self.UpdateListCtrl(sorted_data)

    def GetListCtrlData(self):
        data = []
        for index in range(self.dvlc.GetItemCount()):
            item = [
                self.dvlc.GetTextValue(index, col)
                for col in range(self.dvlc.GetColumnCount())
            ]
            data.append(item)
        return data

    @staticmethod
    def to_datetime(time_str):
        try:
            return datetime.strptime(time_str, "%H:%M")
        except ValueError:
            return datetime.strptime("00:00", "%H:%M")  # Default value for incorrect data    


    def GetIndexFromDataViewItem(self, item):
        for index in range(self.dvlc.GetItemCount()):
            if self.dvlc.GetStore().GetItem(index) == item:
                return index
        raise ValueError("Item index not found")

    def OnSelectSamples(self, event):
        
        #Clear selected_samples before populating it again
        self.selected_samples.clear()
        #print("selected samples", self)
        
        selected_items =self.dvlc.GetSelections()
        #print("total selected:", len(selected_items)) #print total count
        
        for item in selected_items:
            try:
                item_index = self.GetIndexFromDataViewItem(item)
                item_data = [
                    self.dvlc.GetTextValue(item_index, col)
                    for col in range(self.dvlc.GetColumnCount())
                ]
                #print("Item Data:", item_data)
                self.selected_samples.append(item_data)
            except Exception as e:
                #print(f"Error retrieving data for index {item_index}::{e}")
                
                   
                #print("Item Data:", item_data)  # Check if item data is retrieved correctly

                self.selected_samples.append(item_data)
        
                    
        #print("Selected Samples:", self.selected_samples)  # Check the content of selected samples
        #call a method or perform actions with selected_samples here or trigger another function
        self.ProcessSelectedSamples()
    
    # Inside ProcessSelectedSamples
    def ProcessSelectedSamples(self):
        selected_samples = self.selected_samples  # Your selected samples list
        #print("Processing Selected Samples:", selected_samples)  # Check if data is received here correctly
        if selected_samples:
            self.OpenSecondWindow(selected_samples)
        else:
            pass

    def TransformSamples(self, samples):
        # Perform transformation of selected samples into the format accepted by UpdateListCtrl
        transformed_data = []
        for sample in samples:
            # Convert the DataViewListCtrl format (sample data) to the expected format for UpdateListCtrl
            transformed_item = [value for value in sample]
            transformed_data.append(transformed_item)
        return transformed_data
        print("transformed data", transformed_data)
    

    def OpenSecondWindow(self, selected_samples):
        #print("Opening Second Window with Samples:", selected_samples)  # Check if data is received here correctly
        if selected_samples is not None:
            
            app = wx.GetApp()  # Get the wx.App instance
            app.frame2 = BAX_SecondWindow(None, title="Create BAX Run", selected_samples=selected_samples)
            #app.frame2.UpdateData(selected_samples)
            app.frame2.Show()
        else:
            print("No Samples selected.")

        
class OverlayPanel(wx.Panel):
    def __init__(self, parent, size, pdf_path):
        super().__init__(parent)
        self.size = size
        self.pdf_path = pdf_path
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        if gc:
            self.DrawOverlay(gc)

    def DrawOverlay(self, gc):
        pdf_document = fitz.open(self.pdf_path)
        pdf_page = pdf_document.load_page(0)

        # Convert PDF to image
        pixmap = pdf_page.get_pixmap()
        width, height = pixmap.width, pixmap.height
        image_data = pixmap.samples

        # Convert image data to wx.Bitmap
        wx_bitmap = wx.Bitmap.FromBuffer(width, height, image_data)

        # Draw the PDF image
        gc.DrawBitmap(wx_bitmap, 0, 0, width, height)

        # Draw grid and sample IDs
        grid_size = (12, 8)  # Adjust as needed
        cell_width = width // grid_size[0]
        cell_height = height // grid_size[1]

        gc.SetPen(wx.Pen(wx.Colour(255, 0, 0), 2))  # Red grid lines

        for col in range(1, grid_size[0]):
            x = col * cell_width
            gc.StrokeLine(x, 0, x, height)

        for row in range(1, grid_size[1]):
            y = row * cell_height
            gc.StrokeLine(0, y, width, y)

        gc.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        gc.SetTextForeground(wx.Colour(0, 0, 255))  # Blue text

        for col in range(grid_size[0]):
            for row in range(grid_size[1]):
                sample_id = f"Sample {col * grid_size[1] + row + 1}"
                x = col * cell_width + cell_width // 2
                y = row * cell_height + cell_height // 2
                gc.DrawText(sample_id, x, y)


class GeneUP_SecondWindow(wx.Frame):
    def __init__(self, parent, title, selected_samples=None):
        super().__init__(parent, title=title, size=(1300, 400))
        self.selected_samples = selected_samples if selected_samples else []
        self.mgr = wx.aui.AuiManager(self)
        self.pdf_path = "/Users/carlosparedes/Desktop/Lab Automation/WS513_PCR_Template.pdf"
        
        self.middle_sizer = None 
        
        
        # Create panels
        self.top_panel = wx.Panel(self)
        self.middle_panel = wx.Panel(self)
        bottom_panel = wx.Panel(self)


        desired_order = ["E.Coli", "STEC", "Salmonella", "Listeria", "L.Mono"]
        # Top Panel
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
       
        for test_name in desired_order:
            for data in selected_samples:
                if data[1] == test_name:
                    
                    button = wx.Button(self.top_panel, label= test_name, style = wx.BU_EXACTFIT)
                    top_sizer.Add(button, 1, wx.EXPAND)
                    break
                
        self.top_panel.SetSizer(top_sizer)

        # Middle Panel
        self.UpdateData(selected_samples)  # Call UpdateData to initialize the middle_panel

        # Bottom Panel
        bottom_panel = wx.Panel(self)
        self.panel = wx.Panel(self)
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(bottom_panel, label="Save Layout", style=wx.BU_EXACTFIT)
        save_button.Bind(wx.EVT_BUTTON, self.OnSaveLayout)
        overlay_button = wx.Button(bottom_panel, label= "View Worksheet with Overlay)", style=wx.RIGHT)
        overlay_button.Bind(wx.EVT_BUTTON, self.OnOverlayView)
        bottom_sizer.Add(overlay_button, 0, wx.EXPAND)
        bottom_sizer.Add(save_button, 0, wx.EXPAND)
        bottom_panel.SetSizer(bottom_sizer)

        
        
        
        # Add panes to the AuiManager
        self.mgr.AddPane(
            self.top_panel,
            wx.aui.AuiPaneInfo().Top().Layer(0).BottomDockable(False).TopDockable(False).LeftDockable(False).RightDockable(False)
        )
        self.mgr.AddPane(
            self.middle_panel,
            wx.aui.AuiPaneInfo().Center().Layer(1).BottomDockable(False).TopDockable(False).LeftDockable(False).RightDockable(False)
        )
        self.mgr.AddPane(
            bottom_panel,
            wx.aui.AuiPaneInfo().Bottom().Layer(2).BottomDockable(False).TopDockable(False).LeftDockable(False).RightDockable(False)
        )

        # Update the manager
        self.mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    
    def UpdateData(self, selected_samples):
        self.buttons = []
        self.middle_sizer = wx.GridBagSizer(8, 12)
        #print("selected samples in second window", selected_samples)
        
        
        
        desired_order = ["E.Coli", "STEC", "Salmonella", "Listeria", "L.Mono"]
        test_groups = {}
        col_offset = 0

        #labels = [str(i) for i in range(1, 97)]

        
        for test_name in desired_order:
            for label_index in range(len(selected_samples)):
                label = selected_samples[label_index][0]
                current_test_name = selected_samples[label_index][1]

                if current_test_name == test_name:
                    if test_name not in test_groups:
                        test_groups[test_name] = {'column': len(test_groups) + col_offset, 'row': 0}

                    col = test_groups[test_name]['column']
                    row = test_groups[test_name]['row']

                    button = wx.Button(self.middle_panel, label=label, style=wx.BU_EXACTFIT)
                    self.middle_sizer.Add(button, pos=(row, col), flag=wx.EXPAND)
                    button.Bind(wx.EVT_BUTTON, lambda event: self.ChangeValue(event, button))
                    self.buttons.append(button)
                    #button = wx.Colour
                    #self.buttons.SetBackgroundColour ((255, 230, 200,255))
                    #print(f"Button placed at ({row}, {col}) with label: {label}")
                
                    
                    # Increment row or change column when needed
                    test_groups[test_name]['row'] += 1
                    if test_groups[test_name]['row'] >= 8:
                        test_groups[test_name]['column'] += 1
                        col_offset += 1
                        test_groups[test_name]['row'] = 0
            
        
    # Assuming num_columns is the total number of columns in your grid
        for col in range(12):
            for row in range(8):
                if self.middle_sizer.FindItemAtPosition((row, col)) is None:
                    label_index = col * 8 + row + 1
                    label = str(label_index) if label_index <= 96 else str(label_index)
                    button = wx.Button(self.middle_panel, label=label, style=wx.BU_EXACTFIT)
                    self.middle_sizer.Add(button, pos=(row, col), flag=wx.EXPAND)
                    button.Bind(wx.EVT_BUTTON, lambda event, btn=button: self.ChangeValue(event, btn))
                    self.buttons.append(button)
                    
                    
        
        
        
        self.middle_panel.SetSizerAndFit(self.middle_sizer)
        self.middle_sizer.Fit(self.middle_panel)
        self.mgr.Update()

                    



    def ChangeValue(self, event, button):
        dlg = wx.TextEntryDialog(self, "What Sample ID would you like to run in this well?", "Reassign Well", button.GetLabel())
        if dlg.ShowModal() == wx.ID_OK:
            new_label = dlg.GetValue()
            button.SetLabel(new_label)
        dlg.Destroy()
    
    
    def GetTransformedName(self, sample_id):
        transformation_map = {
            "Cronobacter": "CRO",
            "E.Coli": "ECO",
            "STEC": "EH1",
            "Listeria": "LIS",
            "L.Mono": "LMO",
            "Salmonella": "SLM",
            # Add more transformations if needed
        }

        for sample in self.selected_samples:
            if sample[0] == sample_id:
                test_name = sample[1]
                transformed_name = transformation_map.get(test_name.strip(), "")
                #if not transformed_name:
                    #print(f"No transformation found for '{test_name.strip()}'")
                #else:
                    #print("Transformed Name:", transformed_name)
                
                return transformed_name
    
        print(f"No sample found for sample ID: '{sample_id}'")
        return ""
    
    
    
    def OnSaveLayout(self, event):
        test_order = ["E.Coli", "STEC", "Salmonella", "Listeria", "L.Mono"]
        grouped_samples = {test: [] for test in test_order}

        # Group selected samples by test name
        for sample in self.selected_samples:
            test_name = sample[1]
            if test_name in grouped_samples:
                grouped_samples[test_name].append(sample)

        grid_data = []
        for test_name in test_order:
            if grouped_samples[test_name]:
                # Add a separator for better readability
                #grid_data.append([f"----- {test_name} -----", ""])
                # Append samples for each test name in the desired order
                for sample in grouped_samples[test_name]:
                    sample_id = sample[0]
                    transformed_name = self.GetTransformedName(sample_id)
                    grid_data.append([sample_id, transformed_name,"", "", "", ""])

        with wx.FileDialog(
            self,
            "Save CSV file",
            wildcard="CSV files (*.csv)|*.csv",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            filepath = fileDialog.GetPath()

            with open(filepath, "w", newline="") as file:
                writer = csv.writer(file)
                #writer.writerow(["Sample ID", "Transformed Test Code", "", "", "", ""])
                writer.writerows(grid_data)
        
        #CSV for GeneUp needs to be in the following format:
        #"Sample ID", "Assay", "Matrix", "Customer", "Production Lot #", "Notes"
        #for EX: "Sample ID", "ECO", "", "", "", ""
        #EX2: "231127001-RAP", "LIS", "Dog Food", "RAP", "1Q2 214B", ""
    
    
    def OnOverlayView(self, event):
    

        # Create a new frame to display the PDF with overlay
        overlay_frame = wx.Frame(None, title="Worksheet with Overlay", size=(800, 600))

        # Create the custom overlay panel with the specified PDF path
        overlay_panel = OverlayPanel(overlay_frame, self.pdf_path, (800, 600))

        pdf_path = "/Users/carlosparedes/Desktop/Lab Automation/WS513_PCR_Template.pdf"
       
        pdf_window = fitz.open(pdf_path)

        # Extract the first page
        pdf_page = pdf_window.load_page(0)

        # Convert PDF to image
        pixmap = pdf_page.get_pixmap()
        width, height = pixmap.width, pixmap.height
        image_data = pixmap.samples

        # Convert image data to wx.Bitmap
        wx_bitmap = wx.Bitmap.FromBuffer(width, height, image_data)

        # Display the image using wx.StaticBitmap
        static_bitmap = wx.StaticBitmap(overlay_panel, wx.ID_ANY, wx_bitmap)

        # Create a sizer for overlay_panel
        overlay_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        overlay_panel_sizer.Add(static_bitmap, 1, wx.EXPAND)
        overlay_panel.SetSizer(overlay_panel_sizer)
        
        # Show the overlay frame
        overlay_frame.Show()

    
    def OnClose(self, event):
        self.mgr.UnInit()
        self.Destroy()


class BAX_SecondWindow(wx.Frame):
    def __init__(self, parent, title, selected_samples=None):
        super().__init__(parent, title=title, size=(1300, 400))
        self.selected_samples = selected_samples if selected_samples else []
        self.mgr = wx.aui.AuiManager(self)
        self.pdf_path = "/Users/carlosparedes/Desktop/Lab Automation/WS557_BAX_PCR_Template.pdf"
        self.middle_sizer = None 
        
        
        # Create panels
        self.top_panel = wx.Panel(self)
        self.middle_panel = wx.Panel(self)
        bottom_panel = wx.Panel(self)


        desired_order = ["E.Coli", "STEC", "Salmonella", "Listeria", "L.Mono"]
        # Top Panel
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
       
        for test_name in desired_order:
            for data in selected_samples:
                if data[1] == test_name:
                    
                    button = wx.Button(self.top_panel, label= test_name, style = wx.BU_EXACTFIT)
                    top_sizer.Add(button, 1, wx.EXPAND)
                    break
                
        self.top_panel.SetSizer(top_sizer)

        # Middle Panel
        self.UpdateData(selected_samples)  # Call UpdateData to initialize the middle_panel

        # Bottom Panel
        bottom_panel = wx.Panel(self)
        self.panel = wx.Panel(self)
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(bottom_panel, label="Save Layout", style=wx.BU_EXACTFIT)
        save_button.Bind(wx.EVT_BUTTON, self.OnSaveLayout)
        overlay_button = wx.Button(bottom_panel, label= "View Worksheet with Overlay)", style=wx.RIGHT)
        overlay_button.Bind(wx.EVT_BUTTON, self.OnOverlayView)
        bottom_sizer.Add(overlay_button, 0, wx.EXPAND)
        bottom_sizer.Add(save_button, 0, wx.EXPAND)
        bottom_panel.SetSizer(bottom_sizer)

        
        
        
        # Add panes to the AuiManager
        self.mgr.AddPane(
            self.top_panel,
            wx.aui.AuiPaneInfo().Top().Layer(0).BottomDockable(False).TopDockable(False).LeftDockable(False).RightDockable(False)
        )
        self.mgr.AddPane(
            self.middle_panel,
            wx.aui.AuiPaneInfo().Center().Layer(1).BottomDockable(False).TopDockable(False).LeftDockable(False).RightDockable(False)
        )
        self.mgr.AddPane(
            bottom_panel,
            wx.aui.AuiPaneInfo().Bottom().Layer(2).BottomDockable(False).TopDockable(False).LeftDockable(False).RightDockable(False)
        )

        # Update the manager
        self.mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    
    def UpdateData(self, selected_samples):
        self.buttons = []
        self.middle_sizer = wx.GridBagSizer(8, 12)
        #print("selected samples in second window", selected_samples)
        
        
        
        desired_order = ["E.Coli", "STEC", "Salmonella", "Listeria", "L.Mono"]
        test_groups = {}
        col_offset = 0

        #labels = [str(i) for i in range(1, 97)]

        
        for test_name in desired_order:
            for label_index in range(len(selected_samples)):
                label = selected_samples[label_index][0]
                current_test_name = selected_samples[label_index][1]

                if current_test_name == test_name:
                    if test_name not in test_groups:
                        test_groups[test_name] = {'column': len(test_groups) + col_offset, 'row': 0}

                    col = test_groups[test_name]['column']
                    row = test_groups[test_name]['row']

                    button = wx.Button(self.middle_panel, label=label, style=wx.BU_EXACTFIT)
                    self.middle_sizer.Add(button, pos=(row, col), flag=wx.EXPAND)
                    button.Bind(wx.EVT_BUTTON, lambda event: self.ChangeValue(event, button))
                    self.buttons.append(button)
                    #button = wx.Colour
                    #self.buttons.SetBackgroundColour ((255, 230, 200,255))
                    #print(f"Button placed at ({row}, {col}) with label: {label}")
                
                    
                    # Increment row or change column when needed
                    test_groups[test_name]['row'] += 1
                    if test_groups[test_name]['row'] >= 8:
                        test_groups[test_name]['column'] += 1
                        col_offset += 1
                        test_groups[test_name]['row'] = 0
            
        
    # Assuming num_columns is the total number of columns in your grid
        for col in range(12):
            for row in range(8):
                if self.middle_sizer.FindItemAtPosition((row, col)) is None:
                    label_index = col * 8 + row + 1
                    label = str(label_index) if label_index <= 96 else str(label_index)
                    button = wx.Button(self.middle_panel, label=label, style=wx.BU_EXACTFIT)
                    self.middle_sizer.Add(button, pos=(row, col), flag=wx.EXPAND)
                    button.Bind(wx.EVT_BUTTON, lambda event, btn=button: self.ChangeValue(event, btn))
                    self.buttons.append(button)
                    
                    
        
        
        
        self.middle_panel.SetSizerAndFit(self.middle_sizer)
        self.middle_sizer.Fit(self.middle_panel)
        self.mgr.Update()

                    



    def ChangeValue(self, event, button):
        dlg = wx.TextEntryDialog(self, "What Sample ID would you like to run in this well?", "Reassign Well", button.GetLabel())
        if dlg.ShowModal() == wx.ID_OK:
            new_label = dlg.GetValue()
            button.SetLabel(new_label)
        dlg.Destroy()
    
    
    def GetTransformedName(self, sample_id):
        transformation_map = {
            "Cronobacter": "CRO",
            "E.Coli": "ECO",
            "STEC": "EH1",
            "Listeria": "LIS",
            "L.Mono": "LMO",
            "Salmonella": "SLM",
            # Add more transformations if needed
        }

        for sample in self.selected_samples:
            if sample[0] == sample_id:
                test_name = sample[1]
                transformed_name = transformation_map.get(test_name.strip(), "")
                #if not transformed_name:
                    #print(f"No transformation found for '{test_name.strip()}'")
                #else:
                    #print("Transformed Name:", transformed_name)
                
                return transformed_name
    
        print(f"No sample found for sample ID: '{sample_id}'")
        return ""
    
    
    
    def OnSaveLayout(self, event):
        test_order = ["E.Coli", "STEC", "Salmonella", "Listeria", "L.Mono"]
        grouped_samples = {test: [] for test in test_order}

        # Group selected samples by test name
        for sample in self.selected_samples:
            test_name = sample[1]
            if test_name in grouped_samples:
                grouped_samples[test_name].append(sample)

        grid_data = []
        for test_name in test_order:
            if grouped_samples[test_name]:
                # Add a separator for better readability
                #grid_data.append([f"----- {test_name} -----", ""])
                # Append samples for each test name in the desired order
                for sample in grouped_samples[test_name]:
                    sample_id = sample[0]
                    transformed_name = self.GetTransformedName(sample_id)
                    grid_data.append([sample_id, transformed_name,"", "", "", ""])

        with wx.FileDialog(
            self,
            "Save CSV file",
            wildcard="CSV files (*.csv)|*.csv",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            filepath = fileDialog.GetPath()

            with open(filepath, "w", newline="") as file:
                writer = csv.writer(file)
                #writer.writerow(["Sample ID", "Transformed Test Code", "", "", "", ""])
                writer.writerows(grid_data)
        
        #CSV for GeneUp needs to be in the following format:
        #"Sample ID", "Assay", "Matrix", "Customer", "Production Lot #", "Notes"
        #for EX: "Sample ID", "ECO", "", "", "", ""
        #EX2: "231127001-RAP", "LIS", "Dog Food", "RAP", "1Q2 214B", ""
    
    
    def OnOverlayView(self, event):
        

        # Create a new frame to display the PDF with overlay
        overlay_frame = wx.Frame(None, title="Worksheet with Overlay", size=(800, 600))

        # Create the custom overlay panel with the specified PDF path
        overlay_panel = OverlayPanel(overlay_frame, self.pdf_path, (800, 600))

    
        pdf_path = "/Users/carlosparedes/Desktop/Lab Automation/WS557_BAX_PCR_Template.pdf"
       
        pdf_window = fitz.open(pdf_path)

        # Extract the first page
        pdf_page = pdf_window.load_page(0)

        # Convert PDF to image
        pixmap = pdf_page.get_pixmap()
        width, height = pixmap.width, pixmap.height
        image_data = pixmap.samples

        # Convert image data to wx.Bitmap
        wx_bitmap = wx.Bitmap.FromBuffer(width, height, image_data)

        # Display the image using wx.StaticBitmap
        static_bitmap = wx.StaticBitmap(overlay_panel, wx.ID_ANY, wx_bitmap)

        # Create a sizer for overlay_panel
        overlay_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        overlay_panel_sizer.Add(static_bitmap, 1, wx.EXPAND)
        overlay_panel.SetSizer(overlay_panel_sizer)
        
        # Show the overlay frame
        overlay_frame.Show()

    
    def OnClose(self, event):
        self.mgr.UnInit()
        self.Destroy()


class Romer_Frame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self.panel = wx.Panel(self)

        # Display PDF using PyMuPDF
        pdf_path =  "/Users/carlosparedes/Desktop/Lab Automation/WS509_ELISA_Template.pdf"
        pdf_document = fitz.open(pdf_path)

        # Extract the first page
        pdf_page = pdf_document.load_page(0)

        # Convert PDF to image
        pixmap = pdf_page.get_pixmap()
        width, height = pixmap.width, pixmap.height
        image_data = pixmap.samples

        # Convert image data to wx.Bitmap
        wx_bitmap = wx.Bitmap.FromBuffer(width, height, image_data)

        # Display the image using wx.StaticBitmap
        static_bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, wx_bitmap)

        # Set the static_bitmap as the main sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(static_bitmap, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

        self.Show()

        
class VIDAS_Frame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self.panel = wx.Panel(self)

        # Create a splitter window
        splitter = wx.SplitterWindow(self.panel)

        # Create the left panel for the PDF
        pdf_panel = wx.Panel(splitter)
        pdf_path = "/Users/carlosparedes/Desktop/Lab Automation/WS543_VIDAS_Template.pdf"
       
        pdf_window = fitz.open(pdf_path)

        # Extract the first page
        pdf_page = pdf_window.load_page(0)

        # Convert PDF to image
        pixmap = pdf_page.get_pixmap()
        width, height = pixmap.width, pixmap.height
        image_data = pixmap.samples

        # Convert image data to wx.Bitmap
        wx_bitmap = wx.Bitmap.FromBuffer(width, height, image_data)

        # Display the image using wx.StaticBitmap
        static_bitmap = wx.StaticBitmap(pdf_panel, wx.ID_ANY, wx_bitmap)

        # Create a sizer for pdf_panel
        pdf_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pdf_panel_sizer.Add(static_bitmap, 1, wx.EXPAND)
        pdf_panel.SetSizer(pdf_panel_sizer)

        # Create the right panel for the grid
        grid_panel = wx.Panel(splitter)
        overlay_grid = SampleIdGrid(grid_panel, (600, 400))

        # Create the main sizer for the splitter
        splitter_sizer = wx.BoxSizer(wx.HORIZONTAL)
        splitter_sizer.Add(pdf_panel, 1, wx.EXPAND)
        splitter_sizer.Add(grid_panel, 1, wx.EXPAND)

        # Set the splitter_sizer on the splitter
        splitter.SplitVertically(pdf_panel, grid_panel)

        # Create a bottom-right sizer for the button
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer()
        button_sizer.Add(wx.Button(self.panel, label="Print WorkSheet with Overlay"), 0, wx.RIGHT)

        # Create the main sizer for the frame
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(splitter, 1, wx.EXPAND)
        main_sizer.Add(button_sizer, 0, wx.EXPAND)

        self.panel.SetSizer(main_sizer)

        self.Show()


class SampleIdGrid(gridlib.Grid):
    def __init__(self, parent, size):
        super().__init__(parent, -1, size=size)
        self.CreateGrid(5, 5)  # Replace with the actual dimensions of your matrix
        self.SetDefaultCellBackgroundColour(wx.Colour(255, 255, 255))  # Set background color
        self.EnableEditing(False)  # Disable editing


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None, title="Micro Department Sample Manager")
    frame.Show()
    app.MainLoop()
