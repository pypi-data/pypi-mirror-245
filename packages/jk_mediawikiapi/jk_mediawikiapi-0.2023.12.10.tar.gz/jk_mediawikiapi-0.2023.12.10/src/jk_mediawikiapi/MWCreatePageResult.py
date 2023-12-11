


import jk_prettyprintobj

from .MWTimestamp import MWTimestamp



class MWCreatePageResult(jk_prettyprintobj.DumpMixin):

	def __init__(self, title:str, pageID:int, oldRevID:int, bIsNew:bool, timestamp:MWTimestamp):
		self.title = title
		self.pageID = pageID
		self.oldRevID = oldRevID
		self.bIsNew = bIsNew
		self.timestamp = timestamp
	#

	def __bool__(self):
		return True
	#

	def __str__(self):
		return "MWCreatePageResult(" \
			+ "title=" + repr(self.title) \
			+ ", pageID=" + repr(self.pageID) \
			+ ", oldRevID=" + repr(self.oldRevID) \
			+ ", bIsNew=" + repr(self.bIsNew) \
			+ ", timestamp=" + repr(self.timestamp) \
			+ ")"
	#

	"""
	def dump(self):
		print("MWCreatePageResult[")
		print("\ttitle: ", self.title)
		print("\tpageID: ", self.pageID)
		print("\toldRevID: ", self.oldRevID)
		print("\tbIsNew: ", self.bIsNew)
		print("\ttimestamp: ", self.timestamp)
		print("]")
	#
	"""

	def _dumpVarNames(self) -> list:
		return [
			"title",
			"pageID",
			"oldRevID",
			"bIsNew",
			"timestamp",
		]
	#

#








