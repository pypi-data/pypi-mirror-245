from ultipa.structs import DBType
from ultipa.structs.InsertType import InsertType
from ultipa.structs.Schema import Schema
from ultipa.types import ULTIPA
from ultipa.types.types import OrderType, UltipaEquation
from ultipa.utils import common as COMMON
from ultipa.utils.ufilter import ufilter as FILTER
from ultipa.utils.ufilter.new_ufilter import *


class OrderBy:
	def __init__(self, schemaName: str, propertyName: str, orderType: OrderType):
		self.schemaName = '@' + schemaName
		self.propertyName = propertyName
		self.orderType = orderType.value

	@property
	def toString(self):
		return "%s.%s %s" % (self.schemaName, self.propertyName, self.orderType)


class GroupBy:
	def __init__(self, schemaName: str, propertyName: str):
		self.schemaName = '@' + schemaName
		self.propertyName = propertyName

	@property
	def toString(self):
		return "%s.%s" % (self.schemaName, self.propertyName)


class CommonSchema:
	def __init__(self, schema: str, property: str):
		self.schemaName = '@' + schema
		self.propertyName = property

	@property
	def toString(self):
		return "%s.%s" % (self.schemaName, self.propertyName)


class UltipaPath:
	def __init__(self, nodeSchema: List[CommonSchema], edgeSchema: List[CommonSchema]):
		self.nodeSchema = nodeSchema
		self.edgeSchema = edgeSchema

	@property
	def toString(self):
		if self.nodeSchema == '*':
			nodeSchema = '*'
		else:
			nodeSchema = ','.join([i.toString for i in self.nodeSchema])

		if self.edgeSchema == '*':
			edgeSchema = '*'
		else:
			edgeSchema = ','.join([i.toString for i in self.edgeSchema])

		return "{%s}{%s}" % (nodeSchema, edgeSchema)


class UltipaReturn:
	def __init__(self, schemaName: str, propertyName: str, equation: UltipaEquation = None, alias: List[str] = None,
				 path: UltipaPath = None):
		self.schemaName = '@' + schemaName
		self.propertyName = propertyName
		self.equation = equation
		self.alias = alias
		self.path = path

	@property
	def toString(self):
		if self.path:
			return "path%s" % (self.path.toString)
		if self.alias and self.propertyName and not self.schemaName and not self.equation:
			return "%s{%s}" % (self.alias, ','.join(self.propertyName))

		if self.equation and self.alias:
			return "%s(%s.%s) as %s" % (self.equation.value, self.schemaName, self.propertyName, self.alias)
		return "{%s.%s}" % (self.schemaName, self.propertyName)


class Return:
	def __init__(self, alias: str, propertys: List[str] = None, allProperties: bool = False, limit: int = COMMON.LIMIT):
		if propertys is None:
			propertys = []
		self.aliasName = alias
		self.propertys = propertys
		self.all = allProperties
		self.limit = limit

	@property
	def toString(self):
		if self.all:
			return "%s{%s} limit %s" % (self.aliasName, "*", self.limit)
		if len(self.propertys) == 1:
			return "%s.%s limit %s" % (self.aliasName, self.propertys[0], self.limit)
		else:
			return "%s{%s} limit %s" % (self.aliasName, ','.join(self.propertys), self.limit)




class CreateUser:
	def __init__(self, username: str, password: str, graphPrivileges: [dict] = None,
				 systemPrivileges: List[str] = None, policies: List[str] = None):
		self.username = username
		self.password = password
		self.graph_privileges = graphPrivileges
		self.system_privileges = systemPrivileges
		self.policies = policies

class AlterUser(CreateUser):
	def __init__(self, username: str, password: str = None, graph_privileges: [dict] = None,
				 system_privileges: List[str] = None, policies: List[str] = None):
		super().__init__(username, password, graph_privileges, system_privileges, policies)


class GetUserSetting:
	def __init__(self, username: str, type: str):
		self.username = username
		self.type = type


class SetUserSetting:
	def __init__(self, username: str, type: str, data: str):
		self.username = username
		self.type = type
		self.data = data


class ShowTask:
	def __init__(self, id: int = None, name: str = None, limit: int = None, status: str = ''):
		self.id = id
		self.limit = limit
		self.name = name
		self.status = status


class ClearTask:
	def __init__(self, id: int = None, name: str = None, status: str = None, all: bool = False):
		self.id = id
		self.name = name
		self.status = status
		self.all = all


class InsertNodeBulk:
	def __init__(self, schema: str, rows: List[dict], insertType: InsertType, silent: bool = False,
				 batch: bool = False, n: int = 100, timeZone=None, timeZoneOffset=None):
		self.schema = schema
		self.rows = rows
		self.silent = silent
		self.insertType = insertType
		self.batch = batch
		self.n = n
		self.timeZone = timeZone
		self.timeZoneOffset = timeZoneOffset


