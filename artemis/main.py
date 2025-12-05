from src.agent.context_window_memory import ContextWindowMemory
from src.agent.assistant import create_assistant


def main():
    print("Artemis simulation!")
    memory = ContextWindowMemory()
    bot = create_assistant()
    while True:
        query = input('\nUser: ')
        if query.lower() in ['exit', 'quit']:
            break

        memory.put({'role': 'user', 'content': query})

        response = []
        for response_chunk in bot.run(messages=memory.recall()):
            response.append(response_chunk)
            print(response_chunk, end='', flush=True)

        print()  # New line after response


if __name__ == "__main__":
    main()
