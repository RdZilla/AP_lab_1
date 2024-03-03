from xml.etree import ElementTree as ET
import json
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from datetime import datetime
# from typing import Type




# ====================================================================================================================
# Work with database
class Polygraphy:

    # Description of polygraphy
    def __init__(self, number, author, title, year): #, shelf
        self.__number = number
        self.__author = author
        self.__title  = title
        self.__year   = year
        # self.__shelf  = shelf

    def get_number(self): return self.__number
    def get_author(self): return self.__author
    def get_title (self): return self.__title
    def get_year  (self): return self.__year
    # def get_shelf (self): return self.__shelf

    def presence(self): print()
    def absence (self): print()

class Book(Polygraphy):

    def presence(self): print('Книга в наличии')
    def absence (self): print('Книга отсутствует')

class Magazine(Polygraphy):

    def presence(self): print('Журнал в наличии')
    def absence (self): print('Журнал отсутствует')

def readUserBD (user_data, login, password): # Read JSON file Users database

    global flag

    # variable to check login and password
    flag = 0

    # database full check
    if len(UserLoginNpassword['User']) == 0:
        print('Отсутствуют пользователи')

    # check login and password
    else:
        for point in UserLoginNpassword['User']:
            if point['login'] == login and point['password'] == password:
                flag = 1

def readBDBook (book_data): # Read JSON file Books database

    # displaying the database in a separate window
    BookBD = open('BookBD.txt', 'w')

    # database full check
    if (len(data['Books']) == 0):
        print('Отсутствуют книги в реестре')

    else:
        for point in data['Books']:
            stringBook = ('Number - ' + str(point['number']) + ', book - ' + str(point['author'])
                          + ' ' + str(point['title']) + ', year - ' + str(point['year']) + '\n')
            BookBD.write(stringBook)

    BookBD.close()

def readBDMagazine (magazine_data): # Read XML file Magazines database

    # displaying the database in a separate window
    MagazineBD = open('MagazineBD.txt', 'w')

    # database full check
    if len(root) == 0:
        print('Отсутствуют журналы в реестре')

    else:
        for element in root:
            stringBook = ('Number: ' + str(element.text) + ', publishing house: ' + str(element[0].text)
                          + ', title: ' + str(element[1].text) + ', year:' + str(element[2].text) + '\n')
            MagazineBD.write(stringBook)

    MagazineBD.close()

def findBookNumber(book_data, BookNumber):

    # database full check
    if len(data['Books']) == 0:
        print('Отсутствуют книги в реестре')

    else:
        k = 0 # check presence book in books database

        for point in data['Books']:
            k += 1

            if point['number'] == BookNumber:
                s = (str(point['author']), str(point['title']), int(point['year']))
                txtBook.insert(END, s) # input string in textbox
                txtBook.insert(END, '\n') #input indent in textbox

        if k < int(BookNumber): print('Книга не найдена') # check presence book in books database

def findMagazineNumber (magazine_data, MagazineNumber):

    # database full check
    if len(root) == 0:
        print('Отсутствуют журналы в реестре')

    else:
        k = 0 # check presence magazine in magazines database

        for element in root:
            k += 1
            if element.text == MagazineNumber:
                s = (str(element[0].text), str(element[1].text), str(element[2].text))
                txtMagazine.insert(END, s) # input string in textbox
                txtMagazine.insert(END, '\n') #input indent in textbox

        if k < int(MagazineNumber): print('Журнал не найден') # check presence magazine in magazines database

def addBookToBD(book_data, number=None, author=None, title=None, year=None):

    nonData_flag = False
    new_number = ''
    new_author = ''
    new_title  = ''
    new_year   = ''

    if number is None and author is None and title is None and year is None:
        nonData_flag = True
        new_number = str(input())
        new_author = str(input())
        new_title  = str(input())
        new_year   = str(input())

    if nonData_flag is True:
        data['Books'].append({'number': new_number, 'author': new_author, 'title': new_title, 'year': new_year})
    else:
        data['Books'].append({'number': number, 'author': author, 'title': title, 'year': year})

    with open('Book_BD_json.txt', 'w') as outfile:
        json.dump(data, outfile)

