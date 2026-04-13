

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup #import beautifulsoup4, not beautifulsoup
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import json
import ssl
from concurrent.futures import ThreadPoolExecutor


# Library Cat Ver. 4.5

# Tips:

# (https://www.jetbrains.com/help/pycharm/navigating-through-the-source-code.html#recent_locations)

# shift F3 --go up to next occurance
# ctrl F3 -- go down to next occurance
# ctrl shift e -- recent edited locations

# conditional breakpoints: select line with red dot, right click
# put in condition ex: instance.getTitle() == 'Rome in olden times'; then click Resume Program if desired
# on left side of debugger window

# 1. Accesses the webpage
# 2. Performs a search (for example on a topic)
# 3. Pulls json data from that search
#         New: Extracts only the Entities key from dictionary
# 4. Organizes the json data into title, author, format, description ...
#          New: Adds new function to store data once all needed fields are filled
# 5. Prints out the above organized data
# 6. Prints a list of only the format wanted. Eg: books (but not properly sifted)
# 7. sorts through materials and prints out only the books (or other desired items)
# 8. Move all code into discrete functions
# 9. remove one of the list depths in the output
# 10. allow for two search terms
# 11. Allow for multiple search terms
# 12. Build an interface which can  accept input and then run the input through the program
# 13. Fix the structure of the code: keep the main program out of the mainwindow class
# 14. work on getting all results printed to screen (back to books only to simply set up of interface)
# 15. Improve interface: set up columns which can be updated with results and which dynamically resize
# 16. Improve printout formatting, remove extra marks (eg: ' and " and { } ) and create proper spacing between data points
# 17. Post two pages worth of search terms to the interface (currently prints out page 1's results twice)
#       17 a. Post page 1 and page 2 results to interface (note can not do more than 2 pages, results are flipped: page 2, then page 1)
#       17 b. Post 3 pages of results. Two pages is often not enough
# 18. Add publication date field to print out
# 19. Remove extra space added at begining of each item on printout
# 20. Improve colour and font
# 21.  Improve size of window and columns
# 22. Space results out better
# 23. Put results into normal order (they are currently posting last to first)
# 24. get rid of extra space at top of list
# 25. Clear search results from previous searches if needed
# 26. Use a better font
# 27. Apply new font for search box as well
# 28. Rename elements from list prinout for BK and MUSIC_CD to BOOK and CD respectively
# 29. Re-structure program to use classes for each item
# Remember large print is classed as format: LPRINT
# 30. when any None objects are in the attributes, you can not concatenate with them, fixed inside LibItem class
# 31.  Improved printout
# 32. Added LPRINT to storeData() so that any LPRINT items do not throw off the results
# 33. Check on description getting. It does not seem to be getting all descriptions from the JSON. Try Shakespeare and see Mark Van Doren's book is not
# getting a description.
# 34. fix empty lists getting printed on DVD and Bluray and CD if there is no author
# 35. Added newline to updateResults so that if no author is given, the subtitle still gets printed to a newline rather than on the same line as 'BOOK'.
        # Did same for CDs.

# 36. add function to abbreviate the length of the description -- added characterLimit()

# 37. Adds cache for keeping history of searches -- self.resultsCache = [] in MainWindow
# 38. Adds Function for appending results to the cache list -- cacheHistoryofSearches()
# 39. Adds button beside search bar

# 40. Adds cache list of search terms given by the user. (not yet tested)
# 41. Add button as drop down menu with filler content to test
#         a. Populate button with search terms

# 42 Add test function to search history

# 43 Make search history functional for first item of search: able to re-post first series of results
    # Note: Fixed this using lambda x = SearchTerm: ....

# 44. This is version 3.0 and cleans up discarded code from the experiments for the Search History Menu.

# 45. ver 3.1 Add button to select number of pages accessed from source:
    # Note: If two searches of the same search term are used, the history button only accesses the first series
    # of results from the history cache due to how it searches for the first instance of the search term in the
    # search term history cache

# 46. Ver 3.2 Adds clear history function to search history menu. Note: the menu items themselves do nto clear until
# the next Search.


# 47. Ver. 3.3 (major improvement) Added 4 scroll bars, took away some duplicate code lines in the interface, tried
# adjusting some 'weight' values to get text boxes to expand with main window, did not work.

# 48. Ver 3.4 fixed colon in books and dvd printouts to separate between title and subtitle

# 49. Ver. 3.5 Beginning the process of switching the output of each item to the screen to be a Label rather than text
# This important improvement is the first step in making all text a label beginning with the Books inside the updateResults() method

