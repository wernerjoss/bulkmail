#!/usr/bin/env python3

# ....bulkmail.py: send bulk email to recipients in RecListFileName
# ....Werner Joss, 2017 - 2023
# ....License: GPL
# ....Message is from MsgFileName, preceeded by 'Hallo <Name>,\n'
# ....RecListFileName must contain one Recipient per line in the form 'Vorname Name <email>'	note: surrounding <> for email Adress is required !
# ....Default Subject may be overridden in MsgFile (line starting with 'Subject:'
# ....this can send messages with utf-8 encoding, not just ascii (as bulkmail_asc.py) 30.04.17
# ....add max No of Msgs sent per run (SPAM Protection) 10.03.18
# ....guess gender :) - see https://pypi.python.org/pypi/gender-detector 10.03.18 - 
# ....replaced by gender_guesser: https://pypi.org/project/gender-guesser/ 02/2020
# ....getopt Argument Parser 11.03.18
# ....add Attach File Option 11.03.18
# ....fix some bugs 18.03.18
# ....ported to python3 02/2020

# Note: from python3.11 (Debian bookworm), this needs a dedicated environment, e.g. in ~/.env/venv with gender-guesser and PyYAML installed,
# see https://python.land/virtual-environments/virtualenv

import getopt, os, sys
import smtplib
from email.utils import formatdate
import time, datetime
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import codecs
import yaml # needed for cfgfile
import gender_guesser.detector as gender_detector

def send_email(FROM, TO, SUBJECT, TEXT, att_file):

	date = datetime.datetime.now().strftime('%d %b %Y %H:%M')

	# Prepare actual message

	msg = MIMEMultipart()
	msg['Subject'] = SUBJECT
	msg['From'] = FROM
	msg['To'] = TO[0]
	#msg['Date'] = date	#	obsolete, does not work any more
	msg["Date"] = formatdate(localtime=True)


	text = MIMEText(TEXT.encode('utf-8'), 'plain', 'utf-8')
	msg.attach(text)

	# add attachment
	if len(att_file) > 0:
		anhang = MIMEApplication(open(att_file, "rb").read())
		anhang.add_header('Content-Disposition', 'attachment', filename=att_file)
		msg.attach(anhang)

	try:
		server = smtplib.SMTP(smtp_server, 25)  # be sure to use correct port (25 for std smtp)
		server.ehlo()
		server.starttls()
		server.login(user, pwd)
		server.sendmail(FROM, TO, msg.as_string('utf-8'))
		server.close()
	except:
		logtext = 'failed to send mail to %s' % TO
		print(logtext)
		if CreateLogFile:
			LogFile.write(logtext)

def usage(progname):
	print('usage: %s [-l -s -n -d Delay] -r <RecListFileName> -m <MsgFileName> -a <AttachFileName>' % progname)
	print('(-l = create Logfile, -s = Simulate, -n = Nice, -p = Polite)')
	sys.exit(2)

# read config from yaml file:
cfgpath = os.path.abspath(os.path.dirname(__file__))
try:
	cfgfile = cfgpath + '/bulkmail.yaml'	# config file must reside in same Dir as Program !
	with open(cfgfile, "r") as configfile:
		cfg = yaml.load(configfile, Loader=yaml.FullLoader)
		configfile.close()
		
except:	# Defaults:
	print("Warning: Config File not found, using Defaults (which will most likely NOT work!")
	cfg = {
		'FROM': 'George Bush <ghwbush@whitehouse.gov>',
		'smtp_server': 'smtp1.whitehouse.gov',
		'user': 'gbush',
		'pwd': 'obama',
		'editor': 'kate',
		'lang': 'de'
	}
	print(cfg)

FROM = cfg['FROM']
smtp_server = cfg['smtp_server']
user = cfg['user']
pwd = cfg['pwd']

Simulate = False	# nomen est omen :)
Nice = False #  True: Anrede 'Liebe(r)' statt 'Hallo' :)
Polite = False
CreateLogFile = False
TO = [FROM]  # must be a list
SUBJECT = 'Test bulk email'
TEXT = 'Test sending bulk-mail using smtp server'
RecListFileName = 'Recipients.lst'
MaxMsgNum = 128 # max. no# of messages to be sent in one run (SPAM Protection!) 10.03.18

RecListFileName = ''
MsgFileName = ''
AttachFileName = ''
Delay = 0
try:
	progname = sys.argv[0]
	argv = sys.argv[1:] # wichtig !
	opts, args = getopt.getopt(argv,"lsnphd:r:m:a:",["RecListFileName=","MsgFileName=","AttachFileName=","Delay="])
	#print ('opts',opts)
	#print ('argv',argv)
except getopt.GetoptError as err:
	print(str(err))
	usage(progname)
