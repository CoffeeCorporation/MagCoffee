from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkChatEventType
from datetime import datetime, timedelta
import vk_api
from datetime import datetime
import datetime
import random
import random as rand
import requests as req
import time
import json
import re
import configparser
import os

config = configparser.ConfigParser()
now = datetime.datetime.now()
coincd = 0

def greg():
    config.read(path)
    config.get('Global', 'Regs')


def configupdate():
    with open(path, "w") as config_file:
        config.write(config_file)


def vkmsg(text):
    vk.method('messages.send',
              {'peer_id': event.object.peer_id,
               'message': text,
               'random_id': 0})


def createConfig(path):
    config = configparser.ConfigParser()


if __name__ == "__main__":
    path = "database.txt"
    createConfig(path)


def newcoin():
    unix = int(time.time())
    config.read(path)
    r = random.randint(-5000, 5000)
    value = config.get('Global', 'CoinValue')
    newvalue = int(value) + int(r)
    t = config.get('Global', 'CoinTime')
    if int(newvalue) <= 1500:
        config.read(path)
        config.set('Global', 'CoinValue', '1500')
        with open(path, "w") as config_file:
            config.write(config_file)
    else:
        config.read(path)
        config.set('Global', 'CoinValue', '%s' % newvalue)
        with open(path, "w") as config_file:
            config.write(config_file)
    print('Новый курс гипервалюты: %s -> %s' % (value, config.get('Global', 'CoinValue')))
    newtime = unix + 1800
    config.set('Global', 'CoinTime', '%s' % newtime)
    with open(path, "w") as config_file:
        config.write(config_file)


vk = vk_api.VkApi(token="f3ba2ed7167ad15e9d61f1ddf666dbcc3bec9b79a4534ec460691b5de0bd2f20da2a13a849377320104d1")
vk._auth_token()
vk.get_api()

