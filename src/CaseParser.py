import re 
import xml.etree.ElementTree as ET
#from collections import defaultdict
import json

class CaseParser(object):

    def __init__(self): 
        self.textTags = {"fullCaseName", "docketNumber", "courtName",
                            "citeForThisResource", "caseOpinionBy"}
        self.multiTags = {"judge", "counselor"} 

    def parse_case(self, case_string): 
        parsed = dict()
        citations = list() 
        for t in xmlTree.iter()
	        if t.tag in self.textTags: 
	            parsed[t.tag] = t.text
	        elif t.tag in self.multiTags: 
	            if t.tag not in parsed: 
	                parsed[t.tag] = set():
	            for sub_t in t.iter(): 
	                if sub_t.tag == "nameText": 
	                    parsed[t.tag].add(sub_t.tet)
	        elif "date" in t.tag.lower() or t.tag == "jurisSystem":
	            try:
	                t.attrib["fullDate"] = ''.join([t.attrib[time] for time in ["year","month","day"])
	            except KeyError as ke:
	                pass
	            parsed[t.tag] = t.attrib
	        elif t.tag == "keyValue":
	            citation = ''.join(t.attrib["value"].split())
	            citations.append(citation) 
	        elif "}source" in t.tag: 
	        	parsed["productContentSetIdentifier"] = t.text

	    return parsed
	                

