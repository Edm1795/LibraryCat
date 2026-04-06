import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup #import beautifulsoup4, not beautifulsoup
from tkinter import *
from tkinter import ttk
import json
import ssl
from ctypes import windll  # used for fixing blurry fonts on win 10 and 11


# Library Cat Ver. 3.4a

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
# 12. Build an interface which can accept input and then run the input through the program
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

Ver. 3.4a
# 49. Fixed blurry font display for win 11. 
     Added import from ctypes import windll
     added to MainWindow: windll.shcore.SetProcessDpiAwareness(1)


###### Fundamental Program Flow ##########

### Key Point: getSearchTerms() returns the search results as a list of classes ###

# The root is looping inside of the mainwindow class. The Mainwindow init sets up the interface and contains a call
# to the bindings() method (this is continually called). Bindings() in turn calls self.getSearchTerms()
# which checks if the input in the interface has had the enter key pressed and takes the input terms.
# Self.getSearchTerms() then runs the actual program (mainprogram()) with those search terms which also returns
# the results. Those results are then sent to updateResults() which prints them to the screen.

# Class for containing all information about a given library item, ex: a book, a dvd.
class LibItem:
    def __init__(self, form, author, title, subtitle, description, date):
        self.form = form
        self.author = author
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.pubDate = date


    def getFormat(self):
        if self.form == None:  # check for None in attribute and replace with '' if so; avoids concatenation errors in printout
            return ''
        else:
            return self.form

    def getAuthor(self):
        if self.author == None or self.author == []:  # if author is None or [] change it to '' so that neither None nor a [] get printed to the screen
            return ''
        else:
            return str(self.author)

    def getTitle(self):
        if self.title == None:
            return ''
        else:
            return self.title

    def getSubTitle(self):
        if self.subtitle == None:
            return ''
        else:
            return self.subtitle

    def getDescription(self):
        if self.description == None:
            return ''
        else:
            return self.description

    def getPubDate(self):
        if self.pubDate == None:
            return ''
        else:
            return self.pubDate


