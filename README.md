# Perplexity API Chatbot

A Python chatbot that uses Perplexity's Sonar API to provide web search-powered conversational AI.

## Features

- 🔍 **Web Search Integration**: Powered by Perplexity's real-time web search
- 📚 **Citations**: Automatic source citations for factual information
- 💬 **Conversation Memory**: Maintains conversation history
- ❓ **Related Questions**: Suggests follow-up questions
- ⚙️ **Configurable**: Customizable parameters for different use cases
- 🎯 **OpenAI Compatible**: Uses familiar OpenAI client library

## Setup

### 1. Get Your API Key

1. Visit [Perplexity AI Settings](https://www.perplexity.ai/settings/api)
2. Generate an API key
3. Copy the key for use in step 2

### 2. Set Up Environment Variables

Create a `.env` file in the project root and add your API key:

```env
SONAR_API_KEY=your-api-key-here
```

**Alternative: Set as system environment variable**

**Windows PowerShell:**
```powershell
$env:SONAR_API_KEY="your-api-key-here"
```

**Windows Command Prompt:**
```cmd
set SONAR_API_KEY=your-api-key-here
```

**Linux/macOS:**
```bash
export SONAR_API_KEY="your-api-key-here"
```

### 3. Install Dependencies

```bash
pip install openai python-dotenv
```

Or if using uv (recommended):
```bash
uv sync
```

## Usage

### Interactive Chat

Run the chatbot in interactive mode:

```bash
python main.py
```

Commands while chatting:
- `quit` or `exit` - Exit the chatbot
- `clear` - Clear conversation history
- `config` - Show current configuration

### Programmatic Usage

```python
from main import PerplexityChatbot

# Initialize chatbot
chatbot = PerplexityChatbot()  # Uses SONAR_API_KEY from .env file
# Or pass API key directly:
# chatbot = PerplexityChatbot(api_key="your-api-key")

# Set a custom system prompt
chatbot.set_system_prompt("You are a helpful research assistant.")

# Chat with the bot
response = chatbot.chat("What are the latest developments in AI?")

# Print formatted response
chatbot.print_response(response)

# Access response data
print(response["message"])          # Main response
print(response["citations"])        # Source URLs
print(response["related_questions"]) # Follow-up questions
```

### Configuration Options

Customize the chatbot behavior:

```python
chatbot.update_config(
    model="sonar-reasoning",  # or "sonar-pro"
    temperature=0.2,          # Lower = more focused
    max_tokens=1500,          # Longer responses
    search_mode="academic",   # "web" or "academic"
    return_citations=True,
    return_related_questions=True
)
```

### Advanced Parameters

You can also pass parameters directly to individual chat calls:

```python
response = chatbot.chat(
    "Tell me about quantum computing",
    search_domain_filter=["arxiv.org", "nature.com"],  # Limit to specific domains
    search_recency_filter="month",                      # Recent content only
    temperature=0.1                                     # Override default temperature
)
```

## Available Models

- `sonar-pro` - Fast, general-purpose model (default)
- `sonar-reasoning` - More thorough reasoning capabilities

## Response Structure

Each response contains:

```python
{
    "message": "The main AI response text",
    "model": "sonar-pro",
    "usage": {
        "prompt_tokens": 50,
        "completion_tokens": 200,
        "total_tokens": 250
    },
    "citations": [
        "https://example.com/source1",
        "https://example.com/source2"
    ],
    "search_results": [...],  # Detailed search result objects
    "related_questions": [
        "What are the applications of quantum computing?",
        "How does quantum computing differ from classical computing?"
    ]
}
```

## Example Use Cases

### Research Assistant
```python
chatbot.set_system_prompt(
    "You are a research assistant. Provide comprehensive, well-sourced answers with academic rigor."
)
chatbot.update_config(search_mode="academic", temperature=0.2)
```

### News Summarizer
```python
chatbot.set_system_prompt(
    "You are a news analyst. Provide balanced, factual summaries of current events."
)
chatbot.update_config(search_recency_filter="day", return_citations=True)
```

### Technical Support
```python
chatbot.set_system_prompt(
    "You are a technical support specialist. Provide step-by-step solutions with relevant documentation."
)
chatbot.update_config(search_domain_filter=["docs.python.org", "stackoverflow.com"])
```

## Error Handling

The chatbot handles common errors gracefully:

- **Missing API Key**: Clear instructions on how to set it up
- **API Rate Limits**: Automatic retry with exponential backoff
- **Network Issues**: Graceful error messages

## Contributing

Feel free to submit issues and pull requests to improve the chatbot!

## License

This project is open source. Check the repository for license details.