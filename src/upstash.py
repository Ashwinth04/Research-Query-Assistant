from uuid import uuid4
import tqdm
from langchain.docstore.document import Document
from upstash_vector import Index

class UpstashVectorStore:
    def __init__(self,index,embeddings):
        self.index = index
        self.embeddings = embeddings

    def delete_vectors(self,delete_all,ids = None):
        if(delete_all):
            self.index.reset()
        else:
            self.index.delete(ids)

    def add_documents(self,documents,ids = None,batch_size = 32):
        texts = []
        all_ids = []
        metadatas = []
        print("\n\n\n\n",len(documents),"\n\n\n\n")
        for document in documents:
            text = document.page_content
            metadata = document.metadata
            # metadata = {"context": text,**metadata}
            metadata = {**metadata,"context":text}

            texts.append(text)
            metadatas.append(metadata)

            if(len(texts) >= batch_size):
                ids = [str(uuid4()) for _ in range(len(texts))]
                all_ids.extend(ids)
                embeddings = self.embeddings.embed_documents(texts)
                self.index.upsert(vectors = zip(ids,embeddings,metadatas))
                texts = []
                metadatas = []
        if(len(texts) > 0):
            ids = [str(uuid4()) for _ in range(len(texts))]
            all_ids.extend(ids)
            embeddings = self.embeddings.embed_documents(texts)
            self.index.upsert(vector = zip(ids,embeddings,metadatas))

        n = len(all_ids)
        print(f"Successfully indexed {n} vectors into upstash vector database")
        # print(self.index.stats())
        return all_ids
    
    def similarity_search_with_score(self, query, k=4):
        query_embedding = self.embeddings.embed_query(query)
        query_results = self.index.query(
            query_embedding,
            top_k=k,
            include_metadata=True,
        )
        output = []
        for query_result in query_results:
            score = query_result.score
            metadata = query_result.metadata
            print(f"Retrieved Metadata: {metadata}")  # Print complete metadata
            context = metadata.get("context")
            # if context:
            #     print(f"Context as String: {context}")  # Print context only if it exists

            # Ensure context is a string before creating Document
            if not isinstance(context, str):
                print("Unexpected context type")
                continue  # Skip this document if context has an unexpected type
            print("correct")
            doc = Document(
                page_content=context,
                metadata=metadata,
            )
            output.append((doc, score))
        return output
