# -*- coding: utf-8 -*- 

#
# Remove 'multi-polygon' in OSM.
# 
# multi-polygon's landuse to way.
#

import sys
import copy

from xml.etree import ElementTree
from xml.etree.ElementTree import Element


if __name__ == "__main__":

	param = sys.argv

	if len(param) < 2:
		sys.exit("arg invalid.")

	file_name = param[1]

	tree = ElementTree.parse(file_name)
	root = tree.getroot()

	# enumerate relation tags.
	relation_list = root.findall(".//relation")
	for relation in relation_list:
		
		landuse = ""
		
		# find "landuse" in relation tag.
		for tag in relation.findall(".//tag"):
			if(tag.get('k') == "landuse"):
				landuse = tag
				break

		# find "outer" in relation tag.
		for member in relation.findall(".//member"):
			if(member.get('role') == "outer"):
				
				ref = member.get('ref')	# ref => get way id
				
				# add "landuse" to way.
				for way in root.findall(".//way"):
					if(way.get('id') == ref):
						print("outer landuse", way.get('id'),landuse.get("v"))
						way.append(landuse);

		# find "inner" in relation tag.
		for member in relation.findall(".//member"):
			if(member.get('role') == "inner"):				
				ref = member.get('ref')	# ref => get way id

				# add "landuse(vineyard)" to way.
				for way in root.findall(".//way"):
					if(way.get('id') == ref):
						changed_inner = 0
						
						print("inner landuse", way.get('id'))
						for tag_inner in way.findall(".//tag"):
							if(tag_inner.get('k') == "landuse"):
								changed_inner = 1
								break

						if(changed_inner == 0):
							landuse_inner = copy.deepcopy(landuse)
							landuse_inner.set('v','vineyard')
							way.append(landuse_inner);

		root.remove(relation)

	tree.write("build/" + file_name)
