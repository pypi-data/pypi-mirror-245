""" DCPIM is a general purpose Python 3.x library that contains a lot of
	commonly done operations inside of a single package. (C) 2018-2023
	Patrick Lambert - http://dendory.net - Provided under the MIT License
"""

__VERSION__ = "1.0.4"

import re
import os
import sys
import time
import uuid
import json
import string
import random
import fnmatch
import hashlib
import smtplib
import logging
import logging.handlers
import datetime
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar

def syslog(log_name, log_debug = False):
	""" Return a handle for syslog with sensible defaults.
			@param log_name: The name to use in syslog
			@param log_debug: Log at a debug log level
	"""
	log = logging.getLogger(log_name)
	if log_debug:
		log.setLevel(logging.DEBUG)
	else:
		log.setLevel(logging.INFO)
	handler = logging.handlers.SysLogHandler(address = '/dev/log')
	handler.setFormatter(
		logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
	)
	log.addHandler(handler)
	return log

def urlencode(text):
	""" Encode text for use on a URL bar.
			@param text: The text to encode
	"""
	return urllib.parse.quote_plus(text)

def max_len(text, maxlen):
	""" Return a string capped at a specific length.
			@param text: The text to return
			@param maxlen: The maximum length of the string
	"""
	return text if len(text)<=maxlen else text[0:maxlen-3]+'...'

def remove_tags(text):
	""" Return the text without any HTML tags in it.
			@param text: The text to process
	"""
	return re.sub(r'<[^<]+?>', '', text)

def is_int(number):
	""" Check if a variable can be cast as an int.
			@param number: The number to check
	"""
	try:
		_ = int(number)
		return True
	except:
		return False

def is_float(number):
	""" Check if a variable can be cast as a floating point.
			@param number: The number to check
	"""
	try:
		_ = float(number)
		return True
	except:
		return False

def base36(number):
	""" Converts an integer to an alphanumeric string.
			@param number: The number to convert
	"""
	b36 = ""
	alphabet = string.digits + string.ascii_uppercase

	while int(number) > 0:
		number, i = divmod(int(number), len(alphabet))
		b36 = alphabet[i] + b36

	return b36

def guid(length=16):
	""" Return a unique ID based on the machine, current time in
		milliseconds, and random number.
			@param length: The length of the ID (optional,
			defaults to 16 bytes)
	"""
	hw = str(base36(uuid.getnode() + int(time.time()*1000000)))
	pad = ''.join(random.choice(string.ascii_uppercase
	+ string.digits) for i in range(length-len(hw)))
	return str(hw + pad).upper()

def in_tag(text, first, last=None):
	""" Return what's between the first occurrence of 2 unique tags, or in
		between an HTML tag.
			@param text: The text to evaluate
			@param first: The first tag
			@param last: The last tag (optional, takes the first as a closing
			HTML tag otherwise)
	"""
	try:
		if last:
			start = text.index(first) + len(first)
			tmp = text[start:]
			end = tmp.index(last)
			result = tmp[:end]
		else:
			last = "</" + first + ">"
			first = "<" + first
			start = text.index(first) + len(first)
			tmp = text[start:]
			start = tmp.index(">") + 1
			end = tmp.index(last, start)
			result = tmp[start:end]
		return result.replace('\n','').replace('\r','').strip()
	except ValueError:
		return ""

def args(arg_format="dict"):
	""" Return the arguments passed to the script, divided by spaces or dashes.
			@param arg_format: Whether to return as a space separated string or as
			a dash separated dict
	"""
	p = ""
	sys.argv.pop(0)
	for arg in sys.argv:
		p += arg + " "
	if arg_format.lower() != "dict":
		if len(p) > 0:
			return p[:-1]
		else:
			return p
	else:
		d = []
		if len(p) > 0:
			p = " " + p[:-1]
			for arg in p.split(' -'):
				d.append("-" + arg)
			d.pop(0)
		return d