# 50. Ver. 3.51, added filter to grab the link to the image of the book jacket cover (or any item cover potentially?) This link is not being stored any
# where currently, that is the next step, so far it merely prints to the screen as part of each item. This happens in the ProgramFlow function:
#         if key == 'medium': # access the link to the image of the jacket of the book (a syndetics link)

# 51. Ver 3.511 Added image to LibItem class to hold the link to the image; added all neccessary extra arguments to the programFlow Function as well

# 52. Ver. 3.52, rather major addition to LibItem Class. It now automatically runs a new method in the init (saveImage()) which calls the link of the image
# and saves that to a variable. (This seems to slow down the search results quite noticably).

# 53. Images now show on left side of book column

######

# 54 Ver. 4.0 (Scrollable)
# Finally settled on solution to making scrollable frames using a scroll class which has the canvas inside of it
# This version still needs some refactoring, name updates
# Basic Idea: Added ScrollableFrame Class, then call the class for each frame and grid those to the main frame:

# First vertical frame of items
#frame1 = ScrollableFrame(self.master)
#frame1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# Second frame of items
#frame2 = ScrollableFrame(self.master)
#frame2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

# 55.
# frames now expand with the main window, added row configure in to init

# 56.
# Fixed display of author name. Turns out the author was stored as a single item in a list
# Fixed mostly the width of columns by shortening the search bar to 40

#57.
# Fixed history function; updated so that it works on scrollable frames

#58.
# Rebuilt LibItem() and parsing of JSON data from website

# 59.
# Added parameters to LibItem(), added wrap to updateResults; fixed image problem (missing self in variable name for the link self.jacket)

# 60.
# Added binding of click function to every label
# Shortened display of item description

# 70
# added popup window for any given item on display with details
# popup repopulates new info inside original popup

# 71 
# added smal button on top right of each item for use to yet to be made
# expanded spacing of frames using column configure to fill all unused space

###### Fundamental Program Flow ##########

### Key Point: getSearchTerms() returns the search results as a list of classes ###

# The root is looping inside of the mainwindow class. The Mainwindow init sets up the interface and contains a call
# to the bindings() method (this is continually called). Bindings() in turn calls self.getSearchTerms()
# which checks if the input in the interface has had the enter key pressed and takes the input terms.
# Self.getSearchTerms() then runs the actual program (mainprogram()) with those search terms which also returns
# the results. Those results are then sent to updateResults() which prints them to the screen.

# Class for containing all information about a given library item, ex: a book, a dvd.