# Main() --> Mainwindow --> self.bindings() method --> self.getSearchTerms() --> mainprogram() --> ProgramFlow() --> returns results to mainProgram()
class MainWindow:
    def __init__(self, master):

        # Caching search terms given by the user. Used for populating the search history menu
        self.searchTermsCache = []
        # ['water','history','England']

        # List for caching results which can be re-accessed by the user
        self.resultsCache = []

        # Set initial value for number of result pages to gather from source
        self.numOfResultPages = 1

        # Counter for keeping track of number of searches made, used to clear text fields of previous searches
        self.count = 1
        self.fontTuple = ("Candara", 14)

        # Master Window
        self.master = master
        self.master.title('Library Cat V. 3.4')
        # self.master.geometry("+100+100")  # position of the window in the screen (200x300)
        # self.master.geometry("400x400")  # set size of the root window (master) (1500x700)

        # Option Menu
        self.numOfSearchPages = [1, 2, 3, 4]
        self.master.option_add('*tearOff', FALSE)
        variable = IntVar()
        variable.set('Number of Pages')

        windll.shcore.SetProcessDpiAwareness(1)  # used for fixing blurry fonts on win 10 and 11

        # creating widget
        self.dropdown = OptionMenu(self.master, variable, *self.numOfSearchPages, command=lambda x=variable: self.setNumOfResultPages(x))
        self.dropdown.grid(row=0, column=3)

        # Menu Bar
        self.menubar = Menu(self.master)
        self.file1 = Menu(self.menubar, tearoff=0)
        self.functions = ['Open', 'Save', 'Save as', 'Close', 'Appearance']
        for item in self.functions:
            self.file1.add_command(label=item)
        # file1.add_command(label="Open")
        # file1.add_command(label="Save")
        # file1.add_command(label="Save as...")
        # file1.add_command(label="Close")

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
        self.label.grid(row='0', column=0)
        self.frame.grid(row=0, column=1, columnspan=2)
        # self.frame.config(width=500, height=10)
        self.frame.config(relief=RIDGE)
        self.entry = ttk.Entry(self.frame, width='100', font=self.fontTuple)
        self.entry.grid(row=0, column=1)

        # Instantiate frames
        self.frame1 = Frame(self.master)
        self.frame2 = Frame(self.master)
        self.frame3 = Frame(self.master)
        self.frame4 = Frame(self.master)

        # creating and placing scrollbar
        scrollbar = Scrollbar(self.frame1, orient='vertical')
        scrollbar2 = Scrollbar(self.frame2, orient='vertical')
        scrollbar3 = Scrollbar(self.frame3, orient='vertical')
        scrollbar4 = Scrollbar(self.frame4, orient='vertical')
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar2.pack(side=RIGHT, fill=Y)
        scrollbar3.pack(side=RIGHT, fill=Y)
        scrollbar4.pack(side=RIGHT, fill=Y)

        # Place frames
        self.frame1.grid(row=1, column=0, sticky="nsew")
        self.frame2.grid(row=1, column=1, sticky="nsew")
        self.frame3.grid(row=1, column=2, sticky="nsew")
        self.frame4.grid(row=1, column=3, sticky="nsew")

        # configure weighting of frames
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)

        # Create font tuple
        # Candara: clear, great for reading, but bland no style to curves

        # Set up text boxes
        self.text1 = Text(self.frame1, bg='#112233', fg='white', font=self.fontTuple, yscrollcommand=scrollbar.set)
        self.text1.insert(INSERT, '')
        self.text1.grid_columnconfigure(0, weight=1)
        self.text1.grid_rowconfigure(0, weight=1)
        self.text1.config(wrap='word')
        self.text1.pack(expand=True, fill=BOTH)

        self.text2 = Text(self.frame2, bg='#112233', fg='white', font=self.fontTuple, yscrollcommand=scrollbar2.set)
        self.text2.insert(INSERT, '')
        self.text2.grid_columnconfigure(0, weight=1)
        self.text2.grid_rowconfigure(0, weight=1)
        self.text2.config(wrap='word')
        self.text2.pack(expand=True, fill=BOTH)

        self.text3 = Text(self.frame3, bg='#112233', fg='white', font=self.fontTuple, yscrollcommand=scrollbar3.set)
        self.text3.insert(INSERT, '')
        self.text3.grid_columnconfigure(0, weight=1)
        self.text3.grid_rowconfigure(0, weight=1)
        self.text3.config(wrap='word')
        self.text3.pack(expand=True, fill=BOTH)

        self.text4 = Text(self.frame4, bg='#112233', fg='white', font=self.fontTuple, yscrollcommand=scrollbar4.set)
        self.text4.insert(INSERT, '')
        self.text4.grid_columnconfigure(0, weight=1)
        self.text4.grid_rowconfigure(0, weight=1)
        self.text4.config(wrap='word')
        self.text4.pack(expand=True, fill=BOTH)


        # binding scrollbar with other widget (Text, Listbox, Frame, etc)

        scrollbar.config(command=self.text1.yview)
        scrollbar2.config(command=self.text2.yview)
        scrollbar3.config(command=self.text3.yview)
        scrollbar4.config(command=self.text4.yview)


        # Main function listens for entry of search terms and initiates main program
        self.bindings(self.master)  # the bindings() function initiates the whole program flow by checking if the return key
                               # has been depressed in the interface

    def clearTextFields(self):
        self.text1.delete('1.0', 'end')
        self.text2.delete('1.0', 'end')
        self.text3.delete('1.0', 'end')
        self.text4.delete('1.0', 'end')

    def setNumOfResultPages(self, variable):
        self.numOfResultPages = variable
        print(self.numOfResultPages)

    def getNumOfResultPages(self):
        return self.numOfResultPages

    def clearSearchHistory(self):
        self.searchTermsCache = []
        self.resultsCache = []
        print('Results cache:', self.resultsCache,'Search Terms Cache:', self.searchTermsCache)


    def bindings(self, master):

        # This function checks for the return key and then initiates the getSearchTerms() function which in turn does most of the important calls
        self.entry.bind('<Return>', lambda event: self.getSearchTerms())

    def getSearchTerms(self):

        # This function is central to the program's function as it gets the search terms and then runs the program with those terms:
        # 1. gets search terms
        # 2. runs program with search terms
        # 3. sends results to the screen printout function (updateResults())

        searchTerms = self.entry.get()
        self.searchTermsCache.append(searchTerms)
        print('############################## search terms cache:', self.searchTermsCache)

        def printscr():
            print('this is the command test')


        # numOfResultPages = 1  # Number of result pages desired from main source
        self.results = programFlow(searchTerms, self.getNumOfResultPages())  # 1. send searchTerms; 2. specify number of pages of results to get from mainsite; note can not go over 4 pages

        # prints out all attributes of each item found
        for instance in self.results:
            print(instance.__dict__)

        # print('\nResults from main program and sent to interface:', self.results)

        # Control whether text fields need to be cleared or not from previous results
        if self.count == 1:  # If very first time run of the search (of program itself from search bar), no need to clear text fields
            self.count += 1
            self.cacheHistoryofSearches(self.results)

            print(15 * '#')
            print('history of searches', self.resultsCache)
            print('Length of History Cache:', len(self.resultsCache))

            self.updateResults(self.results)

        elif self.count > 1:  # If second or more searches made, clear text fields just before updating to new results
            self.count += 1
            self.clearTextFields()
            self.cacheHistoryofSearches(self.results)

            print(15 * '#')
            print('history of searches', self.resultsCache)
            print('Length of History Cache:', len(self.resultsCache))

            self.updateResults(self.results)

        # Search History Menu
        def displaySelected(searchTerm):
            # Gets item clicked on in menu then updates the screen to those corresponding results
            # Note if two searches of the same search term are used, one gets deleted or lost with only one remaining
            # or at least it does not get accessed in from the history cache.
            print('Search History function initiated by clicking:', searchTerm)
            indexOfSearchTerm = self.searchTermsCache.index(searchTerm)
            self.clearTextFields()
            self.updateResults(self.resultsCache[indexOfSearchTerm])
            # print('Search term sent from Menu History:')
            # print(self.searchTermsCache.index(searchTerm))

        self.history1.delete(0, "end")  # clear history list before reposting new terms, otherwise duplicates show
        for searchTerm in self.searchTermsCache:  # Populate Search History list from cache
            self.history1.add_command(label=searchTerm, command=lambda x=searchTerm: displaySelected(x))
        self.history1.add_command(label='Clear History', command=self.clearSearchHistory)  # add clear history function

            # putting searchTerm into x as part of lambda, then calling x avoids the problem of losing
            # the intended variable

        # including an argument directly (without lambda) in the command call will cause the function to be called automatically upon
        # creatione eg: displaySelected(searchTerm)


    def cacheHistoryofSearches(self, results):
        self.resultsCache.append(results)

    def updateResults(self, results):

        for instance in results:
            if instance.getFormat() == 'BK':
                self.text1.insert('end', 'BOOK' + ' ')  # switch 'BK' for full term "BOOK"
                if instance.getAuthor() != '':  # In other words, if there is an author's name
                    self.text1.insert('end', instance.getAuthor()+'\n')   # add new line after author to separate author from other attributes
                else:
                    self.text1.insert('end',  '\n')  # if there is no author, a newline is still needed so that the title is put to a newline
                if instance.getSubTitle() != '':  # Inserts a colon when needed for a the subtite
                    self.text1.insert('end', instance.getTitle() + ':' + ' ')
                else:
                    self.text1.insert('end', instance.getTitle() + ' ')
                if instance.getSubTitle() != '':
                    self.text1.insert('end', instance.getSubTitle() + '\n')
                if instance.getDescription() != '':  # if the description is None then do not print the description or the '\n'. (If Desc. was None it will already have been changed to a ''
                    slicedText = characterLimit(instance.getDescription(), 50)  # arguments: string, number of characters desired
                    self.text1.insert('end', 'Description: ' + slicedText + '...' + '\n')
                self.text1.insert('end', instance.getPubDate())
                self.text1.insert('end', '\n\n')  # puts empty line between each library item
            if instance.getFormat() == 'DVD':
                self.text2.insert('end', 'DVD' + ' ')
                self.text2.insert('end', ' ')  # insert space between element
                if instance.getAuthor() != '':
                    self.text2.insert('end', instance.getAuthor())
                if instance.getSubTitle() != '':  # Inserts a colon when needed for a the subtite
                    self.text2.insert('end', instance.getTitle() + ':' + ' ')
                    self.text2.insert('end', instance.getSubTitle() + '\n')
                else:
                    self.text2.insert('end', instance.getTitle() + ' ')
                # self.text2.insert('end', instance.getDescription())
                self.text2.insert('end', instance.getPubDate())
                self.text2.insert('end', ' \n\n')  # puts empty line between each library item
            if instance.getFormat() == 'BLURAY':
                self.text3.insert('end', 'BLURAY' + ' ')
                self.text3.insert('end', ' ')  # insert space between element
                if instance.getAuthor() != '':
                    self.text3.insert('end', instance.getAuthor())
                self.text3.insert('end', ' ' + instance.getTitle() + ' ')
                self.text3.insert('end', instance.getSubTitle() + ' ')
                # self.text3.insert('end', instance.getDescription())
                self.text3.insert('end', instance.getPubDate())
                self.text3.insert('end', ' \n\n')  # puts empty line between each library item
            if instance.getFormat() == 'MUSIC_CD':
                self.text4.insert('end', 'CD' + ' ')
                self.text4.insert('end', ' ')  # insert space between element
                if instance.getAuthor() != '':
                    self.text4.insert('end', instance.getAuthor()+'\n')
                else:
                    self.text4.insert('end', '\n')
                self.text4.insert('end',  instance.getTitle() + ' ')
                self.text4.insert('end', instance.getSubTitle() + '\n')
                # self.text4.insert('end', instance.getDescription())
                self.text4.insert('end', instance.getPubDate())
                self.text4.insert('end', ' \n\n')  # puts empty line between each library item


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
    url = 'https://epl.bibliocommons.com/v2/search?query='

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
def storeData(form, author, title, subtitle, description, date):
    '''
    This function  checks if all desired data items have been filled then returns a list of all those items.
    Inputs: string of: form,author,title,subtitle,description
    Outputs: if all and only all desired items are present it returns a list of those items; if all items are not present (if empty or missing anything,
     it returns an empty list []
    '''
    # note: if the format (i.e. 'form') is not one of the types checked for this will throw off the proper correspondance  between  the data points.
    #  A book title will not correspond to the correct author and so on.
    if author != 1 and title != 1 and subtitle != 1 and description != 1 and date != 1 and (
            form == 'VIDEO_ONLINE' or form == 'BK' or form == 'GRAPHIC_NOVEL' or form == 'EBOOK' or form == 'MUSIC_ONLINE' or form == 'MUSIC_CD' or form == 'BLURAY' or form == 'DVD' or form == 'DIGITAL_SCORE' or form == 'AB_ONLINE' or form == 'BOOK_CD' or form == 'AB' or form == 'LPRINT'):
        return [form, author, title, subtitle, date]
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
    while c < numOfResultPages:

        getHTML = performSearch(searchTerms, numOfResultPages, c)

        print('accessing website\n')

        cleanHTML = parseHTML(getHTML)
        extractedJson = getJsonData(cleanHTML)
        jsonDataNoTags = remove_tags(extractedJson)

        print('Pulling json data from catalogue\n')

        # Convert jsonData into a python dictionary
        dataDict = json.loads(jsonDataNoTags)
        # filter out keys which precede the "entities" key
        entities = accessEntitiesKey(dataDict)

        # These lists probably used to hold data before I implemented class based data containers
        books = []
        DVDs = []
        blurays = []
        graphicNovels = []
        CDs = []
        eBooks = []
        videos = []
        audioBooks = []

        author = 1
        title = 1
        subtitle = 1
        form = 1
        description = 1
        date = 1

        # extrapolating key data fields
        # input entities-dict into recursive search of keys and values for all sub-dictionaries
        for key, value in recursive_items(entities):

            if key == 'authors':
                author = value
                print(key, value)
            if key == 'title':
                title = value
                print(key, value, )
            if key == 'subtitle':
                subtitle = value
                print(key, value)
            if key == 'format':
                form = value
                print(key, value)
            if key == 'description':
                description = value
                print(description)
            if key == 'publicationDate':
                date = value
                # print(key, value)

            # checks if all values above have been filled, if all are not full, it will return an empty list
            # therefore the list will either be full of all needed values or totally empty
            # used to stop loop once all required values have been caught, then allows to save those  values before  resetting variables for the next run
            #     Otherwise you would only be left with the values at the very last discovery as each value will get overwritten as it loops
            materials = storeData(form, author, title, subtitle, description, date)

            # determine if list from storeData is a book, video etc. and store in ID

            if materials != []:
                # This will catch the constellation of values for the first item in the results and then stop, and
                # append that object to the list

                listOfItemObjects.append(LibItem(form, author, title, subtitle, description, date))

                form = 1
                author = 1
                title = 1
                subtitle = 1
                description = 1
                date = 1

        c += 1
    return listOfItemObjects  # a list with two tuples [(),()]. Each tuple contains lists of its books... of its search


def main():
    root = Tk()
    MainWindow(root)

    root.mainloop()


main()
