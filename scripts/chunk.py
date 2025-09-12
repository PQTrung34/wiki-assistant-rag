from crawl import WikipediaPage
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
# from langchain.embeddings import HuggingFaceEmbeddings

class Chunking:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    def get_data(self):
        curr_dir = os.getcwd()
        filename = os.path.join(os.path.dirname(curr_dir), 'data', 'wikipedia.txt')
        if not os.path.exists(filename):
            wiki = WikipediaPage()
            wiki.get_all_pages(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        return data
    
    def chunk(self):
        data = self.get_data()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        chunks = text_splitter.split_text(data)
        return chunks

test = Chunking()
print(len(test.chunk()))