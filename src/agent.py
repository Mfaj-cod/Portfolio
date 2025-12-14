import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from .logg import logger
from .prompt import system_prompt

# Load Env
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# content
class ContentDraft(BaseModel):
    type: Literal['blog', 'project', 'about'] = Field(
        description="The type of content: 'blog' for articles, 'project' for project showcases, 'about' for personal bio."
    )
    title: str = Field(description="Title. For 'about', use 'About Me'.")
    content: str = Field(description="HTML content. For projects, describe features. For about, write the bio.")
    tags: str = Field(description="Comma-separated strings. Tech stack for projects, skills for about, topics for blogs.")

# Initialize model ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.7,
    api_key=GOOGLE_API_KEY
)

structured_llm = llm.with_structured_output(ContentDraft)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{topic}")
])

chain = prompt_template | structured_llm


def generate_blog_draft(topic: str):
    try:
        if not GOOGLE_API_KEY:
            return {"error": "API Key missing."}
        result = chain.invoke({"topic": topic})
        return result.dict()
    except Exception as e:
        logger.error(f"Agent error: {e}")
        return None