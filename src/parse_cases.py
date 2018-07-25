import re
import xml.etree.ElementTree as ET

def parse_case(case_string):
	parsed = dict() 
	judges = set()
	xmlTree = ET.fromstring(case_string) 
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
			parsed["citeForThisResource"] = t.attrib
		elif t.tag == "filedDate":
			t.attrib["fullDate"] = ''.join((t.attrib["year"],t.attrib["month"],t.attrib["day"]))
			parsed["filedDate"] = t.attrib
		elif t.tag == "opinion":
			parsed["opinion"] = t.attrib
		elif t.tag == "caseOpinionBy":
			parsed["caseOpinionBy"] = t.text
		elif t.tag == "nameText":
			judges.add(t.text)
	if judges: 
		parsed["judges"] = list(judges)
		
