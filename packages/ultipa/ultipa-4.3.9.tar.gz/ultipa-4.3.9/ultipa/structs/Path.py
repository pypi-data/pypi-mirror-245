# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:20
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Path.py
from typing import Dict, List

from ultipa.structs.Schema import Schema
from ultipa.structs.BaseModel import BaseModel
from ultipa.structs.Edge import Edge
from ultipa.structs.Node import Node


class Path(BaseModel):
	nodeSchemas: Dict[str, Schema] = {}
	edgeSchemas: Dict[str, Schema] = {}

	def __init__(self, nodes: List[Node], edges: List[Edge], nodeSchemas, edgeSchemas):
		self.nodes = nodes
		self.edges = edges
		self.nodeSchemas = nodeSchemas
		self.edgeSchemas = edgeSchemas


	def length(self):
		return len(self.edges)

	def getNodes(self):
		return self.nodes

	def getEdges(self):
		return self.edges

class PathAlias:
	def __init__(self, alias: str, paths: List[Path] = None):
		self.alias = alias
		if paths is None:
			paths = []
		self.paths = paths

	def length(self):
		return len(self.paths)

	def getNodes(self):
		nodes = [i.nodes for i in self.paths]
		return nodes

	def getEdges(self):
		edges = [i.edges for i in self.paths]
		return edges