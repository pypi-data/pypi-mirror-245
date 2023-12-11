# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:18
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Node.py
from typing import Dict, List

from ultipa.structs.BaseModel import BaseModel


class Node(BaseModel):
	_index = None

	def __init__(self, values: Dict, schema: str = None, id: str = None, uuid: int = None, **kwargs):
		self.id = id
		if schema is None:
			if kwargs.get("schema_name") is not None:
				self.schema = kwargs.get("schema_name")
			else:
				self.schema = None
		else:
			self.schema = schema
		self.values = values
		self.uuid = uuid

	def getID(self):
		return self.id

	def getUUID(self):
		return self.uuid

	def getValues(self):
		return self.values

	def getSchema(self):
		return self.schema

	def get(self, propertyName: str):
		return self.values.get(propertyName)

	def set(self, propertyName: str, value):
		self.values.update({propertyName: value})

	def _getIndex(self):
		return self._index

class NodeAlias:
	def __init__(self, alias: str, nodes: List[Node] = None):
		self.alias = alias
		if nodes is None:
			nodes = []
		self.nodes = nodes