


import typing

import jk_prettyprintobj

from .MWPageContent import MWPageContent
from .MWTimestamp import MWTimestamp
from .MWPageRevision import MWPageRevision
from .MWNamespaceInfo import MWNamespaceInfo




class MWPageInfo(jk_prettyprintobj.DumpMixin):

	def __init__(self,
		title:str,
		searchTitle:typing.Union[str,None],
		namespace:MWNamespaceInfo,
		pageID:int,
		#protections:list,
		mainRevision:MWPageRevision,
		):

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

		if mainRevision is not None:
			assert isinstance(mainRevision, MWPageRevision)
		self.mainRevision = mainRevision
	#

	@property
	def fullQualifiedName(self) -> str:
		if self.namespace:
			if self.namespace.nameCanonical:
				return self.namespace.nameCanonical + ":" + self.title
			else:
				return self.title
		else:
			return self.title
	#

	def __str__(self):
		s = "MWPageInfo(" \
			+ "pageID=" + str(self.pageID)
		if self.namespace is not None:
			s += ", namespace=" + repr(self.namespace.nameCanonical)
		s += ", title=" + repr(self.title)
		if self.mainRevision is not None:
			s += ", mainRevision=" + str(self.mainRevision.revisionID)
		s += ")"
		return s
	#

	def _dumpVarNames(self) -> list:
		return [
			"title",
			"namespace",
			"pageID",
			"mainRevision",
		]
	#

#








