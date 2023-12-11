




class DumpMethod(object):

	def dumpLines(self) -> list:
		outputData = [
			self.__class__.__name__ + "[",
		]

		#for attrName in sorted(self.__dict__.keys()):
		for attrName in sorted(dir(self)):
			if attrName.startswith("__"):
				continue
			#attrValue = self.__dict__[attrName]
			attrValue = getattr(self, attrName)
			if callable(attrValue):
				continue

			if attrValue is not None and isinstance(attrValue, DumpMethod):
				nestedLines = attrValue.dumpLines()
				outputData.append("\t" + attrName + " = " + nestedLines[0])
				for nestedLine in nestedLines[1:]:
					outputData.append("\t" + nestedLine)
			else:
				s = "(null)" if attrValue is None else repr(attrValue)
				outputData.append("\t" + attrName + " = " + s)

		outputData.append("]")

		return outputData
	#

	def dump(self, prefix = None, printFunction = None):
		if prefix is not None:
			assert isinstance(prefix, str)
		else:
			prefix = ""
		if printFunction is not None:
			assert callable(printFunction)
		else:
			printFunction = print

		# ----

		outputData = self.dumpLines()

		# ----

		if printFunction is None:
			printFunction = print

		for line in outputData:
			printFunction(prefix + line)
	#

#








