# -*-coding:utf-8-*-
import uuid
import json
from enum import Enum
from typing import List, Dict

from ultipa.structs import DBType
from ultipa.structs.Graph import Graph
from ultipa.structs.Algo import Algo, AlgoResultOpt, ALGO_RESULT
from ultipa.structs.BaseModel import BaseModel
from ultipa.structs.Edge import Edge
from ultipa.structs.EntityRow import EntityRow
from ultipa.structs.Node import Node, NodeAlias
from ultipa.structs.Path import Path, PathAlias
from ultipa.structs.Property import Property
from ultipa.structs.PropertyType import *
from ultipa.structs.ResultType import ResultType
from ultipa.structs.Retry import Retry
from ultipa.structs.Schema import Schema
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.convert import convertToListAnyObject, convertTableToDict, convertToAnyObject, \
	convertAlgoList2AnyObject
from ultipa.utils.errors import ParameterException
from ultipa.utils.logger import LoggerConfig


# T = TypeVar('T')


class TruncateType:
	NODES = 'nodes'
	EDGES = 'edges'


class DirectionType:
	left = 'left'
	right = 'right'


# PROPERTY_BLOB = 'BLOB'


class TaskStatus:
	TASK_WAITING = 0
	TASK_COMPUTING = 1
	TASK_WRITEBACKING = 2
	TASK_DONE = 3
	TASK_FAILED = 4
	TASK_STOP = 5


TaskStatusString = {
	TaskStatus.TASK_WAITING: "TASK_WAITING",
	TaskStatus.TASK_COMPUTING: "TASK_COMPUTING",
	TaskStatus.TASK_WRITEBACKING: "TASK_WRITEBACKING",
	TaskStatus.TASK_DONE: "TASK_DONE",
	TaskStatus.TASK_FAILED: "TASK_FAILED",
	TaskStatus.TASK_STOP: "TASK_STOP"
}


class Code:
	SUCCESS = ultipa_pb2.SUCCESS
	FAILED = ultipa_pb2.FAILED
	PARAM_ERROR = ultipa_pb2.PARAM_ERROR
	BASE_DB_ERROR = ultipa_pb2.BASE_DB_ERROR
	ENGINE_ERROR = ultipa_pb2.ENGINE_ERROR
	SYSTEM_ERROR = ultipa_pb2.SYSTEM_ERROR
	RAFT_REDIRECT = ultipa_pb2.RAFT_REDIRECT
	RAFT_LEADER_NOT_YET_ELECTED = ultipa_pb2.RAFT_LEADER_NOT_YET_ELECTED
	RAFT_LOG_ERROR = ultipa_pb2.RAFT_LOG_ERROR
	UQL_ERROR = ultipa_pb2.UQL_ERROR
	NOT_RAFT_MODE = ultipa_pb2.NOT_RAFT_MODE
	RAFT_NO_AVAILABLE_FOLLOWERS = ultipa_pb2.RAFT_NO_AVAILABLE_FOLLOWERS
	RAFT_NO_AVAILABLE_ALGO_SERVERS = ultipa_pb2.RAFT_NO_AVAILABLE_ALGO_SERVERS
	PERMISSION_DENIED = ultipa_pb2.PERMISSION_DENIED

	UNKNOW_ERROR = 1000


class FollowerRole:
	ROLE_UNSET = ultipa_pb2.ROLE_UNSET
	ROLE_READABLE = ultipa_pb2.ROLE_READABLE
	ROLE_ALGO_EXECUTABLE = ultipa_pb2.ROLE_ALGO_EXECUTABLE


class ServerStatus:
	DEAD = ultipa_pb2.DEAD
	ALIVE = ultipa_pb2.ALIVE


class RaftPeerInfo:
	def __init__(self, host, status=None, isLeader=False, isAlgoExecutable=False, isFollowerReadable=False,
				 isUnset=False):
		self.host = host
		self.status = status
		self.isLeader = isLeader
		self.isAlgoExecutable = isAlgoExecutable
		self.isFollowerReadable = isFollowerReadable
		self.isUnset = isUnset


class ClusterInfo:
	def __init__(self, redirect: str, raftPeers: List[RaftPeerInfo], leader: RaftPeerInfo = None):
		self.redirect = redirect
		self.leader = leader
		self.raftPeers = raftPeers


class Status:
	def __init__(self, code: Code, message: str, clusterInfo: ClusterInfo = None):
		self.code = code
		self.message = message.strip('\n')
		if clusterInfo:
			self.clusterInfo = clusterInfo


