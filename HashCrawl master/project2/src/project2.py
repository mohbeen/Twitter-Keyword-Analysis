from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from time import sleep, time
from tweepy import Stream
from Tkinter import *
from sys import exit
import tkMessageBox

"""Twitter Keys"""

ckey = 'DIPd04KOiBvct871tJAXAWAp3' 
csecret = '3pqlXTUdyf7kio9wag50UhSrReWg09Si0Zx4BH65VxSyeSzrOC' 
atoken = '2937228617-sSEg7GVhXxuwzYD0cGygWq0tT1pu0RjJi4V6ZLG'
asecret = 'WUV7wdyPXjFKAJKwXUi7d0YuaQDCjwYNWUl6svmWlP5AD'

""" Pre-defining variables """
logged_in = False
keyw = ''

xxfile = ''

file = ''

x = 0

class listener(StreamListener):
	
	def on_data(self, data):
		global file, x
		print file
		try:
			if x == 0:
				tkMessageBox.showinfo("Success", "Saving tweets to file")
				x = 1
			tweet = data.split(',"text":"')[1].split('","source')[0]
			saveThis = str(time()) + ' :: ' + tweet
			
			saveFile = open(file, 'a')
			saveFile.write(saveThis)
			saveFile.write('\n\n')
			saveFile.close()
			return True

		except BaseException, e:
			print str(e)
			
	def on_error(self, status):
		exit()

		
def _login():
	global logged_in
	if username.get().lower() != "admin" or password.get() != "password":
		tkMessageBox.showinfo("Error", "Incorrect login details")
	else:
		tkMessageBox.showinfo("Success", "Welcome, Admin!")
		gui.destroy()
		logged_in = True
		_init()	
		
		
def _search():
	global ckey, csecret, atoken, asecret, keyw, xxfile, file
	key = keyw.get()
	file = xxfile.get()
	if len(key) == 0:
		tkMessageBox.showinfo("Error", "Please provide a valid keyword!")
		return False
	
	""" Twitter Auth """
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	twitterStream = Stream(auth, listener(), timeout = 60)
	twitterStream.filter(track=[key])
	"""  End """
	
def _close():
	exit()
	
	
def _init():
	global logged_in, keyw, xxfile
	if logged_in == False:
		tkMessageBox.showinfo("Error", "You must login to use this!")
		return False
		
	Gui = Tk()
	Gui.title("Hash Crawl")
	Gui.minsize(width = 550, height = 150)
	Gui.configure(bg='gray')
	Gui.geometry("200x200")
	
	fm = Frame(Gui)
	
	Keyw = Label(Gui, text = "Please enter a Keyword to filter:", width = 30, fg='red', font='bold')
	keyw = Entry(Gui, bd = 1)
	
	xfile = Label(Gui, text = "Enter a file name to save:", width = 30, fg='red', font='bold')
	xxfile = Entry(Gui, bd = 1)
		
	submit = Button(Gui, text = "Search", padx = 20, bd = 1, command = _search)
	quit = Button(Gui, text = "Quit", padx = 20, bd = 1, command = _close)
	
	Templates = Button(Gui, text = "Create Template", padx = 20, bd = 1)
	
	Message = Text(Gui, height=4, width=50, bg="gray", fg="black")
	
	Keyw.pack(side=TOP, fill=X)
	keyw.pack(side=TOP, fill=X)
	
	xfile.pack(side=TOP,  fill=X)
	xxfile.pack(side=TOP, fill=X)
	
	submit.pack(side=TOP)
	quit.pack(side=TOP)
	
	Templates.pack(side=TOP)
	
	Message.pack(side=BOTTOM)
	Quote = """You can now search keywords. \nThen save them in a file of your choice"""
	Message.insert(END, Quote)
	
	fm.pack(fill=BOTH)
	
	Gui.mainloop()
	

""" GUI SETTINGS """
gui = Tk()
gui.title("Hash Crawl") # Title of the GUI
gui.minsize(width = 100, height = 100) # width/height 
gui.configure(bg='gray')

Welcome= Label(gui, text = "Welcome to Hashcrawl", bg="gray", fg="red", font=('bold','24'))

message = Text(gui, height=6, width=50, bg="gray", fg="black")

Username = Label(gui, text = "Username", width = 10,) # Username label 
username = Entry(gui, bd = 1)# username textbox

Password = Label(gui, text = "Password", width = 10)  #Password Label 
password = Entry(gui, show = "*", bd = 1)	# Password textbox

submit = Button(gui, text = "Login", padx = 45, bd = 2, command = _login)#submit button

""" Display gui to screen """
Welcome.pack()

message.pack()
quote = """This system enables you to search keywords from \nTwitter and return real time results. \n\nPlease enter the login details below to access thesystem"""
message.insert(END, quote)

Username.pack(padx=5, pady=5, side=LEFT) 	
username.pack(padx=5,pady=10,side=LEFT)

Password.pack(padx=5, pady=5, side =LEFT)
password.pack(padx=5, pady=10, side=LEFT)
		
submit.pack(padx= 45, pady=20, side=BOTTOM)

gui.mainloop()	
	



