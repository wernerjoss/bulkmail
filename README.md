## bulkmail.py: send bulk email to recipients in RecListFileName

This Program is a bulk Mailer, written in Python 3, intended exactly for what the name indicates:  
Sending Mail to a List of recipients, but, as opposed to the standard CC (or BCC) Feature from conventional MUA's, each individual Mail ist personalised,
which means, each Recipient is addressed by his/her first Name.  
Additionally, there is an Option 'nice' which can be used to make the Text even more nice (by using 'Liebe(r) XYZ' instead of 'Hallo XYZ').  
And, yes, this nice Approach is even gender sensitive :-)
For a History about Develompment, see [this Blog Post](https://hoernerfranzracing.de/werner/blog/spam-schleuder-version-2-0).

This is an improved Version from this [original gist](https://gist.github.com/wernerjoss/9ba0d815bb91d043f929d98670f99064).  
After some more improvements and future plannings (see TODO) I decided to make a real project out of it.  
As an Addition to the CLI Version, it also has a GUI Frontend, written with PyQt5:

![](screenshot.png)

## Usage:
The CLI Version, bulkmail.py, is the core function of this Program.  
It takes the Recipient File Name and the Message File Name as mandatory Arguments, others for Simulation (Test before actual sending!),
Logfile creation, Nice Salutation and Attachment (File) are optional.  
Configuration (SMTP Server, Sender Credentials) is (currently) inside the source code and must be adapted to your needs before actual use.  
bulkmail.py should be stored somewhere in your PATH, e.g. /usr/local/bin .  
The same applies for the GUI Frontend bmgui.py/bmgui_layout.py.
Be sure to provide the Recipints List File in the correct Format !  
(each Line holds Fist Name, blank, Last Name, blank, <email address> - empty Lines or Lines beginning with # are ignored).
Before real world use, you should first adapt the File bulkmail.yaml to your actual needs, mandatory working Parameters are those for
accessing your SMTP Server, the value for 'editor' is optional and only needed for the GUI Version.
Also be sure to save the adapted copy for bulkmail.yaml in the same Place where you keep the executable File(s) *.py - e.g. /usr/local/bin

## Hints:
Message sent is from MsgFileName, preceeded by 'Hallo <Name>,\n'  
RecListFileName must contain one Recipient per line in the form 'Vorname Name <email>'	note: surrounding <> for email Adress is required !  
Default Subject should be overridden in MsgFile (1st line starting with 'Subject:')  
Here is a short Explanation of available Options:
-   -l : create Logfile
-   -s : Simulate (do not really send Mails, just list what would be sent)
-   -n : nice - use 'Liebe(r)' instead of 'Hallo' as Salutation
-   -d : (followed by Number) Delay between sending consecutive Mails
-   -h : Help 

## (Old) Changelog for CLI Version:
this can send messages with utf-8 encoding, not just ascii (as bulkmail_asc.py) 30.04.17  
add max No of Msgs sent per run (SPAM Protection) 10.03.18  
guess gender :) - see [gender detector](https://pypi.python.org/pypi/gender-detector) 10.03.18  
- replaced by [gender_guesser](https://pypi.org/project/gender-guesser/) 02/2020   
getopt Argument Parser 11.03.18  
add Attach File Option 11.03.18  
fix some bugs 18.03.18  

## TODO:
- Session Management (remember last used Files...) ?
- Localisation (say 'Hallo' or 'Hello', 'Liebe(r)' or 'Dear' to Recipients...)
- enable optional encryption for recipients from local keyring