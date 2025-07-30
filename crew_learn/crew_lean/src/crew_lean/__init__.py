import os
from crewai import LLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_perplexity_llm(modelName="sonar", **kwargs):
    """
    Create a Perplexity LLM instance.
    
    Args:
        modelName: "sonar", "sonar_reasoning", or "sonar_deep_research"
        **kwargs: Additional LLM parameters
    
    Returns:
        LLM instance configured for Perplexity
    """
    model_map = {       
        "sonar": "sonar", 
        "sonar_reasoning": "sonar-reasoning", 
        "sonar_deep_research": "sonar-deep-research"
    }
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable not set")
    
    default_params = {
        "model": model_map.get(modelName, model_map["sonar"]),
        "api_key": api_key,
        "base_url": "https://api.perplexity.ai",
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    # Merge with user-provided kwargs
    default_params.update(kwargs)    
    return LLM(**default_params)

try: 
    RESEARCH_LLM = create_perplexity_llm(modelName="sonar_reasoning", max_tokens=8000)
    REPORTING_LLM = create_perplexity_llm(modelName="sonar")
except Exception as e:
    raise Exception(f"An error occurred while creating the LLM: {e}")

# Export what should be available when importing this module
__all__ = [
    "RESEARCH_LLM",
    "REPORTING_LLM"    
]