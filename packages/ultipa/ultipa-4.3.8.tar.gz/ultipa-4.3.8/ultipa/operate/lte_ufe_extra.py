from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import DBType
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig

class LteUfeExtra(BaseExtra):

	def lte(self, request: ULTIPA_REQUEST.LTE,
			requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		:param requestConfig:
		:EXP: conn.lte(ULTIPA_REQUEST.LteUfe(property='name',type=DBType.DBNODE))
		:param request: ULTIPA_REQUEST
		:return:
		'''
		command = request.type == DBType.DBNODE and CommandList.lteNode or CommandList.lteEdge
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(request.schemaName.toString)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def ufe(self, request: ULTIPA_REQUEST.UFE,
			requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		:param requestConfig:
		:EXP: conn.ufe(ULTIPA_REQUEST.LteUfe(property='name',type=DBType.DBEDGE))
		:param request: ULTIPA_REQUEST
		:return:
		'''
		command = request.type == DBType.DBNODE and CommandList.ufeNode or CommandList.ufeEdge
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(request.schemaName.toString)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
