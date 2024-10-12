'''
이 단계에서는 사용자의 질문 그리고 질문과 관련된 문서를 받아서 질문에 대한 답변을 생성하는 프롬프트를 작성합니다.
RAG에서 가장 중요한 단계임
'''

from dotenv import load_dotenv
from langchain_teddynote import logging
import os
from langchain_openai import ChatOpenAI
from langchain_teddynote.messages import stream_response  # 스트리밍 출력
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate



os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "LangChain-test-dongik"
os.environ["LANGCHAIN_API_KEY"] = "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"

logging.langsmith("LangChain-test-dongik")

load_dotenv()

prompt = PromptTemplate.from_template("{topic} 에 대해 쉽게 설명해주세요.")

model = ChatOpenAI(
    model="gpt-4o",
    max_tokens=2048,
    temperature=0.1,
)


#==============================================================

#1. 프롬프트 생성 방법 1: 프롬프트 템플릿 사용 (PromptTemplate)
#from_template() 메소드를 사용하여 PromptTemplate 객체 생성
# topic = "김정은"

# prompt = PromptTemplate.from_template("{topic} 에 대해 쉽게 설명해주세요.")

# #print(prompt.format(topic=topic))

# chain = prompt | model

# answer = chain.invoke({"topic": topic})

# print(answer)



#==============================================================

#이 부분에 실제로 가장 관련 있는 텍스트 청크를 넣어줌

texts = "민동익이란 학생은 2001년 7월 3일에 태어났고 서울에서 태어났습니다. 그는 1녀2남 중에서 제일 막내입니다."
template = "다음 텍스트를 보고 민동익이란 학생이 형이 있는 지 없는 지 알려주세요. 텍스트: {texts}"
prompt = PromptTemplate.from_template(
    template
)

chain = prompt | model

answer = chain.invoke({"texts": texts}).content

print(answer)

#==============================================================

#방법 2. PromptTemplate 객체 생성과 동시에 prompt 생성

# template = "다음 텍스트를 보고 민동익이란 학생이 형이 있는 지 없는 지 알려주세요. 텍스트: {texts}"
# prompt = PromptTemplate(input_variables=["texts"], template=template)

# chain = prompt | model

# answer = chain.invoke({"texts": texts}).content

# print(answer)

# template 정의
template = "{country}의 수도는 어디인가요?"

# PromptTemplate 객체를 활용하여 prompt_template 생성
prompt = PromptTemplate(
    template=template,
    input_variables=["country"],
)

prompt.format(country="대한민국")


#==============================================================

template2 = "{country1}과 {country2}의 수도는 각각 어디인가요?"

# PromptTemplate 객체를 활용하여 prompt_template 생성
prompt2 = PromptTemplate(
    template=template2,
    input_variables=["country1"],
    partial_variables={
        "country2": "미국"  # dictionary 형태로 partial_variables를 전달
    },
)

#partial_variables: 부분 변수 채움



