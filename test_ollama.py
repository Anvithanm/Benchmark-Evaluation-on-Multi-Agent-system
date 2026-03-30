from openai import OpenAI

# Modify to point to Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required but not used
)

response = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[
        {"role": "user", "content": "what is 2 + 3"}
    ]
)

print(response.choices[0].message.content)