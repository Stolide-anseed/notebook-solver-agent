from langchain_core.messages import HumanMessage
from src.preprocessing import preprocess_text
from src.ingestion import extract_text_from_pdf
from src.text_splitter import splitter_text
from src.generetor_promt import generator
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
load_dotenv()

class ResearchRespons(BaseModel):
    question: str
    summary: str
    sources: list[str]
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object=ResearchRespons)




llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                             api_key='AIzaSyA1Lpv7I_-vYOe1tAM5XC5qa0kZHI4Cay4')

raw_text = extract_text_from_pdf("data/raw/3_BASIC_ML.pdf")
clean_text = preprocess_text(raw_text).lower()

question = splitter_text(clean_text)

promt = generator()

agent = create_agent(model = llm)

raw_response = agent.invoke({
    "messages": [
        HumanMessage(content=question)
    ]
})

text = raw_response["messages"][-1].content

structured_response = parser.parse(text)
print(structured_response)