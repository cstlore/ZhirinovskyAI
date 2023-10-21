import telebot
from telebot import types
import openai

openai.api_key = "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"
openai.api_base = "http://localhost:1337"


class interface_bot:
    users_context = {}
    gpt_type = 'gpt-3.5-turbo'

    def __init__(self):
        self.bot = telebot.TeleBot(token='6630339132:AAHFdkmCKJdy3-rYGZkbVYhIcFTgXeKlYoo')
        self.bot.set_my_commands([
            telebot.types.BotCommand("/help", "Информация о боте"),
            telebot.types.BotCommand("/clear_context", "Очистить контекст"),
            telebot.types.BotCommand("/gpt3", "Использовать ChatGPT 3.5"),
            telebot.types.BotCommand("/gpt4", "Использовать ChatGPT 4 (Возможны ошибки)")
        ])

        @self.bot.message_handler(commands=['clear_context'])
        def clear_context(message):
            self.users_context[message.from_user.id] = []
            self.bot.send_message(message.chat.id, text='Контекст сброшен, можно начинать диалог')

        @self.bot.message_handler(commands=['gpt3'])
        def set_gpt3(message):
            self.gpt_type = 'gpt-3.5-turbo'
            self.bot.send_message(message.chat.id, text='Установлен ChatGPT 3.5')

        @self.bot.message_handler(commands=['gpt4'])
        def set_gpt4(message):
            self.gpt_type = 'gpt-4'
            self.bot.send_message(message.chat.id, text='Установлен ChatGPT 4')

        @self.bot.message_handler(commands=['help'])
        def help_bot(message):
            self.bot.send_message(message.chat.id, text="""""")

        @self.bot.message_handler(content_types=['text'])
        def echo(message):
            m = self.bot.send_message(message.chat.id, text='Loading...')
            self.get_answer(message.text, m, message)

        self.bot.polling(none_stop=True)

    def get_answer(self, txt, m, mes):
        try:
            if mes.from_user.id not in self.users_context:
                self.users_context[mes.from_user.id] = []
            ans = self.get_completion(txt, m, mes).choices[0].message.content
            print(ans)
            self.users_context[mes.from_user.id].append({'role': 'user', 'content': txt})
            self.users_context[mes.from_user.id].append({'role': 'assistant', 'content': ans})
            print(self.users_context)
            splited_text = [ans[i:i + 4096] for i in range(0, len(ans), 4096)]
            for i in splited_text:
                self.bot.send_message(m.chat.id, text=i)
        except Exception as e:
            self.bot.send_message(m.chat.id, text=e.__class__.__name__)
            print(e)

    def get_completion(self, text, m, mes):
        chat_completion = openai.ChatCompletion.create(
            model=self.gpt_type,
            messages=self.users_context[mes.from_user.id] + [{"role": "user", "content": text}]
        )
        return chat_completion


bot = interface_bot()
