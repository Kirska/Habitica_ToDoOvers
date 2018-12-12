# Habitica To-Do Overs
The Habitica To-Do Overs project is an API tool created for [Habitica](https://habitica.com).
The tool is currently running at [this link](https://kirska.pythonanywhere.com). You can go there to actually use the tool.
### What is a To-Do Over?
A To-Do Over is a To-Do task that automatically repeats upon completion.

As an example, say you need to do laundry once a week, but you don't care what day of the week it gets done, and you'll need to do it every week. 

Enter To-Do Overs. 

You can create a To-Do Over task with a length of 7 days, and you can mark it complete anytime in that 7 day period, and when you do, the tool will automatically create a new to-do for laundry with 7 days from THAT date.

*You can also create a task without a due date, and it will simply be recreated once it's marked completed.*

Other than that, the tasks work exactly like the [built-in to-do tasks in Habitica](https://habitica.wikia.com/wiki/To-Dos).
### Creator
The tool was built in Django (Python) by [Kirska](https://github.com/Kirska). This tool is in no way affiliated with Habitica.
## FAQ
* When is the tool run?
    * The script is run daily. It may take up to a day for your new tasks to appear on Habitica once you complete one.
* What about privacy? Why do I have to provide Habitica data?
    * The tool must store your user ID and API token in order to create your tasks automatically. Your API token is encrypted before it is stored. If you login with your Habitica email and password, that data is never stored. The tool fetches your user ID and API token from Habitica if you login with your email/password. The site uses cookies to store session data, but it is encrypted.
* Can we get repeat tasks created faster?
    * The current server is a free service provided by Python Anywhere. The task could be run more often than once a day with a paid plan but I'm cheap. If anyone would like to sponsor the server, please contact Kirska.
* Can I run this locally?
    * The tool is a pretty standard Django app, with a scheduled Python script. If you'd like to run it on your local machine and not put your data on the interwebs, feel free to do so.
* Can I get rid of that note that says "Automatically created by..."?
    * Yes, if you edit your task on the tool you can get rid of that note.
## Ideas
Here are some ideas for positive habits you can use this tool for:
* Cleaning a room of your home (your bedroom, the kitchen, etc.)
* Doing laundry
* Cleaning your pet's habitat
* Doing the dishes
* Calling your parents
* Buying groceries
* Leg day at the gym
## Issues, Bugs, and Suggestions
If you have any problems or suggestions please open an issue here or contact Kirska. Pull requests are also welcome.
