import os
import re
import nest_asyncio
from dotenv import load_dotenv
from markdownify import markdownify
import fitz  # PyMuPDF
from langchain_upstage import UpstageDocumentParseLoader

load_dotenv()
nest_asyncio.apply()

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# 파서 설정
parser = LlamaParse(
    result_type="markdown",  # "markdown"과 "text" 사용 가능
    num_workers=8,  # worker 수 (기본값: 4)
    verbose=True,
    language="ko",
)

# SimpleDirectoryReader를 사용하여 파일 파싱
file_extractor = {".pdf": parser}

documents = SimpleDirectoryReader(
    input_files=["example_pdf.pdf"],
    file_extractor=file_extractor,
).load_data()

# 각 페이지별로 Markdown 파일로 저장
output_dir = "parsed_pages"
os.makedirs(output_dir, exist_ok=True)

def remove_headers_and_footers(text):
    # 정규식을 사용하여 불필요한 헤더와 푸터 제거
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        # 헤더와 푸터로 간주되는 특정 패턴을 제거 (예: 페이지 번호, 문서 제목, 저작권 정보 등)
        if not re.match(r'^(Page \d+|Document Title|Footer Text|Copyright|Licensed to:|Issue Ref:)', line, re.IGNORECASE):
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def extract_tables_and_figures_with_upstage(pdf_path):
    loader = UpstageDocumentParseLoader(
        pdf_path,
        split="page",
        use_ocr=True,
        exclude=["header", "footer"],
    )
    documents = loader.load()
    elements = []

    for doc in documents:
        for element in doc.chunks:
            if element.type == "table":
                elements.append({
                    "type": "table",
                    "page": doc.metadata["page_number"],
                    "html": markdownify(element.text)
                })
            elif element.type == "figure":
                elements.append({
                    "type": "figure",
                    "page": doc.metadata["page_number"],
                    "html": f'<figure><img src="{element.src}" alt="Figure from page {doc.metadata["page_number"]}"></figure>'
                })

    return elements

# PDF에서 이미지와 도표에 대한 메타데이터 추출
pdf_path = "example_pdf.pdf"
elements_metadata = extract_tables_and_figures_with_upstage(pdf_path)

for i, doc in enumerate(documents):
    cleaned_text = remove_headers_and_footers(doc.text)
    # Markdownify를 사용하여 HTML 같은 텍스트를 더 예쁜 Markdown으로 변환
    markdown_text = markdownify(cleaned_text)
    
    # 도표 및 이미지 정보를 HTML로 추가
    for element in elements_metadata:
        if element["page"] == i + 1:
            markdown_text += f"\n\n{element['html']}\n"

    output_path = os.path.join(output_dir, f"page_{i+1}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_text + "\n\n")
    print(f"페이지 {i+1}의 데이터가 {output_path}에 저장되었습니다.")
    