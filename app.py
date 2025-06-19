from dotenv import load_dotenv
import os
import streamlit as st
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq

def main():
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    st.set_page_config(page_title="Chat with your PDF")
    st.header("Chat with your PDF 🤖")

    pdf = st.file_uploader("Load your PDF", type="pdf")

    if pdf is not None:
        Pdf_reader = PdfReader(pdf)
        text = ""
        for page in Pdf_reader.pages:
            text += page.extract_text()


        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # Embeddings generation
        embeddings = HuggingFaceEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)


        user_question = st.text_input("Ask question about yourPDF:")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            llm = ChatGroq(model = "qwen-qwq-32b")
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents = docs, question = user_question)

            st.write(response)





if __name__ == '__main__':
    main()