class LibItem:
    def __init__(self,callNumber, authors, metaDataID, jacket, audiences, compositeSubjectHeadings, itemFormat, title, subtitle, primaryLanguage, publicationDate, description, subjectHeadings, materialType, totalCopies):
        '''
        A class for library items such as books, CDs, DVDs. It takes in many fields of meta data for each item

        '''
        self.callNumber = callNumber
        self.authors = authors
        self.metaDataId = metaDataID
        self.jacket = jacket # a dictionary with links to small and medium sized jacket images
        self.audiences = audiences
        self.compositeSubjectHeadings = compositeSubjectHeadings
        self.itemFormat = itemFormat
        self.title = title
        self.subtitle = subtitle
        self.primaryLanguage = primaryLanguage
        self.publicationDate = publicationDate
        self.description = description
        self.subjectHeadings = subjectHeadings
        self.materialType = materialType
        self.totalCopies = totalCopies

        self.image = None  # initialize to a value; this will take the image data itself once saveImage() is run
        self.imageLarge = None # store the larger thumbnail for use in single item popup display details
        #self.saveImage() # run saveimage()

    def getCallNumber(self):
        return self.callNumber or ''

    def getMetaDataId(self):
         return self.metaDataId or ''

    def getAuthors(self):  # the author comes as a list with one item in string form ['cooke, Tim']
        if self.authors == None or self.authors == []:  # if author is None or [] change it to '' so that neither None nor a [] get printed to the screen
            return ''
        else:
            return self.authors[0]  # returns the string inside the list

    def getImageLink(self, imageSize):
        '''
        This method pulls the link for the jacket image of a book, CD etc... The link is stored as an attribute in self.jacket with
        three sizes: s, m l. Specify in the call which size you want
        :param imageSize: string s,m, or l
        :return: string: the url to the image
        '''
        if imageSize == 's':
            return self.jacket.get('small', '')
        elif imageSize == 'm':
            return self.jacket.get('medium', '')
        elif imageSize == 'l':
            return self.jacket.get('large', '')
        else:
            return ''

    def getAudiences(self):
        return self.audiences or ''

    def getTitle(self):
        return self.title or ''

    def getPubDate(self):
        return self.publicationDate or ''

    def getCompositeSubjectHeadings(self):
        return self.compositeSubjectHeadings or ''

    def getFormat(self):
        return self.itemFormat or ''

    def getSubTitle(self):
        return self.subtitle or ''

    def getPrimaryLanguage(self):
        return self.primaryLanguage or ''

    def getPublicationDate(self):
        return self.publicationDate or ''

    def getSubjectHeadings(self):
        return self.subjectHeadings or ''

    def getMaterialType(self):
        return self.materialType or ''

    def getTotalCopies(self):
        return self.totalCopies or ''

    def getDescription(self):
        return self.description or ''

    def getImage(self):
        # returns the actual image for displaying
        return self.image

    def getImageLarge(self):

        if self.imageLarge is None:
            self.saveImageLarge()
        return self.imageLarge

    def saveImage(self):
        '''
        This method which is called automatically after all the objects are created; it then
        goes through the objects again adding only the image component. It saves the medium size image
        to the image variable for use in the default display. (For the large image used in the popup window
        see the saveImageLarge()). It uses the imageLink to access the webpage holding the iamge and then saves the data
        '''

        # turning off the ctx stuff seems to speed up the fetching noticeably

        # ctx = ssl.create_default_context()
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE

        # Fetch the image
        try:  # if the item has no link connected with it, the urllib function will throw an error, therefore handle the error as a pass

            # Use urllib to fetch the image
            with urllib.request.urlopen(self.getImageLink('m')) as response:  # use a medium size image for the default results page display
                imgData = response.read()  # Read the image data from the URL

            # Open the image using Pillow
            openedImage = Image.open(BytesIO(imgData))

            originalWidth, originalHeight = openedImage.size

            # Calculate new dimensions while keeping the aspect ratio
            newWidth = 75  # Example new width
            aspectRatio = originalHeight / originalWidth
            newHeight = int(newWidth * aspectRatio)

            # Resize with the calculated dimensions
            resizedImage = openedImage.resize((newWidth, newHeight))

            # Convert the image to a format that Tkinter can display
            self.image = ImageTk.PhotoImage(resizedImage)

        except:
            pass

    def saveImageLarge(self):
        '''
        This method is for getting and saving the large image used in the popup window for simgle item display
        '''

        # turning off the ctx stuff seems to speed up the fetching noticeably

        # ctx = ssl.create_default_context()
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE

        # Fetch the image


        try:  # if the item has no link connected with it, the urllib function will throw an error, therefore handle the error as a pass

            # Use urllib to fetch the image
            with urllib.request.urlopen(self.getImageLink('l')) as response:  # use a medium size image for the default results page display
                imgData = response.read()  # Read the image data from the URL

            # Open the image using Pillow
            openedImage = Image.open(BytesIO(imgData))

            originalWidth, originalHeight = openedImage.size

            # Calculate new dimensions while keeping the aspect ratio
            newWidth = 250  # Example new width
            aspectRatio = originalHeight / originalWidth
            newHeight = int(newWidth * aspectRatio)

            # Resize with the calculated dimensions
            resizedImage = openedImage.resize((newWidth, newHeight))

            # Convert the image to a format that Tkinter can display
            self.imageLarge = ImageTk.PhotoImage(resizedImage)

        except:
            pass


class PopupWindow:
    def __init__(self, parent, title="Popup"):
        self.window = Toplevel(parent)
        self.window.title(title)

        self.window.geometry("300x200")

        label = Label(self.window, text="This is a popup")
        label.pack(pady=20)

        close_btn = Button(self.window, text="Close", command=self.window.destroy)
        close_btn.pack()

