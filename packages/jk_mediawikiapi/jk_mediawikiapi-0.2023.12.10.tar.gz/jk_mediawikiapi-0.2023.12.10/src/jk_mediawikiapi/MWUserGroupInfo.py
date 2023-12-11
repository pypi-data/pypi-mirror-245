


import jk_prettyprintobj




class MWUserGroupInfo(jk_prettyprintobj.DumpMixin):

	def __init__(self, name:str, privileges):
		assert isinstance(name, str)
		self.name = name

		for item in privileges:
			assert isinstance(item, str)
		self.privileges = set(privileges)
	#

	def _dumpVarNames(self) -> list:
		return [
			"name",
			"privileges",
		]
	#

#