def readBDClient_Card(client_data, clientId):  # Read Client database

    with open('Client_Card.txt') as fileClientBD:    # Update Clients database
        ClientBD = json.load(fileClientBD)

    # database full check
    if len(ClientBD) == 0:
        ClientBD['Client'] = []

    # database full check
    if len(ClientBD['Client']) == 0:
        print('Отсутствуют читатели в реестре')

    else:
        for point in ClientBD['Client']:
            if point['ClientId'] is clientId:
                lblFio.configure(text=point['FIO'])
                btnAddBook.configure(state='normal')        # activate button
                btnDelBook.configure(state='normal')        # activate button
                btnAddMagazine.configure(state='normal')    # activate button
                btnDelMagazine.configure(state='normal')    # activate button
                lblFio.place(relx=0.02, rely=0.15)          # show label Full name
                txtBook.delete(1.0, END)                    # clear textbox
                txtMagazine.delete(1.0, END)                # clear textbox

                for point in ClientBD['Client'][int(clientId) - 1]['BookId']:
                    BookNumber = str(point) # getting book's number
                    findBookNumber('Book_BD_json.txt', BookNumber)

                for point in ClientBD['Client'][int(clientId) - 1]['MagazineId']:
                    MagazineNumber = str(point) # getting magazine's number
                    findMagazineNumber('Magazine_BD_XML', MagazineNumber)

def addBookToList (book_data, clientId, BookNumber):   # Add Book number to Client database

    # database full check
    if (len(data['Books']) == 0):
        print('Отсутствуют книги в реестре')

    else:
        k = 0  # check presence book in magazines database

        for point in data['Books']:
            k += 1

            if point['number'] == BookNumber:  # check presence magazine in magazines database
                current_idBook = point['number']

        if k < int(BookNumber): # check presence magazine in magazines database
            print('Книга не найдена')

        else:
            # database full check
            if len(ClientBD['Client']) == 0:
                print('Отсутствуют читатели в реестре')

            else:
                for point in ClientBD['Client']:
                    if point['ClientId'] is clientId:
                        ClientBD['Client'][int(clientId)-1]['BookId'].append(current_idBook)

            with open('Client_Card.txt', 'w') as outfile:  # update database
                json.dump(ClientBD, outfile)

def DeleteBookFromList (client_data, clientId, BookNumber):  # Delete book number from client database

    # database full check
    if len(ClientBD['Client']) == 0:
        print('Отсутствуют читатели в реестре')

    for point in ClientBD['Client']:
        if point['ClientId'] is clientId:
            ClientBD['Client'][int(clientId) - 1]['BookId'].remove(BookNumber)

    with open('Client_Card.txt', 'w') as outfile:  # update database
        json.dump(ClientBD, outfile)

def addMagazineToList(magazine_data, clientId, MagazineNumber):   # Add Magazine number to Client database

    # database full check
    if len(root) == 0:
        print('Отсутствуют журналы в реестре')

    else:
        k = 0  # check presence magazine in magazines database
        for element in root:
            k += 1

            if element.text == MagazineNumber:  # check presence magazine in magazines database
                current_idMagazine = element.text

        if k < int(MagazineNumber):
            print('Журнал не найден')

        else:
            with open('Client_Card.txt') as fileClientBD:
                ClientBD = json.load(fileClientBD)

            if len(ClientBD['Client']) == 0:
                print('Отсутствуют читатели в реестре')

            else:
                for point in ClientBD['Client']:
                    if point['ClientId'] is clientId:
                        ClientBD['Client'][int(clientId) - 1]['MagazineId'].append(current_idMagazine)

            with open('Client_Card.txt', 'w') as outfile:  # Update Clients database
                json.dump(ClientBD, outfile)

