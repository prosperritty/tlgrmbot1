import telebot

TOKEN = '***'

bot = telebot.TeleBot(TOKEN)

user_dict = {}
class User:
    def __init__(self, name):
        self.name = name
        self.subject = None
        self.comm = None
        
@bot.message_handler(commands=['start', 'send'])
def send_welcome(message):
    msg = bot.reply_to(message, "Welcome!\nWrite the subject you want to comment on.")
    bot.register_next_step_handler(msg, process_subject_step)
    
def process_subject_step(message):
    try:
        chad_id = message.chat.id
        try:
            name = '@' + message.from_user.username
        except:
            name = message.from_user.first_name
        user = User(name)
        user_dict[chad_id] = user
        subject = message.text
        user.subject = subject
        msg = bot.reply_to(message, 'Leave a comment here.')
        bot.register_next_step_handler(msg, process_comm_step)
    except Exception as a:
        bot.reply_to(message, 'oppps') 

def process_comm_step(message):
    try:
        chat_id = message.chat.id
        comm = message.text 
        user = user_dict[chat_id]
        user.comm = comm
        bot.send_message(chat_id, 'Thank, ' + user.name + ', for your comment on subject: ' + user.subject + "\n\n" + user.comm)
    except Exception as a:
        bot.reply_to(message, 'oppps') 
    with open('info.txt', 'a+', encoding='utf-8') as file:
            file.write( '\n\n' + user.name + '\n' + user.subject + '\n' + user.comm)
            file.close
    
    
bot.infinity_polling()