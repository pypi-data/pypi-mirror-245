"""Run tests for DCPIM utils."""

import dcpim

JSONFILE = "/tmp/" + dcpim.guid() + ".json"
json_data = {'name': "Hello world", 'results': ["test 1", "test 2", "test 3"]}

# guid
assert len(dcpim.test("guid", [])) == 16
assert len(dcpim.test("guid", [32])) == 32

# in_tag
assert dcpim.test("in_tag", [
	"<p>This is a link to <a href='http://google.com'>Google</a>.</p>",
	"a"
]) == "Google"
assert dcpim.test("in_tag", [
	"this random string is something, right?",
	"random", ","
]) == "string is something"
assert dcpim.test("in_tag", [
	"this random string is something, right?",
	"umbrella", ","
]) == ""

# save
assert not dcpim.test("save", [JSONFILE, json_data])

# load
assert dcpim.test("load", [JSONFILE]) == json_data

# unixtime
assert dcpim.test("unixtime", []) > 1

# now
assert len(dcpim.test("now", [])) == 19

# max_len
assert dcpim.test("max_len", [
	"This text is too long to fit in the max len.",
	25
]) == "This text is too long ..."

# remove_spaces
assert dcpim.test("remove_spaces", [
	"  This is  a test of   the \"emergency  broadcast system\". "
]) == "This is a test of the \"emergency broadcast system\"."

# syslog
assert dcpim.test("syslog", ["test"])

# urlencode
assert dcpim.test("urlencode", [
	"This is a % symbol!"
]) == "This+is+a+%25+symbol%21"

# is_int
assert dcpim.test("is_int", [5]) is True
assert dcpim.test("is_int", [5.10]) is True
assert dcpim.test("is_int", ["5"]) is True
assert dcpim.test("is_int", ["test"]) is False

# is_float
assert dcpim.test("is_float", [2]) is True
assert dcpim.test("is_float", [2.87]) is True
assert dcpim.test("is_float", ["2.87"]) is True
assert dcpim.test("is_float", ["test"]) is False

# base36
assert dcpim.test("base36", [92837]) == "1ZMT"

# args
assert dcpim.test("args", []) == []

# unixtime2datetime
assert dcpim.test("unixtime2datetime", [1000000]) == "1970-01-12 13:46:40"

# datetime2unixtime
assert dcpim.test("datetime2unixtime", ["1970-01-12 13:46:40"]) == 1000000

# days_since
assert dcpim.test("days_since", ["1970-01-12 13:46:40"]) > 19678

# hashstr
assert dcpim.test("hashstr", [
	"This is a test."
]) == "a8a2f6ebe286697c527eb35a58b5539532e9b3ae3b64d4eb0a46fb657b41562c".upper()

# in_list
assert dcpim.test("in_list", [
	[json_data],
	"name",
	"Hello world"
]) is True
assert dcpim.test("in_list", [
	[json_data],
	"name",
	"John"
]) is False
assert dcpim.test("in_list", [
	[json_data],
	"age",
	42
]) is False

# remove_spaces
assert dcpim.test("remove_spaces", [
	" This  is   a test.  "
]) == "This is a test."

# download
assert dcpim.test("download", [
	"https://github.com/dcpim/utils/archive/refs/heads/main.zip",
	"/tmp/main.zip"
]) > 10000

# cmd
assert dcpim.test("cmd", ["date > /dev/null && echo 1"]) == "1"

# alphanum
assert dcpim.test("alphanum", ["Sp@c1al str%"]) == "Spc1alstr"
assert dcpim.test("alphanum", ["Sp@c1al str%", False, True]) == "Spc1al str"
assert dcpim.test("alphanum", ["Sp@c1al str%", True, False]) == "Sp@c1alstr"

# curl
assert "html" in dcpim.test("curl", ["https://google.com"])

# header
assert "Content-Type" in dcpim.test("header", [])

# hashfile
assert len(dcpim.test("hashfile", ["README.md"])) > 2

# list_files
assert len(dcpim.test("list_files", ["."])) > 5

# DynamoDB
TABLE = dcpim.guid()
assert "TableDescription" in dcpim.test("db_create", [TABLE])
assert "RequestId" in dcpim.test("db_put", [
	TABLE,
	"key1",
	"My value"
])
assert "RequestId" in dcpim.test("db_put", [
	TABLE,
	"key2",
	"A first value"
])
assert "RequestId" in dcpim.test("db_put", [
	TABLE,
	"key2",
	"A second value"
])
assert "RequestId" in dcpim.test("db_put", [
	TABLE,
	"key3",
	{'name': 'John Doe', 'age': 28}
])
assert dcpim.test("db_get", [TABLE, "key2"]) \
	== "A second value"
assert dcpim.test("db_get", [TABLE, "key3"]) \
	== "{'name': 'John Doe', 'age': 28}"
assert len(dcpim.test("db_get", [TABLE])) == 3
assert "TableDescription" in dcpim.test("db_delete", [TABLE])
