
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langsmith import Client
from retriever_loader import RetrieverLoader
from langchain_core.runnables import RunnablePassthrough

DATASET = Path("data/vtv_corpus.txt")



def main():
    retriever_loader = RetrieverLoader(DATASET)
    client = Client()
    prompt = client.pull_prompt("lookie")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
    rag_chain = ({"context" : retriever_loader.get_retriever() | 
                  (lambda docs: "\n\n".join(doc.page_content for doc in docs)), 
                  "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())
    
    query = rag_chain.invoke("Doporuč mi nějaké dobré televizní pořady. Mám rád zpravodajství.")
    print(query)


if __name__ == "__main__":
    main()