def DeleteMagazineFromList (client_data, clientId, MagazineNumber):  # Delete magazine number from client database

    # database full check
    if len(ClientBD['Client']) == 0:
        print('Отсутствуют читатели в реестре')

    for point in ClientBD['Client']:
        if point['ClientId'] is clientId:
            ClientBD['Client'][int(clientId) - 1]['MagazineId'].remove(MagazineNumber)

    with open('Client_Card.txt', 'w') as outfile:  # Update Clients database
        json.dump(ClientBD, outfile)

# ====================================================================================================================




# ====================================================================================================================
# Work with window Login

# Button "Entry" click event
def btnEntryClicked():

    global login, password, WorkWindow

    # delete user's space in "login" to prevent invalid entry (null entry)
    loginWithSpace = entLogin.get()
    login = loginWithSpace.replace(' ', '')

    # delete user's space in "password" to prevent invalid entry (null entry)
    passwordWithSpace = entPassword.get()
    password = passwordWithSpace.replace(' ', '')

    # check null entry
    if (login == '') and (password == ''):
        messagebox.showerror('Ошибка', 'Введите логин и пароль')

    # check null entry
    elif login == '':
        messagebox.showerror('Ошибка', 'Введите логин')

    # check null entry
    elif password == '':
            messagebox.showerror('Ошибка', 'Введите пароль')

    else:
        readUserBD('User_Logins_n_passwords_json.txt', login, password)
        if flag == 1:  # check login and password
            EntryBtn.configure    (text="       Загрузка...      ", bg="gainsboro", state='disabled')
            entLogin.configure    (state='disabled')
            entPassword.configure (state='disabled')

            LoginWindow.withdraw() # close authorization window
            MainWindow()           # start program's work window

        else:
            messagebox.showerror('Ошибка', 'Неправильный логин или пароль') # check login and password
# ====================================================================================================================




# ====================================================================================================================
# Work with window Main

# time display
def update_time(): # show time

    global lblDataNTime

    lblDataNTime.config(text=f"{datetime.now():%d-%m-%Y %H:%M:%S}")
    WorkWindow.after(100, update_time)  # Schedule the same function to execute after 100 milliseconds

# Button "Find" click event
def btnLibraryCardClicked():

    global libraryCard

    txtBook.delete     (1.0, END)  # clear textbox
    txtMagazine.delete (1.0, END)  # clear textbox

    lblFio.configure         (text = 'Нет пользователя с таким именем')
    btnAddBook.configure     (state='disabled')
    btnDelBook.configure     (state='disabled')
    btnAddMagazine.configure (state='disabled')
    btnDelMagazine.configure (state='disabled')

    # delete user's space in "id library card" to prevent invalid entry (null entry)
    libraryCardWithSpace = entLibraryCard.get()
    libraryCard = libraryCardWithSpace.replace(' ', '')

    # check null entry
    if libraryCard == '':
        lblFio.place_forget()
        messagebox.showerror('Ошибка', 'Введите номер читательского билета')

    else:
        readBDClient_Card('Client_Card.txt', libraryCard)  # Read Client database

# Button "Add" on notebook "Books" click event
def btnAddBookClicked():

    readBDBook('Book_BD_json.txt') # displaying the database in a separate window
    # opening the books' database in a separate window for convenience
    subprocess.Popen(['C:\\Windows\\System32\\notepad.exe', "BookBD.txt"])
    AddBookWindow()

# Button "Add" on notebook "Magazines" click event
def btnAddMagazineClicked():

    readBDMagazine('Magazine_BD_XML') # displaying the database in a separate window
    # opening the magazines' database in a separate window for convenience
    subprocess.Popen(['C:\\Windows\\System32\\notepad.exe', "MagazineBD.txt"])
    AddMagazineWindow()

# Button "Delete" on notebook "Books" click event
def btnDeleteBookClicked():

    readBDBook('Book_BD_json.txt') # displaying the database in a separate window
    # opening the books' database in a separate window for convenience
    subprocess.Popen(['C:\\Windows\\System32\\notepad.exe', "BookBD.txt"])
    DeleteBookWindow()

