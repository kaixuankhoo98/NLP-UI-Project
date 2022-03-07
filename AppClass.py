from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pandas as pd

from search import TextSearcher


class App:

    def __init__(self,root):
        root.title("Patient free text explorer")
        root.geometry("900x640")               
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)       

        self.header_combo_boxes = None
        self.df = None

        root_frame = self.configureHomePage(root)
        choose_headers_frame, self.header_combo_boxes = self.configureHeaderSelectFrame(root)    

        # Dictionary to store all of our frames -- frames are essentially a "new page" for our application
        # making it so that we do not need to have multiple windows, rather it can be done all in one window.
        # Widgets (buttons, labels, etc.) can all be added to a frame such that only the top-most frame's widgets
        # are displayed
        
        self.frames_dict = {"root frame":root_frame, "choose headers": choose_headers_frame}
        self.root = root        

        # Configure all the other pages in our application
        self.configureMainMenu()
        self.configureFreqPage()
        self.configureSearchPage()

        # Display the rootframe
        self.frames_dict["root frame"].tkraise()

        
    def configureHomePage(self,root):
        
        """
        Inputs: (self, root) where root is the parent window of the Tk application

        Configures the homepage frame

        returns: configured homepage frame (type ttk.frame)
        
        """

        root_frame = ttk.Frame(root, padding=(3,3,12,12))
        root_frame.grid(column=0, row=0, sticky=(N,S,E,W))
        root_frame.columnconfigure(1,weight=1)
        root_frame.rowconfigure(1,weight=1)
        root_frame.columnconfigure(0,weight=1)
        root_frame.rowconfigure(0,weight=1)

        title = ttk.Label(root_frame, justify=CENTER, text = "Patient\n\nFree Text\n\nExplorer", font=("bold",25))
        title.grid(column=0, columnspan=2,row=0,rowspan=2)
        load_csv_button = ttk.Button(root_frame, text="Open CSV", command=self.loadCSVClick)
        load_csv_button.grid(column=1, row=3,sticky=(N,S,E,W))
        instruction_button = ttk.Button(root_frame, text="Instructions", command=self.instructionsClick)
        instruction_button.grid(column=0,row=3,sticky=(N,S,E,W))

        # Need to alter button click command so that it checks whether the CSV file has been loaded and alerts the user to do so if it has not
        next_button = ttk.Button(root_frame,text="Next", command= lambda: self.frames_dict["main frame"].tkraise())
        next_button.grid(column=0,row=4, sticky=(N,S,E,W))

        return root_frame
    
    def addPageFrame(self, frame_name,root):
        
        """
        Inputs (self, frame_name, root), where root is the parent window of the Tk application
        and frame_name is a string containing the name of the frame

        Creates a new page frame and adds it so the class dictionary that contains all of the frame pages

        returns the newly created frame

        """

        new_frame = ttk.Frame(root, padding=(3,3,12,12))
        new_frame.grid(column=0,row=0,sticky=(N,S,E,W))

        self.frames_dict[frame_name] = new_frame
        return new_frame

    def configureHeaderSelectFrame(self,root):

        """
        Inputs: (self, root) where root is the parent window of the Tk application

        Configures the choose headers frame
        This frame allows the user to select the relevant headers from their CSV file

        returns: configured homepage frame (type ttk.frame), combo boxes (type list of combo boxes)
        
        """
        # Set up the frame, in which all the widgets in this page are placed
        choose_headers = ttk.Frame(root, padding=(3,3,12,12))
        choose_headers.grid(column=0,row=0,sticky=(N,S,E,W))

        ######################## Set up the Labels #######################################################################
        instructions = " Use the drop down menus below to select the header of the csv column that contains the relevant data.\n If there is no such column, select NONE"
        instruction_l = ttk.Label(choose_headers, justify=CENTER, text=instructions, font=("bold",14),)
        instruction_l.grid(column=0,row=0,rowspan=2, columnspan=2,padx=10,pady=10,sticky=(N,S,E,W))
        
        user_id_l = ttk.Label(choose_headers, text = "Select the column that contains UserIDs", font=("bold"))
        user_id_l.grid(column=0,row=3,padx=10,pady=10)

        dob_l = ttk.Label(choose_headers, text = "Select the column that contains users' date of birth", font=("bold"))
        dob_l.grid(column=1,row=3,padx=10,pady=10)

        free_txt_l = ttk.Label(choose_headers, text = "Select the column that contains users' free text", font=("bold"))
        free_txt_l.grid(column=0,row=5,padx=10,pady=10)

        completed_date_l = ttk.Label(choose_headers, text = "Select the column that contains the date the users completed the survey", font=("bold"))
        completed_date_l.grid(column=1,row=5,padx=10,pady=10)

        ms_type_l = ttk.Label(choose_headers, text = "Select the column that contains users' MS type", font=("bold"))
        ms_type_l.grid(column=0,row=7,padx=10,pady=10)

        ms_onset_l = ttk.Label(choose_headers, text = "Select the column that contains users' MS onset year", font=("bold"))
        ms_onset_l.grid(column=1,row=7,padx=10,pady=10)

        ######################## Set up the ComboBoxes ###################################################################
       
        user_id = ttk.Combobox(choose_headers, textvariable=None)
        user_id.grid(column=0,row=4)

        dob = ttk.Combobox(choose_headers, textvariable=None)
        dob.grid(column=1,row=4)

        free_txt = ttk.Combobox(choose_headers, textvariable=None)
        free_txt.grid(column=0,row=6)

        completed_date = ttk.Combobox(choose_headers, textvariable=None)
        completed_date.grid(column=1,row=6)

        ms_type = ttk.Combobox(choose_headers, textvariable=None)
        ms_type.grid(column=0,row=8)

        ms_onset_year = ttk.Combobox(choose_headers, textvariable=None)
        ms_onset_year.grid(column=1,row=8)

        combo_boxes = [user_id, dob, free_txt, completed_date, ms_type, ms_onset_year]   

        ######################## Set up the Buttons #######################################################################

        # Must be a lambda as command expects a defined function
        done_b = ttk.Button(choose_headers, text="Done", command= lambda: self.frames_dict["root frame"].tkraise())
        done_b.grid(column=0,row=10,columnspan=2,sticky=(N,S,E,W))  

        # Insert a blank row before the button to put button at bottom of screen
        choose_headers.rowconfigure(9,weight=1)       

        return choose_headers, combo_boxes
        

    def loadCSVClick(self):       
        # Only permit CSV files, returns the full file path
        
        self.csv_file = filedialog.askopenfilename( title="Select a CSV file", filetypes=(("csv files", "*.csv"),))
        self.chooseCSVHeaders()


    def chooseCSVHeaders(self):
        
        df = pd.read_csv(self.csv_file)

        # Store the dataframe as an object datamember
        self.df = df

        # Stores the column headers of the dataframe        
        self.headers = list(df.columns.values)       
        self.headers.append("NONE") 
        
        # Add the CSV headers as options for the combo boxes
        for combo_box in self.header_combo_boxes:
            combo_box["values"] = list(self.headers)
            combo_box.state(["readonly"])
            # Make the default value "NONE"
            combo_box.current(len(self.headers)-1)

        # Display the choose headers frame
        self.frames_dict["choose headers"].tkraise()       


    
    def instructionsClick(self):
        print("Need to display instructions")

    def configureMainMenu(self):
        main_menu_f = self.addPageFrame("main frame",self.root)

        ############# Configure Buttons ################################################
        freq_b = ttk.Button(main_menu_f, text="Word Frequency Analysis", command= lambda: self.frames_dict["freq frame"].tkraise())
        freq_b.grid(column=0,row=0,sticky=(N,S,E,W))

        search_b = ttk.Button(main_menu_f, text="Search the free text", command= lambda: self.searchEntryButtonClick())
        search_b.grid(column=0,row=1,sticky=(N,S,E,W))

        back_b = ttk.Button(main_menu_f, text="Back", command= lambda: self.frames_dict["root frame"].tkraise())
        back_b.grid(column=0, row=2, sticky=(N,S,E,W))

    def configureFreqPage(self):
        freq_f = self.addPageFrame("freq frame", self.root)

    def configureSearchPage(self):
        search_f = self.addPageFrame("search frame", self.root)

        # Configure search box for query
        search_phrase = StringVar()
        search_box = ttk.Entry(search_f,textvariable=search_phrase)
        search_box.grid(column=0,row=4,sticky=(N,S,E,W))

        self.search_box = search_box

        # Configure search button
        search_button = ttk.Button(search_f,text="Search",command= lambda: self.searchButtonClick())
        search_button.grid(column=0,row=5,sticky=(N,S,E,W))

        # Configure search window list
        window_list = ttk.Combobox(search_f, textvariable=None)
        windows = [5,10,15,20,25,30,"All"]
        window_list["values"] = windows
        window_list.current(3)
        window_list.state(["readonly"])
        window_list.grid(column=1,row=4,sticky=(N,S,E,W))

        self.window_list = window_list

        # Configure the area where query results will be displayed
        results = Text(search_f, width=100, height=10)
        results.grid(row=0,column=0,rowspan=3,columnspan=3,sticky=(N,S,E,W))
        results.insert("1.0","Search results will appear here")
        results.configure(state="disabled")

        self.display_search_results = results
       
        # Configure labels
        search_box_l = ttk.Label(search_f,text="Enter your search term below:")
        search_box_l.grid(column=0,row=3)

        window_l = ttk.Label(search_f,text="Choose how many words either side of your term you wish to extract:")
        window_l.grid(column=1,row=3)

        

    
    def searchButtonClick(self):
        """
        """
        search_phrase = self.search_box.get()
        window = self.window_list.get()

        result = self.searcher.findPhraseInText(search_phrase,window,query_list=None)
        self.display_search_results.configure(state="normal")
        self.display_search_results.delete('1.0','end')
        self.display_search_results.insert('1.0',result)
        self.display_search_results.configure(state="disabled")


        



    def searchEntryButtonClick(self):
        
        self.searcher = TextSearcher(self.df)
        text_header = self.header_combo_boxes[2].get()
        self.searcher.preProcessText(text_header)
        self.frames_dict["search frame"].tkraise()

    


       





root = Tk()
App(root)
root.mainloop()