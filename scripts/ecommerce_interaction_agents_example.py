import asyncio
import json
import openai

# Загрузка промптов из файла
with open("data/agent_prompts.json", "r", encoding="utf-8") as file:
    agent_prompts = json.load(file)

# Захардкоженный API ключ (пример, не используйте этот ключ)
api_key = 'секрет'
api_base = 'секрет'

# Установка API ключа для клиента OpenAI
openai.api_key = api_key
openai.api_base = api_base

# Функция для асинхронной отправки сообщений и получения ответов от модели
async def chat_with_model_async(model, messages):
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=messages
    )
    return response["choices"][0]["message"]["content"]

# Асинхронная функция для обработки диалога
async def handle_dialogue(messages):
    # Подготовка запросов для всех трех агентов
    control_prompt = agent_prompts["DialogueControlAgent"]["prompt"]
    search_prompt = agent_prompts["SearchQueryAgent"]["prompt"]
    consultant_prompt = agent_prompts["ConsultantAgent"]["prompt"]

    # Создание сообщений для запросов
    control_messages = messages + [{"role": "system", "content": control_prompt}]
    search_messages = messages + [{"role": "system", "content": search_prompt}]
    consultant_messages = messages + [{"role": "system", "content": consultant_prompt}]

    # Отправка запросов асинхронно
    control_response, search_response, consultant_response = await asyncio.gather(
        chat_with_model_async("gpt-4-turbo", control_messages),
        chat_with_model_async("gpt-4-turbo", search_messages),
        chat_with_model_async("gpt-4-turbo", consultant_messages)
    )

    # Обработка ответа от DialogueControlAgent
    if "<start_search>" in control_response:
        print("Поисковый запрос:", search_response)
        messages.append({"role": "assistant", "content": search_response})
    elif "<continue>" in control_response:
        print("Консультант:", consultant_response)
        messages.append({"role": "assistant", "content": consultant_response})
    else:
        print("Ошибка: неизвестная команда от DialogueControlAgent.")

# Запуск асинхронного диалога
async def main():
    # Начальное сообщение системы
    messages = [{}]

    print("Добро пожаловать в чат с консультантом! Чего бы вы хотели сделать или купить? Напишите 'выход' для завершения диалога.")
    
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == 'выход':
            print("Диалог завершен.")
            break

        # Добавляем ввод пользователя в историю сообщений
        messages.append({"role": "user", "content": user_input})

        # Обработка диалога
        await handle_dialogue(messages)

# Запуск асинхронного цикла событий
if __name__ == "__main__":
    asyncio.run(main())