# Button "Delete" on notebook "Magazines" click event
def btnDeleteMagazineClicked():

    readBDMagazine('Magazine_BD_XML') # displaying the database in a separate window
    # opening the magazines' database in a separate window for convenience
    subprocess.Popen(['C:\\Windows\\System32\\notepad.exe', "MagazineBD.txt"])
    DeleteMagazineWindow()

# # Button "Change user" click event
def btnCurrentLoginClicked():

    global LoginWindow, WorkWindow, btnCurrentLogin

    WorkWindow.withdraw()  # close work window
    EntryWindow()          # open authorization window

    # kill login window then work window was closed
    LoginWindow.protocol("WM_DELETE_WINDOW", lambda: WorkWindow.destroy())

    # # LoginWindow.update()
    # EntryWindow()
    # # WorkWindow.quit()
    # WorkWindow.destroy()
# ====================================================================================================================




# ====================================================================================================================
# Work with addition windows AddBookWindow и AddMagazineWindow

# Button "Add" on addition window "AddBookWindow" click event
def btnAddBookBookWindowClicked():

    clientId = libraryCard

    # delete user's space in "id book" to prevent invalid entry (null entry)
    BookNumberWithSpace = entBookId.get()
    BookNumber = BookNumberWithSpace.replace(' ', '')

    # check null entry
    if clientId == '' and BookNumber == '':
        messagebox.showerror('Ошибка', 'Введите номер книги и читательского билета')

    # check null entry
    elif clientId == '':
        messagebox.showerror('Ошибка', 'Введите номер читательского билета')

    # check null entry
    elif BookNumber == '':
        messagebox.showerror('Ошибка', 'Введите номер книги')

    else:
        # add book to client
        addBookToList('Client_Card.txt', clientId, BookNumber)
        # input update books' database
        readBDClient_Card('Client_Card.txt', clientId)

# Button "Delete" on addition window "AddBookWindow" click event
def btnDeleteBookBookWindowClicked():

    clientId = libraryCard

    # delete user's space in "id book" to prevent invalid entry (null entry)
    BookNumberWithSpace = entBookId.get()
    BookNumber = BookNumberWithSpace.replace(' ', '')

    # check null entry
    if clientId == '' and BookNumber == '':
        messagebox.showerror('Ошибка', 'Введите номер книги и читательского билета')

    # check null entry
    elif clientId == '':
        messagebox.showerror('Ошибка', 'Введите номер читательского билета')

    # check null entry
    elif BookNumber == '':
        messagebox.showerror('Ошибка', 'Введите номер книги')

    else:
        # add book to client
        DeleteBookFromList('Client_Card.txt', clientId, BookNumber)
        # input update books' database
        readBDClient_Card('Client_Card.txt', clientId)

# Button "Add" on addition window "AddMagazineWindow" click event
def btnAddMagazineMagazineWindowClicked():

    clientId = libraryCard

    # delete user's space in "id magazine" to prevent invalid entry (null entry)
    MagazineNumberWithSpace = entMagazineId.get()
    MagazineNumber = MagazineNumberWithSpace.replace(' ', '')

    # check null entry
    if clientId == '' and MagazineNumber == '':
        messagebox.showerror('Ошибка', 'Введите номер журнала и читательского билета')

    # check null entry
    elif clientId == '':
        messagebox.showerror('Ошибка', 'Введите номер читательского билета')

    # check null entry
    elif MagazineNumber == '':
        messagebox.showerror('Ошибка', 'Введите номер журнала')

    else:
        # add magazine to client
        addMagazineToList('Client_Card.txt', clientId, MagazineNumber)
        # input magazines' database
        readBDClient_Card('Client_Card.txt', clientId)

