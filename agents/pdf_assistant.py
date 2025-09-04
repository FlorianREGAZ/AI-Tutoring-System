from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from core.schemas import AITutorState
from core.prompts import PDF_ASSISTANT_SYSTEM_PROMPT
from utils.debug import print_state
from config import get_config


class PDFAssistantAgent:

    def __init__(self):
        config = get_config()
        self.model = init_chat_model(config.pdf_assistant_model)
        
        # RAG
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=600,
            length_function=len,
        )
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.vector_store = InMemoryVectorStore(embeddings)

    def _get_system_message(self, context: str):
        return SystemMessage(content=f"{PDF_ASSISTANT_SYSTEM_PROMPT}\n\n# PDF content:\n{context}")
    
    def _get_context(self, last_message: HumanMessage):
        docs = self.vector_store.similarity_search(last_message.content)
        return "\n\n".join([doc.page_content for doc in docs])
    
    def add_documents(self, documents: list[Document]):
        splitted_documents = self.recursive_text_splitter.split_documents(documents)
        self.vector_store.add_documents(documents=splitted_documents)

    def invoke(self, state: AITutorState):
        print_state(state, info="Before PDFAssistantAgent")
        history = state["history"]
        
        # Return empty context if no history or no documents in vector store
        if not history or not len(self.vector_store.store):
            return {"pdf_context": None}

        context = self._get_context(history[-1])
        messages = [
            self._get_system_message(context),
            *history
        ]

        response = self.model.invoke(messages)
        return {"pdf_context": response.content}
