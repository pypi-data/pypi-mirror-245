


import sys
import datetime
import pytz
import requests
import dateutil
import dateutil.parser
import typing

import bs4

import jk_furl
import jk_typing
import jk_json
import jk_version



from .MWCreatePageResult import MWCreatePageResult
from .MWNamespaceInfo import MWNamespaceInfo
from .MWUserGroupInfo import MWUserGroupInfo
from .MWExtensionInfo import MWExtensionInfo
from .MWPageContent import MWPageContent
from .MWTimestamp import MWTimestamp
from .MWPageRevision import MWPageRevision
from .MWPageInfo import MWPageInfo
from .MWPage import MWPage
from .MWCategoryInfo import MWCategoryInfo
from .MWUserInfo import MWUserInfo






class MediaWikiClient(object):

	#
	# @var		dict __siteInfo
	# @var		dict<int,MWNamespaceInfo> __namespacesByID
	# @var		dict<str,MWUserGroupInfo> __groupsByName
	#

	__EPOCH = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)

	################################################################################################################################
	#### Initialization Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, wikiURL:str, userName:str, password:str, *, bDebug:bool = False, bDisableSSLCertCheck:bool = False):
		self.__session = requests.Session()
		if bDisableSSLCertCheck:
			self.__session.verify = False

		if not wikiURL.endswith("/"):
			wikiURL += "/"
		self.__apiURL = wikiURL + "api.php"
		self.__indexURL = wikiURL + "index.php"
		self.__userName = userName
		self.__password = password

		self.__bLoggedIn = False

		# ----

		self.__performLogin(userName, password, bDebug=bDebug)
		self.__siteInfo, self.__namespacesByID, self.__groupsByName = self.__performGetSiteInfo()
		self.__namespacesByName = {}
		for n in self.__namespacesByID.values():
			for name in n.names:
				self.__namespacesByName[name] = n

		#self.__siteInfoTimeZone = pytz.timezone(self.__siteInfo["timezone"])
		#self.__siteInfoTimeOffset = self.__siteInfo["timeoffset"]
		# siteInfoTime = dateutil.parser.parse(self.__siteInfo["time"])		# returns current UTC time of server
	#

	################################################################################################################################
	#### Properties
	################################################################################################################################

	@property
	def namespaces(self) -> typing.List[MWNamespaceInfo]:
		return list(self.__namespacesByID.values())
	#

	@property
	def namespacesContent(self) -> typing.List[MWNamespaceInfo]:
		return [ n for n in self.__namespacesByID.values() if n.bContent ]
	#

	@property
	def namespaceSpecial(self) -> MWNamespaceInfo:
		return self.__namespacesByID[-1]
	#

	@property
	def namespaceMain(self) -> MWNamespaceInfo:
		return self.__namespacesByID[0]
	#

	@property
	def namespaceUser(self) -> MWNamespaceInfo:
		return self.__namespacesByID[2]
	#

	@property
	def namespaceFile(self) -> MWNamespaceInfo:
		return self.__namespacesByID[6]
	#

	@property
	def namespaceTemplate(self) -> MWNamespaceInfo:
		return self.__namespacesByID[10]
	#

	@property
	def namespaceHelp(self) -> MWNamespaceInfo:
		return self.__namespacesByID[12]
	#

	@property
	def namespaceCategory(self) -> MWNamespaceInfo:
		return self.__namespacesByID[14]
	#

	@property
	def siteInfoWriteAPIEnabled(self) -> bool:
		if self.__siteInfo:
			return not self.__siteInfo["writeapi"]
		else:
			return None
	#

	@property
	def siteInfoUploadsEnabled(self) -> bool:
		if self.__siteInfo:
			return not self.__siteInfo["uploadsenabled"]
		else:
			return None
	#

	@property
	def siteInfoReadWrite(self) -> bool:
		if self.__siteInfo:
			return not self.__siteInfo["readonly"]
		else:
			return None
	#

	@property
	def siteInfoReadOnly(self) -> bool:
		if self.__siteInfo:
			return self.__siteInfo["readonly"]
		else:
			return None
	#

	@property
	def siteInfoSiteName(self) -> str:
		if self.__siteInfo:
			return self.__siteInfo["sitename"]
		else:
			return None
	#

	@property
	def siteInfoPHPVersion(self) -> jk_version.Version:
		if self.__siteInfo:
			s = self.__siteInfo["phpversion"]
			pos = s.find("-")
			assert pos != 0
			if pos > 0:
				s = s[:pos]
			return jk_version.Version(s)
		else:
			return None
	#

	@property
	def siteInfoMaxUploadSize(self) -> int:
		if self.__siteInfo:
			return self.__siteInfo["maxuploadsize"]
		else:
			return None
	#

	@property
	def siteInfoMaxArticleSize(self) -> int:
		if self.__siteInfo:
			return self.__siteInfo["maxarticlesize"]
		else:
			return None
	#

	@property
	def siteInfoMainPage(self) -> str:
		if self.__siteInfo:
			return self.__siteInfo["mainpage"]
		else:
			return None
	#

	@property
	def siteInfoWikiVersion(self) -> jk_version.Version:
		if self.__siteInfo:
			s = self.__siteInfo["generator"]
			assert s.startswith("MediaWiki ")
			return jk_version.Version(s[10:])
		else:
			return None
	#

	################################################################################################################################
	#### Helper Methods
	################################################################################################################################

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performGetPageContentHTML(self, pageTitle:str, bDebug:bool = False) -> str:
		assert self.__bLoggedIn

		params = {
			"title": pageTitle
		}

		if bDebug:
			print("\n" + ("-" * 120) + "\n>>>> REQUEST >>>>")
			jk_json.prettyPrint(params)

		for key in list(params.keys()):
			v = params[key]
			if isinstance(v, bool):
				if v is False:
					del params[key]

		response = self.__session.get(url=self.__indexURL, params=params)

		if bDebug:
			print("\n<<<< RESPONSE <<<<")
			print("status code = ", response.status_code)
			print("content type = ", response.headers["Content-Type"])
			#print(dir(response))
			#print(repr(response.text))
			print("\n" + ("-" * 120))

		if response.status_code == 404:
			return None
		else:
			return response.text
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performGetPageContentHTMLParsed(self, pageTitle:str, bDebug:bool = False) -> bs4.BeautifulSoup:
		text = self.__performGetPageContentHTML(pageTitle, bDebug)
		if text:
			htmlContent = bs4.BeautifulSoup(text, "lxml")
			""""
			<div class="mw-parser-output">........</div>
			"""
			return htmlContent.find("div", attrs={ "class" : "mw-parser-output"})
		else:
			return None
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performGetRequest(self, params:dict, bDebug:bool = False):
		for key in list(params.keys()):
			v = params[key]
			if isinstance(v, bool):
				if v is False:
					del params[key]

		if bDebug:
			print("\n" + ("-" * 120) + "\n>>>> REQUEST >>>>")
			jk_json.prettyPrint(params)
			url = jk_furl.furl(self.__apiURL)
			url.args = params
			print(url)

		response = self.__session.get(url=self.__apiURL, params=params)
		if bDebug:
			print("\n<<<< RESPONSE <<<<")
			print("HTTP-Code: " + str(response.status_code))
			try:
				jk_json.prettyPrint(response.json())
			except:
				try:
					print(response.text())
				except:
					print(response.content)
			print("\n" + ("-" * 120))

		jsonResponse = response.json()

		return jsonResponse
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performGetMessageText(self, messageID:str, bDebug:bool = False) -> str:
		jsonResponse = self.__performGetRequest({
			"action": "query",
			"format": "json",
			"meta": "allmessages",
			"ammessages": messageID,
		}, bDebug=bDebug)

		jMsgResponse = jsonResponse["query"]["allmessages"][0]
		assert isinstance(jMsgResponse, dict)

		if "missing" in jMsgResponse:
			return None
		else:
			return jMsgResponse["*"]
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performPostRequest(self, params:dict, bDebug:bool = False):
		for key in list(params.keys()):
			v = params[key]
			if isinstance(v, bool):
				if v is False:
					del params[key]

		if bDebug:
			print("\n" + ("-" * 120) + "\n>>>> REQUEST >>>>")
			jk_json.prettyPrint(params)

		response = self.__session.post(url=self.__apiURL, data=params)
		if bDebug:
			print("\n<<<< RESPONSE <<<<")
			print("HTTP-Code: " + str(response.status_code))
			try:
				jk_json.prettyPrint(response.json())
			except:
				try:
					print(response.text())
				except:
					print(response.content)
			print("\n" + ("-" * 120))

		jsonResponse = response.json()

		return jsonResponse
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performLogin(self, userName:str, password:str, bDebug:bool = False):
		if bDebug:
			print("\n" + ("#" * 120))

		# Step 1: GET Request to fetch login token

		loginToken = self.__performGetLoginToken(bDebug=bDebug)

		# Step 2: POST Request to log in. Use of main account for login is not
		# supported. Obtain credentials via Special:BotPasswords
		# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword

		##### OLD AUTH METHOD BEGIN
		# jData = {
		# 	"action": "clientlogin",
		# 	"username": userName,
		# 	"password": password,
		# 	"logintoken": loginToken,
		# 	"rememberMe": True,
		# 	"loginreturnurl": "http://localhost",
		# 	# "pluggableauthlogin0": 1,
		# 	"format": "json",
		# }
		##### OLD AUTH METHOD END
		jData = {
			"action": "login",
			"lgname": userName,
			"lgpassword": password,
			"lgtoken": loginToken,
		 	"format": "json",
		}

		jsonResponse = self.__performPostRequest(jData, bDebug=bDebug)

		##### OLD AUTH METHOD BEGIN
		# if jsonResponse["clientlogin"]["status"] != "PASS":
		# 	raise Exception("Login failed!")
		##### OLD AUTH METHOD END
		if jsonResponse["login"].get("result", "").lower() != "success":
			raise Exception("Login failed!")

		# ----

		self.__bLoggedIn = True

		if bDebug:
			print("\n" + ("#" * 120))
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performGetSiteInfo(self, bDebug:bool = False):
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		# Step 1: GET Request to fetch login token

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"meta": "siteinfo",
			"formatversion": "2",
			"format": "json",
			"siprop": "general|namespaces|namespacealiases|usergroups"
		}, bDebug=bDebug)

		retGeneral = {}
		for keyword in [
			"dbtype", "dbversion", "generator", "maxarticlesize", "maxuploadsize", "phpversion", "sitename", "readonly",
			"time", "timeoffset", "timezone", "uploadsenabled", "writeapi", "mainpage"
		]:
			retGeneral[keyword] = jsonResponse["query"]["general"][keyword]

		retNamespaces = {}
		for jNamespace in jsonResponse["query"]["namespaces"].values():
			ns = MWNamespaceInfo(
				jNamespace["id"],
				jNamespace.get("canonical", jNamespace["name"]),
				jNamespace["name"],
				jNamespace["content"],
				jNamespace["nonincludable"],
				jNamespace["subpages"],
				None
			)
			retNamespaces[ns.namespaceID] = ns
		for jNameSpaceAlias in jsonResponse["query"]["namespacealiases"]:
			ns = retNamespaces[jNameSpaceAlias["id"]]
			ns.nameAlias = jNameSpaceAlias["alias"]


		retUserGroups = {}
		for jUserGroup in jsonResponse["query"]["usergroups"]:
			ug = MWUserGroupInfo(
				jUserGroup["name"],
				jUserGroup["rights"],
			)
			retUserGroups[ug.name] = ug

		if bDebug:
			print("\n" + ("#" * 120))

		return retGeneral, retNamespaces, retUserGroups
	#

	#
	# Perform a query and iterate over the result.
	#
	# @param		str listCommand		The command to use for the MediaWiki "list" parameter.
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __queryIterate(self, listCommand:str, bDebug:bool = False, **kwargs):
		assert isinstance(listCommand, str)
		availableCommands = {
			"allpages": [
				"ap",
				{
				},
			],
			"allcategories": [
				"ac",
				{
					"acprop": "size|hidden",
				},
			],
			"allusers": [
				"au",
				{
					"auprop": "blockinfo|groups|implicitgroups|rights|editcount|registration|centralids"
				},
			]
		}
		assert listCommand in availableCommands
		prefix, jsonArgs = availableCommands[listCommand]
		jsonArgs.update(kwargs)

		accontinue = None

		while True:
			jsonRequest = {
				"action": "query",
				"format": "json",
				"list": listCommand,
				prefix + "dir": "ascending",
				prefix + "limit": "max",
			}
			jsonRequest.update(jsonArgs)
			if accontinue:
				jsonRequest[prefix + "continue"] = accontinue

			jsonResponse = self.__performGetRequest(jsonRequest, bDebug=bDebug)

			"""
			{
				"batchcomplete": "",
				"continue": {
						"accontinue": "Anwendungssoftware",
						"continue": "-||"
				},
				"query": {
						"allcategories": [
							....
						]
					}
				}
			}
			"""

			for item in jsonResponse["query"][listCommand]:
				yield item

			if "continue" in jsonResponse:
				accontinue = jsonResponse["continue"][prefix + "continue"]
			else:
				break
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def ____performGetToken(self, tokenType:str, bDebug:bool = False) -> str:
		assert isinstance(tokenType, str)
		assert tokenType in [ "login", "csrf", "createaccount", "patrol", "rollback", "userrights", "watch" ]

		if tokenType != "login":
			assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"meta": "tokens",
			"type": tokenType,
			"format": "json"
		}, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		return jsonResponse["query"]["tokens"][tokenType + "token"]
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performGetCSRFToken(self, bDebug:bool = False) -> str:
		return self.____performGetToken("csrf", bDebug=bDebug)
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performGetLoginToken(self, bDebug:bool = False) -> str:
		return self.____performGetToken("login", bDebug=bDebug)
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performGetCreateAccountToken(self, bDebug:bool = False) -> str:
		return self.____performGetToken("createaccount", bDebug=bDebug)
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __performGetUserRightsToken(self, bDebug:bool = False) -> str:
		return self.____performGetToken("userrights", bDebug=bDebug)
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __validatePassword(self, userName:str, password:str, bDebug:bool = False) -> bool:
		assert self.__bLoggedIn

		# ----

		jsonRequest = {
			"action": "validatepassword",
			"format": "json",
			"user": userName,
			"password": password,
			"email": "example@example.com",
			"realname": "Manfred Mustermann",
		}

		jsonResponse = self.__performPostRequest(jsonRequest, bDebug=bDebug)

		return jsonResponse["validatepassword"]["validity"] in [ "Good", "Change" ]
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __getVerifyUser(self, user:typing.Union[str,MWUserInfo], bDebug:bool = False) -> MWUserInfo:
		assert self.__bLoggedIn

		# ----

		if isinstance(user, str):
			assert user
			userName = user
			userInfo = self.getUserInfo(userName, bDebug=bDebug)
			if not userInfo:
				raise Exception("No such user: " + repr(userName))
			return userInfo
		elif isinstance(user, MWUserInfo):
			userName = user.name
			userInfo = user
			return userInfo
		else:
			raise Exception("Invalid value specified for argument 'user':" + repr(user))
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def __getVerifyUserGroup(self, group:typing.Union[str,MWUserGroupInfo], bDebug:bool = False) -> MWUserGroupInfo:
		assert self.__bLoggedIn

		# ----

		if isinstance(group, str):
			assert group
			if group not in self.__groupsByName:
				raise Exception("No such group: " + repr(group))
			return self.__groupsByName[group]
		elif isinstance(group, MWUserGroupInfo):
			return group
		else:
			raise Exception("Invalid value specified for argument 'group':" + repr(group))
	#

	################################################################################################################################
	#### Public Methods
	################################################################################################################################

	#
	# @return		MWExtensionInfo[]		Returns a list of MWExtensionInfo objects
	#
	def listExtensions(self, bDebug:bool = False) -> list:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"meta": "siteinfo",
			"formatversion": "2",
			"format": "json",
			"siprop": "extensions"
		}, bDebug=bDebug)

		ret = []
		for jExtension in jsonResponse["query"]["extensions"]:
			if "description" in jExtension:
				description = jExtension["description"]
			elif "descriptionmsg" in jExtension:
				description = self.__performGetMessageText(jExtension["descriptionmsg"], bDebug=bDebug)
			else:
				description = None

			ei = MWExtensionInfo(
				jExtension["name"],
				jExtension["type"],
				jExtension["author"],
				jExtension.get("license-name"),
				jExtension["url"],
				jExtension.get("version"),
				description,
			)
			ret.append(ei)

		if bDebug:
			print("\n" + ("#" * 120))

		return ret
	#

	def getPageInfo(self, pageTitle:str, bDebug:bool = False) -> typing.Union[MWPageInfo,None]:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"format": "json",
			"titles": pageTitle,
			"prop": "info|categories|categoryinfo|pageprops|revisions",
			"intestactions": "read",
			"inprop": "url|displaytitle|talkid|protection",
			"rvprop": "ids|timestamp|flags|user|userid|size|slotsize|sha1|slotsha1|contentmodel|comment|tags|roles",
			"formatversion": 2,
		}, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		if "-1" in jsonResponse["query"]["pages"]:
			return None
		else:
			if "normalized" in jsonResponse["query"]:
				_pageTitle = jsonResponse["query"]["normalized"][0]["to"]
				_searchTitle = jsonResponse["query"]["normalized"][0]["from"]
			else:
				_pageTitle = pageTitle
				_searchTitle = pageTitle

			r = jsonResponse["query"]["pages"]
			jPageInfo = r[0]
			jRevision = jPageInfo["revisions"][0]

			return MWPageInfo(
				title=_pageTitle,
				searchTitle=_searchTitle,
				namespace=self.__namespacesByID[jPageInfo["ns"]],
				pageID=jPageInfo["pageid"],
				mainRevision=MWPageRevision(
					revisionID=jRevision["revid"],
					parentRevisionID=jRevision.get("parentid"),
					content=None,
					bIsMinorRevision="minor" in jRevision and jRevision["minor"],
					timeStamp=MWTimestamp(jRevision["timestamp"]),
					userName=jRevision["user"],
					tags=None,
					sha1=jRevision["sha1"],
					size=jRevision["size"]
				)
			)
	#

	#
	# @param		int[]|str[]|MWNamespaceInfo[]	(optional) The namespaces to query for pages
	# @param		bool bDebug						(optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#												printed containing information about the direct low level communication with the server.
	#												The default value is <c>False</c>.
	#
	def listPages(self, namespaces:typing.Union[typing.List[typing.Union[str,int,MWNamespaceInfo]],typing.Tuple[typing.Union[str,int,MWNamespaceInfo]],None] = None, bDebug:bool = False) -> typing.Iterator[MWPageInfo]:
		if namespaces is not None:
			tempList = []
			for x in namespaces:
				if isinstance(x, str):
					tempList.append(self.__namespacesByName[x])
				elif isinstance(x, int):
					tempList.append(self.__namespacesByID[x])
				elif isinstance(x, MWNamespaceInfo):
					tempList.append(x)
			namespaces = tempList
		else:
			namespaces = [ self.__namespacesByID[0] ]

		# ----

		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		for namespace in namespaces:
			if bDebug:
				print("Now listing pages from namespace:")
				namespace.dump()

			extraArgs = {
				"apnamespace": namespace.namespaceID
			}

			for jPageInfo in self.__queryIterate("allpages", bDebug=bDebug, **extraArgs):
				yield MWPageInfo(
					title = jPageInfo["title"],
					searchTitle = None,
					namespace = self.__namespacesByID[jPageInfo["ns"]],
					pageID = jPageInfo["pageid"],
					mainRevision = None,
				)

		if bDebug:
			print("\n" + ("#" * 120))
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def listCategories(self, bDebug:bool = False) -> typing.Iterator[MWCategoryInfo]:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		for jCategoryInfo in self.__queryIterate("allcategories", bDebug=bDebug):
			yield MWCategoryInfo(
				name = jCategoryInfo["*"],
				nPages = jCategoryInfo["pages"],
				nTotalPages = jCategoryInfo["size"],
				nSubCategories = jCategoryInfo["subcats"],
			)

		if bDebug:
			print("\n" + ("#" * 120))
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def logout(self, bDebug:bool = False):
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		csrfToken = self.__performGetCSRFToken(bDebug=bDebug)

		jsonResponse = self.__performGetRequest({
			"action": "logout",
			"token": csrfToken,
			"format": "json"
		}, bDebug=bDebug)

		self.__bLoggedIn = False

		if bDebug:
			print("\n" + ("#" * 120))
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def getPageContent(self, pageTitle:str, bDebug:bool = False) -> MWPage:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"format": "json",
			"titles": pageTitle,
			"prop": "revisions",
			"rvslots": "*",
			"rvprop": "content|ids|timestamp|flags|user|userid|size|slotsize|sha1|slotsha1|contentmodel|comment|tags|roles",
			"formatversion": 2,
			"rvlimit": 1,
		}, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		jPage = jsonResponse["query"]["pages"][0]
		if "revisions" not in jPage:
			return None

		if "normalized" in jsonResponse["query"]:
			_pageTitle = jsonResponse["query"]["normalized"][0]["to"]
			_searchTitle = jsonResponse["query"]["normalized"][0]["from"]
		else:
			_pageTitle = pageTitle
			_searchTitle = pageTitle

		jRevision = jPage["revisions"][0]
		ret = MWPage(
			title=_pageTitle,
			searchTitle=_searchTitle,
			namespace=self.__namespacesByID[jPage["ns"]],
			pageID=jPage["pageid"],
			mainRevision=MWPageRevision(
				revisionID=jRevision["revid"],
				parentRevisionID=jRevision.get("parentid"),
				content=MWPageContent(
					content=jRevision["slots"]["main"]["content"],
					contentformat=jRevision["slots"]["main"]["contentformat"],
					contentmodel=jRevision["slots"]["main"]["contentmodel"],
					sha1=jRevision["slots"]["main"]["sha1"],
					size=jRevision["slots"]["main"]["size"]
				),
				bIsMinorRevision="minor" in jRevision and jRevision["minor"],
				timeStamp=MWTimestamp(jRevision["timestamp"]),
				userName=jRevision["user"],
				tags=jRevision["tags"],
				sha1=jRevision["sha1"],
				size=jRevision["size"]
			)
		)

		return ret
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def getPageContentHTML(self, pageTitle:str, bDebug:bool = False) -> str:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		ret = self.__performGetPageContentHTML(pageTitle, bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		return ret
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def getPageContentHTMLParsed(self, pageTitle:str, bDebug:bool = False) -> bs4.BeautifulSoup:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		ret = self.__performGetPageContentHTMLParsed(pageTitle, bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		return ret
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def uploadPageContent(self,
		pageID:typing.Union[int,None],
		pageTitle:typing.Union[str,None],
		pageContent:str,
		summary:str = "",
		bIsMinor:bool = True,
		bIsBot:bool = False,
		bDontEditIfExists:bool = False,
		bDontEditIfNotExists:bool = False,
		bDebug:bool = False) -> typing.Union[MWCreatePageResult,None]:

		if pageID is not None:
			assert isinstance(pageID, int)
			assert pageTitle is None
		else:
			assert isinstance(pageTitle, str)
			assert pageTitle

		assert isinstance(pageContent, str)
		assert pageContent

		assert isinstance(summary, str)

		assert isinstance(bIsMinor, bool)

		assert isinstance(bDontEditIfExists, bool)

		assert isinstance(bDontEditIfNotExists, bool)

		# ----

		assert self.__bLoggedIn

		# ----

		if bDebug:
			print("\n" + ("#" * 120))

		csrfToken = self.__performGetCSRFToken(bDebug = bDebug)

		jsonRequest = {
			"action": "edit",
			"format": "json",
			"text": pageContent,
			"summary": summary,
			"minor": bIsMinor,
			"bot": bIsBot,
			"recreate": True,
			"createonly": bDontEditIfExists,
			"nocreate": bDontEditIfNotExists,
			"contentformat": "text/x-wiki",
			"contentmodel": "wikitext",
			"token": csrfToken,
		}
		if pageID is not None:
			jsonRequest["pageid"] = pageID
		else:
			jsonRequest["title"] = pageTitle

		jsonResponse = self.__performPostRequest(jsonRequest, bDebug=bDebug)

		jEdit = jsonResponse["edit"]
		if jEdit["result"] == "Success":
			if "nochange" in jEdit:
				# no change
				pageID = jEdit["pageid"]
				ret = MWCreatePageResult(pageTitle, pageID, None, False, None)
			else:
				# create or edit has been performed
				bIsNew = "new" in jEdit
				revID = jEdit["newrevid"]
				timestamp = MWTimestamp(jEdit["newtimestamp"])
				pageID = jEdit["pageid"]
				oldRevID = jEdit.get("oldrevid")
				ret = MWCreatePageResult(pageTitle, pageID, oldRevID, bIsNew, timestamp)
		else:
			ret = None

		if bDebug:
			print("\n" + ("#" * 120))

		return ret
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def listUsers(self, bDebug:bool = False) -> typing.Iterator[MWUserInfo]:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		for jUserInfo in self.__queryIterate("allusers", bDebug=bDebug):
			yield MWUserInfo(
				userID = jUserInfo["userid"],
				name = jUserInfo["name"],
				groups = jUserInfo["groups"],
				implicitGroups = jUserInfo["implicitgroups"],
				tRegistration = MWTimestamp(jUserInfo["registration"]),
				rights = jUserInfo["rights"],
				nEditCount = jUserInfo["editcount"],
			)

		if bDebug:
			print("\n" + ("#" * 120))
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def getUserInfo(self, userName:str, bDebug:bool = False) -> typing.Union[MWUserInfo,None]:
		assert isinstance(userName, str)

		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		userInfo = None
		for jUserInfo in self.__queryIterate("allusers", bDebug=bDebug):
			if jUserInfo["name"].lower() == userName.lower():
				userInfo = MWUserInfo(
					userID = jUserInfo["userid"],
					name = jUserInfo["name"],
					groups = jUserInfo["groups"],
					implicitGroups = jUserInfo["implicitgroups"],
					tRegistration = MWTimestamp(jUserInfo["registration"]),
					rights = jUserInfo["rights"],
					nEditCount = jUserInfo["editcount"],
				)
				break

		if bDebug:
			print("\n" + ("#" * 120))

		return userInfo
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def createUser(self, userName:str, password:str, bDebug:bool = False) -> MWUserInfo:
		assert isinstance(userName, str)
		assert userName

		assert isinstance(password, str)
		assert password

		# ----

		assert self.__bLoggedIn

		# ----

		for userInfo in self.listUsers(bDebug):
			if userInfo.name.lower() == userName.lower():
				raise Exception("User already exists: " + repr(userName))

		# ----

		if bDebug:
			print("\n" + ("#" * 120))

		bPwdIsValid = self.__validatePassword(userName, password, bDebug=bDebug)
		if not bPwdIsValid:
			if bDebug:
				print("\n" + ("#" * 120))

			raise Exception("The password specified is not usable!")

		token = self.__performGetCreateAccountToken(bDebug)

		jsonRequest = {
			"action": "createaccount",
			"format": "json",
			"createtoken": token,
			"username": userName,
			"password": password,
			"retype": password,
			"createreturnurl": "http://localhost",
		}

		jsonResponse = self.__performPostRequest(jsonRequest, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		if jsonResponse["createaccount"]["status"] == "PASS":
			return self.getUserInfo(userName)
		elif jsonResponse["createaccount"]["status"] == "FAIL":
			raise Exception("Creating user " + repr(userName) + " failed! Reason: " + jsonResponse["createaccount"]["messagecode"])
		else:
			raise Exception("Creating user " + repr(userName) + " failed!")
	#

	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	#
	def validatePassword(self, userName:str, password:str, bDebug:bool = False) -> bool:
		assert isinstance(userName, str)
		assert userName

		assert isinstance(password, str)
		assert password

		# ----

		assert self.__bLoggedIn

		# ----

		if bDebug:
			print("\n" + ("#" * 120))

		ret = self.__validatePassword(userName, password, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		return ret
	#

	#
	# Adds an (existing) user to an (existing) group. This method is indempotent.
	# On error an exception is raised.
	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	# @return		bool				Returns <c>True</c> if the user has not yet been in the specified group. Returns <c>False</c> if the user already is in that group.
	#
	def addUserToGroup(self, user:typing.Union[str,MWUserInfo], group:typing.Union[str,MWUserGroupInfo], bDebug:bool = False) -> bool:
		assert self.__bLoggedIn

		# ----

		if bDebug:
			print("\n" + ("#" * 120))

		# ----

		userInfo = self.__getVerifyUser(user, bDebug=bDebug)
		userName = userInfo.name

		groupInfo = self.__getVerifyUserGroup(group, bDebug=bDebug)
		groupName = groupInfo.name

		# ----

		token = self.__performGetUserRightsToken(bDebug)

		jsonRequest = {
			"action": "userrights",
			"format": "json",
			"userid": userInfo.userID,
			"add": groupName,
			"expiry": "never",
			"token": token,
		}

		jsonResponse = self.__performPostRequest(jsonRequest, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		return groupName in jsonResponse["userrights"]["added"]
	#

	#
	# Removes an (existing) user from an (existing) group. This method is indempotent.
	# On error an exception is raised.
	#
	# @param		bool bDebug			(Optional) Specify <c>True</c> or <c>False</c> to enable or disable debugging. If debugging is enabled, text messages are
	#									printed containing information about the direct low level communication with the server.
	#									The default value is <c>False</c>.
	# @return		bool				Returns <c>True</c> if the user has not yet been in the specified group. Returns <c>False</c> if the user already is in that group.
	#
	def removeUserFromGroup(self, user:typing.Union[str,MWUserInfo], group:typing.Union[str,MWUserGroupInfo], bDebug:bool = False) -> bool:
		assert self.__bLoggedIn

		# ----

		if bDebug:
			print("\n" + ("#" * 120))

		# ----

		userInfo = self.__getVerifyUser(user, bDebug=bDebug)
		userName = userInfo.name

		groupInfo = self.__getVerifyUserGroup(group, bDebug=bDebug)
		groupName = groupInfo.name

		# ----

		token = self.__performGetUserRightsToken(bDebug)

		jsonRequest = {
			"action": "userrights",
			"format": "json",
			"userid": userInfo.userID,
			"remove": groupName,
			"expiry": "never",
			"token": token,
		}

		jsonResponse = self.__performPostRequest(jsonRequest, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		return groupName in jsonResponse["userrights"]["removed"]
	#

#














