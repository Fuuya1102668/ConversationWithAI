import ollama

def chat_with_ollama(messages):
    response = ollama.chat(
        model="llama3",
        messages=messages,
    )
    return response["message"]["content"]

def main():
    print("Welcome to the Ollama chatbot!")
    print("Type 'quit' or press 'Ctrl+D' to exit the conversation.")

    messages = []
    while True:
        try:
            user_input = input("You: ")

            messages.append({"role": "user", "content": user_input})
            response = chat_with_ollama(messages)
            messages.append({"role": "assistant", "content": response})
            print(f"Ollama: {response}")

        except EOFError:
            print("\nThank you for chatting with Ollama. Goodbye!")
            break

if __name__ == '__main__':
    main()