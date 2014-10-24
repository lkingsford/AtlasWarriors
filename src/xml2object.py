import xml.etree.ElementTree as ET

def parse(filename, objectConstructor):
	tree = ET.parse(filename)
	root = tree.getroot()
	items = []
	for i in root:
		item = objectConstructor()
		for j in i:
			t = item.__dict__[j.tag]
			v = j.text
			if isinstance(t, bool):
				v = v == 'true'
			elif isinstance(t, int):
				v = int(v)			
			item.__dict__[j.tag] = v
		items.append(item)
	return items
	
