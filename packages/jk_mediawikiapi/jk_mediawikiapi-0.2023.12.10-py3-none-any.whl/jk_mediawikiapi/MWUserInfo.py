


import typing

import jk_prettyprintobj

from .MWPageContent import MWPageContent
from .MWTimestamp import MWTimestamp
from .MWPageRevision import MWPageRevision
from .MWNamespaceInfo import MWNamespaceInfo




class MWUserInfo(jk_prettyprintobj.DumpMixin):

	def __init__(self,
		userID:int,
		name:str,
		groups:typing.List[str],
		implicitGroups:typing.List[str],
		tRegistration:MWTimestamp,
		rights:typing.List[str],
		nEditCount:int,
		):

		assert isinstance(userID, int)
		self.userID = userID

		assert isinstance(name, str)
		self.name = name

		assert isinstance(groups, (list, tuple))
		for x in groups:
			assert isinstance(x, str)
		self.groups = groups

		assert isinstance(implicitGroups, (list, tuple))
		for x in implicitGroups:
			assert isinstance(x, str)
		self.implicitGroups = implicitGroups

		assert isinstance(tRegistration, MWTimestamp)
		self.tRegistration = tRegistration

		assert isinstance(rights, (list, tuple))
		for x in rights:
			assert isinstance(x, str)
		self.rights = rights

		assert isinstance(nEditCount, int)
		self.nEditCount = nEditCount
	#

	def _dumpVarNames(self) -> list:
		return [
			"userID",
			"name",
			"groups",
			"implicitGroups",
			"tRegistration",
			"rights",
			"nEditCount",
		]
	#

#








