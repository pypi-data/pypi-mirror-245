


import typing

import jk_prettyprintobj

from .MWPageContent import MWPageContent
from .MWTimestamp import MWTimestamp




class MWPageRevision(jk_prettyprintobj.DumpMixin):

	def __init__(self, revisionID:int, parentRevisionID:typing.Union[int,None], content:MWPageContent, bIsMinorRevision:bool, tags:list, timeStamp:MWTimestamp, userName:str, sha1:str, size:int):
		assert isinstance(revisionID, int)
		self.revisionID = revisionID

		if parentRevisionID is not None:
			assert isinstance(parentRevisionID, int)
		self.parentRevisionID = parentRevisionID

		if content is not None:
			assert isinstance(content, MWPageContent)
		self.content = content

		assert isinstance(bIsMinorRevision, bool)
		self.bIsMinorRevision = bIsMinorRevision

		if tags is not None:
			assert isinstance(tags, list)
		self.tags = tags

		assert isinstance(timeStamp, MWTimestamp)
		self.timeStamp = timeStamp

		assert isinstance(userName, str)
		self.userName = userName

		assert isinstance(sha1, str)
		self.sha1 = sha1

		assert isinstance(size, int)
		self.size = size
	#

	def toJSON(self) -> dict:
		ret = {
			"revisionID": self.revisionID,
			"parentRevisionID": self.parentRevisionID,
			"content": self.content.toJSON() if self.content is not None else None,
			"tags": self.tags if self.tags is not None else None,
			"timeStamp": self.timeStamp.orgText if self.timeStamp is not None else None,
			"userName": self.userName,
			"sha1": self.sha1,
			"size": self.size,
			"bIsMinorRevision": self.bIsMinorRevision,
		}
		return ret
	#

	def _dumpVarNames(self) -> list:
		return [
			"revisionID",
			"parentRevisionID",
			"content",
			"bIsMinorRevision",
			"tags",
			"timeStamp",
			"userName",
			"sha1",
			"size",
		]
	#

#








