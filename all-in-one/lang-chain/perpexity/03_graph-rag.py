"""
GraphRAG Implementation with Neo4j and LangChain
Building Knowledge-Grounded LLM Systems
"""

import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# LangChain imports
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_neo4j import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_text_splitters  import TokenTextSplitter
from langchain_neo4j import GraphCypherQAChain
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_perplexity import ChatPerplexity
from langchain_huggingface import HuggingFaceEmbeddings
class GraphRAGSystem:
    """Main class for GraphRAG system with Neo4j and LangChain"""
    
    def __init__(self):
        """Initialize the GraphRAG system with necessary connections"""
        load_dotenv()
        
        # Environment variables        
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "neo4j123")
        
        # Initialize connections
        self.graph = self._initialize_neo4j_connection()
        self.llm = self._initialize_llm()
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")      
        
        # Knowledge extraction prompt
        self.kg_prompt = self._create_knowledge_extraction_prompt()
        
    def _initialize_neo4j_connection(self) -> Neo4jGraph:
        """Initialize connection to Neo4j database"""
        print("Connecting to Neo4j...")
        graph = Neo4jGraph(
            url=self.neo4j_uri,
            username=self.neo4j_username,
            password=self.neo4j_password
        )
       
        # Stop and remove existing container
            # docker stop neo4j
            # docker rm neo4j

# # Run with APOC plugin enabled
        # docker run -d \
        #     --name neo4j \
        #     -p 7474:7474 -p 7687:7687 \
        #     -v neo4j_data:/my_neo4j/data \
        #     -v neo4j_logs:/my_neo4j/logs \
        #     -e NEO4J_AUTH=neo4j/neo4j123 \
        #     -e NEO4J_PLUGINS='["apoc"]' \
        #     neo4j:latest
        print("Successfully connected to Neo4j")
        return graph
    
    def _initialize_llm(self) -> ChatPerplexity:
        """Initialize Perplexity Generative AI LLM"""
        print("Initializing Perplexity LLM...")
        os.environ["PPLX_API_KEY"] = self.perplexity_api_key
        return ChatPerplexity(model="sonar", temperature=0.7)

    def _create_knowledge_extraction_prompt(self) -> PromptTemplate:
        """Create prompt template for knowledge extraction"""
        return PromptTemplate.from_template("""
Extract entities and relationships from the text.

Text: {text}

Return output strictly in this JSON format:
{{
    "entities": [
        {{"name": "...", "type": "..."}}
    ],
    "relationships": [
        {{"source": "...", "relation": "...", "target": "..."}}
    ]
}}
""")
    
    def extract_knowledge_from_text(self, text: str) -> Dict[str, Any]:
        """Extract entities and relationships from text using LLM"""
        print("Extracting knowledge from text...")
        response = self.llm.invoke(
            self.kg_prompt.format(text=text)
        )
        
        try:
            kg_data = json.loads(response.content)
            print(f"Extracted {len(kg_data.get('entities', []))} entities and {len(kg_data.get('relationships', []))} relationships")
            return kg_data
        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {e}")
            return {"entities": [], "relationships": []}
    
    def load_documents(self, documents: List[str]) -> List[Document]:
        """Load and chunk documents for processing"""
        print("Loading and chunking documents...")
        text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)
        
        doc_objects = [Document(page_content=doc) for doc in documents]
        chunked_docs = text_splitter.split_documents(doc_objects)
        
        print(f"Created {len(chunked_docs)} document chunks")
        return chunked_docs
    
    def build_knowledge_graph_from_documents(self, documents: List[Document]):
        """Build knowledge graph from documents using LLMGraphTransformer"""
        print("Building knowledge graph from documents...")
        
        # Initialize LLM Graph Transformer
        llm_transformer = LLMGraphTransformer(llm=self.llm)
        
        # Convert documents to graph documents
        graph_documents = llm_transformer.convert_to_graph_documents(documents)
        
        # Add to Neo4j
        self.graph.add_graph_documents(
            graph_documents,
            baseEntityLabel=True,
            include_source=True
        )
        
        print("Knowledge graph built successfully")
    
    def create_vector_index(self, index_name: str = "document_embeddings"):
        """Create vector index for semantic search"""
        print(f"Creating vector index: {index_name}...")
        
        vector_index = Neo4jVector.from_existing_graph(
            self.embeddings,
            search_type="hybrid",
            node_label="Document",
            text_node_properties=["text"],
            embedding_node_property="embedding",
            index_name=index_name,
            url=self.neo4j_uri,
            username=self.neo4j_username,
            password=self.neo4j_password
        )
        
        print("Vector index created successfully")
        return vector_index
    
    def setup_cypher_qa_chain(self, examples: List[Dict[str, str]] = None):
        """Setup GraphCypherQAChain for natural language querying"""
        print("Setting up Cypher QA chain...")
        
        # Default examples for few-shot learning
        if examples is None:
            examples = [
                {
                    "question": "How many entities are there?",
                    "query": "MATCH (n) RETURN count(n) as count"
                },
                {
                    "question": "What are the relationships?",
                    "query": "MATCH ()-[r]->() RETURN type(r) as relationship, count(r) as count"
                }
            ]
        
        # Create Cypher QA chain
        chain = GraphCypherQAChain.from_llm(
            graph=self.graph,
            llm=self.llm,
            verbose=True,
            allow_dangerous_requests=True
        )
        
        print("Cypher QA chain ready")
        return chain
    
    def query_graph_with_natural_language(self, question: str, chain: GraphCypherQAChain) -> str:
        """Query the knowledge graph using natural language"""
        print(f"\nQuerying: {question}")
        response = chain.invoke({"query": question})
        return response
    
    def hybrid_retrieval(self, question: str, vector_index: Neo4jVector, k: int = 3) -> List[str]:
        """Perform hybrid retrieval combining graph and vector search"""
        print(f"Performing hybrid retrieval for: {question}")
        
        # Vector similarity search
        semantic_docs = vector_index.similarity_search(question, k=k)
        semantic_facts = [doc.page_content for doc in semantic_docs]
        
        # Graph retrieval (simplified - can be extended with Cypher queries)
        graph_facts = []
        
        # Combine results
        combined_context = semantic_facts + graph_facts
        print(f"Retrieved {len(combined_context)} context items")
        
        return combined_context
    
    def generate_answer_with_context(self, question: str, context: List[str]) -> str:
        """Generate answer using LLM with retrieved context"""
        context_str = "\n".join(context)
        
        prompt = f"""Based on the following context, answer the question.

Context:
{context_str}

Question: {question}

Answer:"""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def build_knowledge_graph_manual(self, text: str):
        """Manually build knowledge graph using extract_knowledge_from_text method"""
        print("Building knowledge graph manually from text...")
        
        # Extract knowledge using LLM
        kg_data = self.extract_knowledge_from_text(text)
        
        # Create entities
        for entity in kg_data.get("entities", []):
            entity_name = entity.get("name")
            entity_type = entity.get("type", "Entity")
            
            query = f"""
            MERGE (e:{entity_type} {{name: $name}})
            RETURN e
            """
            self.graph.query(query, params={"name": entity_name})
        
        # Create relationships
        for rel in kg_data.get("relationships", []):
            source = rel.get("source")
            relation = rel.get("relation", "RELATED_TO").upper().replace(" ", "_")
            target = rel.get("target")
            
            query = f"""
            MATCH (s {{name: $source}})
            MATCH (t {{name: $target}})
            MERGE (s)-[r:{relation}]->(t)
            RETURN r
            """
            self.graph.query(query, params={"source": source, "target": target})
        
        print("Manual knowledge graph built successfully")
    
    def load_sample_data(self):
        """Load sample data into Neo4j for demonstration"""
        print("Loading sample data...")
        
        sample_query = """
        MERGE (neo4j:Technology {name: 'Neo4j'})
        SET neo4j.type = 'Graph Database'
        
        MERGE (langchain:Technology {name: 'LangChain'})
        SET langchain.type = 'Framework'
        
        MERGE (graphrag:Concept {name: 'GraphRAG'})
        SET graphrag.type = 'Architecture'
        
        MERGE (llm:Technology {name: 'LLM'})
        SET llm.type = 'AI Model'
        
        MERGE (langchain)-[:INTEGRATES_WITH]->(neo4j)
        MERGE (graphrag)-[:USES]->(neo4j)
        MERGE (graphrag)-[:USES]->(langchain)
        MERGE (graphrag)-[:IMPROVES]->(llm)
        """
        
        self.graph.query(sample_query)
        print("Sample data loaded successfully")


