from ollama import chat

response = chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Say hello in exactly 3 sentences."
        }
    ],
    options={
        "temperature": 0.7,
        "num_predict": 100,
        "num_ctx" : 200
        
    }
)

print(response.message.content)