class ItemPopup:
    '''
    This class opens a popup window for details of any given item. It is called by an external helpful method in the MainWindow()
    called openItem. OpenItem checks if a popup is already open and if so clears the internal contents and refill's with the new
    item clicked.
    Inputs: parent window: self.master
    object: the item object with all metadata coming with it
    '''
    def __init__(self, parent,object):
        self.window = Toplevel(parent)
        self.window.attributes("-topmost", True)
        self.window.geometry("700x400")
        self.window.geometry("700x400+600+200")
        self.fontTuple = ("Candara", 14)

        # container frame (so we can clear it easily)
        self.container = Frame(self.window)
        self.container.pack(fill="both", expand=True)

    def load_item(self, object):

        wrapInPix = 400

        # clear previous content
        for widget in self.container.winfo_children():
            widget.destroy()

        self.window.title('Details: ' + object.getTitle())

        # --- LEFT COLUMN (IMAGE) ---
        jacket = object.getImageLarge()
        jacketLabel = Label(self.container, image=jacket, bg="#112233")
        jacketLabel.image = jacket
        jacketLabel.grid(row=0, column=0, sticky='ns', padx=10, pady=10)

        # --- RIGHT COLUMN ---
        data_frame = Frame(self.container)
        data_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        data_frame.grid_columnconfigure(0, weight=1)

        # helper to build a field row (frame-based)
        def add_field(parent, label_text, value_text, row, wrap=None):
            field_frame = Frame(parent)
            field_frame.grid(row=row, column=0, sticky="ew", pady=2)
            field_frame.grid_columnconfigure(1, weight=1)

            # left label (field name)
            Label(field_frame, text=label_text, font=self.fontTuple, anchor="nw", justify="left")\
                .grid(row=0, column=0, sticky="nw", padx=(0, 5))

            # right value (actual data)
            Label(field_frame, text=value_text, font=self.fontTuple, anchor="nw", justify="left", wraplength=wrap)\
                .grid(row=0, column=1, sticky="nw")

        # fields (same order as before, just structured)
        add_field(data_frame, "Title:", object.getTitle(), 0)
        add_field(data_frame, "Subtitle:", object.getSubTitle(), 1)
        add_field(data_frame, "Authors:", object.getAuthors(), 2)
        add_field(data_frame, "Description:", object.getDescription(), 3, wrapInPix)
        add_field(data_frame, "Call Number:", object.getCallNumber(), 4)
        add_field(data_frame, "Published:", object.getPubDate(), 5)



class ScrollableFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = Canvas(self, width=200)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # --- grid layout ---
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Mouse wheel binding ---
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

