from ultipa.types.types import TruncateType
from ultipa.operate.base_extra import BaseExtra
from ultipa.utils import UQLMAKER, CommandList
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.configuration.RequestConfig import RequestConfig

JSONSTRING_KEYS = ["graph_privileges", "system_privileges", "policies", "policy", "privilege"]
formatdata = ['graph_privileges']


class TruncateExtra(BaseExtra):

	def truncate(self, request: ULTIPA_REQUEST.Truncate,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		command = CommandList.truncate
		requestConfig.graphName = request.graphSetName
		uqlMaker = UQLMAKER(command, commonParams=requestConfig)
		uqlMaker.addParam("graph", request.graphSetName)
		if request.dbType:
			if request.dbType == TruncateType.NODES:
				if request.all:
					uqlMaker.addParam("nodes", "*")
				if not request.all and request.schema:
					uqlMaker.addParam("nodes", "@" + request.schema, notQuotes=True)
			if request.dbType == TruncateType.EDGES:
				if request.all:
					uqlMaker.addParam("edges", "*")
				if not request.all and request.schema:
					uqlMaker.addParam("edges", "@" + request.schema, notQuotes=True)

		# if request.all and not request.dbType:
		#     uqlMaker = UQLMAKER(command,commandP=request.dbType,commonParams=requestConfig)

		return self.UqlUpdateSimple(uqlMaker)

	def compact(self, graph:str,
				requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		command = CommandList.compact
		uqlMaker = UQLMAKER(command, commonParams=requestConfig)
		uqlMaker.addParam("graph", graph)
		return self.UqlUpdateSimple(uqlMaker)

	def mount(self, graph:str,
			  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		commonP = []
		if graph:
			commonP = graph
			requestConfig.graphName = graph
		uqlMaker = UQLMAKER(command=CommandList.mount, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commonP)
		return self.UqlUpdateSimple(uqlMaker)

	def unmount(self, graph:str,
				requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		commonP = []
		if graph:
			commonP = graph
			requestConfig.graphName = graph
		uqlMaker = UQLMAKER(command=CommandList.unmount, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commonP)
		return self.UqlUpdateSimple(uqlMaker)
