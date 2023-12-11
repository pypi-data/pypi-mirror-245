# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:21
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : EntityRow.py
from typing import Dict


class EntityRow:
	_index = None
	def __init__(self, values: Dict, schema: str = None, id: str = None, from_id: str = None, to_id: str = None,
				 uuid: int = None, from_uuid: int = None, to_uuid: int = None, **kwargs):
		self.uuid = uuid
		self.id = id
		self.from_uuid = from_uuid
		self.to_uuid = to_uuid
		self.from_id = from_id
		self.to_id = to_id
		if schema is None:
			if kwargs.get("schema_name") is not None:
				self.schema = kwargs.get("schema_name")
			else:
				self.schema = None
		else:
			self.schema = schema
		self.values = values

	def _getIndex(self):
		return self._index