

import typing

import jk_prettyprintobj

from .MWTimestamp import MWTimestamp





class MWUploadFileResult(jk_prettyprintobj.DumpMixin):

	def __init__(self, title:str, bIsNew:bool, timestamp:MWTimestamp, mimeType:str, sha1:str, size:int, width:typing.Union[int,None], height:typing.Union[int,None]):
		self.title = title
		self.timestamp = timestamp
		self.bIsNew = bIsNew
		self.mimeType = mimeType
		self.sha1 = sha1
		self.size = size
		self.width = width
		self.height = height
	#

	def __bool__(self):
		return True
	#

	def __str__(self):
		return "MWUploadFileResult(" \
			+ "title=" + repr(self.title) \
			+ ", bIsNew=" + repr(self.bIsNew) \
			+ ", timestamp=" + repr(self.timestamp) \
			+ ", mimeType=" + repr(self.mimeType) \
			+ ", sha1=" + repr(self.sha1) \
			+ ", size=" + repr(self.size) \
			+ ", width=" + repr(self.width) \
			+ ", height=" + repr(self.height) \
			+ ")"
	#

	def _dumpVarNames(self) -> list:
		return [
			"title",
			"timestamp",
			"bIsNew",
			"mimeType",
			"sha1",
			"size",
			"width",
			"height",
		]
	#

#








