import os, sqlite3, datetime
today = str(datetime.date.today())#Each record will have the date recorded.
programDirectory = os.getcwd()
databaseDirectory = (programDirectory + "/Databases")

class InventoryItem:
    def __init__(self, dateDelivered, barcodeNumber, description, owner, ownerNumber):
        self.dateDelivered = dateDelivered
        self.barcodeNumber = barcodeNumber
        self.description = description
        self.owner = owner
        self.ownerNumber = ownerNumber

def createTable(c, nameOfDatabase, tableColumns):
    try:
        c.execute("CREATE TABLE " + nameOfDatabase + tableColumns)

        print("Creating the Database table:  " + nameOfDatabase)
    except sqlite3.OperationalError:
        print("The table  " + nameOfDatabase + " is already present and does not need to be created.")

def databaseSetup():
    dataBaseNames = ["Current_Inventory","Sold_Goods"]
    for nameOfDatabase in dataBaseNames:
        conn = sqlite3.connect(nameOfDatabase+'.db')
        c = conn.cursor()
        if nameOfDatabase == "Current_Inventory":
            createTable(c, nameOfDatabase,"(ID INTEGER PRIMARY KEY,Date TEXT,BarcodeNumber TEXT,"
                                                     "Description TEXT,Owner TEXT,OwnerNumber TEXT)")
        elif nameOfDatabase == "Sold_Goods":
            createTable(c, nameOfDatabase,"(ID INTEGER PRIMARY KEY,ArrivalDate TEXT,BarcodeNumber TEXT,"
                                                     "Description TEXT,Owner TEXT,OwnerNumber TEXT,"
                                                     "SalePrice,SaleDate)")
        else:
            print("Error")

#Make sure that all directories are present.
#Make sure that the Database is present and set up with all of the apopriate tables.
def initialSetup():  #This will ensure that all required files and directories are present before continuing.


    print("Initializing setup.\n")

    # Create directories
    neededDirectories = ['Databases']
    for i in neededDirectories:
        try:
            # Create target Directory
            os.mkdir(i)
            print("Directory " +i+ " Created ")
        except FileExistsError:
            print("Directory "+ i+ " already exists")
    print("All directories are present.\n")

    os.chdir(databaseDirectory)
    databaseSetup()

def updateSoldDb(i):
    import sqlite3
    databaseChoice = "Sold_Goods.db"
    conn = sqlite3.connect(databaseChoice)
    c = conn.cursor()
    print("How much did you sell the item for?")
    salesPrice = input(">")
    c.execute("INSERT INTO Sold_Goods VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
              (i.dateDelivered, i.barcodeNumber, i.description, i.owner,
               i.ownerNumber, salesPrice,today))  # This line of code added a new row to the database.
    conn.commit()

def removeDatabaseRow():
    import sqlite3
    os.chdir(databaseDirectory)
    databaseChoice = "Current_Inventory.db"
    conn = sqlite3.connect(databaseChoice)
    c = conn.cursor()
    conn.row_factory = lambda cursor, row: row[0]

    print("What inventory item would you like to sell?")

    #Produces a numerical list based off of the desired sqlite column
    possibleChoices = [c.execute('SELECT * FROM Current_Inventory').fetchall()]
    acceptableChoices = []
    nameChoices = []
    for i in possibleChoices: #Whole table
        for s in i: #Each row
            rowObj = InventoryItem(s[1], s[2],s[3],s[4],s[5])
            acceptableChoices.append({s[3]:rowObj})
            nameChoices.append(s[3])
    #acceptableChoices.append("Exit")        #Would like to shrink into one line. (you can't append a list to a list)

    #Prompts the user to select the item to remove from the database.
    userChoice = listDisplay(nameChoices)

    for i in acceptableChoices: #All row objects. "For every item in the inventory"
        try:
            i = i[userChoice]
            updateSoldDb(i)
        except KeyError:
            continue


    #remove data
    c.execute('DELETE FROM Current_Inventory WHERE Description = ?',(userChoice,)) #userChoice needs to be a tuple or it will throw a "no such column as userChoice"
    conn.commit()

    #Converts the string back so the confirmation sentences is grammatically correct.
    print(userChoice+" has been deleted from Inventory")
    mainDirectory()

#Allows the user to add new rows to a table in the Database.
def addDatabaseRow():
    import sqlite3
    os.chdir(databaseDirectory)
    databaseChoice = "Current_Inventory.db"
    conn = sqlite3.connect(databaseChoice)  # create a connection the database/create it if it doesn't exist.
    c = conn.cursor()  # no clue what this does specifically.

    print("What is the barcode number?")
    barcode = input(">")
    print("What is a description of the item?")
    itemDescription = input(">")
    print("What is the name of the owner of the item?")
    ogOwner = input(">")
    print("What is a good number to reach the owner at?")
    cellNumber = input(">")

    newRow = InventoryItem(today,barcode,itemDescription,ogOwner,cellNumber)

    #Append the data to the proper table in the database. Confirm for the user. Return to main menu.
    c.execute("INSERT INTO Current_Inventory VALUES (NULL, ?, ?, ?, ?, ?)",
              (today, newRow.barcodeNumber, newRow.description, newRow.owner,newRow.ownerNumber))  # This line of code added a new row to the database.
    conn.commit()
    print(newRow.description + " has been added.\n")
    mainDirectory()

#Takes a list and converts it into a form that users can select a numerical option. Return value is a string.
#EX. ( '1)Assets' returns 'Assets
def listDisplay(acceptableChoices):

    acceptableChoices.append("Exit")
    print("Which option would you like to choose")
    s = 1   #This is the counter
    for i in acceptableChoices: #Loop through the menu options
        print(str(s) + ") " +i) #Display all of the items in the list as a menu
        s += 1
    userChoice = int(input(">")) #Prompt the user to enter a number
    # Reruns the prompt if the user enters a number that is to big
    while userChoice > len(acceptableChoices):
        print("Invalid data. Please enter a valid number")
        print()
        print("Which option would you like to choose")
        s = 1  # This is the counter
        for i in acceptableChoices:  # Loop through the menu options
            print(str(s) + ") " + i)  # Display all of the items in the list as a menu
            s += 1
        userChoice = int(input(">"))
    #Closes the program if the user selects "Exit"
    #At some point I would like it to step back one function
    if userChoice == (s-1) and acceptableChoices[-1] == "Exit":
        print("Exiting")
        exit()
    #Converts the users numerical entry into the string version of the option selected.
    userChoiceFINAL = acceptableChoices[(int(userChoice)-1)]
    #Return the variable
    return userChoiceFINAL

#Firing order of all other functions.
def mainDirectory():
    os.chdir(programDirectory)

    acceptableChoices = ["Take in new Inventory", "Sell an inventory item",]        #Need to add "See most upd to date financial data"

    userChoice = listDisplay(acceptableChoices)

    if userChoice == acceptableChoices[0]:            #Add An Account
        addDatabaseRow()        #Decide if the user is adding an asset or a liability Add the item to the appropriate database.
    elif userChoice == acceptableChoices[1]:            #Remove An Account
        removeDatabaseRow()


                                                        #Exit is handled in the listDisplay function.

if __name__ == "__main__":
    print("Hell, Welcome to the Personal Finance Software V1.00")
    initialSetup()
    mainDirectory()