# Button "Delete" on addition window "AddMagazineWindow" click event
def btnDeleteMagazineMagazineWindowClicked():

    clientId = libraryCard

    # delete user's space in "id magazine" to prevent invalid entry (null entry)
    MagazineNumberWithSpace = entMagazineId.get()
    MagazineNumber = MagazineNumberWithSpace.replace(' ', '')

    # check null entry
    if clientId == '' and MagazineNumber == '':
        messagebox.showerror('Ошибка', 'Введите номер журнала и читательского билета')

    # check null entry
    elif clientId == '':
        messagebox.showerror('Ошибка', 'Введите номер читательского билета')

    # check null entry
    elif MagazineNumber == '':
        messagebox.showerror('Ошибка', 'Введите номер журнала')

    else:
        # add magazine to client
        DeleteMagazineFromList('Client_Card.txt', clientId, MagazineNumber)
        # input update magazines' database
        readBDClient_Card('Client_Card.txt', clientId)
# ====================================================================================================================




# ====================================================================================================================
# Addition windows

# additional window "AddBookWindow" description
def AddBookWindow():

    global WorkAddBookWindow, entBookId

    WorkAddBookWindow = Toplevel()                 # create work window
    WorkAddBookWindow.iconbitmap('Work_icon.ico')  # work's window icon
    WorkAddBookWindow.title("Добавление книги")    # work's window title

    w = WorkAddBookWindow.winfo_screenwidth()      # windwow's width
    h = WorkAddBookWindow.winfo_screenheight()     # windwow's height
    w = w // 2                                     # screen centering
    h = h // 2
    w = w - 260                                    # window's location
    h = h - 110
    WorkAddBookWindow.geometry('240x80+{}+{}'.format(w, h))
    WorkAddBookWindow.resizable(False, False)

    frameAddBook = Frame(WorkAddBookWindow, width=500, height=200, bg='gray80')
    frameAddBook.place(relx=0, rely=0)

    lblIdBook = Label(frameAddBook, text='Введите номер книги', font=("Century Gothic", 13),
                      width=0, height=0, bg='gray80')
    lblIdBook.place (relx=0.02, rely=0.02)

    entBookId = Entry(frameAddBook, width=20)
    entBookId.place(relx=0.03, rely=0.20)
    entBookId.focus()

    btnAddBookBookWindow = Button(frameAddBook, text='Добавить', font=("Century Gothic", 10), bg='gray90',
                                  width=10, height=0, command=btnAddBookBookWindowClicked)
    btnAddBookBookWindow.place(relx=0.29, rely=0.18)

    WorkAddBookWindow.mainloop()

# additional window "DeleteBookWindow" description
def DeleteBookWindow():

    global WorkDeleteBookWindow, entBookId

    WorkDeleteBookWindow = Toplevel()                 # create work window
    WorkDeleteBookWindow.iconbitmap('Work_icon.ico')  # work's window icon
    WorkDeleteBookWindow.title("Удаление книги")      # work's window title

    w = WorkDeleteBookWindow.winfo_screenwidth()      # windwow's width
    h = WorkDeleteBookWindow.winfo_screenheight()     # windwow's height
    w = w // 2                                        # screen centering
    h = h // 2
    w = w + 5                                         # window's location
    h = h - 110
    WorkDeleteBookWindow.geometry('240x80+{}+{}'.format(w, h))
    WorkDeleteBookWindow.resizable(False, False)

    frameDeleteBook = Frame(WorkDeleteBookWindow, width=500, height=200, bg='gray80')
    frameDeleteBook.place(relx=0, rely=0)

    lblIdBook = Label(frameDeleteBook, text='Введите номер книги', font=("Century Gothic", 13),
                      width=0, height=0, bg='gray80')
    lblIdBook.place(relx=0.02, rely=0.02)

    entBookId = Entry(frameDeleteBook, width=20)
    entBookId.place(relx=0.03, rely=0.20)
    entBookId.focus()

    btnDeleteBookBookWindow = Button (frameDeleteBook, text='Удалить', font=("Century Gothic", 10), bg='gray90',
                                      width=10, height=0, command=btnDeleteBookBookWindowClicked)
    btnDeleteBookBookWindow.place(relx=0.29, rely=0.18)

    WorkDeleteBookWindow.mainloop()

