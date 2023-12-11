from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import Schema
from ultipa.structs import DBType
from ultipa.types import ULTIPA, ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList

BOOL_KEYS = ["index", "lte"]
REPLACE_KEYS = {
	"name": "schemaName",
	"type": "propertyType",
}


class SchemaExtra(BaseExtra):

	def createSchema(self, schema: Schema,
					 requestConfig: RequestConfig = RequestConfig()):

		'''
		// create node schema
		create().node_schema("<name>", "<description>");

		// create edge schema
		create().edge_schema("<name>", "<description>");
		:return:
		'''

		command = schema.DBType == DBType.DBNODE and CommandList.createNodeSchema or CommandList.createEdgeSchema
		commandP = [f"`{schema.name}`"]
		if schema.description:
			commandP.append(schema.description)
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def listSchema(self, dbType: DBType = None, schemaName: str = None,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		return self.showSchema(dbType, schemaName, requestConfig)

	def showSchema(self, dbType: DBType = None, schemaName: str = None,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		// list all schema
		list().schema()

		// list node schema
		list().node_schema()

		// list edge schema()
		list().edge_schema()

		'''
		if dbType != None:
			if dbType == DBType.DBNODE:
				command = CommandList.showNodeSchema
			elif dbType == DBType.DBEDGE:
				command = CommandList.showEdgeSchema
			else:
				command = CommandList.showSchema

			if schemaName:
				commandP = '@' + schemaName
			else:
				commandP = ''
		else:
			command = CommandList.showSchema
			commandP = ''

		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker)
		return res

	def alterSchema(self, dbType: DBType, schemaName: str, newSchemaName: str, description: str = None,
					requestConfig: RequestConfig = RequestConfig()):
		'''
		// alter a node schema
		alter().node_schema(@<schema>).set({name:"<name>", description:"<desc>"})

		// alter an edge schema
		alter().edge_schema(@<schema>).set({name:"<name>", description:"<desc>"})
		:return:
		'''
		command = dbType == DBType.DBNODE and CommandList.alterNodeSchema or CommandList.alterEdgeSchema
		commandP = '@' + schemaName
		update_dict = {}
		if newSchemaName:
			update_dict.setdefault('name', newSchemaName)
		if description:
			update_dict.update({'description': description})
		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		uqlMaker.addParam("set", update_dict)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropSchema(self, dbType: DBType, schemaName: str,
				   requestConfig: RequestConfig = RequestConfig()):

		'''
		// drop node schema
		drop().node_schema(@<schema>)

		// drop edge schema
		drop().edge_schema(@<schema>)
		:return:
		'''
		command = dbType == DBType.DBNODE and CommandList.dropNodeSchema or CommandList.dropEdgeSchema
		commandP = '@' + schemaName

		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
