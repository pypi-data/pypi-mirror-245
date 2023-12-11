


import jk_prettyprintobj




#
# This class provides information about a Semantic MediaWiki property.
#
class SMWPropertyInfo(jk_prettyprintobj.DumpMixin):

	def __init__(self, name:str, label:str):
		self.name = name
		self.label = label
	#

	def _dumpVarNames(self) -> list:
		return [
			"name",
			"label",
		]
	#

#








