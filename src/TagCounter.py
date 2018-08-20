import xml.etree.ElementTree as ET

class TagCounter(object): 

	def __init__(self): 
		self.tag_counts = dict() 

	def update_counts(self, case_string): 
		xmlTree = ET.fromstring(case_string)
		all_tags = set()
		for t in xmlTree.iter(): 
			all_tags.add(t.tag) 
			if t.tag not in self.tag_counts: 
				self.tag_counts[t.tag] = [0, 0] 
			self.tag_counts[t.tag][0] += 1
		for tag in all_tags: 
			self.tag_counts[tag][1] += 1

	def get_counts(self):
		return self.tag_counts
		
