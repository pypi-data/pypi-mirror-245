from ultipa import DBType
from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig


class IndexExtra(BaseExtra):

	def showIndex(self, dbType: DBType = None,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListIndex:
		'''
		:param requestConfig:
		:EXP: conn.showIndex(ULTIPA_REQUEST.ShowIndex())
		:param request: ULTIPA_REQUEST
		:return:
		'''
		if dbType != None:
			command = dbType == DBType.DBNODE and CommandList.showNodeIndex or CommandList.showEdgeIndex
		else:
			command = CommandList.showIndex
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		return res

	def showFulltext(self, dbType: DBType = None,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListFulltextIndex:
		'''
		:param requestConfig:
		:EXP: conn.showIndex(ULTIPA_REQUEST.ShowIndex())
		:param request: ULTIPA_REQUEST
		:return:
		'''
		if dbType != None:
			command = dbType == DBType.DBNODE and CommandList.showNodeFulltext or CommandList.showEdgeFulltext
		else:
			command = CommandList.showFulltext
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		return res

	def createIndex(self, request: ULTIPA_REQUEST.CreateIndex,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		:param requestConfig:
		:EXP: conn.createIndex(ULTIPA_REQUEST.CreatIndex(node_property='name'))
		:param request: ULTIPA_REQUEST
		:return:
		'''
		command = request.DBtype == DBType.DBNODE and CommandList.createNodeIndex or CommandList.createEdgeIndex
		commandP = request.toString
		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def createFulltext(self, request: ULTIPA_REQUEST.CreateFulltext,
					   rquestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		command = request.DBtype == DBType.DBNODE and CommandList.createNodeFulltext or CommandList.createEdgeFulltext
		commandP = [request.toString, request.name]
		uqlMaker = UQLMAKER(command=command, commonParams=rquestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropIndex(self, request: ULTIPA_REQUEST.DropIndex,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		:EXP: conn.dropIndex(ULTIPA_REQUEST.DropIndex(node_property='node'))
		:param request: ULTIPA_REQUEST
		:return:
		'''
		command = request.DBtype == DBType.DBNODE and CommandList.dropNodeIndex or CommandList.dropEdgeIndex
		commandP = request.toString

		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropFulltext(self, request: ULTIPA_REQUEST.DropFulltext,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		command = request.DBtype == DBType.DBNODE and CommandList.dropNodeFulltext or CommandList.dropEdgeFulltext
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(request.fulltextName)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
