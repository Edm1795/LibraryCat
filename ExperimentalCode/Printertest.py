from tkinter import *
from tkinter import ttk



class MainWindow:
    def __init__(self,master):

        # Master Window
        self.master = master
        self.master.title('Library Cat Testing Ground')
        self.master.geometry("+200+450") # position of window in the screen
        self.master.geometry("1500x500") # set size of root window (master)

        # Search Bar
        self.frame = Frame(master)
        self.label = Label(self.frame, text = "Search:")
        self.label.grid(row='0',column = 0)
        self.frame.grid(row=0, column=1,)
        self.frame.config(width=500,height=100,)
        self.frame.config(relief = RIDGE)
        self.entry = Entry(self.frame,width = '50',bg = 'pink')
        self.entry.grid(row='0',column = 1)
        self.bindings(master) # the bindings() function initiates the whole program flow by checking if the return key has been depressed in the interface

        # Instantiate frames
        self.frame1 = Frame(master, background="pink", width=100, height=40,borderwidth=10)
        self.frame2 = Frame(master, background="pink", width=100, height=40,borderwidth=10)
        self.frame3 = Frame(master, background="bisque", width=100, height=40)
        self.frame4 = Frame(master, background="pink", width=100, height=40)

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

        #Set up text boxes
        self.text1 = Text(self.frame1)
        self.text1.insert(INSERT,'')
        self.text1.grid_columnconfigure(0, weight=2)
        self.text1.grid_rowconfigure(0, weight=2)
        self.text1.config(wrap='word')
        self.text1.pack()

        self.text2 = Text(self.frame2)
        self.text2.insert(INSERT,'')
        self.text2.grid_columnconfigure(0, weight=2)
        self.text2.grid_rowconfigure(0, weight=2)
        self.text2.config(wrap='word')
        self.text2.pack()

        self.text3 = Text(self.frame3)
        self.text3.insert(INSERT,'')
        self.text3.grid_columnconfigure(0, weight=2)
        self.text3.grid_rowconfigure(0, weight=2)
        self.text3.grid_rowconfigure(0, weight=2)
        self.text3.config(wrap='word')
        self.text3.pack()

        self.text4 = Text(self.frame4)
        self.text4.insert(INSERT,'')
        self.text4.grid_columnconfigure(0, weight=2)
        self.text4.grid_rowconfigure(0, weight=2)
        self.text4.grid_rowconfigure(0, weight=2)
        self.text4.config(wrap='word')
        self.text4.pack()


        #self.text.config(wrap='word')
    def bindings(self,master):
        # This function checks for the return key and then initiates the getSearchTerms() function which in turn does most of the important calls
        self.entry.bind('<Return>', lambda event: self.getSearchTerms())

    def getSearchTerms(self):

        # this function is central to the program's function as it gets the search terms and then runs the program with those terms:
        # 1. gets search terms
        # 2. runs program with search terms
        # 3. sends results to the screen printout function (updateResults())

        # searchTerms =  self.entry.get()
        # self.results = mainProgram(searchTerms)
        # print(self.results)

        # test set I
        # self.updateResults(([['BK', ['Fischer, Bobby'], 'Bobby Fischer Teaches Chess', ''], ['BK', ['Chandler, Murray'], 'How to Beat your Dad at Chess', ''], ['BK', ['Chernev, Irving'], 'Winning Chess', 'How to Perfect your Attacking Play'], ['BK', ['Levens, David'], 'Chess Basics', ''], ['BK', ['Chess, Shira'], 'Ready Player Two', 'Women Gamers and Designed Identity'], ['BK', ['Levens, David'], 'Chess Basics', '']], [['DVD', [], 'How to Play Chess', 'Lessons From An International Master']], [], [['MUSIC_CD', [], 'Chess', '']]))


        #Test set II
        self.updateResults(([['BK', ['Robinson, Nathan J.'], 'Trump',
                  'Anatomy of A Monstrosity : How This Happened, What It Means, and What to Do About It'],
                 ['BK', ['Trump, Donald'], 'Trump', 'The Art of the Deal'],
                 ['BK', ['Scaramucci, Anthony'], 'Trump, the Blue-collar President', ''],
                 ['BK', ['Badiou, Alain'], 'Trump', '']], [], [], []))

    # Structure of data: a four tuple where each element is a list of lists
    # ([['BK', ['Fischer, Bobby'], 'Bobby Fischer Teaches Chess', ''], ['BK', ['Chandler, Murray'], 'How to Beat your Dad at Chess', '']],[[]],[[]],[[]])
    #                                                                                                                    0                                                                                                                              1      2     3

    def updateResults(self,results):
        #inserts search results into text boxes of interface
        # results is a four-part tuple: 0,1,2,3, books, dvds, blurays, cds
        for item in results[0]: # pop individual items from the list as a stack b/c text.insert() reverses the order of the print out.
            while len(item) > 0:
                x = item.pop()
                if x == None:
                    x = ' '
                self.text1.insert(1.0, item.pop())
                self.text1.insert(1.0, ' ')# insert space between item's info: BK Author Title
            self.text1.insert( 1.0, ' \n')
        for item in results[1]: # pop individual items from the list as a stack b/c text.insert() reverses the order of the print out.
            while len(item) > 0:
                x = item.pop()
                if x == None:
                    x = ' '
                self.text2.insert(1.0, item.pop())
                self.text2.insert(1.0, ' ')
            self.text2.insert( 1.0, ' \n')
        for item in results[2]: # pop individual items from the list as a stack b/c text.insert() reverses the order of the print out.
            while len(item) > 0:
                x = item.pop()
                if x == None:
                    x = ' '
                self.text3.insert(1.0, item.pop())
                self.text3.insert(1.0, ' ')
            self.text3.insert( 1.0, ' \n')
        for item in results[3]:  # pop individual items from the list as a stack b/c text.insert() reverses the order of the print out.
             while len(item) > 0:
                 x = item.pop()
                 if x == None:
                     x = ' '
                 self.text4.insert(1.0, item.pop())
                 self.text4.insert(1.0, ' ')
             self.text4.insert(1.0, ' \n')

