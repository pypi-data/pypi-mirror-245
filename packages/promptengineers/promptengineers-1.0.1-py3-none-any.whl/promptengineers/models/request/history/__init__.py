"""Chat History Request Models"""
from typing import Optional

from promptengineers.models.request.chat import ReqBodyChat

class ReqBodyChatHistory(ReqBodyChat): # pylint: disable=too-few-public-methods
	"""A message to send to the chatbot."""
	title: Optional[str] = None

	class Config: # pylint: disable=too-few-public-methods
		"""A message to send to the chatbot."""
		json_schema_extra = {
			"example": {
				"title": "World Series 2001 Chatbot",
				"model": "gpt-3.5-turbo",
				"temperature": 0.8,
				"stream": False,
				"messages": [
					{"role": "system", "content": "You are a helpful assistant."},
					{"role": "user", "content": 'Who won the 2001 world series?'},
					{"role": "assistant", "content": 'The arizona diamondbacks won the 2001 world series.'},
					{"role": "user", "content": 'Who were the pitchers?'},
				]
			}
		}

class ReqBodyListChatHistory(ReqBodyChatHistory): # pylint: disable=too-few-public-methods
	"""A message to send to the chatbot."""

	class Config: # pylint: disable=too-few-public-methods
		"""A message to send to the chatbot."""
		json_schema_extra = {
			"example": {
				"chats": [
					{
						"_id": "653e147a126c8e67d951fd20",
						"title": "World Series 2001 Chatbot",
						"model": "gpt-3.5-turbo",
						"temperature": 0.8,
						"stream": False,
						"messages": [
							{"role": "system", "content": "You are a helpful assistant."},
							{"role": "user", "content": 'Who won the 2001 world series?'},
							{"role": "assistant", "content": 'The arizona diamondbacks won the 2001 world series.'},
							{"role": "user", "content": 'Who were the pitchers?'},
						],
						"functions": [],
						"vectorstore": "",
						"user_id": "63f0962f9a09c84c98ab6caf",
						"created_at": 1698523723,
						"updated_at": 1698562747
					},
					{
						"_id": "6539f7f3126c8e67d951fc77",
						"temperature": 0.9,
						"model": "gpt-3.5-turbo",
						"messages": [
							{
								"role": "system",
								"content": "PERSONA:\nImagine you super intelligent AI assistant that is an expert on the context.\n\nINSTRUCTION:\nUse the following pieces of context to answer the question at the end. If you don't know the answer or if the required code is not present, just say that you don't know, and don't try to make up an answer. \n\nOUTPUT FORMAT RULES:\nCode snippets should be wrapped in triple backticks, along with the language name for proper formatting,  if applicable. This also includes yaml and Dockerfile's. If showing how to install dependencies like npm, pip, cargo, etc use the bash backticks.\nExample:\n```python\nprint(\"Hello World!\")\n```"
							},
							{
								"role": "user",
								"content": "Can you summarize the readme on chat-extension repository "
							},
							{
								"role": "assistant",
								"content": "I'm sorry, but I couldn't find the README for the chat-extension repository."
							}
						],
						"tools": [
							"github_get_repository",
							"github_list_organization_repos",
							"github_issues_assigned_to_auth_user",
							"github_repo_issue",
							"github_repo_issue_create",
							"github_repo_issue_update",
							"github_repo_pull_create"
						],
						"functions": [],
						"vectorstore": "",
						"user_id": "63f0962f9a09c84c98ab6caf",
						"created_at": 1698297843,
						"updated_at": 1698297843
					}
				]
			}
		}