class InsertEdgeBulk:
	def __init__(self, schema: str, rows: List[dict], insertType: InsertType, silent: bool = False,
				 create_node_if_not_exist: bool = False, batch: bool = False, n: int = 100, timeZone=None,
				 timeZoneOffset=None):
		self.schema = schema
		self.rows = rows
		self.silent = silent
		self.create_node_if_not_exist = create_node_if_not_exist
		self.insertType = insertType
		self.batch = batch
		self.n = n
		self.timeZone = timeZone
		self.timeZoneOffset = timeZoneOffset


class InsertNode:
	def __init__(self, nodes: List[dict], schema: str, overwrite: bool = False, upsert: bool = False,
				 isReturnID: bool = True):
		self.nodes = nodes
		self.schemaName = '@' + schema
		self.overwrite = overwrite
		self.upsert = upsert
		self.isReturnID = isReturnID

	def setSchema(self, schema: str):
		self.schemaName = '@' + schema


class InsertEdge:
	def __init__(self, edges: List[dict], schema: str, overwrite: bool = False, upsert: bool = False,
				 isReturnID: bool = True):
		self.edges = edges
		self.schemaName = '@' + schema
		self.overwrite = overwrite
		self.upsert = upsert
		self.isReturnID = isReturnID

	def setSchema(self, schema: str):
		self.schemaName = '@' + schema


class SearchNode:
	def __init__(self, select: Return, id=None,
				 filter: UltipaFilter or list or str = None):
		if id is None:
			id = []
		self.id = id
		self.filter = filter
		self.select = select


class SearchEdge(SearchNode):
	pass


class UpdateNode:
	def __init__(self, values: dict, uuid: [int] = None, filter: UltipaFilter = None, silent: bool = False):
		if uuid is None:
			uuid = []
		self.id = uuid
		self.filter = filter
		self.values = values
		self.silent = silent


class UpdateEdge(UpdateNode):
	pass


class DeleteNode:
	def __init__(self, uuid: [int] = None, filter: UltipaFilter = None, silent: bool = False):
		if uuid is None:
			uuid = []
		self.id = uuid
		self.filter = filter
		self.silent = silent


class DeleteEdge(DeleteNode):
	pass



class AlterGraph:
	def __init__(self, oldGraphName: str, newGraphName: str, newDescription: str = None):
		self.oldGraphName = oldGraphName
		self.newGraphName = newGraphName
		self.newDescription = newDescription


class LTE:

	def __init__(self, schemaName: CommonSchema, type: DBType):
		'''LTE UFE Node and Edge property'''
		self.schemaName = schemaName
		self.type = type


class UFE(LTE):
	...


# class Property:
# 	def __init__(self, type: DBType, name: str = ''):
# 		self.type = type
# 		self.name = name



class Index(CommonSchema):
	def __init__(self, type: DBType, schema: str, property: str):
		super().__init__(schema=schema, property=property)
		self.DBtype = type


class ShowIndex():
	def __init__(self, type: DBType):
		self.DBtype = type


class ShowFulltext(ShowIndex):
	def __init__(self, type: DBType):
		super().__init__(type=type)


class CreateIndex(Index):
	def __init__(self, type: DBType, schema: str, property: str):
		super().__init__(type, schema, property)


class CreateFulltext(Index):
	def __init__(self, type: DBType, schema: str, property: str, name: str):
		super().__init__(type, schema, property)
		self.name = name


class DropIndex(Index):
	def __init__(self, type: DBType, schema: str, property: str):
		super().__init__(type, schema, property)


class DropFulltext:
	def __init__(self, type: DBType, name: str = ""):
		self.fulltextName = name
		self.DBtype = type



class SearchAB:
	def __init__(self, src: int = None, dest: int = None, depth: int = COMMON.DEPTH, limit: int = COMMON.LIMIT,
				 select: List[str] = None,
				 select_node_properties: List[str] = None, select_edge_properties: List[str] = None,
				 shortest: bool = False, nodeFilter: dict = None,
				 edgeFilter: dict = None, path_ascend: str = '', path_descend: str = '',
				 direction: ULTIPA.DirectionType = None, turbo: bool = False, osrc: str = '',
				 odest: str = '', no_circle: bool = False, boost: bool = False):
		self.src = src
		self.dest = dest
		self.depth = depth
		self.shortest = shortest
		self.node_filter = nodeFilter
		self.edge_filter = edgeFilter
		self.path_ascend = path_ascend
		self.path_descend = path_descend
		self.direction = direction
		self.no_circle = no_circle


class Searchkhop:
	def __init__(self, src: int = None, depth: int = COMMON.DEPTH, limit: int = COMMON.LIMIT,
				 select: List[str] = None, select_node_properties: List[str] = None,
				 select_edge_properties: List[str] = None,
				 node_filter: dict = None, edge_filter: dict = None, direction: ULTIPA.DirectionType = None,
				 turbo: bool = False, osrc: str = ''):
		self.src = src
		self.depth = depth
		self.limit = limit
		self.select = select
		self.select_node_properties = select_node_properties
		self.select_edge_properties = select_edge_properties
		self.node_filter = node_filter
		self.edge_filter = edge_filter
		self.direction = direction
		self.turbo = turbo
		self.osrc = osrc


class Download:
	def __init__(self, fileName: str, taskId: str, savePath: str = None):
		self.fileName = fileName
		self.taskId = taskId
		self.savePath = savePath


