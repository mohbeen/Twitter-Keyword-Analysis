"""self is a reference to the instance of the object
   for example self for HelpPage is this particular HelpPage,
   for LoginPage --- this particular instance of LoginPage and so on
   Since we arange the widgets on the object we create, it is natural
   to use self. Read any python documentation about classes, OOP and self"""
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from Tkinter import *
from time import time
import tkMessageBox
import tkFileDialog
import threading
import traceback
import os

"""Twitter Keys"""

ckey = 'DIPd04KOiBvct871tJAXAWAp3' 
csecret = '3pqlXTUdyf7kio9wag50UhSrReWg09Si0Zx4BH65VxSyeSzrOC' 
atoken = '2937228617-sSEg7GVhXxuwzYD0cGygWq0tT1pu0RjJi4V6ZLG'
asecret = 'WUV7wdyPXjFKAJKwXUi7d0YuaQDCjwYNWUl6svmWlP5AD'

class HelpPage(Toplevel):
    def __init__(help, master):
        Toplevel.__init__(help, master)
        help.__master = master

	hTitle = Label(help, text = "Hashcrawl Help Page", fg = "red", font = ('bold','24'))
	
	htext = Label(help, height = 25, width = 100, fg="black")
	
	hTitle.pack()
	
	
	htext.pack()
	quote = """
	\nHow to log in? 
	\nEnter user name and password then click the log in button.
	\nHow do I search for a specific tweet? 
	\nOnce logged in type the word you want to filter.
	\nHow do I save the results?
	\nCan I search previous results?
	\nYes, select a keyword from the left hand side, click it and press 'search'
	\nWhere are my results?
	\nThe results are displayed in the screen on the right of the search column.
	\nYou can save the file by pressing 'save' and choosing a file name.
	\nWhere will my saved file be? 
	\nYou will be prompted with a directory to save the file into and is visable and accesible from the root folder of Tweepy."""
	
	htext["text"] = quote
	
				

class Listener(StreamListener):
    def __init__(twitter, dataText):
        twitter.__dataText = dataText

    def on_data(twitter, data):
        try:
            """ Display information on the widget """
            tweet = data.split(',"text":"')[1].split('","source')[0]
            twitter.__dataText.config(state = NORMAL)
            twitter.__dataText.insert(END, str(time()) + ' :: ' + tweet + '\n\n')
            twitter.__dataText.config(state = DISABLED)
            return True
        except Exception as e:
            tkMessageBox.showerror(title = 'Exception', message = traceback.format_exc())
            return True

    def on_error(self, status):
        tkMessageBox.showerror(title = 'Error', message = 'Tweepy stream error #' + str(status))
        return False

    def on_exception(self, exception):
        tkMessageBox.showerror(title = 'Exception', message = traceback.format_exc())
        return False
                    
