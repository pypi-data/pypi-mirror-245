"""Библиотека florest.py\nСамая лучшая библиотека в Python!"""
import random
import socket
from discord import SyncWebhook
from discord import Embed
import discord
from rcon.source import Client
import openai
from functools import partial
import base64


class Florest():
    """Класс о Флоресте."""
    name = 'Кирилл'
    nickname = 'Флорест'
    def Crash_Server(adress, port):
        """Функция уничтожает любой сервер путём запросов."""
        fake_ip = '182.21.20.32'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((adress, port))
        s.sendto(("GET /" + adress + " HTTP/1.1\r\n").encode('ascii'), (adress, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (adress, port))
        s.close()
    def generate_otvetka(cool: int):
        """Сгенерируйте генениальную ответку.\nПараметр `cool: int` отвечает за уровень крутости ответки. Минимум - 1, максимум 5."""
        cool_otvet_1 = ['Ты идиот?', 'Иди лечись.', 'Ты клоун.']
        cool_otvet_2 = ['Я не могу быть, как ты.', 'Кто обзывается, тот сам и называется.', 'Ты своё имя сказал?']
        cool_otvet_3 = ['Кто обзывается, тот так сам и называется.', 'Алмазно пофиг.', 'Ты гений без "ни".']
        if cool == 1:
            otvetka = random.choice(cool_otvet_1)
            return otvetka
        if cool == 2:
            otvetka = random.choice(cool_otvet_2)
            return otvetka
        if cool == 3:
            otvetka = random.choice(cool_otvet_3)
            return otvetka
        else:
            return f'Error: вы ввели значение {cool}, оно меньше 1, или больше 5.'
    def ugadayka(chislo: int):
        """Угадайте число от 1 до 5."""
        spisok = [1, 2, 3, 4, 5]
        chislo1 = random.choice(spisok)
        if chislo == chislo1:
            return f'Вы выиграли, поздравляем!'
        if chislo != chislo1:
            return f'Вы проиграли. Надеемся, в следующий раз, получится.'
    def random_chisle(one: int, two: int):
        """Функция сгенерирует рандомное значение от `one` до `two`."""
        r = random.randint(a=one, b=two)
        return r
    def random_choice(list: list):
        """Функция используется для выбора рандомного значения из списка. В аргемент `list` вписывайте список."""
        r = random.choice(list)
        return r
    def decode_text(text: str):
        """Функция для того, чтобы из текста декодировать в base64."""
        message_bytes = text.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('utf-8')
        return base64_message
    def decode_base64(code: str):
        """Декодировать base64 код в текст."""
        base64_bytes = code.encode('utf-8')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('utf-8')
        return message  
class Response():
    """Короче, в этом классе все функции, которые что-то пишут и делают."""
    def write_webhook_message(link, message):
        """Напишите сообщение от имени вебхука в Discord!\nПараметр `link` - указывайте ССЫЛКУ на вебхук.\nПараметр `message` - указывайте сообщение."""
        if not 'https://discord.com/api/webhooks/' in link:
            return f'Вы какую-то хрень ввели в параметр "link", а не ссылку на вебхук.'
        if 'https://discord.com/api/webhooks/' in link:
            webhook = SyncWebhook.from_url(url=link)
            webhook.send(message)
            return f'Успешно отправлено сообщение от имени вебхука {webhook.name}.'
    def send_embed(link: str, title: str = None, description: str = None):
        """Отправьте эмбед это имени вебхука, стандартный цвет: зеленый."""
        if title and description and 'https://discord.com/api/webhooks/' in link:
            embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Color.green()
            )
            webhook = SyncWebhook.from_url(url=link)
            webhook.send(embed=embed)
            return f'Успешно отправлено сообщение от имени вебхука {webhook.name}.'
        if description and 'https://discord.com/api/webhooks/' in link:
            embed = discord.Embed(
                description=description,
                colour=discord.Color.green()
            )
            webhook = SyncWebhook.from_url(url=link)
            webhook.send(embed=embed)
            return f'Успешно отправлено сообщение от имени вебхука {webhook.name}.'
        if title and 'https://discord.com/api/webhooks/' in link:
            embed = discord.Embed(
                title=title,
                colour=discord.Color.green()
            )
            webhook = SyncWebhook.from_url(url=link)
            webhook.send(embed=embed)
            return f'Успешно отправлено сообщение от имени вебхука {webhook.name}.'
        if not title and description:
            return f'Надо ввести хотя-бы параметр `title`, или параметр `description`.'
        if not 'https://discord.com/api/webhooks/' in link:
            return f'Вы ввели какую-то хрень в параметр `link`, а не ссылку на вебхук.'
    def rcon(ip: str, port: int, password: str, command: str, *, argument: str):
        """Прописывайте команды на своём Minecraft сервере с помощью RCON."""
        if all:
                with Client(ip, port=port, passwd=password) as client:
                    client.run(command, argument)
                    return f'Успешно!'