# Import Libraries
import os
import re
import random
import numpy as np
import pandas as pd
import fitz # PyMuPDF
import torch
import spacy
import en_core_web_trf 
from sentence_transformers import util, SentenceTransformer

from tqdm import tqdm

class DataEmbedding:
    def __init__(self, pdf_folder_path):
        self.pdf_folder_path = pdf_folder_path

    def remove_new_line(text: str) -> str:
        """
        Remove new line from the pdf text
        """
        new_text = text.replace("\n", " ")
        return new_text

    def get_pdf_text(self):

        total_file_count = len(os.listdir(self.pdf_folder_path))

        files_pages_text = []

        for count, file in enumerate(os.listdir(self.pdf_folder_path)):
            if file.endswith((".pdf", ".PDF")):
                pdf_path = os.path.join(self.pdf_folder_path, file)                
                doc = fitz.open(pdf_path)
                total_pages = doc.page_count()

                for page_number, page in tqdm(enumerate(doc)):
                    text = page.get_text()
                    text = self.remove_new_line(text)
                    files_pages_text.append({"filename": file,
                                             "page_number": page_number+1,
                                             "page_char_count": len(text),
                                             "page_word_count": len(text.split(" ")),
                                             "page_sentence_count_raw": len(text.split(". ")),
                                             "page_token_count": len(text) / 4,  # 1 token = ~4 chars
                                             "text": text})
                    
                print(f"Processed {count+1} of {total_file_count} files")           

        return files_pages_text

     



                
        