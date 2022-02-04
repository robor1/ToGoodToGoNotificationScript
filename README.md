# ToGoodToGoNotificationScript
Using an unofficial To Good To Go API, this Python script will allow you to receive notifications from your To Good To Good favourites list when a new magic bag is available for a store
#Before running

Windows commands below, linux won't be too different from this.

## Initial setup:

Set destination of virtual environment (will need to be done whenever moving the directory of the virtual environment).
Access the activate text file (<Project Folder>\tgtgAPI\Scripts\activate), go down to the line with VIRTUAL_ENV="" and
fill in the text box with the location of your virtual environment.

Example virtual environment location: C:\Users\JohnSmith\Documents\ToGoodToGoNotificationScript\tgtgApi

## Run Instructions

1. Active venv
<Project directory>\tgtgApi\Scripts\activate.exe 

2. Use this command in the terminal in the same directory as the file tgtgApiTestProg.py 
python tgtgApiTestProg.py <email adress of tgtg account>

3. validate login on email address

Now it should be running

#Current Goals to achieve

- [x] Upload to GitHub (DONE)

- [x] Add logic to detect when a store has just added magic bags, and when a store has just sold its last magic bag (DONE)

- [ ] Add a text to speech bot to notify the user when the above has happened

- [ ] Polish up code

- [ ] Figure out venv and best way to run the program

- [ ] Check funtionality on linux and mac