class NodeTable:
	def __init__(self, schemas: List[object], nodeRows: List[Node] = None):
		self.schemas = schemas
		if nodeRows is None:
			nodeRows = []
		self.nodeRows = nodeRows

	def __del__(self):
		pass


class NodeEntityTable:
	def __init__(self, schemas: List[object], nodeRows: List[EntityRow] = None):
		self.schemas = schemas
		if nodeRows is None:
			nodeRows = []
		self.nodeRows = nodeRows

	def __del__(self):
		pass


class EdgeTable:
	def __init__(self, schemas: List[object], edgeRows: List[Edge] = None):
		self.schemas = schemas
		if edgeRows is None:
			edgeRows = []
		self.edgeRows = edgeRows


class EdgeEntityTable:
	def __init__(self, schemas: List[object], edgeRows: List[EntityRow] = None):
		self.schemas = schemas
		if edgeRows is None:
			edgeRows = []
		self.edgeRows = edgeRows

	def __del__(self):
		pass


class EdgeAlias:
	def __init__(self, alias: str, edges: List[Edge]):
		self.alias = alias
		self.edges = edges


class Attr:
	def __init__(self, alias: str, values: any, type: ResultType = None, type_desc: str = None):
		self.name = alias
		self.values = values
		self.type = type
		self.type_desc = type_desc


class AttrNode:
	def __init__(self, alias: str, values: List[List[Node]], type: ResultType = None, type_desc: str = None):
		self.name = alias
		self.values = values
		self.type = type
		self.type_desc = type_desc


class AttrEdge:
	def __init__(self, alias: str, values: List[List[Edge]], type: ResultType = None, type_desc: str = None):
		self.name = alias
		self.values = values
		self.type = type
		self.type_desc = type_desc


class AttrPath:
	def __init__(self, alias: str, values: List[List[Path]], type: ResultType = None, type_desc: str = None):
		self.name = alias
		self.values = values
		self.type = type
		self.type_desc = type_desc


class UltipaAttr:

	def __init__(self, type: PropertyType, values: any, has_attr_data: bool = False, has_ultipa_data: bool = False,
				 type_desc: any = None):
		self.values = values
		self.type = type
		self.type_desc = type_desc
		self.has_attr_data = has_attr_data
		self.has_ultipa_data = has_ultipa_data


class AttrNewAlias:
	def __init__(self, alias: str, attr: UltipaAttr):
		self.alias = alias
		self.attr = attr


class ResultAlias:
	def __init__(self, alias: str, result_type: int):
		self.alias = alias
		self.result_type = result_type


class Table(BaseModel):
	def __init__(self, table_name: str, headers: List[dict], table_rows: List[List]):
		self.name = table_name
		self.rows = table_rows
		self.headers = headers

	def getHeaders(self):
		return self.headers

	def getRows(self):
		return self.rows

	def getName(self):
		return self.name

	def headerToDicts(self) -> List[Dict]:
		return convertTableToDict(self.rows, self.headers)


class ArrayAlias:
	def __init__(self, alias: str, elements):
		self.alias = alias
		self.elements = elements


class ExplainPlan:
	def __init__(self, alias, childrenNum, uql, infos):
		self.alias = alias
		self.children_num = childrenNum
		self.uql = uql
		self.infos = infos
		self.id = str(uuid.uuid4())


