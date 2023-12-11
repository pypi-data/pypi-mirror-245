


import typing

import jk_prettyprintobj




class MWNamespaceInfo(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, namespaceID:int, nameCanonical:str, namePublic:str, bContent:bool, bNonIncludable:bool, bAllowsSubpages:bool, nameAlias:str):
		self.namespaceID = namespaceID
		self.bContent = bContent
		self.__nameCanonical = nameCanonical
		self.namePublic = namePublic
		self.bNonIncludable = bNonIncludable
		self.bAllowsSubpages = bAllowsSubpages
		self.__nameAlias = nameAlias

		self.__names = None
		self.__rebuildNames()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def names(self) -> typing.Tuple[str]:
		return self.__names
	#

	@property
	def nameAlias(self) -> typing.Union[str,None]:
		return self.__nameAlias
	#

	@nameAlias.setter
	def nameAlias(self, value):
		self.__nameAlias = value
		self.__rebuildNames()
	#

	@property
	def nameCanonical(self) -> typing.Union[str,None]:
		return self.__nameCanonical
	#

	@nameCanonical.setter
	def nameCanonical(self, value):
		self.__nameCanonical = value
		self.__rebuildNames()
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __rebuildNames(self):
		names = [ self.namePublic ]

		if self.__nameCanonical is not None:
			if self.__nameCanonical not in names:
				names.append(self.__nameCanonical)

		if self.__nameAlias is not None:
			if self.__nameAlias not in names:
				names.append(self.__nameAlias)

		self.__names = tuple(names)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __str__(self):
		return "NameSpace<" + str(self.namespaceID) + ":" + repr(self.__nameCanonical) + ">"
	#

	def __repr__(self):
		return "NameSpace<" + str(self.namespaceID) + ":" + repr(self.__nameCanonical) + ">"
	#

	def _dumpVarNames(self) -> list:
		return [
			"namespaceID",
			"bContent",
			"nameCanonical",
			"namePublic",
			"bNonIncludable",
			"bAllowsSubpages",
			"nameAlias",
			"names",
		]
	#

#








