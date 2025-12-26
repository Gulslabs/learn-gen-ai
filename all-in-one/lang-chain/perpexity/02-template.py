import os
from langchain_core.prompts import PromptTemplate
from langchain_perplexity import ChatPerplexity
os.environ["PPLX_API_KEY"] = os.getenv("PERPLEXITY_API_KEY")
llm = ChatPerplexity(model="sonar", temperature=0)

template = """
Explain {concept} in simple and concise way
"""
prompt = PromptTemplate.from_template(template)
prompt_text = prompt.format(concept="Photosynthesis")
response = llm.invoke(prompt_text)
print(response.content)
print(prompt.invoke("Photosynthesis"))