class DataItem(BaseModel):

	def __init__(self, alias: str, data: any, type: str):
		self.alias = alias
		self.data = data
		self.type = type

	def asNodes(self) -> List[Node]:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			if self.data is None:
				return []
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_NODE):
			error = f"DataItem {self.alias} is not Type Node"
			raise ParameterException(error)
		return self.data

	def asFirstNodes(self) -> Node:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_NODE):
			error = f"DataItem {self.alias} is not Type Node"
			raise ParameterException(error)
		return self.data[0] if len(self.data) > 0 else None

	def asEdges(self) -> List[Edge]:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			if self.data is None:
				return []
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_EDGE):
			error = f"DataItem {self.alias} is not Type Edge"
			raise ParameterException(error)
		return self.data

	def asFirstEdges(self) -> Edge:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_EDGE):
			error = f"DataItem {self.alias} is not Type Edge"
			raise ParameterException(error)
		return self.data[0] if len(self.data) > 0 else None

	def asPaths(self) -> List[Path]:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			if self.data is None:
				return []
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_PATH):
			error = f"DataItem {self.alias} is not Type Path"
			raise ParameterException(error)
		return self.data

	def asAttr(self) -> Attr:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_ATTR):
			error = f"DataItem {self.alias} is not Type Attribute list"
			raise ParameterException(error)

		return self.data

	def asNodeList(self) -> AttrNode:
		return self.asAttr()

	def asEdgeList(self) -> AttrEdge:
		return self.asAttr()

	def asPathList(self) -> AttrPath:
		return self.asAttr()

	def asTable(self) -> Table:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_TABLE):
			error = f"DataItem {self.alias} is not Type Table"
			raise ParameterException(error)
		return self.data

	def asSchemas(self) -> List[Schema]:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			if self.data is None:
				return []
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_TABLE):
			error = f"DataItem {self.alias} is not Type Table"
			raise ParameterException(error)
		alias = self.data.getName()
		if alias.startswith("_node"):
			type = "node"
		elif alias.startswith("_edge"):
			type = "edge"

		else:
			type = None

		headers = self.data.getHeaders()
		rows = self.data.getRows()
		tableListDict = convertTableToDict(rows, headers)
		REPLACE_KEYS = {
			"totalNodes": "total",
			"totalEdges": "total",
		}
		BOOL_KEYS = ["index", "lte"]
		JSON_KEYS = ["properties"]
		convert2Int = ["totalNodes", "totalEdges"]
		responseKeyFormat = ResponseKeyFormat(keyReplace=REPLACE_KEYS, boolKeys=BOOL_KEYS, jsonKeys=JSON_KEYS,
											  convert2Int=convert2Int)
		dataList = responseKeyFormat.changeKeyValue(tableListDict)
		schemaList = []
		for data in dataList:
			responseKeyFormat = ResponseKeyFormat(boolKeys=BOOL_KEYS)
			properList = responseKeyFormat.changeKeyValue(data.get("properties"))
			propertyList = [
				Property(name=propo.get("name"), description=propo.get("description"), type=propo.get("type"),
						 lte=propo.get("lte")) for propo in properList]

			schemaList.append(
				Schema(name=data.get("name"), description=data.get("description"), properties=propertyList,
					   dbType=None, type=type, total=data.get("total")))

		return schemaList

	def asProperties(self) -> List[Property]:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			if self.data is None:
				return []
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_TABLE):
			error = f"DataItem {self.alias} is not Type Table"
			raise ParameterException(error)
		headers = self.data.getHeaders()
		rows = self.data.getRows()
		table_rows_dict = convertTableToDict(rows, headers)
		BOOL_KEYS = ["lte"]
		responseKeyFormat = ResponseKeyFormat(boolKeys=BOOL_KEYS)
		dataList = responseKeyFormat.changeKeyValue(table_rows_dict)
		return [Property(name=data.get("name"), description=data.get("description"), type=data.get("type"),
						 lte=data.get("lte"), schema=data.get("schema")) for data in dataList]

	def asGraphs(self) -> List[Graph]:
		REPLACE_KEYS = {
			"graph": "name",
		}
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			if self.data is None:
				return []
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_TABLE):
			error = f"DataItem {self.alias} is not Type Table"
			raise ParameterException(error)
		headers = self.data.getHeaders()
		rows = self.data.getRows()
		table_rows_dict = convertTableToDict(rows, headers)
		responseKeyFormat = ResponseKeyFormat(keyReplace=REPLACE_KEYS)
		data = responseKeyFormat.changeKeyValue(table_rows_dict)
		data = convertToListAnyObject(data)
		return data

	def asAlgos(self) -> List[Algo]:
		if self.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
			if self.data is None:
				return []
			return self.data
		if self.type != ResultType.getTypeStr(ResultType.RESULT_TYPE_TABLE):
			error = f"DataItem {self.alias} is not Type Table"
			raise ParameterException(error)
		headers = self.data.getHeaders()
		rows = self.data.getRows()
		table_rows_dict = convertTableToDict(rows, headers)
		algo_list = []
		for data in table_rows_dict:
			paramDict = json.loads(data.get("param"))
			result_opt = int(paramDict.get("result_opt"))
			paramDict.update(paramDict)
			result_opt_obj = AlgoResultOpt()
			result_opt_obj.can_realtime = True if result_opt & ALGO_RESULT.WRITE_TO_CLIENT else False
			result_opt_obj.can_visualization = True if result_opt & ALGO_RESULT.WRITE_TO_VISUALIZATION else False
			result_opt_obj.can_write_back = True if result_opt & (
					ALGO_RESULT.WRITE_TO_DB | ALGO_RESULT.WRITE_TO_FILE) else False
			paramDict.update({"result_opt": result_opt_obj})
			algo_list.append(paramDict)

			algoObj = Algo(paramDict.get("name"), paramDict.get("description"), paramDict.get("version"),
						   paramDict.get("result_opt"),
						   paramDict.get("parameters"), paramDict.get("write_to_stats_parameters"),
						   paramDict.get("'write_to_db_parameters'"),
						   paramDict.get("'write_to_file_parameters'"))

			algo_list.append(algoObj)
		return algo_list

	def asAny(self) -> any:
		return self.data

	def asKV(self):
		return self.toDict()


