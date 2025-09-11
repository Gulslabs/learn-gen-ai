import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))




def get_gemini_response(prompt: str) -> str:    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)    
    print(f"Prompt Tokens: {model.count_tokens(prompt).total_tokens}")
    print(f"Response Tokens: {model.count_tokens(response.text).total_tokens}")
    return response.text

if __name__ == "__main__":
    user_question = input("\nEnter your question for Gemini: ")
    response = get_gemini_response(user_question)
    print("Gemini Response:", response)
