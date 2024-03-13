import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from upstash_vector import Index
from prompt_template import RAG_PROMPT_TEMPLATE
from upstash import UpstashVectorStore
from callbacks import StreamHandler
from index_papers import return_documents_list

load_dotenv()


class RAG:
    def __init__(self, chat_box, embeddings):
        self.chat_box = chat_box
        self.set_llm()
        self.embeddings = embeddings
        self.index = Index(
            url=os.environ.get("UPSTASH_URL"),
            token=os.environ.get("UPSTASH_TOKEN"),
        )
        self.vectorstore = UpstashVectorStore(self.index, self.embeddings)

    def set_llm(self):
        chat_box = self.chat_box.container().empty()
        stream_handler = StreamHandler(chat_box)
        llm = ChatOpenAI(
            max_tokens=400,
            streaming=True,
            callbacks=[stream_handler],
        )
        self.llm = llm

    def get_context(self, query):
        results = self.vectorstore.similarity_search_with_score(query)
        context = ""

        for doc, _ in results:
            context += doc.page_content + "\n===\n"
        return context, results

    @staticmethod
    def get_prompt(question, context):
        prompt = RAG_PROMPT_TEMPLATE.format(question=question, context=context)
        return prompt

    def predict(self, query):
        return_documents_list(query,10,20)
        context, source_documents = self.get_context(query)
        print(context,source_documents)
        prompt = self.get_prompt(query, context)
        print(context)
        answer = self.llm.predict(prompt)
        prediction = {
            "answer": answer,
            "source_documents": source_documents,
        }
        self.vectorstore.delete_vectors(True)
        return prediction