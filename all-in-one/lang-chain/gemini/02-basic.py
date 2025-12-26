import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Setup API Key
# Get your key from https://aistudio.google.com/
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# 2. Initialize Gemini Pro Model
# "gemini-pro" is the standard text model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # or "gemini-pro"    
    temperature=0.7
)
# 3. Create a Prompt Template
# This allows you to programmatically change the 'topic'
template = """
You are a technical expert. Explain the concept of {topic} 
to a 20-year-old using an analogy involving a sports game.
"""

prompt = PromptTemplate.from_template(template)

# 4. Create a Chain (using LCEL syntax)
# Prompt -> LLM -> Output Parser (makes the output a clean string)
chain = prompt | llm | StrOutputParser()

# 5. Invoke the chain programmatically
response = chain.invoke({"topic": "blockchain technology"})

print(response)