# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 14:46
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Property.py
from typing import List

from ultipa.structs.BaseModel import BaseModel
from ultipa.structs.PropertyType import PropertyTypeStr, PropertyType

class Property:
	name: str
	description: str
	lte: bool
	schema: str
	type: PropertyTypeStr
	subTypes: List[PropertyTypeStr]

	def __init__(self, name: str,
				 type: PropertyTypeStr = PropertyTypeStr.PROPERTY_STRING,
				 description: str = '', subTypes: List[PropertyTypeStr] = None,lte: bool = None,schema: str=None):
		self.type = type
		self.subTypes = subTypes
		self.description = description
		self.name = name
		self.lte = lte
		self.schema = schema

	_PropertyMap = {
		"string": PropertyType.PROPERTY_STRING,
		"int32": PropertyType.PROPERTY_INT32,
		"int64": PropertyType.PROPERTY_INT64,
		"uint32": PropertyType.PROPERTY_UINT32,
		"uint64": PropertyType.PROPERTY_UINT64,
		"float": PropertyType.PROPERTY_FLOAT,
		"double": PropertyType.PROPERTY_DOUBLE,
		"datetime": PropertyType.PROPERTY_DATETIME,
		"timestamp": PropertyType.PROPERTY_TIMESTAMP,
		"text": PropertyType.PROPERTY_TEXT,
		"blob": PropertyType.PROPERTY_BLOB,
		"_id": PropertyType.PROPERTY_ID,
		"_uuid": PropertyType.PROPERTY_UUID,
		"_from": PropertyType.PROPERTY_FROM,
		"_to": PropertyType.PROPERTY_TO,
		"_from_uuid": PropertyType.PROPERTY_FROM_UUID,
		"_to_uuid": PropertyType.PROPERTY_TO_UUID,
		"_ignore": PropertyType.PROPERTY_IGNORE,
		"unset": PropertyType.PROPERTY_UNSET,
		"point": PropertyType.PROPERTY_POINT,
		"decimal": PropertyType.PROPERTY_DECIMAL,
		"list": PropertyType.PROPERTY_LIST,
		"set": PropertyType.PROPERTY_SET,
		"map": PropertyType.PROPERTY_MAP,
		"null": PropertyType.PROPERTY_NULL,
	}

	_PropertyReverseMap = {
		PropertyType.PROPERTY_STRING: "string",
		PropertyType.PROPERTY_INT32: "int32",
		PropertyType.PROPERTY_INT64: "int64",
		PropertyType.PROPERTY_UINT32: "uint32",
		PropertyType.PROPERTY_UINT64: "uint64",
		PropertyType.PROPERTY_FLOAT: "float",
		PropertyType.PROPERTY_DOUBLE: "double",
		PropertyType.PROPERTY_DATETIME: "datetime",
		PropertyType.PROPERTY_TIMESTAMP: "timestamp",
		PropertyType.PROPERTY_TEXT: "text",
		PropertyType.PROPERTY_BLOB: "blob",
		PropertyType.PROPERTY_ID: "_id",
		PropertyType.PROPERTY_UUID: "_uuid",
		PropertyType.PROPERTY_FROM: "_from",
		PropertyType.PROPERTY_TO: "_to",
		PropertyType.PROPERTY_FROM_UUID: "_from_uuid",
		PropertyType.PROPERTY_TO_UUID: "_to_uuid",
		PropertyType.PROPERTY_IGNORE: "_ignore",
		PropertyType.PROPERTY_UNSET: "unset",
		PropertyType.PROPERTY_POINT: "point",
		PropertyType.PROPERTY_DECIMAL: "decimal",
		PropertyType.PROPERTY_LIST: "list",
		PropertyType.PROPERTY_SET: "set",
		PropertyType.PROPERTY_MAP: "map",
		PropertyType.PROPERTY_NULL: "null",
	}

	def setSubTypesbyType(self, type: str):
		if "string" in type:
			self.subTypes = [PropertyType.PROPERTY_STRING]

		if "int32" in type:
			self.subTypes = [PropertyType.PROPERTY_INT32]

		if "uint32" in type:
			self.subTypes = [PropertyType.PROPERTY_UINT32]

		if "int64" in type:
			self.subTypes = [PropertyType.PROPERTY_INT64]

		if "uint64" in type:
			self.subTypes = [PropertyType.PROPERTY_UINT64]

		if "float" in type:
			self.subTypes = [PropertyType.PROPERTY_FLOAT]

		if "double" in type:
			self.subTypes = [PropertyType.PROPERTY_DOUBLE]

		if "datetime" in type:
			self.subTypes = [PropertyType.PROPERTY_DATETIME]

		if "timestamp" in type:
			self.subTypes = [PropertyType.PROPERTY_TIMESTAMP]

		if "text" in type:
			self.subTypes = [PropertyType.PROPERTY_TEXT]

	def isIdType(self) -> bool:
		idTypes = [
			PropertyType.PROPERTY_ID,
			PropertyType.PROPERTY_TO,
			PropertyType.PROPERTY_UUID,
			PropertyType.PROPERTY_FROM,
			PropertyType.PROPERTY_FROM_UUID,
			PropertyType.PROPERTY_TO_UUID,
		]
		return self.type in idTypes

	def isIgnore(self):
		return self.type == PropertyType.PROPERTY_IGNORE

	def setTypeStr(self, value):
		self.type = self.getStringByPropertyType(value)

	def setTypeInt(self, value):
		self.type = self.getPropertyTypeByString(value)

	def getStringType(self):
		return self.getStringByPropertyType(self.type)

	def getPropertyTypeByString(self, v):
		if not self._PropertyMap.get(v):
			if "[" in v:
				self.setSubTypesbyType(v)
				return PropertyType.PROPERTY_LIST

		return self._PropertyMap.get(v)

	def getStringByPropertyType(self, v):
		return self._PropertyReverseMap[v]

	@staticmethod
	def _getStringByPropertyType(v):
		return Property._PropertyReverseMap[v]

	@staticmethod
	def _getPropertyTypeByString(v):
		return Property._PropertyMap.get(v)