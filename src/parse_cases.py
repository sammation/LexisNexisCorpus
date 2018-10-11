import re
import xml.etree.ElementTree as ET
from collections import defaultdict

source = "}source"

def parse_case(case_string):
	'''extract relevant information from a case_string'''
	parsed = dict() 
	judges = set()
	counselors = set() 
	citations = list()
	citeForThisResource = list() 
	paginationSchemes = set() 
	
	# case string is xml
	xmlTree = ET.fromstring(case_string) 
	# for each field in the resulting xml tree:
	# 	if we care about it:
	#		add it to the parsed dict
	for t in xmlTree.iter():
		if t.tag == "fullCaseName":
			parsed["fullCaseName"] = t.text
		elif t.tag == "docketNumber":
			parsed["docketNumber"] = t.text
		elif t.tag == "courtName":
			parsed["courtName"] = t.text
		elif t.tag == "jurisSystem":
			parsed["jurisSystem"] = t.attrib
		elif t.tag == "citeForThisResource":
			t.attrib["citeText"] = t.text
			citeForThisResource.append(t.attrib)
		elif t.tag == "opinion":
			parsed["opinion"] = t.attrib
		elif t.tag == "caseOpinionBy":
			parsed["caseOpinionBy"] = t.text
		elif t.tag == "judge":
			for sub_t in t.iter(): 
				if sub_t.tag == "nameText":
					judges.add(sub_t.text)
		elif t.tag == "counselor":
			for sub_t in t.iter(): 
				if sub_t.tag == "nameText":
					counselors.add(sub_t.text) 
		elif t.tag == "keyValue":
			citation = ''.join(t.attrib["value"].split())
			citations.append(citation)
		elif t.tag == "filedDate":
			t.attrib["fullDate"] = ''.join((t.attrib["year"],t.attrib["month"],t.attrib["day"]))
			parsed["filedDate"] = t.attrib
		elif t.tag == "decisionDate":
			t.attrib["fullDate"] = ''.join((t.attrib["year"],t.attrib["month"],t.attrib["day"]))
			parsed["decisionDate"] = t.attrib
		elif t.tag == "paginationScheme": 
			paginationSchemes.update((v for k,v in t.attrib.items()))
		elif t.tag[-len(source):] == source: 
			parsed["productContentSetIdentifier"] = t.text

	# add the elements that may appear more than once and only if they appeared
	if judges: 
		parsed["judges"] = list(judges)
	if citations:
		parsed["citations"] = citations
	if counselors: 
		parsed["counselors"] = list(counselors) 
	if paginationSchemes: 
		parsed["paginationSchemes"] = list(paginationSchemes)
	if citeForThisResource: 
		parsed["citeForThisResource"] = citeForThisResource

	#parsed["caseText"] = '\n'.join((text for text in xmlTree.itertext() if text))
	parsed["caseText"] = case_string # add the entire case string 
	return parsed 		
