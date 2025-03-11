# def process_chat(self, user_query: str) -> AIResponse:
#     """Analyze journal entry using LangChain with chat history"""
#
#     content = """
#     You are a helpful assistant focused on the well-being of
#     others. Ypu always give accurate information and provide information
#     on how to help others. Especially if you notice a negative mood.
#     If you do not understand, ask for clarification or more context
#     and if you do not know the answer, say so.
#     """
#     system_message = SystemMessage(content=content)
#     self.memory.add_user_message(user_query)
#
#     history_messages = [
#         HumanMessage(content=entry["message"])
#         if entry["sender"] == "user"
#         else SystemMessage(content=entry["message"])
#         for entry in self.chat_history
#     ]
#     human_message = HumanMessage(content=user_query)
#     prompt = ChatPromptTemplate(
#         messages=[
#             system_message,
#             self.memory.messages,
#             human_message,
#         ]
#     )
#
#     chain = prompt | self.llm
#     ai_msg = chain.invoke({})
#     self.memory.add_ai_message(ai_msg.content)
#
#     self.update_chat_history({"sender": "user", "message": user_query})
#     self.update_chat_history({"sender": "ai", "message": ai_msg.content})
#     print(self.chat_history)
#
#     return ai_msg.content