class MainWindow:
    def __init__(self, master):

        # Caching search terms given by the user. Used for populating the search history menu
        self.searchTermsCache = []

        # List for caching results which can be re-accessed by the user
        self.resultsCache = []

        # Set initial value for number of result pages to gather from source
        self.numOfResultPages = 1

        self.count = 1
        self.fontTuple = ("Candara", 14)

        self.master = master
        self.master.title('Library Cat V. 4.8')

        # allow resizing
        #self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1) # Rows holding results
        self.master.grid_columnconfigure(0, weight=1) # First vertical frame

        #initialize the grid value for all 4 frames for display (-1 used so that first grid is actually 0)
        self.gridCacheValList=[0,0,0,0,]

        # Option Menu
        self.numOfSearchPages = [1, 2, 3, 4]
        self.master.option_add('*tearOff', FALSE)
        variable = IntVar()
        variable.set('Number of Pages')

        self.dropdown = OptionMenu(self.master, variable, *self.numOfSearchPages, command=lambda x=variable: self.setNumOfResultPages(x))
        self.dropdown.grid(row=0, column=3)

        # Menu Bar
        self.menubar = Menu(self.master)
        self.file1 = Menu(self.menubar, tearoff=0)
        self.functions = ['Open', 'Save', 'Save as', 'Close', 'Appearance']
        for item in self.functions:
            self.file1.add_command(label=item)

        self.file1.add_separator()
        self.file1.add_command(label="Exit", command=self.master.quit)

        self.menubar.add_cascade(label="File", menu=self.file1)

        edit1 = Menu(self.menubar, tearoff=0)
        edit1.add_command(label="Undo")
        edit1.add_separator()
        edit1.add_command(label="Cut")
        edit1.add_command(label="Copy")
        edit1.add_command(label="Paste")
        edit1.add_command(label="Delete")
        edit1.add_command(label="Select All")

        self.menubar.add_cascade(label="Edit", menu=edit1)

        help1 = Menu(self.menubar, tearoff=0)
        help1.add_command(label="About")
        self.menubar.add_cascade(label="Help", menu=help1)

        self.history1 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Search History", menu=self.history1)

        self.master.config(menu=self.menubar)

        # Search Bar
        self.frame = ttk.Frame(self.master)
        self.label = ttk.Label(self.frame, text="Search:", font=self.fontTuple)
        self.label.grid(row=0, column=0)
        self.frame.grid(row=0, column=1, columnspan=2)
        self.frame.config(relief=RIDGE)

        self.entry = ttk.Entry(self.frame, width='40', font=self.fontTuple)
        self.entry.grid(row=0, column=1)

        # First vertical frame of items
        self.frame1 = ScrollableFrame(self.master)
        self.frame1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Second frame of items
        self.frame2 = ScrollableFrame(self.master)
        self.frame2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Third frame of items
        self.frame3 = ScrollableFrame(self.master)
        self.frame3.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # Fourth frame of items
        self.frame4 = ScrollableFrame(self.master)
        self.frame4.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)

        self.master.grid_rowconfigure(1, weight=1)

        self.popup = None # store whether or not a popup window is open so that popups can be reused in the same window

        for col in range(4):
            self.master.grid_columnconfigure(col, weight=1)

        self.bindings(self.master)


    def updateGridCacheValues(self,newValue,frameNum):

        '''
        This method updates the value for self.gridCacheValFrame1 in the init. It starts at -1
        so that on the first run (after incrementing by 1) it will actually start at 0. After each run
        of the gridLabel() method, the cache value is updated so that any new labels added to the needed
        frame will follow sequentially from the last label.
        input: int: the value needed to be cached.
        '''

        self.gridCacheValList[frameNum - 1] = newValue  # update the relevant value in the ValList (needs to subtract 1. Eg frame1 is actualy index 0 on newGridValuegridLabel(self,gridCacheValList,label):

    def gridLabel(self,gridCacheValList,label):

        '''
        This method grids the labels to a given frame. First it gets the position of the last label that was grided
        and then grids the new label just under that previous label. Finally it calls the update cache method and updates the
        cache to the last position it left off from for the label
        Inputs: the instantiated label itself
        List of ints: the cached values of the last label for each frame eg: [3,3,2,1]
        '''

        gridCacheValList = gridCacheValList

        if label.master == self.frame1.scrollable_frame: # access the frame in which the label resides and check for a match

            frameNum=1
            label.grid(row=gridCacheValList[0], column=0, sticky="nsew", padx=1, pady=5)
            newGridValue=gridCacheValList[0]+1

            self.updateGridCacheValues(newGridValue,frameNum)

        if label.master == self.frame2.scrollable_frame:
            frameNum=2
            label.grid(row=gridCacheValList[1], column=0, sticky="nsew", padx=1, pady=5)
            newGridValue = gridCacheValList[1] + 1
            self.updateGridCacheValues(newGridValue,frameNum)

        if label.master == self.frame3.scrollable_frame:
            frameNum=3
            label.grid(row=gridCacheValList[2], column=0, sticky="nsew", padx=1, pady=5)
            newGridValue = gridCacheValList[2] + 1
            self.updateGridCacheValues(newGridValue,frameNum)

        if label.master == self.frame4.scrollable_frame:
            frameNum=4
            label.grid(row=gridCacheValList[3], column=0, sticky="nsew", padx=1, pady=5)
            newGridValue = gridCacheValList[3] + 1
            self.updateGridCacheValues(newGridValue,frameNum)

    def clearTextFields(self):

        '''
        This method clears the text displayed to the frames. This is not used anymore now
        that labels are being used to display better content
        '''

        for widget in self.scrollable_frame1.winfo_children():
            widget.destroy()
        self.text2.delete('1.0', 'end')
        self.text3.delete('1.0', 'end')
        self.text4.delete('1.0', 'end')

    def clearWidgetsInFrames(self):

        '''
        Clear the widgets for the scrollable frame in each vertical frame.
        This is called when a new search is conducted
        '''

        frames = [self.frame1, self.frame2, self.frame3, self.frame4]

        for frame in frames:
            for widget in frame.scrollable_frame.winfo_children():
                widget.destroy()

    def setNumOfResultPages(self, variable):
        self.numOfResultPages = variable

    def getNumOfResultPages(self):
        return self.numOfResultPages

    def clearSearchHistory(self):
        self.searchTermsCache = []
        self.resultsCache = []

    def bindings(self, master):
        self.entry.bind('<Return>', lambda event: self.getSearchTerms())

    def getSearchTerms(self):
        searchTerms = self.entry.get()
        self.searchTermsCache.append(searchTerms)

        self.results = programFlow(searchTerms, self.getNumOfResultPages()) # returns the list of LibItem objects

        if self.count == 1:
            self.count += 1
            self.cacheHistoryofSearches(self.results)
            self.updateResults(self.results)
        else:
            self.count += 1
            self.clearWidgetsInFrames()
            self.cacheHistoryofSearches(self.results)
            self.updateResults(self.results)

        def displaySelected(searchTerm):
            indexOfSearchTerm = self.searchTermsCache.index(searchTerm)
            self.clearWidgetsInFrames()
            self.updateResults(self.resultsCache[indexOfSearchTerm])

        self.history1.delete(0, "end")
        for searchTerm in self.searchTermsCache:
            self.history1.add_command(label=searchTerm, command=lambda x=searchTerm: displaySelected(x))
        self.history1.add_command(label='Clear History', command=self.clearSearchHistory)

    def mouseOver(self,event):
        event.widget.config(bg="#24405b")

    def mouseOff(self,event):
        event.widget.config(bg="#112233")

    def cacheHistoryofSearches(self, results):
        self.resultsCache.append(results)

    def onClick(self,object):
        print(object.getTitle())

    def openPopup(self,object):
        PopupWindow(self.master, "My Popup")

    def itemPopup(self, object):
        ItemPopup(self.master,object)

    def openItem(self, object):
        if self.popup is None or not self.popup.window.winfo_exists():
            self.popup = ItemPopup(self.master,object)

        self.popup.load_item(object)


    def updateResults(self, results):

        '''
        This method builds the text string for the label to be displayed on the screen. Results is a list of LibItem objects
        :param results: A list of all the LibItem objects
        :return:
        '''

        # List of item formats, once loop finds a match, it takes the second item of the tuple for display, it also uses the third item to
        # display the item to the correct frame (used lower down in the Label call "format[2]"
        listOfFormats = [('BK', 'BOOK',self.frame1.scrollable_frame), ('DVD', 'DVD',self.frame2.scrollable_frame), ('MUSIC_CD', 'CD',self.frame3.scrollable_frame), ('GRAPHIC_NOVEL', 'GRAPHIC NOVEL',self.frame4.scrollable_frame)]
        wrapInPix=350 # wrap length of the text for each line

        for instance in results:  # results is a list of LibItem objects
            for format in listOfFormats:
                if instance.getFormat() == format[0]:
                    posting = format[1] + ' ' # Use the 2nd item from the tuple for displaying to user. Eg "BOOK"

                    if instance.getAuthors() != '':
                        posting += instance.getAuthors() + '\n'
                    else:
                        posting += '\n'

                    if instance.getSubTitle() != '':
                        posting += instance.getTitle() + ': '
                    else:
                        posting += instance.getTitle() + '\n'

                    if instance.getSubTitle() != '':
                        posting += instance.getSubTitle() + '\n'

                    if instance.getDescription() != '':
                        posting += 'Description: ' + characterLimit(instance.getDescription(), 30) + '...\n'

                    posting += instance.getPubDate() + '\n\n'

                    tile = Frame(format[2], bg='#112233', padx=5, pady=5)
                    #tile.grid(row=row, column=col, sticky='ew', pady=2)
                    tile.grid_columnconfigure(0, weight=1)

                    top_bar = Frame(tile, bg='#112233')
                    top_bar.grid(row=0, column=0, sticky='ew')
                    top_bar.grid_columnconfigure(0, weight=1)

                    btn = Button(top_bar,text="o", bd=0, relief="flat", highlightthickness=0, padx=2, pady=2)
                    btn.grid(row=0, column=1, sticky='ne')
                    #btn.image = img

                    content = Frame(tile, bg='#112233')
                    # content.grid_rowconfigure(0, weight=1)
                    content.grid_columnconfigure(0, weight=1)
                    content.grid(row=1, column=0, sticky='ew')

                    if instance.getImage() is None:
                        label = Label(content, text=posting, anchor='w', justify='left',
                              font=self.fontTuple, wraplength=wrapInPix,
                              fg="white", bg='#112233')
                    else:
                        label= Label(content, text=posting, anchor='w', justify='left',
                              compound="left", image=instance.getImage(),
                              font=self.fontTuple, wraplength=wrapInPix,
                              fg="white", bg='#112233')

                    label.grid(row=0, column=0, sticky='nsew')
                    self.gridLabel(self.gridCacheValList,tile)
                    #label.pack(side='top', fill='x')
                    label.bind("<Enter>", self.mouseOver)
                    label.bind("<Leave>", self.mouseOff)

                    #### Important Line: bind a function (onClick()) to each label; each one binds the object itself to that label and lets
                    #### you call any function from that object
                    #label.bind("<Button-1>", lambda e, o=instance: self.onClick(o))
                    #label.bind("<Button-1>", lambda e, o=instance: self.openPopup(o))
                    label.bind("<Button-1>", lambda e, o=instance: self.openItem(o))
                    #label.bind("<Button-1>", self.on_click)  # Left mouse click, simple click maker runs func without args


