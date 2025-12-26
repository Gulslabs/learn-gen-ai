import os
import pandas as pd
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_perplexity import ChatPerplexity

os.environ["PPLX_API_KEY"] = os.getenv("PERPLEXITY_API_KEY")
llm = ChatPerplexity(model="sonar", temperature=0)

examples = [{
    "question": "Who is the president of India?",
    "answer": "The president of India is Pranab Mukherjee"
}, {
    "question": "Who is the current Union Home Minister of India?",
    "answer": "The current union home minister of India is Amit Shah"
}]

examples = pd.DataFrame(examples)
examples = examples.to_dict("records")

# Define the template for each example
prompt_template = PromptTemplate.from_template("""
Question: {question}
Answer: {answer}
""")

few_shot_prompt_template_strict = FewShotPromptTemplate(
    examples=examples,
    example_prompt=prompt_template,
    suffix="""Question: {input}
Answer: """,
    input_variables=["input"],
    prefix="""Follow these examples exactly. Your answer should:
1. Be a single sentence
2. Start with the same pattern as the examples
3. Contain no bold text, no references, no citations
4. Be simple and direct
Examples:"""
)
# Using the more explicit version
chain = few_shot_prompt_template_strict | llm
print("\n" + "="*50 + "\n")
print(chain.invoke({"input": "Who is the president of India?"}).content)
print("\n" + "="*50 + "\n")