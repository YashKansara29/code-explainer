import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Configure standard logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the local .env file
load_dotenv()

# Initialize and validate the Gemini API configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY is missing from the environment variables.")
    raise ValueError("Critical configuration error: GEMINI_API_KEY not found.")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the FastAPI application instance with metadata
app = FastAPI(
    title="AI Code Explainer API",
    description="Backend service for analyzing and explaining Python code using the Gemini API.",
    version="1.0.0"
)

# Configure Cross-Origin Resource Sharing (CORS)
# This middleware is required to allow the browser frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Note: In a production environment, restrict this to your specific frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    """
    Data model for the incoming request payload.
    Enforces that the client sends a JSON object with a 'code' string.
    """
    code: str

@app.post("/explain")
async def explain_code(request: CodeInput):
    """
    Endpoint to process code submissions and return an AI-generated explanation.
    Returns a JSON object containing the Markdown-formatted explanation.
    """
    # Validate that the input string is not empty or composed solely of whitespace
    if not request.code.strip():
        logger.warning("Received an empty code submission from the client.")
        raise HTTPException(
            status_code=400, 
            detail="Payload validation failed: The 'code' field cannot be empty."
        )

    try:
        # Define the system prompt to enforce consistent formatting and behavior from the model
        system_instructions = """
        You are an expert software engineering tutor. Analyze the Python code provided by the user. 
        You must format your response using Markdown, utilizing exactly these three headings:
        ### Explanation
        ### Step-by-step breakdown
        ### Possible improvements
        """
        
        # Instantiate the Gemini model with the defined system instructions
        model = genai.GenerativeModel(
           model_name="gemini-2.5-flash",
            system_instruction=system_instructions
        )

        # Execute the API call
        # A low temperature (0.3) is used to ensure deterministic, logical, and highly accurate output
        response = model.generate_content(
            request.code,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3
            )
        )
        
        # Extract and return the generated text payload
        return {"result": response.text}

    except Exception as e:
        # Log the full exception for server-side debugging
        logger.error(f"Failed to generate content via Gemini API: {str(e)}")
        # Return a sanitized 500 status code to the client
        raise HTTPException(
            status_code=500, 
            detail="An internal server error occurred during code analysis."
        )