


class MWAPIException(Exception):

	def __init__(self, jsonResponse:dict):
		self.errCode = jsonResponse["error"]["code"]
		self.errMsg = jsonResponse["error"]["info"]
		s = jsonResponse["error"]["code"] + ": " + jsonResponse["error"]["info"]
		super().__init__(s)
	#

#








