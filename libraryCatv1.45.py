import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from lxml import etree
from tkinter import *
from tkinter import ttk
import json
import ssl

# Library Cat Ver. 1.45 This is the same as v4.0 in effect but cleans up the structure of the code. see item number 13.

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




class MainWindow:
    def __init__(self,master):

        self.frame = ttk.Frame(master)
        self.label = ttk.Label(self.frame, text = "Search:")
        self.label.grid(row='0',column = 0)

        self.frame.pack()
        self.frame.config(height=100, width=500)
        self.frame.config(relief = RIDGE)

        self.entry = ttk.Entry(self.frame,width = '50')
        self.entry.grid(row='0',column = 1)
        self.bindings(master)

        self.frameTwo = ttk.Frame(master)
        self.frameTwo.pack()
        self.frameTwo.config(height=400, width=800)
        self.frameTwo.config(relief=RIDGE)

        # sizing is measured by characters not pixels
        self.text = Text(self.frameTwo, height=25, width=100)
        self.text.pack()
        self.text.config(wrap = 'word')
        # self.text.insert(1.0, self.searchResults)

    def bindings(self,master):
        self.entry.bind('<Return>', lambda event: self.getSearchTerms())
    def getSearchTerms(self):
        searchTerms =  self.entry.get()




        # ignore ssl cert errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Problem: getting access to the search function inside the website
        # Answer: Make function which adjusts the url itself (rather than accessing the search field
        # needed for making a search. Eg: "https://epl.bibliocommons.com/v2/search?query=plato"

        # This function is no longer needed, it was used for getting search terms from the console's input.
        # def getSearchTerms():
        #
        #     searchTerms = input('Search: ')
        #     return searchTerms

        def twoSearchTerms(searchTerms):
            # determines if multiple search terms were inputted
            # if more than one search term, return true
            # if one search term only, return false
            if len(searchTerms.strip().split(' ')) > 1:
                return True
            else:
                return False

        def listOfSearchTerms(searchTerms):
            return searchTerms.split(' ')

        def performSearch(searchTerms):

            '''This function composes the correct url command for any number of search terms given.
               Inputs: searchTerms in raw string format
               Outputs: html of whole website for the given search terms
            '''

            # convert all search terms to list form
            termsList = listOfSearchTerms(searchTerms)
            # base url without any search terms added
            url = 'https://epl.bibliocommons.com/v2/search?query='

            # if only one search term is given, take base url + search term
            # if multiple search terms given take base url + 1st search term, then add following
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
        def storeData(form, author, title, subtitle, description):

            '''
            This function  checks if all desired data items have been filled then returns a list of all those items.
            Inputs: string of: form,author,title,subtitle,description
            Outputs: if all and only all desired items are present it returns a list of those items; if all items are not present (if empty or missing anything)
             it returns an empty list [].
            '''
            # note: if the format (ie form) is not one of the types checked for this will throw off the proper correspondance  between  the data points.
            #  A book title will not correspond to the correct author and so on.
            if author != 1 and title != 1 and subtitle != 1 and description != 1 and (
                    form == 'VIDEO_ONLINE' or form == 'BK' or form == 'GRAPHIC_NOVEL' or form == 'EBOOK' or form == 'MUSIC_ONLINE' or form == 'MUSIC_CD' or form == 'BLURAY' or form == 'DVD' or form == 'DIGITAL_SCORE' or form == 'AB_ONLINE' or form == 'BOOK_CD'):
                return [form, author, title, subtitle]

            elif form != 1 and (
                    form != 'VIDEO_ONLINE' or form != 'BK' or form != 'GRAPHIC_NOVEL' or form != 'EBOOK' or form != 'MUSIC_ONLINE' or form != 'MUSIC_CD' or form != 'BLURAY' or form != 'DVD' or form != 'DIGITAL_SCORE' or form != 'AB_ONLINE' or form != 'BOOK_CD') and author != 1 and title != 1 and subtitle != 1 and description != 1:
                return [form, author, title,subtitle]
                # This additional clause handles cases when an unknown format is found(something other than all those listed in the 'if' clause). In such a case, if all fields are full (including an unknown format) a list will still be returned with those items. It will not neccessarily get printed off however (depending on the settings in the print function. This should ensure a proper correspondance between data fields even when unknown formats exist in the raw data

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

        def printResults(books, videos, eBooks, DVDs, blurays, CDs, graphicNovels):
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

        # ################ Program Processes Start Here  #######################
        #searchTerms = getSearchTerms()
        print()
        getHTML = performSearch(searchTerms)

        print('accessing website\n')

        cleanHTML = parseHTML(getHTML)
        extractedJson = getJsonData(cleanHTML)
        jsonDataNoTags = remove_tags(extractedJson)

        print('Pulling json data from catalogue\n')

        # Convert jsonData into a python dictionary
        dataDict = json.loads(jsonDataNoTags)
        # filter out keys which precede the "entities" key
        entities = accessEntitiesKey(dataDict)

        books = []
        DVDs = []
        blurays = []
        graphicNovels = []
        CDs = []
        eBooks = []
        videos = []

        author = 1
        title = 1
        subtitle = 1
        form = 1
        description = 1

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
                # print(key, value)

            # checks if all values above have been filled, if all are not full, it will return an empty list
            # therefore the list will either be full of all needed values or totally empty

            materials = storeData(form, author, title, subtitle, description)

            # determine if list from storeData is a book, video etc. and store in ID
            if materials != []:
                # getBooks() determines if the list from storeData is a book ('BK'); if the list from
                # storeData is not a book it returns None, and if so, the None object will actually get inserted
                # as an item into the new list (books) causing the list to fill up with None objects

                print(materials, '\n')
                if getBooks(materials) != None:
                    books.append(getBooks(materials))
                if getDVDs(materials) != None:
                    DVDs.append(getDVDs(materials))
                if getBlurays(materials) != None:
                    blurays.append(getBlurays(materials))
                if getGraphicNovels(materials) != None:
                    graphicNovels.append(getGraphicNovels(materials))

                if getCDs(materials) != None:
                    CDs.append(getCDs(materials))
                if getEbooks(materials) != None:
                    eBooks.append(getEbooks(materials))
                if getVideos(materials) != None:
                    videos.append(getVideos(materials))

                # if books != None:
                # print(books)
                # if graphicNovels != None:
                # print(graphicNovels)
                # if CDs != None:
                # print(Cds)
                # if eBooks != None:
                # print(eBooks)
                # if videos != None:
                # print(videos)

                form = 1
                author = 1
                title = 1
                subtitle = 1
                description = 1

        # update the mainwindow with the results
        self.text.insert(1.0, books)

        # print to the console all the results
        printResults(books, videos, eBooks, DVDs, blurays, CDs, graphicNovels)






def main():

    root = Tk()
    MainWindow(root)
    root.mainloop()

main()