d = ''' ([['BK', ['Fischer, Bobby'], 'Bobby Fischer Teaches Chess', ''], ['BK', ['Chandler, Murray'], 'How to Beat your Dad at Chess', ''], ['BK', ['Chernev, Irving'], 'Winning Chess', 'How to Perfect your Attacking Play'], ['BK', ['Levens, David'], 'Chess Basics', ''], ['BK', ['Chess, Shira'], 'Ready Player Two', 'Women Gamers and Designed Identity'], ['BK', ['Levens, David'], 'Chess Basics', '']], [['DVD', [], 'How to Play Chess', 'Lessons From An International Master']], [], [['MUSIC_CD', [], 'Chess', '']]) '''
d2 = 'Results from main program and sent to interface: [([['BK', ['Robinson, Nathan J.'], 'Trump', 'Anatomy of A Monstrosity : How This Happened, What It Means, and What to Do About It'], ['BK', ['Trump, Donald'], 'Trump', 'The Art of the Deal'], ['BK', ['Scaramucci, Anthony'], 'Trump, the Blue-collar President', ''], ['BK', ['Badiou, Alain'], 'Trump', '']], [], [], []), ([['BK', ['Robinson, Nathan J.'], 'Trump', 'Anatomy of A Monstrosity : How This Happened, What It Means, and What to Do About It'], ['BK', ['Trump, Donald'], 'Trump', 'The Art of the Deal'], ['BK', ['Scaramucci, Anthony'], 'Trump, the Blue-collar President', ''], ['BK', ['Badiou, Alain'], 'Trump', '']], [], [], [])]'
def main():

    root = Tk()
    z = MainWindow(root)

    root.mainloop()

main()