def twoSearchTerms(searchTerms):
    # determines if multiple search terms were inputted

    # if more than one search term, return true
    # if one search term only, return false
    if len(searchTerms.strip().split(' ')) > 1:
        return True
    else:
        return False

def characterLimit(text,limit):

    '''Slices any string given to it
    inputs: text as string; number of characters wanted
    outputs: the sliced string'''

    return text[0:limit]

def listOfSearchTerms(searchTerms):
    return searchTerms.split(' ')


def performSearch(searchTerms, numOfResultPages, pagesAccessedCounter):
    '''This function composes the correct url command for any number of search terms given
       inputs: str: searchTerms; int: numOfResultPages (number of pages of catalogue results to print to interface); counter for number of times program has accessed website (comes from programFlow())
       outputs: html of whole website for the given search terms
    '''
    # ignore ssl cert errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # convert all search terms to list form
    termsList = listOfSearchTerms(searchTerms)
    # base url without any search terms added
    url="https://hpl.bibliocommons.com/v2/search?query="
    #url='https://calgary.bibliocommons.com/v2/search?searchType=smart&query='
    #url = 'https://epl.bibliocommons.com/v2/search?query='


    # if only one search term is given, take base url + search term
    # if multiple search terms given take base url + 1st search term, then add the remaining
    # search terms with %20 preceding them until all terms have been added
    if twoSearchTerms == False:
        url = url + termsList[0]
        return url
    else:
        url = url + termsList[0]
        c = 1
        while c < len(termsList):
            url = url + '%20' + termsList[c]
            c += 1

    #  composes URL for more than one page of results (currently only up to 2 pages)
    if numOfResultPages > 1:  # composing url for page 1, page 2 etc of catalogue results
        #  if looking for more than one page of results
        if pagesAccessedCounter == 0:  # if calling for first page of results
            html = urllib.request.urlopen(url, context=ctx).read()
            return html
        elif pagesAccessedCounter == 1:  # if calling for 2nd page or more
            url = url + '&page=2'
            html = urllib.request.urlopen(url, context=ctx).read()
            return html
        elif pagesAccessedCounter == 2:  # if calling for 2nd page or more
            url = url + '&page=3'
            html = urllib.request.urlopen(url, context=ctx).read()
            return html
        elif pagesAccessedCounter == 3:  # if calling for 2nd page or more
            url = url + '&page=4'
            html = urllib.request.urlopen(url, context=ctx).read()
            return html

    else:  # if the original setting for the program is to only get 1 page of results (techincally not neccessary to have this clause)

        html = urllib.request.urlopen(url, context=ctx).read()
        return html


