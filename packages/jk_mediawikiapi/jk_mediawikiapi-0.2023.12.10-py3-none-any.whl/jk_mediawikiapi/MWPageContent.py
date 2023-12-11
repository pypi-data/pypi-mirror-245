


import jk_prettyprintobj




class MWPageContent(jk_prettyprintobj.DumpMixin):

	def __init__(self, content:str, contentformat:str, contentmodel:str, sha1:str, size:int):
		assert isinstance(content, str)
		self.content = content

		assert isinstance(contentformat, str)
		self.contentformat = contentformat

		assert isinstance(contentmodel, str)
		self.contentmodel = contentmodel

		assert isinstance(sha1, str)
		self.sha1 = sha1

		assert isinstance(size, int)
		self.size = size
	#

	def toJSON(self) -> dict:
		ret = {
			"content": self.content,
			"contentformat": self.contentformat,
			"contentmodel": self.contentmodel,
			"sha1": self.sha1,
			"size": self.size,
		}
		return ret
	#

	def _dumpVarNames(self) -> list:
		return [
			"content",
			"contentformat",
			"contentmodel",
			"sha1",
			"size",
		]
	#

#








