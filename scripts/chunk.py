from .crawl import WikipediaPage
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Chunking:
    def __init__(self):
        pass

    def get_data(self):
        curr_dir = os.getcwd()
        data_dir = os.path.join(curr_dir, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        filename = os.path.join(data_dir, 'wikipedia.txt')
        if not os.path.exists(filename):
            wiki = WikipediaPage()
            wiki.get_all_pages(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        return data
    
    def get_chunks(self):
        data = self.get_data()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100,
                                                       separators=['\n\n', '\n', '. ', ' ', ''])
        chunks = text_splitter.split_text(data)
        return chunks