class Policy:

	def __init__(self, name: str, graphPrivileges: dict = None, systemPrivileges: List[str] = None,
				 policies: List[str] = None):
		self.name = name
		self.graph_privileges = graphPrivileges
		self.system_privileges = systemPrivileges
		self.policies = policies


class CreatePolicy(Policy):
	pass


class AlterPolicy(Policy):
	pass


class GetPolicy:
	def __init__(self, name: str):
		self.name = name


class DropPolicy(GetPolicy):
	pass


class GrantPolicy:
	def __init__(self, username: str = '', graphPrivileges: dict = None,
				 systemPrivileges: List[str] = None, policies: List[str] = None):
		self.username = username
		self.graph_privileges = graphPrivileges
		self.system_privileges = systemPrivileges
		self.policies = policies


class RevokePolicy(GrantPolicy):
	pass


class NodeSpread:
	def __init__(self, src: int = None, depth: int = COMMON.DEPTH, limit: int = COMMON.LIMIT,
				 select: List[str] = None, selectNodeProperties: List[str] = None,
				 selectEdgeProperties: List[str] = None, nodeFilter: FILTER = None, edgeFilter: FILTER = None,
				 spread_type: str = None,
				 direction: ULTIPA.DirectionType = None, osrc: str = None):
		self.src = src
		self.depth = depth
		self.limit = limit
		self.select = select
		self.select_node_properties = selectNodeProperties
		self.select_edge_properties = selectEdgeProperties
		self.node_filter = nodeFilter
		self.edge_filter = edgeFilter
		self.spread_type = spread_type
		self.direction = direction
		self.osrc = osrc


class AutoNet:
	def __init__(self, srcs: List[int], dests: List[int] = None, depth: int = COMMON.DEPTH,
				 limit: int = COMMON.LIMIT,
				 select: List[str] = None, selectNodeProperties: List[str] = None,
				 selectEdgeProperties: List[str] = None,
				 shortest: bool = False, nodeFilter: FILTER = None, edgeFilter: FILTER = None,
				 turbo: bool = False, noCircle: bool = False, boost: bool = False):
		self.srcs = srcs
		self.dests = dests
		self.depth = depth
		self.limit = limit
		self.select = select
		self.select_node_properties = selectNodeProperties
		self.select_edge_properties = selectEdgeProperties
		self.shortest = shortest
		self.node_filter = nodeFilter
		self.edge_filter = edgeFilter
		self.turbo = turbo
		self.no_circle = noCircle
		self.boost = boost


class Export:
	def __init__(self, type: DBType, limit: int, schema: str, properties: List[str] = None):
		self.type = type
		self.limit = limit
		self.properties = properties
		self.schema = schema


class TEdgeItem:
	e = 'e'
	le = 'le'
	re = 're'


class TNodeItem:
	n = 'n'


class TemplateBaseItem:
	def __init__(self, name, alias: str, filter=None):
		self.name = name
		self.alias = alias
		self.filter = filter


class TemplateEdgeItem(TemplateBaseItem):
	def __init__(self, name: TEdgeItem, alias: str = '', filter=None, nodeFilter=None, steps: List[str] = None):
		super().__init__(name=name, alias=alias, filter=filter)
		self.node_filter = nodeFilter
		self.steps = steps


class TemplateNodeItem(TemplateBaseItem):
	...


class Template:
	def __init__(self, alias: str, items: List[TemplateEdgeItem or TemplateNodeItem], limit: int, _return,
				 order_by: any = None, isKhopTemplate: bool = False, select: list = None
				 ):
		self.alias = alias
		self.items = items
		self.limit = limit
		self.order_by = order_by
		self._return = _return
		self.isKhopTemplate = isKhopTemplate
		self.select = select


class Truncate:
	def __init__(self, graph: str, truncateType: ULTIPA.TruncateType = None, allData: bool = False, schema: str = None):
		self.dbType = truncateType
		self.graphSetName = graph
		self.all = allData
		self.schema = schema


class InstallAlgo:
	def __init__(self, configPath: str, soPath: str):
		self.configPath = configPath
		self.soPath = soPath


class InstallExtaAlgo(InstallAlgo):
	...



class Batch:
	Nodes: List[ULTIPA.EntityRow]
	Edges: List[ULTIPA.EntityRow]
	Schema: Schema

	def __init__(self, Schema: Schema = None, Nodes: List[ULTIPA.EntityRow] = None,
				 Edges: List[ULTIPA.EntityRow] = None):
		if Nodes is None:
			Nodes = []
		if Edges is None:
			Edges = []
		self.Nodes = Nodes
		self.Edges = Edges
		self.Schema = Schema


class InsertNodeTable:
	def __init__(self, schemas: List[Schema], nodeRows: List[ULTIPA.Node]):
		self.schemas = schemas
		self.nodeRows = nodeRows


class InsertEdgeTable:
	def __init__(self, schemas: List[Schema], edgeRows: List[ULTIPA.Edge]):
		self.schemas = schemas
		self.edgeRows = edgeRows
