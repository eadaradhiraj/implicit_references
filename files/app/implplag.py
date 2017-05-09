# -*- coding: utf-8 -*-
import threading, requests, re, sys, json
from bs4 import BeautifulSoup
from nltk import tokenize
import algos

try:
	reload(sys)
	sys.setdefaultencoding('utf8')
	from Queue import Queue
	from itertools import izip_longest as zip_longest
except ImportError:
	from queue import Queue
	from itertools import zip_longest

def getmetadata(filename):
	if not filename.endswith('.pdf'):
		sys.exit(Filename+' is not pdf')
	url = "http://pdfx.cs.man.ac.uk"
	try:
		fin = open('tmp/'+filename, 'rb')
		files = {'file': fin}
	except IOError:
		sys.exit("Error reading file!!")
	try:
		print ('Sending %s to %s' %(filename, url))
		r = requests.post(url, files=files, headers={'Content-Type':'application/pdf'})
		print ('Got status code %d for %s' %(r.status_code, filename))
	except:
		sys.exit("Probable internet disruption. Try Again!!!")
	finally:
		fin.close()
	xml = r.content
	return xml

def getcontrefs(xml):
	soup = BeautifulSoup(xml, "html.parser")
	paratags = soup.findAll("region", attrs = {"class":"DoCO:TextChunk"})
	paras = '\n\n'.join([tag.text for tag in paratags])
	content = paras

	reftags = soup.findAll("ref", attrs = {"class":"deo:BibliographicReference"})
	refs = list()
	for tag in reftags:
		s=tag.text
		if s[0].isdigit():
			refs.append(s[2:])
		elif s[1].isdigit():
			refs.append(s[3:])
		else:
			refs.append(s)
	return {'content':content,'refs':refs}

def parserefs(refs):
	ACCESS_TOKEN = 'fbd89c77ec04ca5ed5e29fa17c097fef'
	url = "http://anystyle.io/parse/references"
	data = {}
	data['format']='json'
	data['access_token']=ACCESS_TOKEN
	data['references']=refs
	postdata = json.dumps(data)
	req = requests.post(url, headers = {'Content-Type': 'application/json;charset=UTF-8'}, data=postdata.encode('utf8')).text
	return json.loads(req)

def getauts(refdets):
	authors=list()
	for ref in refdets:
		try:
			s=ref['author'].replace(' and ',', ').split(', ')
			for each in s:
				try:
					if each[0].isupper() and each[1].islower():
						try:
							authors.append(each[:each.index(' ')])
						except ValueError:
							authors.append(each)
				except IndexError:
					continue
		except KeyError:
			continue
	return authors

def getorder(filename):
	docxml=getmetadata(filename)
	contrefs=getcontrefs(docxml)
	cont=contrefs['content']
	refs=contrefs['refs']
	refdets=parserefs(refs)
	authors=list(set(getauts(refdets)))
	sents=tokenize.sent_tokenize(cont)
	ordr = list()
	for sent in sents:
		for author in authors:
			au=re.compile(r'\b({0})\b'.format(author))
			if au.search(sent): ordr.append(author)
	return {'filename':filename,'order':ordr}

def pattcomp(f1, f2, method='lccs'):
	q = Queue()
	resq = Queue()
	def __worker():
		while True:
			item = q.get()
			resq.put(getorder(item))
			q.task_done()
	for j in range(1,3):
		t = threading.Thread(target=__worker)
		t.daemon = True
		t.start()
	q.put(f1)
	q.put(f2)
	q.join()
	orda=resq.get()
	ordb=resq.get()
	if method=='lccs':
		res=algos.lccs(orda['order'],ordb['order'])
	elif method=='gct':
		res=algos.gct(orda['order'],ordb['order'])
	return {'filename1':orda['filename'],'filename2':ordb['filename'],'orders':zip_longest(orda['order'],ordb['order']), 'comp':res}

if __name__ == '__main__':
	print (pattcomp('doca.pdf','docc.pdf', 'lccs'))

