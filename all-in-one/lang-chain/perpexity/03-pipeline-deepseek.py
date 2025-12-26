from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


model_id = "deepseek-ai/deepseek-coder-6.7b-instruct"  # WILL REQUIRE 10 GB  OF HARD DISK SPACE
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=128
)

llm = HuggingFacePipeline(pipeline=pipe)

# Use in LangChain
response = llm.invoke("Explain quantum computing simply.")
print(response)