# additional window "AddMagazineWindow" description
def AddMagazineWindow():

    global WorkAddMagazineWindow, entMagazineId

    WorkAddMagazineWindow = Toplevel()                  # create work window
    WorkAddMagazineWindow.iconbitmap('Work_icon.ico')   # work's window icon
    WorkAddMagazineWindow.title("Добавление журнала")   # work's window title

    w = WorkAddMagazineWindow.winfo_screenwidth()       # windwow's width
    h = WorkAddMagazineWindow.winfo_screenheight()      # windwow's height
    w = w // 2                                          # screen centering
    h = h // 2
    w = w - 260                                         # window's location
    h = h - 110
    WorkAddMagazineWindow.geometry('240x80+{}+{}'.format(w, h))
    WorkAddMagazineWindow.resizable(False, False)

    frameAddMagazine = Frame(WorkAddMagazineWindow, width=500, height=200, bg='gray80')
    frameAddMagazine.place(relx=0, rely=0)

    lblIdMagazine = Label(frameAddMagazine, text='Введите номер журнала', font=("Century Gothic", 13),
                          width=0, height=0, bg='gray80')
    lblIdMagazine.place (relx=0.02, rely=0.02)

    entMagazineId = Entry(frameAddMagazine, width=20)
    entMagazineId.place(relx=0.03, rely=0.20)
    entMagazineId.focus()

    btnAddMagazineMagazineWindow = Button(frameAddMagazine, text='Добавить', font=("Century Gothic", 10),
                                          bg='gray90', width=10, height=0, command=btnAddMagazineMagazineWindowClicked)
    btnAddMagazineMagazineWindow.place(relx=0.29, rely=0.18)

    WorkAddMagazineWindow.mainloop()

# additional window "DeleteMagazineWindow" description
def DeleteMagazineWindow():

    global WorkDeleteMagazineWindow, entMagazineId

    WorkDeleteMagazineWindow = Toplevel()                 # create work window
    WorkDeleteMagazineWindow.iconbitmap('Work_icon.ico')  # work's window icon
    WorkDeleteMagazineWindow.title("Удаление журнала")    # work's window title

    w = WorkDeleteMagazineWindow.winfo_screenwidth()      # windwow's width
    h = WorkDeleteMagazineWindow.winfo_screenheight()     # windwow's height
    w = w // 2                                            # screen centering
    h = h // 2
    w = w + 5                                             # window's location
    h = h - 110
    WorkDeleteMagazineWindow.geometry('240x80+{}+{}'.format(w, h))
    WorkDeleteMagazineWindow.resizable(False, False)

    frameDeleteMagazine = Frame(WorkDeleteMagazineWindow, width=500, height=200, bg='gray80')
    frameDeleteMagazine.place(relx=0, rely=0)

    lblIdMagazine = Label(frameDeleteMagazine, text='Введите номер журнала', font=("Century Gothic", 13),
                          width=0, height=0, bg='gray80')
    lblIdMagazine.place(relx=0.02, rely=0.02)

    entMagazineId = Entry(frameDeleteMagazine, width=20)
    entMagazineId.place(relx=0.03, rely=0.20)
    entMagazineId.focus()

    btnDeleteMagazineMagazineWindow = Button(frameDeleteMagazine, text='Удалить', font=("Century Gothic", 10),
                                             bg='gray90', width=10, height=0,
                                             command=btnDeleteMagazineMagazineWindowClicked)
    btnDeleteMagazineMagazineWindow.place(relx=0.29, rely=0.18)

    WorkDeleteMagazineWindow.mainloop()
# ====================================================================================================================




# ====================================================================================================================
# Main windows

