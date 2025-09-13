from scripts.chunk import Chunking
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

class VectorStore:
    def __init__(self):
        self.chunking = Chunking()
        self.db_name = 'vector_db'
        self.db_path = os.path.join(os.getcwd(), 'vector_db')

    def store_db(self):
        vector_store = Chroma.from_texts(texts=self.chunking.get_chunks(), # danh sách văn bản đã chia nhỏ
                                         embedding=embeddings,   # embeddings
                                         persist_directory=self.db_path, # folder lưu trữ db
                                        #  collection_name=self.db_name
                        )
        vector_store.persist() # Lưu xuống ổ đĩa
        return vector_store
    
    def load_db(self):
        if os.path.exists(self.db_path) and os.listdir(self.db_path):
            return Chroma(persist_directory=self.db_path,
                                  embedding_function=embeddings,
                                #   collection_name=self.db_name
                        )
        else:
            return self.store_db()