from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from HomePage import HomePage
from MainMenu import MainMenu

class App:

    def __init__(self,root):

        """
        Initalisation for the App class

        Configures all the pages of the app (in terms of their user interface)

        Sets up a dictionary to store all of the App's pages

        """

        root.title("Patient free text explorer")
        root.geometry("900x640")               
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)    


        
        # This will store a list of combo boxes that the user enters the CSV header information in
        # Need to store this in the App class so any other class has access to the user input
        self.csv_header_combo_boxes = None
        self.df = None

        # Dictionary to store all of our frames -- frames are essentially a "new page" for our application
        # making it so that we do not need to have multiple windows, rather it can be done all in one window.
        # Widgets (buttons, labels, etc.) can all be added to a frame such that only the top-most frame's widgets
        # are displayed
            
        self.frames_dict = {}
        self.root = root     

        # Set up the two direct child pages
        homepage = HomePage(self.root,self.addPageFrame("home frame",self.root),self) 
        main_menu = MainMenu(self.root,self.addPageFrame("main frame",self.root),self)     
       
       
        # Display the home page
        self.displayFrame("home frame")      
   
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

    
    def displayFrame(self,frame_name):
        self.frames_dict[frame_name].tkraise()      






# Responsible for creating an instance of the app and running the app
# TODO: should move this into its own main function
root = Tk()
App(root)
root.mainloop()
