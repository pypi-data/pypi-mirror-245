# -*- coding: utf-8 -*-
# @Time    : 2023/1/16 11:06 上午
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : propertyUtils.py
from ultipa.structs.PropertyType import PropertyTypeStr
from ultipa.types import ULTIPA
from typing import List


def isBasePropertyType(type: PropertyTypeStr):
	if type in [PropertyTypeStr.PROPERTY_STRING,
				PropertyTypeStr.PROPERTY_INT,
				PropertyTypeStr.PROPERTY_INT64,
				PropertyTypeStr.PROPERTY_UINT32,
				PropertyTypeStr.PROPERTY_UINT64,
				PropertyTypeStr.PROPERTY_FLOAT,
				PropertyTypeStr.PROPERTY_DOUBLE,
				PropertyTypeStr.PROPERTY_DATETIME,
				PropertyTypeStr.PROPERTY_TIMESTAMP,
				PropertyTypeStr.PROPERTY_TEXT]:
		return True
	return False


def propertyGet(type: ULTIPA.PropertyType):
	return type


def getPropertyTypesDesc(type: PropertyTypeStr, subTypes: List[PropertyTypeStr]):
	if type == PropertyTypeStr.PROPERTY_LIST:
		subType = subTypes[0]
		if isBasePropertyType(subType):
			return f"{subType}[]"
	if type == PropertyTypeStr.PROPERTY_SET:
		subType = subTypes[0]
		if isBasePropertyType(subType):
			return f"set({subType})"
	return type