class SearchTool(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width = 200, height = 200)
        self.__master = master
        self.pack()

        """ Initialize gui """
        self.__buttonWidth = 10
        self.__leftSide = Frame(self)
        self.__leftSide.pack(side = LEFT)

        searchFrame = Frame(self)
        searchFrame.pack(side = TOP)
        
        Welcome = Label(searchFrame, text = "Hashcrawl Search Page", fg="red", font=('bold','24'))
        Welcome.pack(side = LEFT)	
		
        Label(searchFrame, image = img).pack(side = RIGHT)
		
        Label(self, text = 'You can now search keywords on Twitter and return real time results. Please enter a keyword to search on the left.').pack(side = TOP)
        self.__loginFrame = Frame(self)
        self.__loginFrame.pack(side = TOP)
		
        # the label with keyword
        Label(self.__leftSide, text = "Please enter a Keyword to filter:", fg='red', font='bold').pack(side = TOP)
        self.__keywordEntry = Entry(self.__leftSide)
        self.__keywordEntry.pack(side = TOP, fill = X)
        
        # previously entered
        Label(self.__leftSide, text = 'Previously entered:', fg='red', font='bold').pack(side = TOP)
        prevFrame = Frame(self.__leftSide)
        prevFrame.pack(side = TOP)
        scrollBar = Scrollbar(prevFrame)
        scrollBar.pack(side = RIGHT, fill = Y)
        self.__keyList = Listbox(prevFrame, selectmode = SINGLE, yscrollcommand = scrollBar.set)
        self.__keyList.pack(side = LEFT, fill = X)
        scrollBar['command'] = self.__keyList.yview

        self.__list = [] # list with the keys
		# try load the lists from the file
        try:
            f = open('templates.txt', 'r')
            for line in f.readlines():
                self.__list.append(line[:-1])
            f.close()
            for key in self.__list:
                self.__keyList.insert(END, key)
        except IOError:
            pass

        # button which clears the previous results
        self.__clearPrev = Button(self.__leftSide, text = 'Clear previous', width = self.__buttonWidth)
        self.__clearPrev['command'] = self.clearPrev
        self.__clearPrev.pack(side = TOP)

        # button which starts the search
        self.__searchButton = Button(self.__leftSide, text = 'Search', width = self.__buttonWidth)
        self.__searchButton['command'] = self.search
        self.__searchButton.pack(side = TOP)

        # button which stops the search
        self.__stopButton = Button(self.__leftSide, text = 'Stop', width = self.__buttonWidth)
        self.__stopButton['command'] = self.stop
        self.__stopButton.pack(side = TOP)

        # button which clears the widget with retrieved data
        self.__clearButton = Button(self.__leftSide, text = 'Clear', width = self.__buttonWidth)
        self.__clearButton['command'] = self.clear
        self.__clearButton.pack(side = TOP)

        # save data to a file
        self.__saveButton = Button(self.__leftSide, text = 'Save', width = self.__buttonWidth)
        self.__saveButton['command'] = self.save
        self.__saveButton.pack(side = TOP)

        # quit
        self.__quitButton = Button(self.__leftSide, text = 'Quit', width = self.__buttonWidth)
        self.__quitButton['command'] = self.quit
        self.__quitButton.pack(side = TOP)
   
        #logout
        self.__logoutButton = Button(self.__leftSide, text = 'Logout', width = self.__buttonWidth)
        self.__logoutButton['command'] = self.logout
        self.__logoutButton.pack(side = TOP)		
		

        # widget with data
        scrollBar = Scrollbar(self)
        scrollBar.pack(side = RIGHT, fill = Y)
        self.__dataText = Text(self, wrap = WORD, yscrollcommand = scrollBar.set)
        self.__dataText.config(state = DISABLED)
        self.__dataText.pack(side = RIGHT, expand = True, fill = 'both')
        scrollBar['command'] = self.__dataText.yview

        """ Authorization """
        global ckey, csecret, atoken, asecret
	self.__auth = OAuthHandler(ckey, csecret)
	self.__auth.set_access_token(atoken, asecret)
        self.__listener = Listener(self.__dataText)

    """ Clear previous results """
    def clearPrev(self):
        self.__list = []
        self.__keyList.delete(0, END)
    
    """ Start search """
    def search(self):
        # do nothing if search is already running
        try:
            if self.__twitterStream.running:
                tkMessageBox.showwarning(title = 'Warning', message = 'Stop the previous search first')
                return
        except AttributeError:
            pass

        # otherwise start the search
        # get the key from the entry or from the list
        key = self.__keywordEntry.get()
        if key == '':
            key = self.__keyList.curselection()
            if len(key) > 0:
                key = self.__keyList.get(key[0])
            else:
                key = ''
        if key == '':
            tkMessageBox.showwarning(title = 'Warning', message = 'Enter the correct key value or chose from the list')
        else:
            # start the stream
			# attach the entered keyword to the list
            if not key in self.__list:
                self.__list.append(str(key))
                self.__keyList.insert(END, key)
	    self.__twitterStream = Stream(self.__auth, self.__listener, timeout = 60)
            self.__filterThread = threading.Thread(target = self.__startFilter, args = (key,) )
            self.__filterThread.start()

    def __startFilter(self, key):
        try:
            self.__twitterStream.filter(track = [key])
        except Exception:
            tkMessageBox.showerror(title = 'Exception', message = traceback.format_exc())

    """ Stop searching """
    def stop(self):
        # stop the stream
        # join the thread
        try:
            if self.__twitterStream.running:
                self.__twitterStream.disconnect()
                self.__filterThread.join()
        except AttributeError:
            pass

    """ Save data text to the chosen file """
    def save(self):
        # save the crawled data in the chosen file
        filename = tkFileDialog.SaveAs(self, filetypes = [('*.txt files', '.txt')]).show()
        if filename == '':
            tkMessageBox.showerror(title = 'Error', message = 'File name should not be empty')
            return
        f = open(filename, 'w')
        f.write(self.__dataText.get('1.0', END))
        f.close()

    """ Clear data """
    def clear(self):
        # clear data
        self.__dataText.config(state = NORMAL)
        self.__dataText.delete('1.0', END)
        self.__dataText.config(state = DISABLED)

    def quit(self):
        # store previous keys
        f = open('templates.txt', 'w')
        for key in sorted(self.__list):
            f.write(key + '\n')
        f.close()
        # stop and quit
        self.stop()
        self.__master.quit()
 

    def logout(self):
        self.stop()
        self.destroy()
        app = LoginPage(self.__master)		
		
    
        	
	
