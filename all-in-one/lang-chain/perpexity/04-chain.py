import os
from langchain_core.prompts import PromptTemplate
from langchain_perplexity import ChatPerplexity
os.environ["PPLX_API_KEY"] = os.getenv("PERPLEXITY_API_KEY")
llm = ChatPerplexity(model="sonar", temperature=0)

template = """
Explain {concept} in simple and concise way
"""
prompt = PromptTemplate.from_template(template)
# print(prompt.invoke("Prompting LLM"))

chain = prompt | llm
print(chain.invoke({"concept": "Prompting LLM"}).content)