class BaseUqlReply:
	def __init__(self, paths: List[PathAlias], nodes: List[NodeAlias], edges: List[EdgeAlias], tables: List[Table],
				 attrs: List = None, resultAlias: List = None,
				 explainPlan: List[ExplainPlan] = None):
		self.paths = paths
		self.nodes = nodes
		self.edges = edges
		self.tables = tables
		self.attrs = attrs
		# self.arrays = arrays
		self.resultAlias = resultAlias
		self.explainPlan = explainPlan


class UltipaStatistics(BaseModel):
	def __init__(self, edge_affected: int, node_affected: int, engine_time_cost: int, total_time_cost: int):
		self.edgeAffected = edge_affected
		self.nodeAffected = node_affected
		self.engineCost = engine_time_cost
		self.totalCost = total_time_cost


class UqlReply(BaseModel):
	datas: List[DataItem]

	def __init__(self, dataBase: BaseUqlReply, aliasMap: dict = None, datas: List = None):
		if aliasMap == None:
			aliasMap = {}
		self._aliasMap = aliasMap
		if datas is None:
			datas = []
		self.datas: List[DataItem] = datas
		self.explainPlan: List[ExplainPlan] = []
		self._dataBase = dataBase

		for data in self._dataBase.paths:
			if self._aliasMap.get(data.alias):
				self._aliasMap[data.alias].data.extend(data.paths)
				continue
			self._aliasMap[data.alias] = DataItem(data.alias, data.paths,
												  ResultType.getTypeStr(ResultType.RESULT_TYPE_PATH))

		for data in self._dataBase.nodes:
			if self._aliasMap.get(data.alias):
				self._aliasMap[data.alias].data.extend(data.nodes)
				continue
			self._aliasMap[data.alias] = DataItem(data.alias, data.nodes,
												  ResultType.getTypeStr(ResultType.RESULT_TYPE_NODE))

		for data in self._dataBase.edges:
			if self._aliasMap.get(data.alias):
				self._aliasMap[data.alias].data.extend(data.edges)
				continue
			self._aliasMap[data.alias] = DataItem(data.alias, data.edges,
												  ResultType.getTypeStr(ResultType.RESULT_TYPE_EDGE))

		for data in self._dataBase.attrs:
			if self._aliasMap.get(data.name):
				self._aliasMap[data.name].data.append(data)
				continue
			self._aliasMap[data.name] = DataItem(data.name, data, ResultType.getTypeStr(ResultType.RESULT_TYPE_ATTR))

		for data in self._dataBase.tables:
			if self._aliasMap.get(data.name):
				self._aliasMap[data.name].data.extend(data)
				continue
			self._aliasMap[data.name] = DataItem(data.name, data, ResultType.getTypeStr(ResultType.RESULT_TYPE_TABLE))

		for data in self._dataBase.explainPlan:
			self.explainPlan.append(data)

		for data in self._dataBase.resultAlias:
			if self._aliasMap.get(data.alias):
				self.datas.append(self._aliasMap[data.alias])
		if not self.datas:
			for key in self._aliasMap:
				self.datas.append(self._aliasMap[key])


class ReturnReq:
	def __init__(self, graphSetName: str, uql: str, host: str, retry: Retry, uqlIsExtra: bool):
		self.graph_name = graphSetName
		self.uql = uql
		self.host = host
		self.Retry = retry
		self.uqlIsExtra = uqlIsExtra


class ExportReply:
	def __init__(self, data: List[NodeAlias]):
		self.data = data


class PaserAttrListData:
	def __init__(self, type, nodes: List[Node] = None, edges: List[Edge] = None, paths: List[Path] = None,
				 attrs: UltipaAttr = None):
		self.type = type
		self.nodes = nodes
		self.edges = edges
		self.paths = paths
		self.attrs = attrs


class OrderType(Enum):
	desc = 'desc'
	asc = 'asc'


class UltipaEquation(Enum):
	sum = 'sum'
	count = 'count'
