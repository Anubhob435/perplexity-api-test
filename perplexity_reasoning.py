import os
from openai import OpenAI
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.getenv("SONAR_API_KEY")
if not API_KEY:
    raise RuntimeError("SONAR_API_KEY not set. Add it to your environment or .env file.")

# Initialize OpenAI client for Perplexity
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.perplexity.ai"
)


def perplexity_reasoning(query=None):
    """
    Conduct complex reasoning analysis using Perplexity's sonar-reasoning-pro model.
    
    Args:
        query (str, optional): Reasoning query. If None, uses default fusion energy query.
    
    Returns:
        str: The reasoning response content
    """

    if query is None:
        query = "Analyze the feasibility of fusion energy becoming a mainstream power source by 2040."
    
    response = client.chat.completions.create(
        model="sonar-reasoning-pro",
        messages=[
            {"role": "user", "content": query}
        ],
        max_tokens=2048,  # Reasoning typically needs more tokens for detailed analysis
        temperature=0.2,  # Low temperature for logical reasoning
        stream=False
    )
    
    content = response.choices[0].message.content
    
    # Print the response
    print("\n--- Perplexity Reasoning Pro Response ---\n")
    print(content)
    
    # Print citations if available
    citations = getattr(response, 'citations', None)
    if citations:
        print("\nCitations:")
        for i, url in enumerate(citations, 1):
            print(f"  {i}. {url}")
    
    # Save response to markdown file
    md_filename = "perplexity_reasoning_response.md"
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write("# Perplexity Reasoning Pro Analysis\n\n")
        f.write(f"**Query:** {query}\n\n")
        f.write("## Analysis\n\n")
        f.write(content + "\n\n")
        if citations:
            f.write("## Citations\n\n")
            for i, url in enumerate(citations, 1):
                f.write(f"{i}. {url}\n")
    
    print(f"\nResponse saved to {md_filename}")
    return content


# Example usage:
if __name__ == "__main__":
    # Default query about fusion energy
    result = perplexity_reasoning()
    
    # Custom reasoning query
    custom_result = perplexity_reasoning(
        "Evaluate the strategic implications of artificial general intelligence (AGI) development for global economic systems, considering both opportunities and risks."
    )