for opt, arg in opts:
	if opt == '-h':
		usage(progname)
	elif opt in ("-r", "--RecListFileName"):
		RecListFileName = arg
	elif opt in ("-m", "--MsgFileName"):
		MsgFileName = arg
	elif opt in ("-a", "--AttachFileName"):
		AttachFileName = arg
	elif opt in ("-d", "--Delay"):
		Delay = int(arg)	# wichtig: type conv !
		#	print ('Delay', Delay)
	elif opt == '-l':
		CreateLogFile = True
		#   print ('CreateLogFile')
	elif opt == '-n':
		Nice = True
		# print ('Nice', Nice)
	elif opt == '-p':
		Polite = True
		# print ('Polite', Polite)
	elif opt == '-s':
		Simulate = True
		# print ('Simulate')
	else:
		print('invalid option ', arg)
		sys.exit(2)

if (len(MsgFileName) < 1) and (len(RecListFileName) < 1):
	usage(progname)
if len(MsgFileName) < 1:
	print('no msg file specified')
	usage(progname)
if len(RecListFileName) < 1:
	print('no recipients file specified')
	usage(progname)

# read message (and subject) from MsgFile
Msg = ''
try:
	MsgFile = codecs.open(MsgFileName, 'r', 'UTF-8')
	line = MsgFile.readline()  # read 1st line
	if CreateLogFile:
		LogFileName = MsgFileName + '.log'
		LogFile = codecs.open(LogFileName, 'w', 'UTF-8')
	while line:
		sline = line.strip()
		if sline.startswith('Subject:'):
		# extract Subject
			SUBJECT = sline.replace('Subject:', '')
		else:
			Msg += line
		line = MsgFile.readline()

	LogMsg = 'Message:\n' + Msg + '\nhas been sent to:\n'
	if CreateLogFile:
		LogFile.write(LogMsg)
	MsgFile.close()
except:
	print('could not read %s - exiting' % MsgFileName)
	if CreateLogFile:
		LogFile.write('could not read %s - exiting' % MsgFileName)
	sys.exit()

d = gender_detector.Detector()
# process RecListFile, send emails to each recipient
try:
	RecListFile = open(RecListFileName, 'r')
	line = RecListFile.readline();  # read 1st line
	#	print(line)
	lineNum = 1
	try:
		lang = cfg['lang']
	except:
		lang = 'de'
	while line:
		line = line.strip()
		#	print(line)
		if len(line) > 0 and not line.startswith('#'):
			parts = line.split(' ')
			Vorname = parts[0]
			Name = parts[1]
			mailadr = parts[2]
			TO = []
			TO.append(Vorname + ' ' + Name + ' ' + mailadr)
			gender = d.get_gender(Vorname)
			# print('Gender:', gender)
			if (lang == 'de'):
				Greet = 'Hallo' # default
				if (Nice):
					if (gender == 'male'):
						Greet = 'Lieber'
					elif (gender == 'female'):
						Greet = 'Liebe'
				if (Polite):
					if (gender == 'male'):
						Greet = 'Sehr geehrter Herr'
					elif (gender == 'female'):
						Greet = 'Sehr geehrte Frau'
			else:
				Greet = 'Hello'
				if (Nice):
					Greet = 'Dear'
				if (Polite):
					if (gender == 'male'):
						Greet = 'Dear Mr.'
					elif (gender == 'female'):
						Greet = 'Dear Mrs.'
			TEXT = '%s %s,\n%s ' % (Greet, Vorname, Msg)
			if (Polite):
				TEXT = '%s %s,\n%s ' % (Greet, Name, Msg)
			# print('%s %s\n' % (Greet, Vorname))
			if (not Simulate):
				send_email(FROM, TO, SUBJECT, TEXT, AttachFileName)
				print('Message %d from %s has been sent to: %s' % (lineNum, MsgFileName, TO))
			else:
				print('Message %d from %s would be sent to: %s' % (lineNum, MsgFileName, TO))
			if (Delay > 0):
				time.sleep(Delay)
			lineNum += 1
			LogMsg += line + '\n'
			if CreateLogFile:
				LogFile.write(line + '\n')
			if (lineNum > MaxMsgNum):
				line = 'max No of Messages (%d) for run 1 reached, sending stopped!' % (MaxMsgNum)
				LogMsg += line + '\n'
				if CreateLogFile:
					LogFile.write(line + '\n')
				break
		line = RecListFile.readline()
except:
	line = 'could not read %s - exiting' % RecListFileName
	print(line)
	if CreateLogFile:
		LogFile.write(line)
	sys.exit()
RecListFile.close()
if CreateLogFile:
	LogFile.close()

# Log Message as email to Sender
TO = [FROM]
if (not Simulate):
	send_email(FROM, TO, SUBJECT, LogMsg, AttachFileName)
