


import typing

import jk_prettyprintobj

from .MWPageContent import MWPageContent
from .MWTimestamp import MWTimestamp
from .MWPageRevision import MWPageRevision
from .MWNamespaceInfo import MWNamespaceInfo




class MWPage(jk_prettyprintobj.DumpMixin):

	def __init__(self, title:str, searchTitle:typing.Union[str,None], namespace:MWNamespaceInfo, pageID:int, mainRevision:MWPageRevision):
		assert isinstance(title, str)
		self.title = title

		if searchTitle is not None:
			assert isinstance(searchTitle, str)
			self.searchTitle = searchTitle
		else:
			self.searchTitle = title

		assert isinstance(namespace, MWNamespaceInfo)
		self.namespace = namespace

		assert isinstance(pageID, int)
		self.pageID = pageID

		assert isinstance(mainRevision, MWPageRevision)
		self.mainRevision = mainRevision
	#

	def _dumpVarNames(self) -> list:
		return [
			"title",
			"searchTitle",
			"namespace",
			"pageID",
			"mainRevision",
		]
	#

#








