# Perplexity API Demo Response

The Perplexity API is a RESTful interface for conversational AI that stands out for its **real-time web search capabilities, source citations, and compatibility with OpenAI’s Chat Completions format**[5][3][2]. It enables developers to build applications that deliver up-to-date, trustworthy information, and supports a range of specialized models for different use cases.

**Key Features:**

- **Real-Time Search & Citations:** Perplexity models can access and retrieve current information from the web, providing responses with source attributions for transparency and trust[5][3].
- **Multiple Specialized Models:** Options include models like **sonar-pro** (advanced search and reasoning), **sonar-reasoning-pro** (chain-of-thought reasoning), **sonar-deep-research** (in-depth research), and offline models like **r1-1776** for tasks not requiring web search[3][5].
- **Streaming Responses:** The API supports streaming, allowing applications to display responses incrementally as they are generated, improving user experience in real-time chat interfaces[1].
- **Structured Output:** Supports structured data formats, making it easier to integrate with various applications[3].
- **Parameter Customization:** Developers can adjust parameters such as **temperature** (controls randomness), **max_tokens** (response length), and others for fine-tuned outputs[1][5].
- **OpenAI Compatibility:** The API uses the same format as OpenAI’s Chat Completions, so existing OpenAI client libraries can be used with minimal changes—just point them to the Perplexity endpoint[2][5].

**How to Use the Perplexity API:**

1. **Get an API Key:** Sign up at Perplexity and obtain your API key from your account settings[3][4].
2. **Set Up Authentication:** Pass the API key as a header or environment variable (e.g., `PERPLEXITY_API_KEY`)[3].
3. **Choose a Model:** Select the appropriate model for your use case (e.g., `sonar-pro` for advanced search, `sonar-reasoning-pro` for complex reasoning)[3][5].
4. **Format Requests:** Use the OpenAI Chat Completions format for your requests. For example, in Python:
   ```python
   response = openai.ChatCompletion.create(
       model="sonar-pro",
       messages=messages,
       api_base="https://api.perplexity.ai/v1",
       api_ke

## Citations
1. https://blog.neelbuilds.com/comprehensive-guide-on-using-the-perplexity-api
2. https://docs.perplexity.ai/getting-started/quickstart
3. https://www.promptfoo.dev/docs/providers/perplexity/
4. https://www.youtube.com/watch?v=sl2YNoJbEcg
5. https://zuplo.com/blog/2025/03/28/perplexity-api
