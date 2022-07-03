#!/usr/bin/python3 -X utf8

import random
import sys
import tempfile
import os
import shlex
import re

def build_gtypist_file(texts):
	endline = 10
	tf = tempfile.mkstemp()
	fp = open(tf[1], 'w')
	practice_blocks = ""
	num = 0
	for text in texts:
		textlines = len(text.split("\n"))+1
		num += 1
		practice_blocks += """I:excerp {current}/{total}
S:{text}
B:
""".format(text=split_lines_gtypist(text), current=num, total=len(texts))
	fp.write("""K:12:END
B:
{practice_blocks}
T:
 :
 :
 : Congratulations: you successfully completed the {total} book excerp lessons !
*:END
X:
""".format(practice_blocks=practice_blocks, total=len(texts)))
	fp.close()
	return tf[1]

def split_lines_gtypist(text):
	max_line_length = 60
	output = ""
	prefix = ""
	words = text.split(" ")
	last_line = ""
	for word in words:
		if not word:
			continue
		if len(last_line) + len(word) > max_line_length:
			output += prefix + last_line.strip() + "\n"
			last_line = " "
			prefix = " :"
		last_line += " "+word
	output += prefix + last_line.strip()
	return output

def sanitize_textfile(textfile):
	f = open(textfile, 'r')
	re.compile(r' *?(\.,!?:;)')
	text = f.read()
	text = re.sub(r'[^a-zA-Z0-9äöüÄÖÜH!"\$%&/)(=\?ß\+\*#\'_\.:,;@-]', ' ', text)
	text = re.sub(r' +', ' ', text)
	text = re.sub(r'^([\.,!\?:;])', '\\1', text)
	text = re.sub(r'([\.\!\?])', '\\1\n', text)
	f.close()
	f = open(textfile, 'w')
	f.write(text)
	f.close()
	return textfile

def ebook_to_plaintext_tempfile(ebook):
	tempfile1 = "/tmp/_typebook_%s.txt" % os.path.basename(ebook)
	tempfile2 = "/tmp/typebook_%s.txt" % os.path.basename(ebook)
	if not os.path.exists(tempfile2) or os.path.getsize(tempfile2) == 0:
		os.system('ebook-convert %s %s;' % (shlex.quote(ebook), shlex.quote(tempfile1)))
		os.system("cat %s | sed 'H;1h;$!d;x;y/\\n/#/' | sed 's/#/ /g' > %s" % (shlex.quote(tempfile1), shlex.quote(tempfile2)))
	os.unlink(tempfile1)
	return sanitize_textfile(tempfile2)

def random_line_of_textfile(textfile):
	x = 0
	lines = []
	with open(textfile, 'r') as fp:
		lines = fp.readlines()
		x = len(lines)
	random_line = random.randrange(1,x)
	text = lines[random_line].strip()
	while len(text) <= 100:
		random_line = random.randrange(1,x)
		text += " "+lines[random_line].strip()
	return str(text)

def random_word_from_random_line(textfile):
	word = None
	while not word:
		line = random_line_of_textfile(textfile)
		words = line.split(" ")
		# as many iterations as words
		for word in words:
			word = words[random.randrange(0,len(words)-1)]
			word_tmp = re.sub(r"[,\.;\:\?!\"']", "", word)
			if len(word_tmp)<3:
				continue
			word = word_tmp
			break
	return " ".join([word]*10)

def main(ebook, type, num):
	lines = []
	textFile = ebook_to_plaintext_tempfile(ebook)
	for i in range(num):
		if type == "line":
			lines.append(random_line_of_textfile(textFile))
		elif type == "word":
			lines.append(random_word_from_random_line(textFile))
	gtypistFile = build_gtypist_file(lines)
	#os.system("cat %s" % gtypistFile)
	os.system("gtypist %s" % gtypistFile)
	
style = str(sys.argv[1])
num = int(sys.argv[2])
ebook = str(sys.argv[3])
main(ebook, style, num)
