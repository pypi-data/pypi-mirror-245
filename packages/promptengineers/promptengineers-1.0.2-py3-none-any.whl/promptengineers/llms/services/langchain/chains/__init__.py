"""Chain Service"""
from langchain.agents import (AgentType, initialize_agent,
							AgentExecutor, OpenAIFunctionsAgent,
							load_tools)
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent, create_retriever_tool
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import (
    ConversationChain,
	ConversationalRetrievalChain,
	LLMChain
)
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.tools import AIPluginTool
from langchain.chains.chat_vector_db.prompts import QA_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    PromptTemplate
)
from promptengineers.retrieval.strategies import VectorstoreContext
from promptengineers.core.config import APP_ENV
from promptengineers.core.config.tools import AVAILABLE_TOOLS
from promptengineers.llms.utils import get_chat_history
from promptengineers.tools.utils import filter_tools
from promptengineers.prompts.templates import get_system_template


class ChainService:
	"""Chain Service"""
	def __init__(self, model):
		self.model = model

	def condense_question(self, system_message):
		"""Condense a question into a single sentence."""
		return LLMChain(
			llm=self.model,
			prompt=get_system_template(system_message),
		)

	def collect_docs(self, system_message):
		"""Collect documents from the vectorstore."""
		return load_qa_chain(
			self.model,
			chain_type='stuff',
			prompt=get_system_template(system_message)
		)

	def create_executor(
		self,
		content,
		tools,
		chat_history,
		verbose=True if APP_ENV == 'local' or APP_ENV == 'development' else False,
		return_messages = True,
		callbacks = [],
		return_intermediate_steps = True
	):
		# memory = ConversationBufferMemory(
		# 	memory_key="chat_history", 
		# 	return_messages=return_messages, 
		# 	output_key='output'
		# )
		memory = AgentTokenBufferMemory(memory_key="chat_history", llm=self.model, return_messages=return_messages)
		system_message = SystemMessage(content=content)
		prompt = OpenAIFunctionsAgent.create_prompt(
			system_message=system_message,
			extra_prompt_messages=[MessagesPlaceholder(variable_name="chat_history")]
		)
		if len(chat_history) > 0:
			for message in chat_history:
				if message[0] and message[1]:
					memory.chat_memory.add_user_message(message[0])
					memory.chat_memory.add_ai_message(message[1])
				else:
					memory.chat_memory.add_user_message(message[0])
		agent = OpenAIFunctionsAgent(llm=self.model, tools=tools, prompt=prompt)
		return AgentExecutor(
			agent=agent, 
			tools=tools,
			memory=memory, 
			verbose=verbose, 
			callbacks=callbacks, 
			return_intermediate_steps=return_intermediate_steps
		)
	
	# def conversation_retrieval(
	# 	self,
	# 	vectorstore,
	# 	system_message,
	# 	chat_history,
	# 	callbacks = []
	# ):
	# 	"""Retrieve a conversation."""
	# 	tool = create_retriever_tool(
	# 		vectorstore.as_retriever(),
	# 		"search_formio_docs",
	# 		"Searches and returns documents regarding Form.io.",
	# 	)
	# 	tools = [tool]
	# 	system_message = SystemMessage(content=system_message)
	# 	agent_executor = create_conversational_retrieval_agent(
	# 		self.model, 
	# 		tools, 
	# 		system_message=system_message, 
	# 		verbose=True,
	# 		# callbacks=callbacks
	# 	)
	# 	return agent_executor

	def conversation_retrieval(
		self,
		system_message,
		chat_history,
		vectorstore,
		verbose=True if APP_ENV == 'local' or APP_ENV == 'development' else False,
	):
		"""Retrieve a conversation."""
		tool = create_retriever_tool(
			vectorstore.as_retriever(),
			"search_docs",
			"Searches and returns documents. It is a requirement to use this for every query.",
		)
		tools = [tool]
		system_message = SystemMessage(content=system_message)
		prompt = OpenAIFunctionsAgent.create_prompt(
			system_message=system_message,
			extra_prompt_messages=[MessagesPlaceholder(variable_name="chat_history")],
		)
		agent = OpenAIFunctionsAgent(llm=self.model, tools=tools, prompt=prompt)
		memory = AgentTokenBufferMemory(memory_key="chat_history", llm=self.model)
		for message in chat_history:
			if message[0] and message[1]:
				memory.chat_memory.add_user_message(message[0])
				memory.chat_memory.add_ai_message(message[1])
			else:
				memory.chat_memory.add_user_message(message[0])
		agent_executor = AgentExecutor(
			agent=agent,
			tools=tools,
			memory=memory,
			verbose=verbose,
			return_intermediate_steps=True,
		)
		return agent_executor

	# def conversation_retrieval(
	# 	self,
	# 	vectorstore,
	# 	system_message,
	# 	chat_history,
	# 	callbacks = []
	# ):
	# 	"""Retrieve a conversation."""
	# 	memory = ConversationSummaryBufferMemory(llm=self.model, memory_key="chat_history", return_messages=True)
	# 	for message in chat_history:
	# 		if message[0] and message[1]:
	# 			memory.chat_memory.add_user_message(message[0])
	# 			memory.chat_memory.add_ai_message(message[1])
	# 		else:
	# 			memory.chat_memory.add_user_message(message[0])
	# 	return ConversationalRetrievalChain.from_llm(
	# 		condense_question_llm=self.model,
	# 		retriever=vectorstore.as_retriever(),
	# 		memory=memory,
	# 		combine_docs_chain=self.collect_docs(system_message),
	# 		get_chat_history=get_chat_history,
	# 		verbose=True,
	# 		callbacks=callbacks
	# 	)

	# def conversation_retrieval(
	# 	self,
	# 	vectorstore,
	# 	system_message,
	# 	chat_history,
	# 	callbacks = []
	# ):
	# 	"""Retrieve a conversation."""
	# 	memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
	# 	if len(chat_history) > 0:
	# 		for message in chat_history:
	# 			if message[0] and message[1]:
	# 				memory.chat_memory.add_user_message(message[0])
	# 				memory.chat_memory.add_ai_message(message[1])
	# 			else:
	# 				memory.chat_memory.add_user_message(message[0])
	# 	return ConversationalRetrievalChain(
	# 		question_generator=self.condense_question(system_message),
	# 		retriever=vectorstore.as_retriever(),
	# 		memory=memory,
	# 		combine_docs_chain=self.collect_docs(system_message),
	# 		get_chat_history=get_chat_history,
	# 		verbose=True,
	# 		callbacks=callbacks
	# 	)

	# def agent_search(self, tools, chat_history):
	# 	"""Agent search."""
	# 	memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
	# 	if len(chat_history) > 0:
	# 		for message in chat_history:
	# 			if message[0] and message[1]:
	# 				memory.chat_memory.add_user_message(message[0])
	# 				memory.chat_memory.add_ai_message(message[1])
	# 			else:
	# 				memory.chat_memory.add_user_message(message[0])
	# 	return initialize_agent(
	# 		tools,
	# 		self.model,
	# 		agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION or AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
	# 		verbose=True,
	# 		memory=memory,
	# 		get_chat_history=get_chat_history
	# 	)

	def agent_with_tools(
			self, 
			system_message: str, 
			chat_history, 
			tools: list[str] = None,
			available_tools: dict[str, any] = None,
			vectorstore: VectorstoreContext = None,
			plugins: list[str] = None,
			callbacks: list[BaseCallbackHandler] = None
		):
		"""Agent search."""
		filtered_tools = filter_tools(tools or [], available_tools or AVAILABLE_TOOLS)
		
		## Add docs tool
		if vectorstore:
			docs_tool = create_retriever_tool(
				vectorstore.as_retriever(),
				"search_docs",
				"""
				Searches and returns relevant documents. It is a requirement to use this for every query.
				Rewrite the user to be a detailed question.
				""",
			)
			filtered_tools.append(docs_tool)

		## Add plugins
		if plugins and len(plugins) > 0:
			loaded_tools = load_tools(["requests_all"])
			for tool in plugins:
				tool = AIPluginTool.from_plugin_url(tool)
				loaded_tools += [tool]
			filtered_tools += loaded_tools
		## Create agent
		agent_executor = self.create_executor(system_message, filtered_tools, chat_history, callbacks=callbacks)
		return agent_executor

	# def agent_with_plugins(self, plugins, system_message, chat_history, callbacks=[]):
	# 	"""Agent Plugins."""
	# 	loaded_tools = load_tools(["requests_all"])
	# 	for tool in plugins:
	# 		tool = AIPluginTool.from_plugin_url(tool)
	# 		loaded_tools += [tool]
	# 	agent_executor = self.create_executor(system_message, loaded_tools, chat_history, callbacks=callbacks)
	# 	return agent_executor

	def conversation(self):
		prompt_template = ChatPromptTemplate.from_messages(
			[
				MessagesPlaceholder(variable_name="context"),
				HumanMessagePromptTemplate.from_template("{input}")
			]
		)
		memory = ConversationBufferMemory(return_messages=True, memory_key="context")
		llm_chain = ConversationChain(llm=self.model, prompt=prompt_template, memory=memory, verbose=False)

		return llm_chain