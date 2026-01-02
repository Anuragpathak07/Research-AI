# services/llm_service.py
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")  # RTX 3050 6GB should handle llama3 fine

class LLMService:
    def _check_ollama_connection(self):
        """Check if Ollama is accessible"""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            response.raise_for_status()
            return True
        except:
            return False
    
    def generate(self, prompt, temperature=0.3):
        """Generate text using Ollama LLM"""
        # Check connection first
        if not self._check_ollama_connection():
            raise ConnectionError(f"Ollama is not accessible at {OLLAMA_BASE_URL}. Please ensure Ollama is running.")
        
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature
                    }
                },
                timeout=60  # Reduced from 120 to 60 seconds for faster failure
            )
            response.raise_for_status()
            result = response.json()
            response_text = result.get("response", "")
            
            if not response_text or len(response_text.strip()) < 10:
                raise ValueError("Received empty or invalid response from Ollama")
            
            return response_text
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Ollama request timed out after 120 seconds. Check if the model '{OLLAMA_MODEL}' is available.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Could not connect to Ollama at {OLLAMA_BASE_URL}. Please ensure Ollama is running.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Model '{OLLAMA_MODEL}' not found. Please ensure the model is installed: ollama pull {OLLAMA_MODEL}")
            elif e.response.status_code == 500:
                error_text = e.response.text
                # Check for CUDA/GPU memory errors
                if "CUDA" in error_text or "buffer" in error_text or "memory" in error_text.lower():
                    raise ValueError(
                        f"GPU memory allocation failed. The model '{OLLAMA_MODEL}' requires more GPU memory than available.\n\n"
                        f"Solutions:\n"
                        f"1. Use a smaller model: Set OLLAMA_MODEL to a smaller model (e.g., 'llama3:8b' or 'mistral')\n"
                        f"2. Use CPU mode: Restart Ollama with CPU-only mode\n"
                        f"3. Free GPU memory: Close other applications using GPU\n"
                        f"4. Check available models: Run 'ollama list' to see installed models\n\n"
                        f"Original error: {error_text}"
                    )
                else:
                    raise ValueError(f"Ollama server error (500): {error_text}\n\nPlease check if Ollama is running properly: ollama serve")
            else:
                raise ValueError(f"HTTP error from Ollama: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Unexpected error calling Ollama: {str(e)}")
