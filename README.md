# ToGoodToGoNotificationScript
Using an unofficial To Good To Go API, this Python script will allow you to receive notifications from your To Good To Good favourites list when a new magic bag is available for a store
#Before running

Windows commands below, linux won't be too different from this.

## Initial setup:

I would reccommend setting up a virtual enviroment before installing these modules, this is not essential however.

Now install the following modules using pip; tgtg, gtts, pyttsx3 and playsound.

But you can run the following command to do so all at once:

`pip install tgtg gtts pyttsx3 playsound`

## Run Instructions


1. Run python program using the following command

`python Main.py <email adress of Too Good To Go account>`

2. The program will ask you to now validate login via email before being able to make api calls

Now it should be running, a voice notification should now be made whenever a store gets new magic bags or sells out of magic bags

## Current Goals to achieve

- [x] Upload to GitHub (DONE)

- [x] Add logic to detect when a store has just added magic bags, and when a store has just sold its last magic bag (DONE)

- [ ] Add a text to speech bot to notify the user when the above has happened

- [ ] Polish up code

- [ ] Check funtionality on linux and mac