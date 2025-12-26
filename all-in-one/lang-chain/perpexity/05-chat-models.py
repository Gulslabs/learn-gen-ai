import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_perplexity import ChatPerplexity
os.environ["PPLX_API_KEY"] = os.getenv("PERPLEXITY_API_KEY")
llm = ChatPerplexity(model="sonar", temperature=0)
prompt_template = ChatPromptTemplate.from_messages([("system", "You are a Calculator that responds to math_problem. Provide Just the answer no other text"), 
("human", "Answer this math problem: What is two plus two?"),
("ai", "2+2=4"), 
("human", "Answer this math problem: {math_problem}"),
]
)
chain = prompt_template | llm
print(chain.invoke({"math_problem": "What is 487 multiply by 632?"}).content)

