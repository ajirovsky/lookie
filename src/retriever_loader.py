
from langchain_community.document_loaders.csv_loader import CSVLoader
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RetrieverLoader:
    def __init__(self, corpus_path: Path) -> None:
        loader = CSVLoader(corpus_path)
        self.documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(self.documents)
        self.vector_store = Chroma.from_documents(splits, OpenAIEmbeddings())

    def get_retriever(self, k: int = 4):
        return self.vector_store.as_retriever(search_kwargs={"k": k})
        