def load(filename):
	""" Load a JSON file.
			@param filename: The filename to load from
	"""
	with open(filename, 'r', encoding='UTF-8') as fd:
		data = fd.read()
	return json.loads(data)

def save(filename, data):
	""" Save data in a JSON file.
			@param filename: The filename to use
			@param data: The object to save
	"""
	with open(filename, 'w', encoding='UTF-8') as fd:
		fd.write(json.dumps(data, sort_keys = False, indent = 4))

def unixtime():
	""" Return the current UTC time in seconds.
	"""
	return int(time.time())

def unixtime2datetime(unix_time):
	""" Convert unixtime to a date/time string.
			@param unix_time: A numeric unixtime value
	"""
	return datetime.datetime.fromtimestamp(
		int(unix_time)
	).strftime('%Y-%m-%d %H:%M:%S')

def datetime2unixtime(date_time):
	""" Convert date/time string to a unixtime number.
			@param unix_time: A numeric unixtime value
	"""
	return time.mktime(datetime.datetime.strptime(
		date_time,
		"%Y-%m-%d %H:%M:%S"
	).timetuple())

def now():
	""" Return the current UTC date and time in a standard format.
	"""
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def days_since(timestamp):
	""" Return number of days since a specific UTC time and date.
			@param timestamp: A time in 'YYYY-MM-DD HH:MM:SS' format
	"""
	x = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
	y = datetime.datetime.now()
	z = y - x
	return z.days

def hashfile(filename):
	""" Return a unique hash for the content of a file.
			@param filename: The file to hash
	"""
	bsize = 65536
	hasher = hashlib.sha256()
	with open(filename, "rb") as fd:
		while True:
			data = fd.read(bsize)
			if not data:
				break
			hasher.update(data)
	return str(hasher.hexdigest()).upper()

def hashstr(text):
	""" Return a unique hash for a string.
			@param text: The string to hash
	"""
	hasher = hashlib.sha256(text.encode())
	return str(hasher.hexdigest()).upper()

def header(content_type="text/html", filename=None):
	""" Return the header needed for a web application.
			@param content_type: The type of content delivered (optional,
			defaults to text/html)
			@param filename: Set the content to be a downloadable file
			(optional)
	"""
	output = "Content-Type: " + str(content_type) + "; charset=utf-8\n\n"
	if filename:
		output = "Content-Disposition: attachment; filename=" + filename
		output += "\n" + output
	return output

def error():
	""" Return the error message after an exception. Must be used in an
	'except' statement.
	"""
	_, b, _ = sys.exc_info()
	return str(b)

def email(fromaddr, toaddr, subject, body):
	""" This will send an email.
			@param fromaddr: Email of sender
			@param toaddr: Email of recipient
			@param subject: Subject of the email
			@param body: Body of the email
	"""
	smtpobj = smtplib.SMTP("localhost")
	smtpobj.sendmail(str(fromaddr), str(toaddr), "From: " + str(fromaddr)
	+ "\nTo: " + str(toaddr) +"\nSubject: " + str(subject).replace('\n','')
	.replace('\r','') + "\n\n" + str(body) + "\n")

def curl(url, encoding="utf8", cookie=None):
	""" Get the content of a URL.
			@param url: The URL to query
			@param encoding: The decoding format (optional, defaults to UTF-8)
			@param cookie: The cookie string in format key1=value1;key2=value2
			(optional)
	"""
	if cookie:
		headers = {
			'Cookie': cookie,
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) " \
			"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 " \
			"Safari/537.36"
		}
	else:
		headers = {
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) " \
			"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 " \
			"Safari/537.36"
		}
	con = urllib.request.Request(url, headers=headers)
	cj = CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	stream = opener.open(con)
	result = stream.read()
	charset = stream.info().get_param('charset', encoding)
	return result.decode(charset)

def download(url, localfile):
	""" Download a file from the Internet.
			@param url: The url of the file
			@param localfile: Where to save that file
	"""
	urllib.request.urlretrieve(url, localfile)
	return os.stat(localfile).st_size