def main():
    """Main execution function"""
    print("=" * 60)
    print("GraphRAG System with Neo4j and LangChain")
    print("=" * 60)
    
    # Initialize system
    system = GraphRAGSystem()
    
    # Sample documents
    documents = [
        """
        Neo4j is a graph database used by enterprises worldwide.
        LangChain integrates Neo4j for GraphRAG applications.
        GraphRAG improves multi-hop reasoning in Large Language Models.
        """,
        """
        Knowledge graphs store information as entities and relationships.
        This structured representation enables better context retrieval.
        GraphRAG combines semantic similarity with graph traversal.
        """
    ]
    
    # Process documents
    print("\n" + "=" * 60)
    print("STEP 1: Loading and Processing Documents")
    print("=" * 60)
    chunked_docs = system.load_documents(documents)
    
    # Build knowledge graph (Method 1: Automated)
    print("\n" + "=" * 60)
    print("STEP 2: Building Knowledge Graph (Automated)")
    print("=" * 60)
    system.build_knowledge_graph_from_documents(chunked_docs)
    
    # Build knowledge graph (Method 2: Manual extraction)
    # print("\n" + "=" * 60)
    # print("STEP 2b: Building Knowledge Graph (Manual)")
    # print("=" * 60)
    # sample_text = """
    # OpenAI develops GPT models. GPT-4 is used in ChatGPT.
    # Microsoft partners with OpenAI. Azure hosts OpenAI services.
    # """
    # system.build_knowledge_graph_manual(sample_text)
    
    # Load sample data
    print("\n" + "=" * 60)
    print("STEP 3: Loading Sample Data")
    print("=" * 60)
    system.load_sample_data()
    
    # Create vector index
    print("\n" + "=" * 60)
    print("STEP 4: Creating Vector Index")
    print("=" * 60)
    vector_index = system.create_vector_index()
    
    # Setup QA chain
    print("\n" + "=" * 60)
    print("STEP 5: Setting up QA Chain")
    print("=" * 60)
    qa_chain = system.setup_cypher_qa_chain()
    
    # Query examples
    print("\n" + "=" * 60)
    print("STEP 6: Querying the Knowledge Graph")
    print("=" * 60)
    
    questions = [
        "What is Neo4j used for?",
        "How does GraphRAG improve LLMs?",
        "What technologies are connected to LangChain?"
    ]
    
    for question in questions:
        try:
            response = system.query_graph_with_natural_language(question, qa_chain)
            print(f"\nQ: {question}")
            print(f"A: {response.get('result', 'No answer generated')}")
            print("-" * 60)
        except Exception as e:
            print(f"Error processing question: {e}")
    
    print("\n" + "=" * 60)
    print("GraphRAG Pipeline Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()