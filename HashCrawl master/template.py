from Tkinter import *

def _help ():

	hgui= Tk()
	hgui.title("Hash Crawl")
	hgui.minsize(width = 550, height = 150)
	hgui.configure(bg='gray')
	hgui.geometry("600x400")
	
	hTitle = Label(hgui, text = "Hashcrawl Help Page", bg="gray", fg="red", font=('bold','24'))
	
	htext = Text(hgui, height=20, width=70, bg="gray", fg="black")
	
	submit = Button(hgui, text = "Login", padx = 45, bd = 2), command = _login)#submit button
	
	hTitle.pack()
	
	htext.pack()
	quote = """How to log in?\nEnter user name and password then click the log in button.
	\nHow do I search for a specific tweet? \nOnce logged in type the word you want to filter.
	\nHow do I save the results? \nUnder the keyword search you are prompted with a destination you wouldlike to save the file.
	inside that type the name of the file. Make sure you save it as a .txt
	\nWhere will my saved file be? \nThe file you saved will be visable and accesible from the root folder of Tweepy."""
	htext.insert(END, quote)


	hgui.mainloop()
	
	



