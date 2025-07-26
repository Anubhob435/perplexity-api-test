import os
from openai import OpenAI
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PerplexityChatbot:
    def __init__(self, api_key: str = None):
        """
        Initialize the Perplexity chatbot.
        
        Args:
            api_key: Your Perplexity API key. If not provided, will look for SONAR_API_KEY env var.
        """
        if api_key is None:
            api_key = os.getenv('SONAR_API_KEY')
            if not api_key:
                raise ValueError("API key is required. Set SONAR_API_KEY in .env file or pass it directly.")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        
        # Initialize conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
        # Default configuration
        self.config = {
            "model": "sonar-pro",
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": False
        }
    
    def set_system_prompt(self, system_prompt: str):
        """Set or update the system prompt for the chatbot."""
        # Remove existing system message if any
        self.conversation_history = [msg for msg in self.conversation_history if msg["role"] != "system"]
        # Add new system message at the beginning
        self.conversation_history.insert(0, {"role": "system", "content": system_prompt})
    
    def update_config(self, **kwargs):
        """Update chatbot configuration parameters."""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
            else:
                print(f"Warning: Unknown configuration parameter '{key}'")
    
    def chat(self, user_message: str, **additional_params) -> Dict[str, Any]:
        """
        Send a message to the chatbot and get a response.
        
        Args:
            user_message: The user's message
            **additional_params: Additional parameters to override default config
            
        Returns:
            Dictionary containing the response and metadata
        """
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Merge default config with any additional parameters
        request_params = {**self.config, **additional_params}
        request_params["messages"] = self.conversation_history
        
        try:
            # Make the API call
            response = self.client.chat.completions.create(**request_params)
            
            # Extract the assistant's response
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # Prepare response data
            response_data = {
                "message": assistant_message,
                "model": response.model,
                "usage": response.usage,
                "citations": getattr(response, 'citations', []),
                "search_results": getattr(response, 'search_results', []),
                "related_questions": getattr(response, 'related_questions', [])
            }
            
            return response_data
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return {"error": str(e)}
    
    def clear_history(self):
        """Clear the conversation history but keep system prompt if any."""
        system_messages = [msg for msg in self.conversation_history if msg["role"] == "system"]
        self.conversation_history = system_messages
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()
    
    def print_response(self, response_data: Dict[str, Any]):
        """Pretty print the chatbot response."""
        if "error" in response_data:
            print(f"❌ Error: {response_data['error']}")
            return
        
        print("\n" + "="*60)
        print("🤖 Perplexity Assistant Response:")
        print("="*60)
        print(response_data["message"])
        
        if response_data.get("citations"):
            print("\n📚 Citations:")
            for i, citation in enumerate(response_data["citations"], 1):
                print(f"  {i}. {citation}")
        
        if response_data.get("related_questions"):
            print("\n❓ Related Questions:")
            for i, question in enumerate(response_data["related_questions"], 1):
                print(f"  {i}. {question}")
        
        if response_data.get("usage"):
            usage = response_data["usage"]
            print(f"\n📊 Token Usage: {usage.total_tokens} total ({usage.prompt_tokens} prompt + {usage.completion_tokens} completion)")
        
        print("="*60)

def interactive_chat():
    """Run an interactive chat session with the Perplexity chatbot."""
    print("🚀 Perplexity Chatbot")
    print("Type 'quit' to exit, 'clear' to clear history, 'config' to show current config")
    print("-" * 60)
    
    try:
        # Initialize chatbot
        chatbot = PerplexityChatbot()
        
        # Set a default system prompt
        chatbot.set_system_prompt(
            "You are a helpful AI assistant powered by Perplexity's web search capabilities. "
            "Provide accurate, up-to-date information with proper citations when possible."
        )
        
        while True:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'clear':
                chatbot.clear_history()
                chatbot.set_system_prompt(
                    "You are a helpful AI assistant powered by Perplexity's web search capabilities. "
                    "Provide accurate, up-to-date information with proper citations when possible."
                )
                print("🧹 Conversation history cleared!")
                continue
            elif user_input.lower() == 'config':
                print(f"\n⚙️  Current Configuration:")
                for key, value in chatbot.config.items():
                    print(f"  {key}: {value}")
                continue
            elif not user_input:
                continue
            
            # Get response from chatbot
            response = chatbot.chat(user_input)
            chatbot.print_response(response)
    
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 To fix this:")
        print("1. Get your API key from https://www.perplexity.ai/settings/api")
        print("2. Add it to your .env file: SONAR_API_KEY=your-api-key-here")
        print("3. Or pass it directly when creating the chatbot")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    interactive_chat()