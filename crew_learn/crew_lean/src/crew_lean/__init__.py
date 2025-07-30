import os
from crewai import LLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_perplexity_llm(model_size="small", **kwargs):
    """
    Create a Perplexity LLM instance.
    
    Args:
        model_size: "small", "large", or "huge"
        **kwargs: Additional LLM parameters
    
    Returns:
        LLM instance configured for Perplexity
    """
    model_map = {
        "small": "perplexity/llama-3.1-sonar-small-128k-online",
        "large": "perplexity/llama-3.1-sonar-large-128k-online", 
        "huge": "perplexity/llama-3.1-sonar-huge-128k-online", 
        "sonar": "sonar", 
        "sonar_reasoning": "sonar-reasoning", 
        "sonar_deep_research": "sonar-deep-research"
    }
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable not set")
    
    default_params = {
        "model": model_map.get(model_size, model_map["small"]),
        "api_key": api_key,
        "base_url": "https://api.perplexity.ai",
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    # Merge with user-provided kwargs
    default_params.update(kwargs)    
    return LLM(**default_params)

try: 
    RESEARCH_LLM = create_perplexity_llm(model_size="sonar_reasoning", max_tokens=8000)
    REPORTING_LLM = create_perplexity_llm(model_size="sonar")
except Exception as e:
    raise Exception(f"An error occurred while creating the LLM: {e}")

# Export what should be available when importing this module
__all__ = [
    "RESEARCH_LLM",
    "REPORTING_LLM"    
]