from pathlib import Path
import re
from CaseParser import CaseParser as CaseParser


class FileParser(object): 

	def __init__(self): 
		self.caseparser = CaseParser()
		self.case_re = "<courtCaseDoc.*/courtCaseDoc>"

	def parse_file(self, p): 
		# p is a Posfix Path object pointing to a LexisNexis case file
		# returns a list of parsed case dicts
		return [self.caseparser.parse_case(m) for m in re.findall(self.case_re, p.open().read())]