# Login window "EntryWindow" description
def EntryWindow():

    global LoginWindow, login, password, entLogin, entPassword, EntryBtn

    LoginWindow = Tk()                                   # create login window
    LoginWindow.title("Книжная библиотека")              # work's window title
    LoginWindow.iconbitmap('Login_icon.ico')             # work's window icon

    w = LoginWindow.winfo_screenwidth()                  # windwow's width
    h = LoginWindow.winfo_screenheight()                 # windwow's height
    w = w//2                                             # screen centering
    h = h//2
    w = w - 300                                          # window's location
    h = h - 300
    LoginWindow.geometry('600x600+{}+{}'.format(w, h))
    LoginWindow.resizable(False, False)

    frameLibraryCard = Frame(LoginWindow, width=600, height=600)
    frameLibraryCard.place(relx=0, rely=0)

    lblHello = Label(frameLibraryCard, text="Добро пожаловать!", font=("Century Gothic", 30), width=0, height=3)
    lblHello.place(relx=0.18, rely=0)

    lblAuth = Label(frameLibraryCard, text="Авторизируйтесь в системе", font=("Century Gothic", 15), width=0, height=0)
    lblAuth.place(relx=0.255, rely=0.33)

    lblLogin = Label(frameLibraryCard, text="Логин", font=("Century Gothic", 12), width=0, height=0)
    lblLogin.place(relx=0.125, rely=0.47)

    entLogin = Entry(frameLibraryCard, width=55)
    entLogin.place(relx=0.28, rely=0.475)
    entLogin.focus()

    lblPassword = Label(frameLibraryCard, text="Пароль", font=("Century Gothic", 12), width=0, height=0)
    lblPassword.place(relx=0.125, rely=0.58)

    entPassword = Entry(frameLibraryCard, width=55)
    entPassword.place(relx=0.28, rely=0.585)

    EntryBtn = Button(frameLibraryCard, text="           Вход           ", font=("Century Gothic", 12),
                      command=btnEntryClicked)
    EntryBtn.place(relx=0.365, rely=0.7)

    ButtonReg = Button(frameLibraryCard, text="Регистрация", fg='blue', font=("Century Gothic", 12), width=0, height=0,
                       relief=FLAT)
    ButtonReg.place(relx=0.39, rely=0.8)

    MyFont = font.Font(ButtonReg, ButtonReg.cget("font"))
    MyFont.configure(underline=True)
    ButtonReg.configure(font=MyFont)

    LoginWindow.mainloop()

