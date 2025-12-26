
`pip install -qU langchain-text-splitters langchain-community langgraph langchain-openai langchain-core`

Goal: **Build Q&A for https://lilianweng.github.io/posts/2023-06-23-agent/ with Langchain and RAG**

Install: 
`pip install -qU langchain-text-splitters langchain-community langgraph langchain-openai langchain-core`

Step 1: Setup Model:<br/>
	```
		import getpass
		import os
		if not os.environ.get("PPLX_API_KEY"):
		  os.environ["PPLX_API_KEY"] = getpass.getpass("Enter API key for Perplexity: ")
		from langchain.chat_models import init_chat_model
		llm = init_chat_model("llama-3.1-sonar-small-128k-online", model_provider="perplexity")        
	```

Step 2: Choose Embeddings: 
	```
    	import getpass
		import os
		if not os.environ.get("OPENAI_API_KEY"):
		  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

		from langchain_openai import OpenAIEmbeddings
		embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
	```

Step 3: Select VectorStore(In Memory for now):
	```
		from langchain_core.vectorstores import InMemoryVectorStore
		vector_store = InMemoryVectorStore(embeddings)```
	```
Step 4: Load and Chunk Content: 
	```
		import bs4
		from langchain_community.document_loaders import WebBaseLoader
		from langchain_core.documents import Document
		loader = WebBaseLoader(
   		web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    	bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        		)
    		),
			)
		docs = loader.load()
	```
Step 5: Split the text and Index Chunk:
	```
		text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
		all_splits = text_splitter.split_documents(docs)
		# Index Chunks
		_ = vector_store.add_documents(documents=all_splits)
	```
Step 6: Chose a Prompt
	```
		# Define prompt for question-answering
		# N.B. for non-US LangSmith endpoints, you may need to specify
		# api_url="https://api.smith.langchain.com" in hub.pull.
		prompt = hub.pull("rlm/rag-prompt")
	```
Step 7: Define State and Steps for LangGraph. 
	```
	# state
	class State(TypedDict):
	    question: str
	    context: List[Document]
	    answer: str

	# steps
		def retrieve(state: State):
		    retrieved_docs = vector_store.similarity_search(state["question"])
		    return {"context": retrieved_docs}


		def generate(state: State):
		    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
		    messages = prompt.invoke({"question": state["question"], "context": docs_content})
		    response = llm.invoke(messages)
		    return {"answer": response.content}
	```

Step 8: Compile all of it. 
	```
		graph_builder = StateGraph(State).add_sequence([retrieve, generate])
		graph_builder.add_edge(START, "retrieve")
		graph = graph_builder.compile()
	```
Step 9: Answer the Questions. 
	```
		response = graph.invoke({"question": "What is Task Decomposition?"})
		print(response["answer"])

	```