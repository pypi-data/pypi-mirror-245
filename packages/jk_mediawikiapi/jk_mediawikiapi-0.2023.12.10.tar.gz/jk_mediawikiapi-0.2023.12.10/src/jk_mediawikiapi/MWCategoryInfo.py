


import typing

import jk_prettyprintobj

from .MWPageContent import MWPageContent
from .MWTimestamp import MWTimestamp
from .MWPageRevision import MWPageRevision
from .MWNamespaceInfo import MWNamespaceInfo




class MWCategoryInfo(jk_prettyprintobj.DumpMixin):

	def __init__(self,
		name:str,
		nPages:int,
		nTotalPages:int,
		nSubCategories:int
		):

		assert isinstance(name, str)
		self.name = name

		assert isinstance(nPages, int)
		self.nPages = nPages

		assert isinstance(nTotalPages, int)
		self.nTotalPages = nTotalPages

		assert isinstance(nSubCategories, int)
		self.nSubCategories = nSubCategories
	#

	def _dumpVarNames(self) -> list:
		return [
			"name",
			"nPages",
			"nTotalPages",
			"nSubCategories",
		]
	#

#