longpoll = VkBotLongPoll(vk, 193742831)
print('The bot is running')
while True:
    try:
        for event in longpoll.listen():
            config.read(path)
            if int(time.time()) >= int(config.get('Global', 'CoinTime')):
                newcoin()
            if event.type == VkBotEventType.MESSAGE_NEW and '-' not in str(event.object.from_id):
                from_id = event.object.from_id
                user_id = event.object.user_id
                message = event.object.text.lower()
                m = event.object.text
                peer_id = event.object.peer_id
                chat_id = event.chat_id
                sp = message.split(' ')
                msp = m.split(' ')
                config.read(path)
                if peer_id != user_id:
                    if str(from_id) not in str(config.get('Global', 'Regs')):
                        user = vk.method("users.get", {"user_ids": event.object.from_id})
                        name = user[0]['first_name']
                        surname = user[0]['last_name']
                        fullname = '@id' + str(event.object.from_id) + '(' + str(name) + ' ' + str(surname) + ')'
                        config.add_section('%d' % from_id)
                        config.set('%d' % from_id, 'ID', str(from_id))
                        config.set('%d' % from_id, 'Balance', '500000')
                        config.set('%d' % from_id, 'LVL', '1')
                        config.set('%d' % from_id, 'LVLexp', '0')
                        config.set('%d' % from_id, 'MaxLVLexp', '5')
                        config.set('%d' % from_id, 'Coins', '0')
                        config.set('%d' % from_id, 'Kings', '0')
                        config.set('%d' % from_id, 'VIP', '0')
                        config.set('%d' % from_id, 'Ban', '0')
                        config.set('%d' % from_id, 'NickBan', '0')
                        config.set('%d' % from_id, 'NickBanAuthor', '')
                        config.set('%d' % from_id, 'NickBanWarn', '')
                        config.set('%d' % from_id, 'Rang', '0')
                        config.set('%d' % from_id, 'rep', '0')
                        config.set('%d' % from_id, 'Name', str(name))
                        config.set('%d' % from_id, 'Surname', str(surname))
                        config.set('%d' % from_id, 'Nick', 'Player')
                        config.set('Global', 'Regs', str(config.get('Global', 'Regs')) + ' ' + str(from_id))
                        with open(path, "w") as config_file:
                            config.write(config_file)
                        vk.method('messages.send',
                                  {'chat_id': 3,
                                   'message': '👥💬Новый зарегистрированный пользователь!\nПользователь: %s' % fullname,
                                   'random_id': 0})
                    if sp[0] == '/инфа':
                        nick = f"🔮@id{from_id}({config.get('%d' % from_id, 'Nick')})"
                        allsp = 0
                        for i in sp:
                            allsp = int(allsp) + 1
                        if allsp >= 2:
                            text = m[6:]
                            r = random.randint(0, 100)
                            t = random.choice([f'{nick}, Вероятность что {text} произойдёт - {r}%',
                                               f'{nick}, Вероятность {text} - {r}%',
                                               f'{nick}, По примерным замерам, вероятность {text} - {r}%'])
                            vkmsg(t)

                    if sp[0] == '/кто':
                        nick = config.get('%d' % from_id, 'Nick')
                        allsp = 0
                        for i in sp:
                            allsp = int(allsp) + 1
                        if allsp >= 2:
                            text = m[5:]
                            members = vk.method("messages.getConversationMembers", {'peer_id': event.object.peer_id})[
                                'items']
                            vfd = [f"{member['member_id']}" for member in members if member['member_id']]
                            r = random.choice(vfd)
                            members = vk.method("messages.getConversationMembers", {'peer_id': event.object.peer_id})[
                                'profiles']
                            name = [f"{member['first_name']} {member['last_name']} " for member in members if
                                    member['id'] == int(r)]
                            if '?' in str(text):
                                text = text.replace('?', '')
                            if '-' in str(r):
                                name = 'Сообщество'
                                r = 'public' + str(r[1:])
                            else:
                                r = 'id' + str(r)
                                name = random.choice(name)
                            if '-' in str(r):
                                r = r[1:]
                            if str(r[2:]) in str(config.get('Global', 'Regs')).split(' '):
                                name = config.get('%s' % r[2:], 'Nick')
                            t = random.choice([f"🔮@id{from_id}({nick}), {text} точно - @{r}({name})",
                                               f"🔮@id{from_id}({nick}), Какие могут быть вопросы, {text} - @{r}({name})!",
                                               f"🔮@id{from_id}({nick}), 100% {text} это - @{r}({name})",
                                               f"🔮@id{from_id}({nick}), Сам бог подсказал мне, что {text} является - @{r}({name})"])
                            vk.method('messages.send',
                                      {'chat_id': chat_id,
                                       'message': str(t),
                                       'random_id': 0})
                        # if sp[0] == '/одноиз':
                        nick = f"@id{from_id}({config.get('%d' % from_id, 'Nick')})"
                        allsp = 0
                        for i in sp:
                            allsp = int(allsp) + 1
                        if allsp >= 2 and 'или' in str(message):
                            text = m[8:]
                            for i in message.split(' или '):
                                allsp = int(allsp) + 1
                            if allsp >= 2:
                                l = ''
                                for i in text.split(' или '):
                                    l = str(l) + ',' + str(i)
                                l = l.replace('%s' % sp[1], '')
                                l = l.replace(',', '', 2)
                                l = l.replace('/', '', )
                                l = l.replace(',', "', '")
                                l = "['" + str(sp[1]) + "', '" + str(l) + "']"
                                print(l)
                                r = random.choice(l)
                                print(r)
                                t = random.choice([f"{nick}, ты меня за дурака держишь? Естественно - {r}!",
                                                   f"{nick}, я чувствую что правильный выбор - {r}!",
                                                   f"{nick}, 100% - {r}!"])
                                vkmsg(t)
                    if message == '/курс':
                        n = datetime.datetime.today() + timedelta(hours=3)
                        week = n.strftime("%H:%M %d.%m")
                        value = config.get('Global', 'CoinValue')
                        if int(value) <= 7000:
                            vk.method('messages.send',
                                      {'chat_id': chat_id,
                                       'message': '📋Курс гипервалюты на %s %d года\n\n🧬%s $ за одну штуку\n📉Статус: Низкий курс' % (
                                           week, now.year, value),
                                       'random_id': 0})
                        if int(value) > 7000 and int(value) < 15001 or int(value) == 15000 and int(value) < 15001:
                            vk.method('messages.send',
                                      {'chat_id': chat_id,
                                       'message': '📋Курс гипервалюты на %s %d года\n\n🧬%s $ за одну штуку\n📊Статус: Стабильный курс' % (
                                           week, now.year, value),
                                       'random_id': 0})
                        if int(value) > 15000:
                            vk.method('messages.send',
                                      {'chat_id': chat_id,
                                       'message': '📋Курс гипервалюты на %s %d года\n\n🧬%s $ за одну штуку\n📈Статус: Высокий курс' % (
                                           week, now.year, value),
                                       'random_id': 0})
                    if message == '/онлайн':
                        members = vk.method("messages.getConversationMembers", {'peer_id': event.object.peer_id})[
                            'profiles']
                        vfd = [f"{member['first_name']} {member['last_name']} " for member in members if
                               member['online']]
                        count10 = len(vfd)
                        atta = '\n💛'.join(vfd)
                        vk.method("messages.send",
                                  {"peer_id": event.object.peer_id, "message": "👥Сейчас в онлайне:\n " + '\n💛' + atta,
                                   "random_id": 0})
                    if message == '/стат':
                        allvalue = 0
                        allcoins = 0
                        allusers = 0
                        us = config.get('Global', 'Regs').split()
                        for i in us:
                            allvalue = int(allvalue) + int(config.get('%s' % i, 'Balance'))
                            allcoins = int(allcoins) + int(config.get('%s' % i, 'Coins'))
                            allusers = int(allusers) + 1
                        vk.method('messages.send',
                                  {'chat_id': chat_id,
                                   'message': '📋Статистика бота\n\n'
                                              '💵Всего валюты в обороте: %s $\n'
                                              '🧬Всего гипервалюты в обороте: %s\n'
                                              '👥Всего пользователей зарегистрировано: %s\n' % (
                                              allvalue, allcoins, allusers),
                                   'random_id': 0})
                    if sp[0] == '/рулетка':
                        nick = config.get('%d' % from_id, 'Nick')
                        balance = config.get('%d' % from_id, 'Balance')
                        vip = config.get('%d' % from_id, 'VIP')
                        lvlxp = config.get('%d' % from_id, 'LVLexp')
                        value = m[9:]
                        v = 0
                        numk = 0
                        if 'к' in str(value):
                            v = value.replace('к', '')
                        for i in value:
                            if 'к' in str(i):
                                numk = int(numk) + 1
                        if numk > 4:
                            value = value.replace('к', '')
                        testint = value.isdigit()
                        if value == '':
                            vk.method('messages.send',
                                      {'chat_id': chat_id,
                                       'message': '❌' + str(nick) + ', Введите ставку! /рулетка [Ставка]',
                                       'random_id': 0})
                        else:
                            if testint == False and 'к' not in str(value):
                                vk.method('messages.send',
                                          {'chat_id': chat_id,
                                           'message': '❌' + str(nick) + ', Введите ставку! /рулетка [Ставка]',
                                           'random_id': 0})
                            else:
                                if 'к' in str(value) and 'кк' not in str(value):
                                    value = int(v) * 1000
                                if 'кк' in str(value) and 'ккк' not in str(value):
                                    value = int(v) * 1000000
                                if 'ккк' in str(value) and 'кккк' not in str(value):
                                    value = int(v) * 1000000000
                                if 'кккк' in str(value) and 'ккккк' not in str(value):
                                    value = int(v) * 1000000000000
                                if int(value) < 50:
                                    vk.method('messages.send',
                                              {'chat_id': chat_id,
                                               'message': '❌' + str(nick) + ', минимальная ставка - 50$',
                                               'random_id': 0})
                                else:
                                    if int(value) > int(balance):
                                        vk.method('messages.send',
                                                  {'chat_id': chat_id,
                                                   'message': '❌' + str(nick) + ', недостаточно средств!',
                                                   'random_id': 0})
                                    else:
                                        win = random.randint(1, 3)
                                        if int(vip) == 0:
                                            if win == 1:
                                                r0 = ['🎁🎁🎁', '💰💰💰', '💷💷💷']
                                                r = random.choice(r0)
                                                balance = int(balance) + int(value)
                                                config.set('%s' % from_id, 'Balance', '%s' % balance)
                                                nextxp = int(lvlxp) + 2
                                                config.set('%s' % from_id, 'LVLexp', '%s' % nextxp)
                                                vk.method('messages.send',
                                                          {'chat_id': chat_id,
                                                           'message': '🎩Лотерея Магистра Кофе🎩\n💰' + str(
                                                               nick) + ', ваш выигрыш: ' + str(
                                                               value) + ' $\n\n🎰Вам выпало: ' + str(
                                                               r) + '\n💳Ваш баланс: ' + str(balance) + ' $',
                                                           'random_id': 0})
                                                with open(path, "w") as config_file:
                                                    config.write(config_file)
                                            if win == 2 or win == 3:
                                                r0 = ['💵', '💴', '💶', '💷', '💰', '💳', '💎', '🎁']
                                                r1 = random.choice(r0)
                                                r2 = random.choice(r0)
                                                r3 = random.choice(r0)
                                                r = str(r1) + str(r2) + str(r3)
                                                balance = int(balance) - int(value)
                                                config.set('%s' % from_id, 'Balance', '%s' % balance)
                                                vk.method('messages.send',
                                                          {'chat_id': chat_id,
                                                           'message': '🎩Лотерея Магистра Кофе🎩\n💰' + str(
                                                               nick) + ', ваш проигрыш: ' + str(
                                                               value) + ' $\n\n🎰Вам выпало: ' + str(
                                                               r) + '\n💳Ваш баланс: ' + str(balance) + ' $',
                                                           'random_id': 0})
                                                with open(path, "w") as config_file:
                                                    config.write(config_file)
                                        if int(vip) == 1:
                                            if win == 2:
                                                r = random.choice(['🎁🎁🎁', '💰💰💰', '💷💷💷'])
                                                value = int(value) * 3
                                                balance = int(balance) + int(value)
                                                config.set('%s' % from_id, 'Balance', '%s' % balance)
                                                nextxp = int(lvlxp) + 2
                                                config.set('%s' % from_id, 'LVLexp', '%s' % nextxp)
                                                vk.method('messages.send',
                                                          {'chat_id': chat_id,
                                                           'message': '🎩Лотерея Магистра Кофе🎩\n💰' + str(
                                                               nick) + ', ваш выигрыш: ' + str(
                                                               value) + ' $(x3)[VIP]\n\n🎰Вам выпало: ' + str(
                                                               r) + '\n💳Ваш баланс: ' + str(balance) + ' $',
                                                           'random_id': 0})
                                                with open(path, "w") as config_file:
                                                    config.write(config_file)
                                            if win == 1 or win == 3:
                                                r0 = ['💵', '💴', '💶', '💷', '💰', '💳', '💎', '🎁']
                                                r1 = random.choice(r0)
                                                r2 = random.choice(r0)
                                                r3 = random.choice(r0)
                                                r = str(r1) + str(r2) + str(r3)
                                                balance = int(balance) - int(value)
                                                config.set('%s' % from_id, 'Balance', '%s' % balance)
                                                vk.method('messages.send',
                                                          {'chat_id': chat_id,
                                                           'message': '🎩Лотерея Магистра Кофе🎩\n💰' + str(
                                                               nick) + ', ваш проигрыш: ' + str(
                                                               value) + ' $\n\n🎰Вам выпало: ' + str(
                                                               r) + '\n💳Ваш баланс: ' + str(balance) + ' $',
                                                           'random_id': 0})
                                                with open(path, "w") as config_file:
                                                    config.write(config_file)
                    if sp[0] == '/rep':
                        name = config.get('%d' % from_id, 'Name')
                        surname = config.get('%d' % from_id, 'Surname')
                        text = m[5:]
                        if len(text) >= 100:
                            vk.method('messages.send', {'peer_id': event.object.peer_id,
                                                        'message': '💬❗Вы превысили макс. кол-во символов(100)!',
                                                        'random_id': 0})
                        if text == '':
                            vk.method('messages.send',
                                      {'peer_id': event.object.peer_id, 'message': '💬❗Вы не ввели сообщение!',
                                       'random_id': 0})
                        if int(config.get('%d' % from_id, 'rep')) == 1:
                            vk.method('messages.send',
                                      {'peer_id': event.object.peer_id,
                                       'message': '❗Вы уже обращались в репорт!\n\n🔔Ожидайте ответа, максимальное время ожидания - 12 часов',
                                       'random_id': 0})
                        if text != '' and len(text) < 100 and int(config.get('%d' % from_id, 'rep')) == 0:
                            num = 0
                            for i in config.get('Global', 'Rep').split(' '):
                                num = int(num) + 1
                            num = int(num) + 1
                            config.add_section('REPORT-%s' % num)
                            config.set('REPORT-%s' % num, 'ID', '%s' % num)
                            rname = '@id' + str(from_id) + '(' + str(name) + ')'
                            peer = event.object.peer_id
                            fname = '@id%s(%s %s)' % (from_id, name, surname)
                            rtext = m[5:]
                            id = event.object.from_id
                            config.set('REPORT-%s' % num, 'name', '%s' % rname)
                            config.set('REPORT-%s' % num, 'peer', '%s' % peer)
                            config.set('REPORT-%s' % num, 'text', '%s' % rtext)
                            config.set('REPORT-%s' % num, 'User', '%s' % from_id)
                            config.set('REPORT-%s' % num, 'Work', '1')
                            set = str(config.get('Global', 'rep')) + ' ' + str(num)
                            config.set('Global', 'rep', '%s' % set)
                            config.set('%s' % from_id, 'rep', '1')
                            vk.method("messages.send", {"chat_id": 3, "message": '🆕Поступил новый репорт! [ID:' + str(
                                num) + ']\n\n👥Чат: ' + str(chat_id) + '\n👨‍💻Пользователь: ' + str(
                                fname) + '\n 💭Текст репорта: ' + str(
                                rtext) + '\n\n\n Введите /pm %s [текст] для ответа или /npm %s для удаления.\n\n////////////////////////////////' % (
                                                                                 num, num), 'random_id': 0})
                            vkmsg('💬✅Ваше обращение было отправлено в отдел Coffee Help!')
                            configupdate()
                    if sp[0] == '/ник':
                        value = m[4:]
                        nick = config.get('%d' % from_id, 'Nick')
                        if value == '':
                            vk.method('messages.send',
                                      {'chat_id': chat_id,
                                       'message': '❌' + str(nick) + ', введите ник!',
                                       'random_id': 0})
                        if value != '':
                            if '[' in str(value) or '@' in str(value) or '*' in str(value):
                                vkmsg(f'❌{nick}, вы используете запрещённый символ!')
                            if len(value) > 16 and '[' not in str(value) and '@' not in str(value) and '*' not in str(value) and '%' not in str(value):
                                vk.method('messages.send',
                                          {'chat_id': chat_id,
                                           'message': '❌' + str(nick) + ', максимальная длина ника - 15 символов!',
                                           'random_id': 0})
                            if len(value) < 16 and '[' not in str(value) and '@' not in str(value) and '*' not in str(value) and '%' not in str(value):
                                if str(value) == str(nick):
                                    vk.method('messages.send',
                                              {'chat_id': chat_id,
                                               'message': '❌' + str(nick) + ', вы уже используете этот ник!',
                                               'random_id': 0})
                                else:
                                    if 'адм' in message and from_id != 380487228 or 'root' in message and from_id != 380487228 or 'dev' in message and from_id != 380487228 or 'разраб' in message and from_id != 380487228:
                                        vk.method('messages.send',
                                                  {'chat_id': chat_id,
                                                   'message': '❌' + str(nick) + ', отказано в доступе!',
                                                   'random_id': 0})
                                    else:
                                        config.set('%d' % from_id, 'Nick', '%s' % value)
                                        vk.method('messages.send',
                                                  {'chat_id': chat_id,
                                                   'message': '🎩' + str(nick) + ', вы сменили ник на %s' % value,
                                                   'random_id': 0})
                                        with open(path, "w", encoding='utf8') as config_file:
                                            config.write(config_file)
                    if int(config.get('%d' % from_id, 'LVLexp')) >= int(config.get('%d' % from_id, 'maxLVLexp')):
                        nick = config.get('%d' % from_id, 'Nick')
                        lvl = config.get('%d' % from_id, 'LVL')
                        lvlxp = config.get('%d' % from_id, 'LVLexp')
                        lvlmxp = config.get('%d' % from_id, 'maxLVLexp')
                        kings = config.get('%d' % from_id, 'Kings')
                        nextlvl = int(lvl) + 1
                        nextxp = int(lvlmxp) - int(lvlxp)
                        nextmxp = int(lvlmxp) * 1.3
                        k = int(lvlmxp) / 5
                        nextkings = int(kings) + k
                        if '.' in str(nextmxp):
                            nextmxp = str(nextmxp).replace(str(nextmxp).split('.')[1], '')
                            nextmxp = nextmxp.replace('.', '')
                        if '-' in str(nextxp):
                            nextxp = str(nextxp).replace('-', '')
                        if '.' in str(nextkings):
                            nextkings = str(nextkings).replace(str(nextkings).split('.')[1], '')
                            nextkings = nextkings.replace('.', '')
                        if '.' in str(k):
                            k = str(k).replace(str(k).split('.')[1], '')
                            k = k.replace('.', '')
                        config.set('%d' % from_id, 'maxLVLexp', '%s' % nextmxp)
                        config.set('%d' % from_id, 'LVLexp', '%s' % nextxp)
                        config.set('%d' % from_id, 'LVL', '%s' % nextlvl)
                        config.set('%d' % from_id, 'Kings', '%s' % nextkings)
                        vk.method("messages.send",
                                  {"peer_id": event.object.peer_id,
                                   "message": '🆕' + str(
                                       nick) + ', ваш уровень повысился!\n🔱Вы получили %s престижа!' % k,
                                   'random_id': 0})
                        with open(path, "w") as config_file:
                            config.write(config_file)
                    if message == '/баланс':
                        nick = config.get('%d' % from_id, 'Nick')
                        balance = config.get('%d' % from_id, 'Balance')
                        kings = config.get('%d' % from_id, 'Kings')
                        coins = config.get('%d' % from_id, 'Coins')
                        vk.method('messages.send',
                                  {'chat_id': chat_id,
                                   'message': '🖥' + str(nick) + ', ваш баланс:\n\n'
                                                                 '💳Баланс: ' + str(balance) + ' $\n'
                                                                                               '🧬Гипервалюта: ' + str(
                                       coins) + '\n'
                                                '🔱Престиж: ' + str(kings) + '\n'
                                      ,
                                   'random_id': 0})
                    if sp[0] == '/мон':
                        nick = config.get('%d' % from_id, 'Nick')
                        balance = config.get('%d' % from_id, 'Balance')
                        vip = config.get('%d' % from_id, 'VIP')
                        lvlxp = config.get('%d' % from_id, 'LVLexp')
                        v = 0
                        numk = 0
                        allsp = 0
                        for i in sp:
                            allsp = int(allsp) + 1
                        if int(allsp) < 3:
                            vkmsg('❌' + str(nick) + ', ошибка в написании! /мон [орёл\решка] [ставка]')
                        else:
                            if sp[2].isdigit() == False and 'к' not in str(sp[2]):
                                vk.method('messages.send',
                                          {'chat_id': chat_id,
                                           'message': '❌' + str(nick) + ', Введите ставку! /мон [орёл\решка] [ставка]',
                                           'random_id': 0})
                            else:
                                if sp[1] != 'орёл' and sp[1] != 'решка':
                                    vk.method('messages.send',
                                              {'chat_id': chat_id,
                                               'message': '❌' + str(
                                                   nick) + ', Введите сторону! /мон [орёл\решка] [ставка]',
                                               'random_id': 0})
                                else:
                                    value = sp[2]
                                    if 'к' in str(value):
                                        v = value.replace('к', '')
                                    for i in value:
                                        if 'к' in str(i):
                                            numk = int(numk) + 1
                                    if numk > 4:
                                        value = value.replace('к', '')
                                    if 'к' in str(value) and 'кк' not in str(value):
                                        value = int(v) * 1000
                                    if 'кк' in str(value) and 'ккк' not in str(value):
                                        value = int(v) * 1000000
                                    if 'ккк' in str(value) and 'кккк' not in str(value):
                                        value = int(v) * 1000000000
                                    if 'кккк' in str(value) and 'ккккк' not in str(value):
                                        value = int(v) * 1000000000000
                                    if int(value) < 50:
                                        vk.method('messages.send',
                                                  {'chat_id': chat_id,
                                                   'message': '❌' + str(nick) + ', минимальная ставка - 50$',
                                                   'random_id': 0})
                                    else:
                                        if int(value) > int(balance):
                                            vk.method('messages.send',
                                                      {'chat_id': chat_id,
                                                       'message': '❌' + str(nick) + ', недостаточно средств!',
                                                       'random_id': 0})
                                        else:
                                            r = random.choice(['орёл', 'решка'])
                                            if int(vip) == 0:
                                                if str(r) == str(sp[1]):
                                                    win = int(balance) + int(value)
                                                    config.set('%s' % from_id, 'Balance', '%s' % win)
                                                    vkmsg(f'🀄️Японская монетка🀄️\n💰{nick}, ваш выигрыш: {value} $\n\n🎲Вам выпало: {r.title()}\n💳Ваш баланс: {win} $')
                                                    configupdate()
                                                else:
                                                    win = int(balance) - int(value)
                                                    config.set('%s' % from_id, 'Balance', '%s' % win)
                                                    vkmsg(f'🀄️Японская монетка🀄️\n💰{nick}, ваш проигрыш: {value} $\n\n🎲Вам выпало: {r.title()}\n💳Ваш баланс: {win} $')
                                                    configupdate()
                                            if int(vip) == 1:
                                                if str(r) == str(sp[1]):
                                                    value = int(value) * 3
                                                    win = int(balance) + int(value)
                                                    config.set('%s' % from_id, 'Balance', '%s' % win)
                                                    vkmsg(f'🀄️Японская монетка🀄️\n💰{nick}, ваш выигрыш: {value} $(x3) [VIP]\n\n🎲Вам выпало: {r.title()}\n💳Ваш баланс: {win} $')
                                                    configupdate()
                                                else:
                                                    win = int(balance) - int(value)
                                                    config.set('%s' % from_id, 'Balance', '%s' % win)
                                                    vkmsg(f'🀄️Японская монетка🀄️\n💰{nick}, ваш проигрыш: {value} $\n\n🎲Вам выпало: {r.title()}\n💳Ваш баланс: {win} $')
                                                    configupdate()
                    if sp[0] == '/trade':
                        nick = config.get('%d' % from_id, 'Nick')
                        allsp = 0
                        coin = config.get('Global', 'CoinValue')
                        balance = config.get('%d' % from_id, 'Balance')
                        coins = config.get('%d' % from_id, 'Coins')
                        for i in sp:
                            allsp = int(allsp) + 1
                        if allsp == 1:
                            vk.method('messages.send',
                                      {'chat_id': chat_id,
                                       'message': '❌' + str(
                                           nick) + ', введите вариант обмена! /trade [валюта\гвалюта] [Кол-во] (1 гипервалюта = %s $)' % coin,
                                       'random_id': 0})
                        else:
                            if allsp == 2:
                                vk.method('messages.send',
                                          {'chat_id': chat_id,
                                           'message': '❌' + str(
                                               nick) + ', введите кол-во для обмена! /trade [валюта\гвалюта] [Кол-во] (1 гипервалюта = %s $)' % coin,
                                           'random_id': 0})
                            if sp[2].isdigit() == False:
                                vk.method('messages.send',
                                          {'chat_id': chat_id,
                                           'message': '❌' + str(
                                               nick) + ', введите кол-во для обмена! /trade [валюта\гвалюта] [Кол-во] (1 гипервалюта = %s $)' % coin,
                                           'random_id': 0})
                            else:
                                if int(sp[2]) <= 0:
                                    vk.method('messages.send',
                                              {'chat_id': chat_id,
                                               'message': '❌' + str(
                                                   nick) + ', нельзя указать 0 или меньше!',
                                               'random_id': 0})
                                else:
                                    if sp[1] == 'валюта':
                                        price = int(sp[2]) * int(coin)
                                        if int(sp[2]) > int(balance):
                                            vk.method('messages.send',
                                                      {'chat_id': chat_id,
                                                       'message': '❌' + str(
                                                           nick) + ', недостаточно средств!',
                                                       'random_id': 0})
                                        else:
                                            newbalance = int(balance) - int(price)
                                            newcoins = int(coins) + int(sp[2])
                                            config.set('%s' % from_id, 'Balance', '%s' % newbalance)
                                            config.set('%s' % from_id, 'Coins', '%s' % newcoins)
                                            vk.method('messages.send',
                                                      {'chat_id': chat_id,
                                                       'message': '♠' + str(
                                                           nick) + ', вы обменяли %s $ на %s гипервалюты!' % (
                                                                      price, sp[2]),
                                                       'random_id': 0})
                                            with open(path, "w") as config_file:
                                                config.write(config_file)
                                    if sp[1] == 'гвалюта':
                                        price = int(sp[2]) * int(coin)
                                        if int(sp[2]) > int(coins):
                                            vk.method('messages.send',
                                                      {'chat_id': chat_id,
                                                       'message': '❌' + str(
                                                           nick) + ', недостаточно средств!',
                                                       'random_id': 0})
                                        else:
                                            newbalance = int(balance) + int(price)
                                            newcoins = int(coins) - int(sp[2])
                                            config.set('%s' % from_id, 'Balance', '%s' % newbalance)
                                            config.set('%s' % from_id, 'Coins', '%s' % newcoins)
                                            vk.method('messages.send',
                                                      {'chat_id': chat_id,
                                                       'message': '♣' + str(
                                                           nick) + ', вы обменяли %s гипервалюты на %s $!' % (
                                                                      sp[2], price),
                                                       'random_id': 0})
                                            with open(path, "w") as config_file:
                                                config.write(config_file)
                    if message == '/games':
                        vk.method('messages.send',
                                  {'chat_id': chat_id,
                                   'message': '🎮Игровое меню:\n\n'
                                              '🖥/профиль - Ваш игровой профиль\n'
                                              '💰/баланс - Ваш баланс\n'
                                              '🎩/ник - Сменить ваш игровой ник\n'
                                              '🀄️/мон - Сыграть в японскую монетку\n'
                                              '🎲/рулетка - Сыграть в рулетку\n'
                                              '🛍/магазин - Магазин [В РАЗРАБОТКЕ]\n'
                                              '🔧/улучшения - Магазин улучшений [В РАЗРАБОТКЕ] \n'
                                              '🔮/инфа - Вероятность события\n'
                                              '🔮/кто - Присвоение опред. характеристики к случайному пользователю беседы\n'
                                              '☎/rep - Обратиться в тех. поддержку\n'
                                              '📔/ники - Ники пользователей состаящий в конференции\n'
                                              '💬/cid - ID конференции',
                                   'random_id': 0})
                    if message == '/cid':
                        vk.method('messages.send',
                                  {'chat_id': chat_id,
                                   'message': '💬ID данной конференции: %s' % chat_id,
                                   'random_id': 0})
                    if message == '/топ':
                        top1 = 0
                        top2 = 0
                        top3 = 0
                        top4 = 0
                        top5 = 0
                        top1user = None
                        top2user = None
                        top3user = None
                        top4user = None
                        top5user = None
                        us = config.get('Global', 'Regs').split(' ')
                        for i in us:
                            nick = config.get('%s' % i, 'Nick')
                            snick = '@id%s(%s)' % (i, nick)
                            if int(config.get('%s' % i, 'Balance')) > int(top1) and str(i) not in str(top4user) and str(
                                    i) not in str(top2user) and str(i) not in str(top3user) and str(i) not in str(
                                    top5user):
                                top1user = '@id%s(%s)' % (i, nick)
                                top1 = config.get('%s' % i, 'Balance')
                            if int(config.get('%s' % i, 'Balance')) > int(top2) and str(i) not in str(top1user) and str(
                                    i) not in str(top3user) and str(i) not in str(top4user) and str(i) not in str(
                                    top5user):
                                top2user = '@id%s(%s)' % (i, nick)
                                top2 = config.get('%s' % i, 'Balance')
                            if int(config.get('%s' % i, 'Balance')) > int(top3) and str(i) not in str(top1user) and str(
                                    i) not in str(top2user) and str(i) not in str(top4user) and str(i) not in str(
                                    top5user):
                                top3user = '@id%s(%s)' % (i, nick)
                                top3 = config.get('%s' % i, 'Balance')
                            if int(config.get('%s' % i, 'Balance')) > int(top4) and str(i) not in str(top1user) and str(
                                    i) not in str(top2user) and str(i) not in str(top3user) and str(i) not in str(
                                    top5user):
                                top4user = '@id%s(%s)' % (i, nick)
                                top4 = config.get('%s' % i, 'Balance')
                            if int(config.get('%s' % i, 'Balance')) > int(top5) and str(i) not in str(top1user) and str(
                                    i) not in str(top2user) and str(i) not in str(top3user) and str(i) not in str(
                                    top4user):
                                top5user = '@id%s(%s)' % (i, nick)
                                top5 = config.get('%s' % i, 'Balance')
                        vk.method("messages.send",
                                  {"peer_id": event.object.peer_id,
                                   "message": '🏆Топ пользователей бота\n\n'
                                              '🥇1. ' + str(top1user) + ' - ' + str(top1) + ' $\n'
                                                                                            '🥈2. ' + str(
                                       top2user) + ' - ' + str(top2) + ' $\n'
                                                                       '🥉3. ' + str(top3user) + ' - ' + str(
                                       top3) + ' $\n'
                                               '🏅4. ' + str(top4user) + ' - ' + str(top4) + ' $\n'
                                                                                             '🏅5. ' + str(
                                       top5user) + ' - ' + str(top5) + ' $\n',
                                   'random_id': 0})
                    if message == '/профиль':
                        nick = config.get('%d' % from_id, 'Nick')
                        balance = config.get('%d' % from_id, 'Balance')
                        kings = config.get('%d' % from_id, 'Kings')
                        coins = config.get('%d' % from_id, 'Coins')
                        lvl = config.get('%d' % from_id, 'LVL')
                        lvlxp = config.get('%d' % from_id, 'LVLexp')
                        lvlmxp = config.get('%d' % from_id, 'maxLVLexp')
                        if int(config.get('%d' % from_id, 'VIP')) == 0:
                            vk.method('messages.send',
                                      {'chat_id': chat_id,
                                       'message': '🖥' + str(nick) + ', ваш игровой профиль:\n\n'
                                                                     '💾 Игровой уровень: ' + str(lvl) + ' ур. [' + str(
                                           lvlxp) + '/' + str(lvlmxp) + '] EXP.\n'
                                                                        '💳Баланс: ' + str(balance) + ' $\n'
                                                                                                      '🧬Гипервалюта: ' + str(
                                           coins) + '\n'
                                                    '🔱Престиж: ' + str(kings) + '\n'
                                                                                 '🎟VIP Статус: Отключён'
                                          ,
                                       'random_id': 0})
                        if int(config.get('%d' % from_id, 'VIP')) == 1:
                            vk.method('messages.send',
                                      {'chat_id': chat_id,
                                       'message': '🖥' + str(nick) + ', ваш игровой профиль:\n\n'
                                                                     '💾 Игровой уровень: ' + str(lvl) + ' ур. [' + str(
                                           lvlxp) + '/' + str(lvlmxp) + '] EXP.\n'
                                                                        '💳Баланс: ' + str(balance) + ' $\n'
                                                                                                      '🧬Гипервалюта: ' + str(
                                           coins) + '\n'
                                                    '🔱Престиж: ' + str(kings) + '\n'
                                                                                 '🎟VIP Статус: Активен'
                                          ,
                                       'random_id': 0})
                    if sp[0] == '/setnick' and int(config.get('%s' % from_id, 'Rang')) >= 1:
                        allsp = 0
                        text = m[9:]
                        for i in sp:
                            allsp = int(allsp) + 1
                        print(allsp)
                        if int(allsp) >= 2 and '@' in str(message):
                            print(1)
                            user = re.findall(r'/setnick \[id(\d*)\|.*] .*', message)[0]
                            print(greg())
                            if str(user) not in greg():
                                vkmsg('❌Пользователь не найден')
                            else:
                                print(1)
                                members = \
                                vk.method("messages.getConversationMembers", {'peer_id': event.object.peer_id})['items']
                                vfd = [f"{member['member_id']}" for member in members if member['member_id']]
                                if user not in vfd:
                                    vkmsg('❌Пользователь не найден')
                                else:
                                    config.set('%s' % user, 'Nick', '%s' % text)
                                    vkmsg('☑Ник пользователя изменён на %s' % text)
                                    configupdate()
                        else:
                            vkmsg('❌Введите пользователя!')
                    if message == '/ники':
                        nicks = ''
                        num = 0
                        for i in config.get('Global', 'Regs').split(' '):
                            members = vk.method("messages.getConversationMembers", {'peer_id': event.object.peer_id})[
                                'items']
                            vfd = [f"{member['member_id']}" for member in members if member['member_id']]
                            if str(i) in str(vfd):
                                nick = config.get('%s' % i, 'Nick')
                                user = vk.method("users.get", {"user_ids": i})
                                name = user[0]['first_name']
                                surname = user[0]['last_name']
                                num = int(num) + 1
                                nicks = str(nicks) + f'\n{num}.💚@id{i}({name} {surname}) - {nick}'
                        vkmsg(f"📔Ники пользователей данной конференции\n{nicks}")
                    if sp[0] == '/pm' and event.chat_id == 3:

                        text = m[4 + int(len(sp[1])):]
                        allsp = 0
                        for i in sp:
                            allsp = int(allsp) + 1
                        if int(allsp) == 1:
                            vk.method('messages.send',
                                      {'peer_id': event.object.peer_id, 'message': '❗Введите ID репорта!',
                                       'random_id': 0})
                        else:
                            if int(allsp) == 2:
                                vk.method('messages.send',
                                          {'peer_id': event.object.peer_id, 'message': '❗Вы не ввели ответ!',
                                           'random_id': 0})
                            else:
                                if str(sp[1]) not in str(config.get('Global', 'rep').split(' ')):
                                    vk.method('messages.send',
                                              {'peer_id': event.object.peer_id, 'message': '❗Неверный ID репорта!',
                                               'random_id': 0})
                                else:
                                    if int(config.get('REPORT-%s' % sp[1], 'Work')) == 0:
                                        vk.method('messages.send',
                                                  {'peer_id': event.object.peer_id,
                                                   'message': '🔇На данный репорт уже был ответ!',
                                                   'random_id': 0})
                                    else:
                                        vk.method("messages.send", {"peer_id": config.get('REPORT-%s' % sp[1], 'peer'),
                                                                    "message": '💮' + str(
                                                                        config.get('REPORT-%s' % sp[1],
                                                                                   'name')) + ', отдел Coffee Help ответил на ваш вопрос!\n\n💬Вопрос: ' + str(
                                                                        config.get('REPORT-%s' % sp[1],
                                                                                   'text')) + '\n🗣Ответ: ' + str(text),
                                                                    'random_id': 0})
                                        vk.method('messages.send',
                                                  {'peer_id': event.object.peer_id,
                                                   'message': '🔔Вы ответили на репорт!',
                                                   'random_id': 0})
                                        config.set('REPORT-%s' % sp[1], 'Work', '0')
                                        config.set('%s' % config.get('REPORT-%s' % sp[1], 'User'), 'rep', '0')
                                        configupdate()
                    if sp[0] == '/npm' and event.chat_id == 3:
                        allsp = 0
                        for i in sp:
                            allsp = int(allsp) + 1
                        if int(allsp) == 1:
                            vk.method('messages.send',
                                      {'peer_id': event.object.peer_id, 'message': '❗Введите ID репорта!',
                                       'random_id': 0})
                        else:
                            if str(sp[1]) not in str(config.get('Global', 'rep').split(' ')):
                                vk.method('messages.send',
                                          {'peer_id': event.object.peer_id, 'message': '❗Неверный ID репорта!',
                                           'random_id': 0})
                            else:
                                if int(config.get('REPORT-%s' % sp[1], 'Work')) == 0:
                                    vk.method('messages.send',
                                              {'peer_id': event.object.peer_id,
                                               'message': '🔇На данный репорт уже был ответ!',
                                               'random_id': 0})
                                else:
                                    vk.method("messages.send", {"peer_id": config.get('REPORT-%s' % sp[1], 'peer'),
                                                                "message": '💮❗' + str(config.get('REPORT-%s' % sp[1],
                                                                                                  'name')) + ', отдел Coffee Help обнулил ваш репорт!\n\n💬Текст репорта: ' + str(
                                                                    config.get('REPORT-%s' % sp[1], 'text')),
                                                                'random_id': 0})
                                    vk.method('messages.send',
                                              {'peer_id': event.object.peer_id, 'message': '🔕Вы обнулили репорт!',
                                               'random_id': 0})
                                    config.set('REPORT-%s' % sp[1], 'Work', '0')
                                    config.set('%s' % config.get('REPORT-%s' % sp[1], 'User'), 'rep', '0')
                                    configupdate()
                    if int(config.get('%d' % from_id, 'LVLexp')) >= int(config.get('%d' % from_id, 'maxLVLexp')):
                        nick = config.get('%d' % from_id, 'Nick')
                        lvl = config.get('%d' % from_id, 'LVL')
                        lvlxp = config.get('%d' % from_id, 'LVLexp')
                        lvlmxp = config.get('%d' % from_id, 'maxLVLexp')
                        kings = config.get('%d' % from_id, 'Kings')
                        nextlvl = int(lvl) + 1
                        nextxp = int(lvlmxp) - int(lvlxp)
                        nextmxp = int(lvlmxp) * 1.3
                        k = int(lvlmxp) / 5
                        nextkings = int(kings) + k
                        if '.' in str(nextmxp):
                            nextmxp = str(nextmxp).replace(str(nextmxp).split('.')[1], '')
                            nextmxp = nextmxp.replace('.', '')
                        if '-' in str(nextxp):
                            nextxp = str(nextxp).replace('-', '')
                        if '.' in str(nextkings):
                            nextkings = str(nextkings).replace(str(nextkings).split('.')[1], '')
                            nextkings = nextkings.replace('.', '')
                        if '.' in str(k):
                            k = str(k).replace(str(k).split('.')[1], '')
                            k = k.replace('.', '')
                        config.set('%d' % from_id, 'maxLVLexp', '%s' % nextmxp)
                        config.set('%d' % from_id, 'LVLexp', '%s' % nextxp)
                        config.set('%d' % from_id, 'LVL', '%s' % nextlvl)
                        config.set('%d' % from_id, 'Kings', '%s' % nextkings)
                        vk.method("messages.send",
                                  {"peer_id": event.object.peer_id,
                                   "message": '🆕' + str(
                                       nick) + ', ваш уровень повысился!\n🔱Вы получили %s престижа!' % k,
                                   'random_id': 0})
                        with open(path, "w") as config_file:
                            config.write(config_file)
                if event.object.peer_id == event.object.from_id and from_id != 380487228:
                    vk.method("messages.send",
                              {"peer_id": event.object.peer_id,
                               "message": '⚠Данный диалог недоступен на данный момент!', 'random_id': 0})
    except Exception as err:
        print(err)
        if "code" not in str(err) and 'host' not in str(err):
            vk.method("messages.send",
                      {"peer_id": event.object.peer_id, "message": '\n❗Обнаружена ошибка: ' + str(err),
                       'random_id': 0})