# Main work window "MainWindow" description
def MainWindow():

    global WorkWindow, lblDataNTime, entLibraryCard, btnCurrentLogin, btnAddBook, btnDelBook, \
        btnAddMagazine, btnDelMagazine, lblFio, txtBook, txtMagazine

    WorkWindow = Toplevel()                # create work window
    WorkWindow.iconbitmap('Work_icon.ico') # work's window icon

    w = WorkWindow.winfo_screenwidth()     # windwow's width
    h = WorkWindow.winfo_screenheight()    # windwow's height
    w = w // 2                             # screen centering
    h = h // 2
    w = w - 300                            # window's location
    h = h - 300
    WorkWindow.geometry('600x600+{}+{}'.format(w, h))
    WorkWindow.resizable(False, False)

    lblDataNTime = Label(WorkWindow, font=("Century Gothic", 12))
    lblDataNTime.place(relx=0, rely=0)

    frameLibraryCard = Frame(WorkWindow, width=575, height=50, bg='gray80')
    frameLibraryCard.place(relx=0.02, rely=0.06)

    lblLibraryCard = Label(frameLibraryCard, text="Номер билета:", font=("Century Gothic", 15),
                           width=0, height=0, bg='gray80')
    lblLibraryCard.place(relx=0.01, rely=0.165)

    entLibraryCard = Entry(frameLibraryCard, width=45)
    entLibraryCard.place(relx=0.3, rely=0.3, height=20)
    entLibraryCard.focus()

    btnLibraryCard = Button(frameLibraryCard, text='Найти', font=("Century Gothic", 10), bg='gray90',
                            width=10, height=0, command=btnLibraryCardClicked)
    btnLibraryCard.place(relx=0.805, rely=0.23)

    lblFio = Label(WorkWindow, text="", font=("Century Gothic", 15), width=0, height=0, bg='gray90')
    lblFio.place_forget()

    Notebook = ttk.Notebook(WorkWindow)
    Notebook.place(relx=0.02, rely=0.2)

    Book_Tab = Frame(Notebook, width=570, height=380)
    Book_Tab.place(relx=0.02, rely=0.2)

    Magazine_Tab = Frame(Notebook, width=570, height=380)
    Magazine_Tab.place(relx=0.02, rely=0.2)

    Notebook.add(Book_Tab, text="Книги")
    Notebook.add(Magazine_Tab, text="Журналы")

    btnAddBook = Button(Book_Tab, text='Добавить', font=("Century Gothic", 10), bg='gray90',
                        width=10, height=0, command=btnAddBookClicked, state='disabled')
    btnAddBook.place(relx=0.18, rely=0.02)

    btnDelBook = Button(Book_Tab, text='Удалить', font=("Century Gothic", 10), bg='gray90',
                        width=10, height=0, command=btnDeleteBookClicked, state='disabled')
    btnDelBook.place(relx=0.65, rely=0.02)

    txtBook = Text(Book_Tab, width=68, height=20)
    txtBook.place(relx=0.02, rely=0.12)

    btnAddMagazine = Button(Magazine_Tab, text='Добавить', font=("Century Gothic", 10), bg='gray90',
                            width=10, height=0, command=btnAddMagazineClicked, state='disabled')
    btnAddMagazine.place(relx=0.18, rely=0.02)

    btnDelMagazine = Button(Magazine_Tab, text='Удалить', font=("Century Gothic", 10), bg='gray90',
                            width=10, height=0, command=btnDeleteMagazineClicked, state='disabled')
    btnDelMagazine.place(relx=0.65, rely=0.02)

    txtMagazine = Text(Magazine_Tab, width=68, height=20)
    txtMagazine.place(relx=0.02, rely=0.12)

    frameLogin = Frame(WorkWindow, width=575, height=50, bg='gray80')
    frameLogin.place(relx=0.02, rely=0.88)

    lblCurrentLogin = Label(frameLogin, text='Текущий логин '+entLogin.get(), font=("Century Gothic", 15),
                            width=0, height=0, bg='gray80')
    lblCurrentLogin.place(relx=0.02, rely=0.2)

    btnCurrentLogin = Button(frameLogin, text='Сменить пользователя', font=("Century Gothic", 10), bg='gray90',
                             width=0, height=0, command=btnCurrentLoginClicked)
    btnCurrentLogin.place(relx=0.7, rely=0.2)

    update_time()
    WorkWindow.protocol("WM_DELETE_WINDOW", LoginWindow.destroy)
    WorkWindow.mainloop()

# ====================================================================================================================




# ====================================================================================================================
# Program

# open book database as JSON
with open('Book_BD_json.txt') as file:
    data = json.load(file)
if len(data) == 0:
    data['Books'] = []

with open('User_Logins_n_passwords_json.txt') as fileLoginPassword:
    UserLoginNpassword = json.load(fileLoginPassword)
if len(UserLoginNpassword) == 0:
    UserLoginNpassword['User'] = []

# open client database as JSON
with open('Client_Card.txt') as fileClientBD:
    ClientBD = json.load(fileClientBD)
if len(ClientBD) == 0:
    ClientBD['Client'] = []

# open magazine database as XML
main = ET.Element('Magazine')
tree = ET.parse('Magazine_BD_XML')
root = tree.getroot()

if (len(root) == 0):
    dataXML = ET.tostring(main, encoding='unicode')
    myFile = open('Magazine_BD_XML', 'w')
    myFile.write(dataXML)
    myFile.close()
# ====================================================================================================================




# start the program from the authorization window
EntryWindow()