def parseHTML(html):
    cleanhtml = BeautifulSoup(html, 'html.parser')

    return cleanhtml


def getJsonData(cleanhtml):
    #### Use .find() with arguments to pinpoint tags: cleanhtml.find(type="application/json") ####
    jsonData = cleanhtml.find(type="application/json")  # .contents gets only contents, however it is in a list
    # print('*************\n\nJson Data',jsonData, '\n\n**********')
    return jsonData


# Need to remove the "<script>" tags, try .text (doesn't seem to work) also try extract().
# extracts front and end script tags
# data from cleanhtml begins thus: <script data-iso-key="_0" type="application/json">{"app":{"coreAssets":{"cdnHost":....
# note the <script.... html tag at beginning (and end, not shown) which needs to be removed
def remove_tags(data):
    for items in data:
        # Remove tags
        return items.extract()

        # cut out first key of dataDict (which contains no needed info) and give only the 'entities' key which


# contains the items needed.
# Output: dictionary of entities.
# not a highly neccessary step in the program

def accessEntitiesKey(dictionary):
    for (k, v) in dictionary.items():
        if k == 'entities':  # enter "entities" key
            entities = {k: v}
            print(entities)
    return entities


# searches through all keys of the dictionary by type
def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)


# Fixed boolean condition suite with (form...or...)
def storeData(form, author, title, subtitle, description, date, image):
    '''dance  between  the data points.
    A book title will not correspond to the correct author and so on.
    This function  checks if all desired data items have been filled then returns a list of all those items.
    Inputs: string of: form,author,title,subtitle,description
    Outputs: if all and only all desired items are present it returns a list of those items; if all items are not present (if empty or missing anything,
     it returns an empty list []
    '''
    # note: if the format (i.e. 'form') is not one of the types checked for this will throw off the proper correspon
    if author != 1 and title != 1 and subtitle != 1 and description != 1 and date != 1 and image != 1 and (
            form == 'VIDEO_ONLINE' or form == 'BK' or form == 'GRAPHIC_NOVEL' or form == 'EBOOK' or form == 'MUSIC_ONLINE' or form == 'MUSIC_CD' or form == 'BLURAY' or form == 'DVD' or form == 'DIGITAL_SCORE' or form == 'AB_ONLINE' or form == 'BOOK_CD' or form == 'AB' or form == 'LPRINT'):
        return [form, author, title, subtitle, date, image]
    else:
        return []


def getBooks(materials):
    if materials[0] == 'BK':
        return materials


def getCDs(materials):
    if materials[0] == 'MUSIC_CD':
        return materials


def getEbooks(materials):
    if materials[0] == 'EBOOK':
        return materials


def getGraphicNovels(materials):
    if materials[0] == 'GRAPHIC_NOVEL':
        return materials


def getVideos(materials):
    if materials[0] == 'VIDEO_ONLINE':
        return materials


def getDVDs(materials):
    if materials[0] == 'DVD':
        return materials


def getBlurays(materials):
    if materials[0] == 'BLURAY':
        return materials


def getAudioBooks(materials):
    if materials[0] == 'AB':
        return materials

