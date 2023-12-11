from kbrainsdk.validation.ingest import validate_ingest_onedrive, validate_ingest_sharepoint, validate_ingest_status
from kbrainsdk.apibase import APIBase
from docx import Document
import PyPDF2
import pandas as pd

class Ingest(APIBase):

    def __init__(self):
        self.FILE_HANDLER = {
            "pdf": self.pdf_handler,
            "txt": self.txt_handler,
            "docx": self.docx_handler
        }

        self.super().__init__()

    def ingest_onedrive(self, email, token, client_id, oauth_secret, tenant_id, environment):

        payload = {
            "email": email,
            "token": token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_ingest_onedrive(payload)

        path = f"/ingest/onedrive/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def ingest_sharepoint(self, host, site, token, client_id, oauth_secret, tenant_id, environment):

        payload = {
            "host": host,
            "site": site,
            "token": token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_ingest_sharepoint(payload)

        path = f"/ingest/sharepoint/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def get_status(self, datasource):

        payload = {
            "datasource": datasource 
        }

        validate_ingest_status(payload)

        path = f"/ingest/status/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def convert_email_to_datasource(self, email):
        return f"drive-{email.lower().replace('@', '-at-').replace('.', '-')}"

    def pdf_handler(self, local_filepath, document_df, filename):
        with open(f"{local_filepath}", 'rb') as book:            
            book_reader = PyPDF2.PdfReader(book)
            number_of_pages = len(book_reader.pages)
            page_list = book_reader.pages        
            for page in range(number_of_pages):
                paragraph_count={"count":0}
                extracted_page = page_list[page]    
                text = extracted_page.extract_text()            
                text = text.replace('\n \n', '\n\n')
                sections = text.split('\n\n')
                sections = list(filter(lambda x: x.strip() != '', sections))         
                section_count = [i+1 for i in range(len(sections))]                  
                page_df = pd.DataFrame({ "text": sections, "section": section_count })
                page_df['file'] = filename
                page_df['page'] = page+1
                page_df['text'] = page_df['text'].apply(lambda x: bytes(x.strip().replace("\n"," "), 'utf-8').decode('utf-8','ignore'))
                page_df['type'] = page_df['text'].apply(lambda x: "header" if len(x) < 100 else "paragraph")            
                page_df['paragraph'] = page_df['type'].apply(lambda x: self.count_paragraphs(x, paragraph_count))            
                
                document_df = pd.concat([document_df, page_df], axis='rows')
        return document_df

    def txt_handler(self, local_filepath, document_df, filename):
        with open(f"{local_filepath}", 'rb') as book:            
            book_reader = PyPDF2.PdfReader(book)
            number_of_pages = len(book_reader.pages)
            page_list = book_reader.pages        
            for page in range(number_of_pages):
                paragraph_count={"count":0}
                extracted_page = page_list[page]    
                text = extracted_page.extract_text()            
                text = text.replace('\n \n', '\n\n')
                sections = text.split('\n\n')
                sections = list(filter(lambda x: x.strip() != '', sections))         
                section_count = [i+1 for i in range(len(sections))]                  
                page_df = pd.DataFrame({ "text": sections, "section": section_count })
                page_df['file'] = filename
                page_df['page'] = int(page+1)
                page_df['text'] = page_df['text'].apply(lambda x: bytes(x.strip().replace("\n"," "), 'utf-8').decode('utf-8','ignore'))
                page_df['type'] = page_df['text'].apply(lambda x: "header" if len(x) < 200 else "paragraph")            
                page_df['paragraph'] = page_df['type'].apply(lambda x: self.count_paragraphs(x, paragraph_count))            
                
                document_df = pd.concat([document_df, page_df], axis='rows')
        return document_df

    def docx_handler(self, local_filepath, document_df, filename):
        doc = Document(local_filepath)
        paragraphs = 1
        sections = 1
        for paragraph in doc.paragraphs:
            text = paragraph.text
            section_type = "header" if len(text) < 200 else "paragraph"
            page_df = pd.DataFrame({ "text": [text], "section": [sections], "file": [filename], "page": [1], "type": [section_type], "paragraph": [paragraphs] })
            document_df = pd.concat([document_df, page_df], axis='rows')
            sections += 1
            if section_type != "header":
                paragraphs += 1
        return document_df

    def count_paragraphs(self, x, paragraph_count):
        if x == "header":
            if paragraph_count["count"] == 0:
                return 1
            return paragraph_count["count"]
        
        paragraph_count["count"] += 1
        return int(paragraph_count["count"])

    def process_document(self, local_filepath, document_name, extension):
        try:
            document_df = pd.DataFrame({"file":[], "page":[], "section":[], "text":[], "type":[], "paragraph": []})
            filename = f"{document_name.strip()}.{extension}"
            document_df = self.FILE_HANDLER[extension.lower()](local_filepath, document_df, filename)
            metafile = f"{local_filepath.replace(f'.{extension}','')}_meta.csv"
            document_df.reset_index(inplace=True, drop=True)
            document_df.to_csv(metafile, escapechar="\\", index=False)                
            return metafile
        except Exception as ex:
            return str(ex)