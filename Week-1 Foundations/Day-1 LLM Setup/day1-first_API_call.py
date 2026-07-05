from ollama import chat

messages = []

while True:
    user_input = input("You: ")

    # stop condition
    if user_input.lower() in ["exit", "quit"]:
        break

    # add user message
    messages.append({"role": "user", "content": user_input})

    # call model
    response = chat(
        model = "llama3.2",
        messages = messages,
        options = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_predict": 200,
            "num_ctx": 1024,
            "seed": 42
        }
    )

    assistant_message = response.message.content

    # print response
    print("AI:", assistant_message)

    # save assistant response
    messages.append({"role": "assistant", "content": assistant_message})