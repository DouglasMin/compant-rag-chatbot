# UpstageLayoutAnalysisLoader

import os
import nest_asyncio
from dotenv import load_dotenv
from langchain_teddynote import logging
from langchain_upstage import UpstageDocumentParseLoader

load_dotenv()
nest_asyncio.apply()

logging.langsmith("LangChain-test-upstage-loaded")

# 파일 경로
file_path = "example_pdf.pdf"
output_md_path = "output.md"  # Path to save the Markdown file

# 문서 로더 설정
loader = UpstageDocumentParseLoader(file_path)

pages = loader.load()  # or loader.lazy_load()
with open(output_md_path, 'w', encoding='utf-8') as md_file:
    for page in pages:
        md_file.write(f"# Page\n{page}\n\n")