def in_list(ldict, key, value):
	""" Find whether a key/value pair is inside of a list of dictionaries.
			@param ldict: List of dictionaries
			@param key: The key to use for comparision
			@param value: The value to look for
	"""
	for l in ldict:
		if key in l and l[key] == value:
			return True
	return False

def remove_spaces(text):
	""" Remove extra spaces from a string.
			@param text: The string to process
	"""
	return re.sub(r'\s\s+', ' ', text).strip()

def cmd(command):
	""" Run a command and return the output.
			@param command: The command to run
	"""
	return os.popen(command).read().rstrip('\n')

def alphanum(text, symbols=False, spaces=False):
	""" Return only letters, numbers and optionally basic symbols and spaces
		in a string.
			@param text: The string to process
			@param symbols: Whether to leave basic symbols
			@param spaces: Whether to leave spaces
	"""
	if spaces and symbols:
		return re.sub(r'[^0-9a-zA-Z \_\-\.\[\]\(\)\@\!\?\:\'\;]+', '', text)
	elif spaces:
		return re.sub(r'[^0-9a-zA-Z ]+', '', text)
	elif symbols:
		return re.sub(r'[^0-9a-zA-Z\_\-\.\[\]\(\)\@\!\?\:\'\;]+', '', text)
	return re.sub(r'[^0-9a-zA-Z]+', '', text)

def list_files(folder, pattern="*"):
	""" Return a list of files in a folder recursively.
			@param folder: The folder to list files from
			@param pattern: The pattern files must match (optional)
	"""
	matches = []
	for root, _, filenames in os.walk(folder):
		for filename in fnmatch.filter(filenames, pattern):
			matches.append(os.path.join(root, filename))
	return matches

def db_create(table):
	""" Create a key/value table in DynamoDB.
			@param table: The name of the table.
	"""
	import boto3
	db = boto3.client('dynamodb')
	result = db.create_table(
 		TableName = table,
 		KeySchema = [
 			{"AttributeName": "key", "KeyType": "HASH"}
 		],
 		AttributeDefinitions = [
 			{"AttributeName": "key", "AttributeType": "S"}
 		],
 			BillingMode = "PAY_PER_REQUEST"
 	)
	status = "CREATING"
	attempts = 10
	while status == "CREATING":
		response = db.describe_table(TableName = table)
		status = response['Table']['TableStatus']
		time.sleep(1)
		attempts -= 1
		if attempts < 0:
			break
	return result

def db_delete(table):
	""" Delete a key/value table from DynamoDB.
			@param table: The name of the table.
	"""
	import boto3
	db = boto3.client('dynamodb')
	result = db.delete_table(
 		TableName = table,
 	)
	return result

def db_put(table, key, value):
	""" Store a key/value in a DynamoDB table.
			@param table: The name of the table.
			@param key: Key name.
			@param value: Value to store.
	"""
	import boto3
	db = boto3.client('dynamodb')
	result = db.put_item(
		TableName = table,
		Item = {
			"key": {'S': key},
			"value": {'S': str(value)}
		}
	)
	return result['ResponseMetadata']

def db_get(table, key = None):
	""" Return the value for a key or a list of key/value
		items from a DynamoDB table.
			@param table: The name of the table.
			@param key: Key name (optional).
	"""
	import boto3
	db = boto3.client('dynamodb')
	if not key:
		output = []
		result = db.scan(TableName = table)
		for item in result['Items']:
			output.append({item['key']['S']: item['value']['S']})
		return output
	result = db.get_item(
		TableName = table,
		Key = { "key": {'S': key} }
	)
	return result['Item']['value']['S']


def test(func, arg):
	""" Test a function with optional arguments.
	"""
	possibles = globals().copy()
	print("* dcpim." + func + "(" + str(arg)[1:-1] + ")")
	method = possibles.get(func)
	try:
		a = method(*arg)
		print(str(a)[:300])
		print()
	except:
		print(error())
		print()
		sys.exit(1)
	return a
