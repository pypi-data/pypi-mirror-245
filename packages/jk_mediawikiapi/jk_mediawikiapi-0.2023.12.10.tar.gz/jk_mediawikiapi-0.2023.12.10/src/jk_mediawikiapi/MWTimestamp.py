


import datetime
import dateutil

import jk_prettyprintobj




class MWTimestamp(jk_prettyprintobj.DumpMixin):
	# @field		str orgText				The time stamp as text as specified by the server
	# @field		datetime tDateTime		The time stamp as `datetime` after parsing

	def __init__(self, timeStampText:str):
		assert isinstance(timeStampText, str)
		self.orgText = timeStampText
		self.tDateTime = dateutil.parser.parse(timeStampText)
	#

	@property
	def asTuple(self) -> tuple:
		return self.tDateTime.timetuple()
	#

	@property
	def asTimeStamp(self) -> float:
		return self.tDateTime.timestamp()
	#

	def __str__(self):
		return str(self.tDateTime)
	#

	def __repr__(self):
		return str(self.tDateTime)
	#

	def _dumpVarNames(self) -> list:
		return [
			"orgText",
			"tDateTime",
		]
	#

#








