import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
# from nltk.tokenize import sent_tokenize
# from sentence_transformers import SentenceTransformer, CrossEncoder


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text +=page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap = 200, length_function = len )  # Basically the chunk_overlap prevents the meaning loss if the chunk size ends in between a para or sentence.
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


# def embed_chunks(chunks):
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     embeddings = model.encode(chunks, convert_to_tensor=True).cpu().numpy()
#     return embeddings



def main():
    load_dotenv()
    st .set_page_config(page_title="Chat with multiple PDFs", page_icon="🤖")
    st.header("Chat with multiple PDFs:")
    st.text_input("Ask question about your documents:")

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your documents here:", accept_multiple_files=True)

        if st.button("Process"):
            with st.spinner("Processing"):
                # Get the pdf text
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text)  Was just added for debugging.


                # Get the text chunks

                text_chunks  = get_text_chunks(raw_text)
                st.write(text_chunks)



                # Create vector store
                vectorstore = get_vectorstore(text_chunks)




if __name__ == "__main__":
    main()