class LoginPage(Frame):
    def __init__(homepage, master):
        Frame.__init__(homepage, master)
        homepage.__master = master
        homepage.pack()
		
        #pack is to position the widget 
        #frame for the logo and the title
        welcomeFrame = Frame(homepage)
        welcomeFrame.pack(side = TOP)
		
		#title 
        Welcome = Label(welcomeFrame, text = "Welcome to Hashcrawl", fg="red", font=('bold','24'))
        Welcome.pack(side = RIGHT)		
		
        Label(homepage, text = 'This system enables you to search keywords from \nTwitter and return real time results. \n\nPlease enter the login details below to access the system').pack(side = TOP)
        homepage.__loginFrame = Frame(homepage)
        homepage.__loginFrame.pack(side = TOP) 

        
        Label(welcomeFrame, image = img).pack(side = LEFT)		
        
		# login
        Label(homepage.__loginFrame, text = 'Login', fg='red', font=('bold','12')).grid(row = 1, column = 1)
        homepage.__loginEntry = Entry(homepage.__loginFrame)
        homepage.__loginEntry.grid(row = 1, column = 2)

        # password
        Label(homepage.__loginFrame, text = 'Password', fg='red', font=('bold','12')).grid(row = 2, column = 1)
        homepage.__passwordEntry = Entry(homepage.__loginFrame, show = '*')
        homepage.__passwordEntry.grid(row = 2, column = 2)
	
        # button
        homepage.__loginButton = Button(homepage, text = 'Login')
        homepage.__loginButton['command'] = homepage.login
        homepage.__loginButton.pack(side = TOP)
		
		# show help frame
        homepage.__helpButton = Button(homepage, text = 'Help', fg='red')
        homepage.__helpButton['command'] = lambda : HelpPage(homepage.__master)
        homepage.__helpButton.pack(side = TOP)

    def login(homepage):
        # check credentials
        login, password = homepage.__loginEntry.get(), homepage.__passwordEntry.get()
        # check login for correctness
        if (login, password) != ('admin', 'password'):
            tkMessageBox.showerror(title = 'Error', message = 'Incorrect login details')
        else:
            homepage.destroy()
            app = SearchTool(homepage.__master)

		
root = Tk()
root.title('Hash Crawl')
img = PhotoImage(file = 'hand.gif')
root.tk.call('wm', 'iconphoto', root._w, img)

app = LoginPage(root)
app.mainloop()
root.quit()