def fetch_image(item):
    item.saveImage()
    return item

def printResults(books, videos, eBooks, DVDs, blurays, CDs, graphicNovels, audioBooks):
    for item in books:
        print(item)
    print()
    for item in videos:
        print(item)
    print()
    for item in eBooks:
        print(item)
    print()
    for item in DVDs:
        print(item)
    print()
    for item in blurays:
        print(item)
    print()
    for item in graphicNovels:
        print(item)
    print()
    for item in CDs:
        print(item)
    for item in audioBooks:
        print(item)


def programFlow(searchTerms, numOfResultPages):
    '''
    This calls all of the functions to access the search terms, access the internet, compose the correct urls and filter all of the results
    and return those results.
    Inputs: str: searchTerms, int: numOfResultPages (number of pages of results from the online catalogue
    Outputs: a list with two tuples: [(),()]. each tuple is one page of results from the main website.
    each tuple in turn contains a list of the books, a list of the dvds etc: [([bk],[bk],[bk],[dvd]),([bk],[dvd],[bluray],[ebook])]
    '''
    results = []  # empty list for appending results of search
    # numOfResultPages += 1 # increment number desired by one so as to run while loop
    c = 0
    listOfItemObjects = []  # Main data structure, contains a list of all objects of library items
    while c < numOfResultPages: # run the loop according to the number of page results desired (determined by user on interface)

        getHTML = performSearch(searchTerms, numOfResultPages, c)

        print('accessing website\n')

        cleanHTML = parseHTML(getHTML)
        extractedJson = getJsonData(cleanHTML)
        jsonDataNoTags = remove_tags(extractedJson)

        print('Pulling json data from catalogue\n')

        # Convert jsonData into a python dictionary
        dataDict = json.loads(jsonDataNoTags)
        # filter out keys which precede the "entities" key
        #entities = accessEntitiesKey(dataDict) # not needed; just use dataDict

        for bib in dataDict['entities']['bibs'].values(): # enter the bib inside entities
            print("NEW ITEM:")

            # Reset all values before starting a fresh run so no old variables carry over from a previous run
            callNumber = None
            authors = None
            metaDataID = None
            jacket = None
            audiences = None
            compositeSubjectHeadings = None
            itemFormat = None
            title = None
            subtitle = None
            primaryLanguage = None
            publicationDate = None
            subjectHeadings = None
            materialType = None
            totalCopies = None

            # Pull all of the relevant metadata from the JSON and assign them to variables and then build the objects with those as properties
            for key, value in bib.items(): # go through each kv in that bib
                if isinstance(value, dict):   # first check if that value is itself a dict; if True print the subkeys
                    for subkey, subvalue in value.items(): # Eg: briefInfo.callNumber: CD MR HIL  briefInfo.format: MUSIC_CD. All bibs have the same 3 part structure
                        if subkey == 'callNumber':
                            callNumber = subvalue
                        if subkey == 'authors':
                            authors = subvalue
                        if subkey == metaDataID:
                            metaDataID = subvalue
                        if subkey == 'jacket':
                            jacket = subvalue
                        if subkey == 'audiences':
                            audiences = subvalue
                        if subkey == 'compositeSubjectHeadings':
                            compositeSubjectHeadings = subvalue
                        if subkey == 'format':
                            itemFormat = subvalue
                        if subkey == 'title':
                            title = subvalue
                        if subkey == 'subtitle':
                            subtitle = subvalue
                        if subkey == 'primaryLanguage':
                            primaryLanguage = subvalue
                        if subkey == 'publicationDate':
                            publicationDate = subvalue
                        if subkey == 'description':
                            description = subvalue
                        if subkey == 'subjectHeadings':
                            subjectHeadings = subvalue
                        if subkey == 'materialType':
                            materialType = subvalue
                        if subkey == 'totalCopies':
                            totalCopies = subvalue

                        print(f"{key}.{subkey}: {subvalue}")
                else: # if False, just print it normally
                    print(f"{key}: {value}")

            print()
            # build the objects and append to list
            listOfItemObjects.append(LibItem(callNumber, authors, metaDataID, jacket, audiences, compositeSubjectHeadings, itemFormat, title, subtitle, primaryLanguage, publicationDate, description, subjectHeadings, materialType, totalCopies))
            #print('object appended')
        c += 1

    # Fetch images afterward. After pulling all of the text based metadata above and creating the objects, add the images into the all the objects
    for item in listOfItemObjects:
        item.saveImage()



    #with ThreadPoolExecutor(max_workers=5) as executor:
        #list(executor.map(fetch_image, listOfItemObjects))

    return listOfItemObjects





def main():
    root = Tk()
    MainWindow(root)

    root.mainloop()


main()
