import logging
import telegram.ext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.ext.dispatcher import run_async
import parser_html
import sql_command
import os

_config = {
    "bot":{
        "token":os.environ['token']
    }
}

PORT = os.getenv('PORT', default=8443)

updater = Updater(_config['bot']['token'], workers=10, use_context=True)


@run_async
def send_async(context, *args, **kwargs):
    context.bot.send_message(*args, **kwargs)


def send_async_to_chat(dispatcher, *args, **kwargs):
    dispatcher.bot.send_message(*args, **kwargs)

def help(update, context):
    """ Prints help text """
    help_message = """
        你好‼️

    这个机器人从乌克兰发送消息🇺🇦❤️ 特别是武汉省🇨🇳 !!
    俄罗斯的宣传最终在速卖通上😡我们很不满意，因此我们的要求是对俄罗斯的打击！ 克里米亚和顿巴斯的回归。 +30,0000 迪亚.Balliv 🤑

    🏆 不要错过 Rozetka 和 Atb 的大折扣 - 不要错过！

    /update - Отримати новини з усіх каналів за останні  30 хв.
    /subscribe - Відстежувати канали
    /subscriptions - Переглянути/відредагувати список каналів
    /add (лінк на канал) - Підписатись на канал
    /dinner - Призупинити відстежування
    /unsubscribe - Відписатись та видалити усі відстежувані канали

    Для чатів використовуйте 
    /update@uanewsuabot 
    /subscribe@uanewsuabot 
    /subscriptions@uanewsuabot 
    /add@uanewsuabot  (лінк на канал)
    /dinner@uanewsuabot
    /unsubscribe@uanewsuabot 
    
    匚几闩扫闩 丫长尸闩丨卄丨 🇺🇦‼️
        """

    chat_id = update.message.chat.id
    updater.bot.send_message(chat_id=chat_id, text=help_message)

def updating(update, context):
    chat_id = update.message.chat.id
    db = sql_command.Database()
    source_list = db.get_subscriptions(chat_id)[chat_id]
    db.close()
    log_text=''
    for i in range(len(source_list)):
        print(source_list[i])
        try:
            _update=parser_html.parse_messages(source_list[i], sec_interval=60*30)
            if len(_update)>0:
                for _message in _update:
                    if _message['text'] not in log_text:
                        log_text += _message['text']
                        send_async(context, chat_id = chat_id, text = f"{'@'+_message['channel'][13:]}\n\n{_message['text']}\n{_message['id']}")

        except:
            pass
            # parser_html.clone_last_update('Error')
def get_pause(update, context):
    db = sql_command.Database()
    resp = db.edit_user(update.message.chat.id, value = 0)
    db.close()
    if resp != None: send_async(context, chat_id = update.message.chat.id, text = "Відстеження оновлень призупинено. Для поновлення - /resume")

def resume(update, context):
    db = sql_command.Database()
    resp = db.edit_user(update.message.chat.id, value = 1)
    db.close()
    if resp != None: send_async(context, chat_id = update.message.chat.id, text = "Відстеження поновлено.")

def add_channel(update, context):
    link = update.message.text.strip('/add ')
    db = sql_command.Database()
    resp = db.add_subscription(update.message.chat.id,link)
    db.close()
    if resp != None:
        send_async(context, chat_id=update.message.chat.id,
                   text=f"Ви підписались на канал {link.replace('https://t.me/','@')}")


def add_channel(update, context):
    link = update.message.text.replace('/add ',"").replace('@uanewsuabot','')
    db = sql_command.Database()
    resp = db.add_subscription(update.message.chat.id,link)
    db.close()
    if resp != None:
        send_async(context, chat_id=update.message.chat.id,
                   text=f"Ви підписались на канал {link.replace('https://t.me/','@')}")

def del_channel(update, context):
    if '/delete' in update.message.text:
        print('message handled')
        link = update.message.text.replace('/delete_','').replace('@uanewsuabot','')
        print(link)
        db = sql_command.Database()
        resp = db.del_subscription(update.message.chat.id, 'https://t.me/'+link)
        print(resp)
        db.close()
        if resp != None:
            send_async(context, chat_id=update.message.chat.id,
                       text=f"Ви відписались від каналу @{link}")
    elif "Z" in update.message.text:
        send_async(context, chat_id = update.message.chat.id, text = "😡😡😡🔥")
    else:
        pass

def get_list_subs(update, context):
    chat_id = update.message.chat.id
    db = sql_command.Database()
    list_channels = db.get_subscriptions(chat_id)[chat_id]
    list_channels = list(map(lambda link:
                             link.replace('https://t.me/','@')+" \t\t\t— /delete_%s" %(link.replace('https://t.me/','')),
                         list_channels))
    db.close()
    send_async(context, chat_id = chat_id, text="Канали, що відстежуються: \n\n" +"\n".join(list_channels))


def send_update(dp):
    print('Ohhh my child will kill russians')
    db = sql_command.Database()
    print('db connected')
    source_list = db.get_links()
    print('souce list gotten')
    print(source_list)
    db.close()
    print('db closed')
    log_text=''
    for link in list(source_list.keys()):
        print(link)
        try:
            _update=parser_html.parse_messages(link, sec_interval=30)
            if len(_update)>0:
                for _message in _update:
                    if _message['text'] not in log_text:
                        log_text += _message['text']
                        for user_id in source_list[link]:
                            print(user_id)
                            send_async_to_chat(dp, chat_id = user_id, text = f"{'@'+_message['channel'][13:]}\n\n{_message['text']}\n{_message['id']}")

        except Exception as e:
            print(e)

#
def subscribe(update, context):
    db=sql_command.Database()
    db.add_user(update.message.chat.id)
    db.close()
    updater.bot.send_message(chat_id=update.message.chat.id,
    text='Ви підпісались на оновлення. Список джерел, на які оформлена підписка: \n\n'+'\n'.join(db.default_subs))

def unsubscribe(update, context):
    db = sql_command.Database()
    db.del_user(update.message.chat.id)
    db.close()
    parser_html.clone_chat_id(update.message.chat.id)
    updater.bot.send_message(chat_id=update.message.chat.id,
    text='Бот не буде більше надсилати повідомлення до чату. Дуже шкода що вас не цікавить війна в Україні')



if __name__ == '__main__':
    print('start bot...')
    job_queue = updater.job_queue
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("update", updating))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CommandHandler("add", add_channel))
    dp.add_handler(CommandHandler("subscriptions", get_list_subs))
    dp.add_handler(CommandHandler("dinner", get_pause))
    dp.add_handler(CommandHandler("resume", resume))

    dp.add_handler(MessageHandler(telegram.ext.filters.Filters.text, del_channel))

    job_queue.run_repeating(send_update, 30)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=_config ['bot']['token'])
    updater.bot.setWebhook('https://mighty-shelf-53994.herokuapp.com/' + _config['bot']['token'])
    updater.idle()
