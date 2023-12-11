# -*- coding: utf-8 -*-
# @Time    : 2023/8/26 12:05
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : subGraph_extra.py
import time

from ultipa import InsertType
from ultipa.configuration.InsertConfig import InsertConfig
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.graph_extra import GraphExtra
from ultipa.operate.property_extra import PropertyExtra
from ultipa.operate.schema_extra import SchemaExtra
from ultipa.structs import Graph, DBType, EntityRow


class SubGraphExtra(GraphExtra,SchemaExtra,PropertyExtra):

	def uqlCreateSubgraph(self, uql: str, subGraphName: str, requestConfig: RequestConfig = RequestConfig()):
		ret = self.uql(uql, requestConfig)
		if ret.status.code != 0:
			return ret
		graphRet = self.getGraph(subGraphName)
		if graphRet.status.code != 0:
			self.createGraph(Graph(graph=subGraphName))
			time.sleep(3)
		dataItems = ret.get(0).asPaths()
		nodeSchemasDict={}
		edgeSchemasDict={}
		schemaNodes = {}
		schemaEdges = {}

		for data in dataItems:
			for nodeSchmemaKey in data.nodeSchemas.keys():
				if nodeSchmemaKey in nodeSchemasDict:
					continue
				dbType = DBType.DBNODE
				nodeSchema = data.nodeSchemas.get(nodeSchmemaKey)
				nodeSchema.DBType = dbType
				if self.showSchema(dbType,nodeSchmemaKey,requestConfig=RequestConfig(graphName=subGraphName)).status.code==0:
					for property in nodeSchema.properties:
						property.type = property.getPropertyTypeByString(property.type)
						subty = []
						for i in property.subTypes:
							subty.append(property.getPropertyTypeByString(i))
						property.subTypes = subty
					nodeSchemasDict.update({nodeSchmemaKey: nodeSchema})
					continue
				self.createSchema(nodeSchema,requestConfig=RequestConfig(graphName=subGraphName))
				for property in nodeSchema.properties:
					self.createProperty(dbType,nodeSchmemaKey,property,requestConfig=RequestConfig(graphName=subGraphName))
				for property in nodeSchema.properties:
					property.type = property.getPropertyTypeByString(property.type)
					subty = []
					for i in property.subTypes:
						subty.append(property.getPropertyTypeByString(i))
					property.subTypes = subty
				nodeSchemasDict.update({nodeSchmemaKey:nodeSchema})
			for edgeSchmemaKey in data.edgeSchemas.keys():
				if edgeSchmemaKey in edgeSchemasDict:
					continue
				dbType = DBType.DBEDGE
				edgeSchema = data.edgeSchemas.get(edgeSchmemaKey)
				edgeSchema.DBType = dbType
				if self.showSchema(dbType,edgeSchmemaKey,requestConfig=RequestConfig(graphName=subGraphName)).status.code==0:
					for property in edgeSchema.properties:
						property.type = property.getPropertyTypeByString(property.type)
						subty = []
						for i in property.subTypes:
							subty.append(property.getPropertyTypeByString(i))
						property.subTypes = subty
					edgeSchemasDict.update({edgeSchmemaKey: edgeSchema})
					continue
				self.createSchema(edgeSchema, requestConfig=RequestConfig(graphName=subGraphName))
				for property in edgeSchema.properties:
					self.createProperty(dbType,edgeSchmemaKey,property,requestConfig=RequestConfig(graphName=subGraphName))
				for property in edgeSchema.properties:
					property.type = property.getPropertyTypeByString(property.type)
					subty = []
					for i in property.subTypes:
						subty.append(property.getPropertyTypeByString(i))
					property.subTypes = subty
				edgeSchemasDict.update({edgeSchmemaKey:edgeSchema})

			for node in data.nodes:
				if schemaNodes.get(node.schema):
					schemaNodes.get(node.schema).append(EntityRow(id=node.id,values=node.values))
				else:

					schemaNodes.update({node.schema:[EntityRow(id=node.id,values=node.values)]})

			for edge in data.edges:
				if schemaEdges.get(edge.schema):
					schemaEdges.get(edge.schema).append(EntityRow(from_id=edge.from_id,to_id=edge.to_id,values=edge.values))
				else:
					schemaEdges.update({edge.schema:[EntityRow(from_id=edge.from_id,to_id=edge.to_id,values=edge.values)]})

		for nodeKey in schemaNodes:
			self.insertNodesBatchBySchema(schema=nodeSchemasDict.get(nodeKey),rows=schemaNodes.get(nodeKey),config=InsertConfig(InsertType.UPSERT,graphName = subGraphName))

		for edgeKey in schemaEdges:
			self.insertEdgesBatchBySchema(schema=edgeSchemasDict.get(edgeKey), rows=schemaEdges.get(edgeKey),
										  config=InsertConfig(InsertType.UPSERT, graphName=subGraphName))

		return ret