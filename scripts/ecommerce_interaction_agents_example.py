import openai
import json

# Загрузка промптов из файла
with open('./agent_prompts.json', 'r', encoding="utf-8") as file:
    agent_prompts = json.load(file)

# Захардкоженный API ключ (пример, не используйте этот ключ)
api_key = 'секрет'
api_base = 'секрет'

# Установка API ключа для клиента OpenAI
openai.api_key = api_key
openai.api_base = api_base

# Начальное сообщение системы
messages = []

# Функция для отправки сообщений и получения ответов от модели
def chat_with_model(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages
    )
    return response['choices'][0]['message']['content']

# Диалог с пользователем
print("Добро пожаловать в чат с консультантом! Чего бы в хотели сделать или купить? Напишите 'выход' для завершения диалога.")
while True:
    user_input = input("Вы: ")
    if user_input.lower() == 'выход':
        print("Диалог завершен.")
        break

    # Добавляем ввод пользователя в историю сообщений
    messages.append({"role": "user", "content": user_input})

    # Запускаем DialogueControlAgent для определения следующего шага
    control_prompt = agent_prompts['DialogueControlAgent']['prompt']
    control_messages = messages + [{"role": "system", "content": control_prompt}]
    control_response = chat_with_model(control_messages)

    print("ОТЛАДКА:", control_response.strip().lower())
    if control_response == "<start_search>":
        # Запускаем SearchQueryAgent для генерации поискового запроса
        search_prompt = agent_prompts['SearchQueryAgent']['prompt']
        search_messages = messages + [{"role": "system", "content": search_prompt}]
        search_response = chat_with_model(search_messages)
        print("Поисковый запрос:", search_response)
        break  # Поиск запущен, диалог завершается
    elif control_response == "<continue>":
        # Запускаем ConsultantAgent для продолжения диалога с пользователем
        consultant_prompt = agent_prompts['ConsultantAgent']['prompt']
        consultant_messages = messages + [{"role": "system", "content": consultant_prompt}]
        consultant_response = chat_with_model(consultant_messages)
        print("Агент:", consultant_response)
        messages.append({"role": "assistant", "content": consultant_response})
    else:
        print("Ошибка: неизвестная команда от DialogueControlAgent.")
        break