from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import DBType
from ultipa.structs.Property import Property
from ultipa.types import ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.propertyUtils import getPropertyTypesDesc

BOOL_KEYS = ["index", "lte"]
REPLACE_KEYS = {
	"name": "propertyName",
	"type": "propertyType",
}


class PropertyExtra(BaseExtra):

	def listProperty(self, requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListProperty:
		return self.showProperty(requestConfig)

	def showProperty(self, requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListProperty:
		command = CommandList.showProperty
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(boolKeys=BOOL_KEYS),
								 isSingleOne=False)
		return res

	def getProperty(self, dbType: DBType, schema: str = None,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseGetProperty:
		if dbType != None:
			if dbType == DBType.DBNODE:
				command = CommandList.showNodeProperty
			elif dbType == DBType.DBEDGE:
				command = CommandList.showEdgeProperty
			else:
				command = CommandList.showNodeProperty
			if schema:
				commandp = ['@' + f"`{schema}`"]
			else:
				commandp = ''
		else:
			command = CommandList.showNodeProperty
			commandp = ''

		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandp)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS, boolKeys=BOOL_KEYS),
								 isSingleOne=False)
		return res

	def createProperty(self, dbType: DBType, schemaName: str, prop: Property,
					   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		command = dbType == DBType.DBNODE and CommandList.createNodeProperty or CommandList.createEdgeProperty
		commandP = ["@" + f"`{schemaName}`", f"`{prop.name}`",
					getPropertyTypesDesc(prop.type, prop.subTypes)]

		if prop.description:
			commandP.append(prop.description)
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker)
		return res

	def dropProperty(self, dbType: DBType, schema: str, property: str,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		command = dbType == DBType.DBNODE and CommandList.dropNodeProperty or CommandList.dropEdgeProperty
		commandP = "@`%s`.`%s`" % (schema, property)
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker)
		return res

	def alterProperty(self, dbType: DBType, schema: str, property: str, newProperty: str = None,
					  description: str = None,
					  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		command = dbType == DBType.DBNODE and CommandList.alterNodeProperty or CommandList.alterEdgeProperty
		commandP = "@`%s`.`%s`" % (schema, property)
		update_dict = {}
		if newProperty:
			update_dict.setdefault('name', newProperty)
		if description:
			update_dict.update({'description': description})
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP)
		uqlMaker.addParam("set", update_dict)
		res = self.uqlSingle(uqlMaker)
		return res
