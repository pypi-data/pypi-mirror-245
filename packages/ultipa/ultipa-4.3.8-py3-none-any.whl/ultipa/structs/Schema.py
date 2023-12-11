# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 11:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Schema.py
from typing import List

from ultipa.structs import DBType
from ultipa.structs.Property import Property
from ultipa.structs.BaseModel import BaseModel


class Schema(BaseModel):

	def __init__(self, name: str, dbType: DBType, type: str = None, description: str = None,
				 properties: List[Property] = None,
				 total: int = None):
		self.description = description
		self.properties = properties
		self.name = name
		self.total = total
		self.type = type
		self.DBType = dbType

	def getProperty(self, name: str):
		find = list(filter(lambda x: x.get('name') == name, self.properties))
		if find:
			return find[0]
		return None
