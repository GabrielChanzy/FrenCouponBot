import sys,time,os
# from pprint import pprint
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
# from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# http://t.me/FrenCouponBot
bot = telepot.Bot(os.environ['BOT'])
gid = os.environ['GID']
wait_for_suggestion = False
nonsense = 0

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # print(content_type, chat_type, chat_id)
    slash = msg['text']
    # emoji = msg['text'].encode('unicode-escape').decode('ascii')
    # print(emoji)

    global wait_for_suggestion
    global nonsense

    if slash == "/redeem":
        print(content_type, chat_type, chat_id, '/redeem')
        nonsense = 0
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="# food\U0001f359 #", callback_data='1'), InlineKeyboardButton(text= "# htht\U0001f60a #", callback_data='2'), InlineKeyboardButton(text= "# hug\U0001f646\U0001f3fb\u200d\u2642\ufe0f #", callback_data='3')],
                [InlineKeyboardButton(text="* suggest:\U0001f937\U0001f3fb\u200d\u2642\ufe0f *", callback_data='4'), InlineKeyboardButton(text="* ask me to suggest:\U0001f937\U0001f3fb\u200d\u2640\ufe0f *", callback_data='5')],
            ])

        bot.sendMessage(chat_id, 'Choose your coupon!', reply_markup=keyboard)

    elif wait_for_suggestion:
        print(content_type, chat_type, chat_id, 'suggestion')
        nonsense = 0
        bot.sendMessage(chat_id, "Ok! Suggesting {0:s} as an activity:)".format(slash))
        bot.sendMessage(gid, "{0:s} suggests that you both {1:s} together!".format(get_handle(msg), slash))
        wait_for_suggestion = False

    elif slash == "/fly":
        print(content_type, chat_type, chat_id, '/fly')
        bot.sendMessage(chat_id, fly(), parse_mode="MarkdownV2")
        bot.sendMessage(chat_id,"Erm use desktop to see")
    
    elif slash == "/start":
        print(content_type, chat_type, chat_id, '/start')
        bot.sendMessage(chat_id, "Hi use the /redeem command to use your coupon sheet!")

    else:
        print(content_type, chat_type, chat_id, 'nonsense')
        nonsense += 1
        print("Blehh -", slash,"\nnonsense:", nonsense)
        if nonsense%3 == 0:
            if nonsense > 12:
                print("nonsense reset")
                nonsense = -2
            else: 
                bot.sendMessage(chat_id, {
                    3: "Hi use the /redeem command to use your coupon sheet!",
                    6: "Use the /redeem command to use your coupon sheet! Thanks!",
                    9: "Ok stop spamming! Use the /redeem command to use your coupon sheet!\U0001f621",
                    12: "K wad ev. Only gonna respond to /redeem\U0001f624",
                }[nonsense])


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    handle = get_handle(msg)
    print('Callback Query:', query_id, from_id, handle, query_data)

    response = {
        '1': ["Sending food coupon!", "{0:s} wants to have a meal with you!"],
        '2': ["Sending htht coupon!", "{0:s} wants to have a chat with you!"],
        '3': ["Sending hug coupon!", "{0:s} wants a hug!"],
        '4': ["What do you suggest?", "{0:s} suggests that you both {1:s} together!"],
        '5': ['Sending "ask me" coupon!', "{0:s} wants you to suggest an activity..."],
    }

    bot.answerCallbackQuery(query_id, text='*RIPPP*')
    # bot.sendMessage(from_id, fly(), parse_mode="MarkdownV2")
    bot.sendMessage(from_id, response[query_data][0])
    if query_data == '4':
        global wait_for_suggestion
        wait_for_suggestion = True
    # send to me
    if query_data != '4':   # suggestionhandled at msg function
        bot.sendMessage(gid, response[query_data][1].format(handle))


def get_handle(msg):
    if 'username' in msg['from']:
        return msg['from']['username']
    elif 'first_name' in msg['from']:
        return msg['from']['first_name']
    else:
       return "Unknown"


def fly():
    fly = [ "```",
        "                   ##################            ",
        "        OOOOOOOOO ##     TICKET     ## OOOOOOOOO ",
        "           OOOOOO ##    ---------   ## OOOOOO    ",
        "              OOO ##    * * * * *   ## OOO       ",
        "                   ##################            ",
        "                    /    /    /                  ",
        "                   .    .    .                   ",
        "                  /    /    /                    ",
        "                 .    .    .                     ",
        "                /    /    /                      ",
        "               .    .    .                       ",
        "              /    /    /                        ",
        "                                                .",
        "```",
    ]
    yes_this_is_art = "\n".join(fly)    # self-validation, checked
    # print(yes_this_is_art)
    return yes_this_is_art




if __name__ == "__main__":
    MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
    print('Listening...')

    while 1:
        time.sleep(1)

