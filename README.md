# bulkmail.py: send bulk email to recipients in RecListFileName
Message is from MsgFileName, preceeded by 'Hallo <Name>,\n'
RecListFileName must contain one Recipient per line in the form 'Vorname Name <email>'	note: surrounding <> for email Adress is required !
Default Subject may be overridden in MsgFile (line starting with 'Subject:'
this can send messages with utf-8 encoding, not just ascii (as bulkmail_asc.py) 30.04.17
add max No of Msgs sent per run (SPAM Protection) 10.03.18
guess gender :) - see https://pypi.python.org/pypi/gender-detector 10.03.18 - replaced by gender_guesser: https://pypi.org/project/gender-guesser/ 02/2020
getopt Argument Parser 11.03.18
add Attach File Option 11.03.18
fix some bugs 18.03.18
