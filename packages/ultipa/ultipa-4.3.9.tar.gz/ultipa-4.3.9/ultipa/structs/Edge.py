# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:19
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Edge.py
from typing import Dict

from ultipa.structs.BaseModel import BaseModel


class Edge(BaseModel):
	_index = None

	def __init__(self, values: Dict, from_id: str = None, from_uuid: int = None, to_id: str = None, to_uuid: int = None,
				 schema: str = None,
				 uuid: int = None, **kwargs):
		if schema is None:
			if kwargs.get("schema_name") is not None:
				self.schema = kwargs.get("schema_name")
			else:
				self.schema = None
		else:
			self.schema = schema

		self.from_id = from_id
		self.from_uuid = from_uuid
		self.to_id = to_id
		self.to_uuid = to_uuid
		self.values = values
		self.uuid = uuid

	def getUUID(self):
		return self.uuid

	def getFrom(self):
		return self.from_id

	def getTo(self):
		return self.to_id

	def getFromUUID(self):
		return self.from_uuid

	def getToUUID(self):
		return self.to_uuid

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