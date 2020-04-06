# -*- coding: utf-8 -*-
import requests
from googletrans import Translator
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton
import json

updater = Updater('1090208372:AAEWV97gUZEHt8-MtSC2rkIGaWKBVGYL0Rc')

MODE, CITY, LOCATION = range(3)


def start_command(bot, update):
    try:
        b = bot.get_chat_member('-1001206881648', update.message.from_user.id)
        if b.status == 'left':
            keyboard = [
                [InlineKeyboardButton('عضویت در کانال', url='https://t.me/jok_khone')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text("برای استفاده از ربات لطفا در کانال زیز عضو شوید و مجددا روی /start کلیک کنید",
                                      reply_markup=reply_markup)
        else:
            keyboards = [
                [InlineKeyboardButton('آب و هوا براساس نام شهر', callback_data='city')],
                [InlineKeyboardButton('آب و هوای محل من', callback_data='location')],
                [InlineKeyboardButton('تبلیغات', callback_data='ads'),
                 InlineKeyboardButton('دیگر ربات های ما', callback_data='robots')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboards, one_time_keyboard=True)
            update.message.reply_text("لطفا گزینه مورد نظر خود را انتخاب کنید", reply_markup=reply_markup)
            del keyboards
            del reply_markup
            del b
            return MODE
    except Exception as ex:
        print(str(ex))


def inline_buttons(bot, update):
    query = update.callback_query
    if query.data == 'city':
        try:
            keyboard = [
                [InlineKeyboardButton('توقف', callback_data='cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text('لطفا نام شهر مورد نظر را به صورت انگلیسی و یا فارسی وارد کنید.',
                                                     reply_markup=reply_markup)
            del keyboard
            del reply_markup
            return CITY
        except Exception as ex:
            print(str(ex))
    elif query.data == 'location':
        try:
            keyboard = [
                [KeyboardButton('ارسال مکان من', request_location=True)],
                [KeyboardButton('توقف')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat.id,
                                            message_id=update.callback_query.message.message_id,
                                            reply_markup=None)
            bot.delete_message(message_id=update.callback_query.message.message_id, chat_id=update.callback_query.message.chat.id)
            bot.send_message(text="لطفا موقعیت مکانی خود را برای ما ارسال کنید\n اگر از تلگرام دسکتاپ استفاده می کنید این قابلیت برای شما در دسترس نمی باشد لطفا عملیات را متوقف کنید", chat_id=update.callback_query.message.chat.id, reply_markup=reply_markup)
            del keyboard
            del reply_markup
            return LOCATION

        except Exception as ex:
            print(str(ex))
    elif query.data == 'ads':
        keyboard = [
            [InlineKeyboardButton('ارتباط با مدیر', url='https://t.me/Ashoj79')],
            [InlineKeyboardButton('توقف', callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
        query.edit_message_text('برای تبلیغات با مدیریت ارتباط برقرار کنید',
                                  reply_markup=reply_markup)
        del keyboard
        del reply_markup
        return MODE
    elif query.data == 'robots':
        keyboard=[
            [InlineKeyboardButton('ربات متن جادویی', url='https://t.me/magic_txt_bot')],
            [InlineKeyboardButton('ربات دانلود از اینستاگرام', url='https://t.me/insta_down_load_bot')],
            [InlineKeyboardButton('ربات دانلود از یوتیوب', url='https://t.me/youtube_down_load_bot')],
            [InlineKeyboardButton('ربات کوتاه کننده لینک', url='https://t.me/short_url_bot')],
            [InlineKeyboardButton('ربات مترجم فارسی', url='https://t.me/fatranslator_bot')],
            [InlineKeyboardButton('توقف', callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
        query.edit_message_text('ربات های ما',
                                  reply_markup=reply_markup)
        del keyboard
        del reply_markup
    elif query.data == 'cancel':
        keyboards = [
            [InlineKeyboardButton('آب و هوا براساس نام شهر', callback_data='city')],
            [InlineKeyboardButton('آب و هوای محل من', callback_data='location')],
            [InlineKeyboardButton('تبلیغات', callback_data='ads'),
             InlineKeyboardButton('دیگر ربات های ما', callback_data='robots')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboards, one_time_keyboard=True)
        query.edit_message_text("لطفا گزینه مورد نظر خود را انتخاب کنید", reply_markup=reply_markup)
        del keyboards
        del reply_markup
        return MODE


def city(bot, update):
    try:
        translator = Translator()
        result = translator.translate(update.message.text, src='fa', dest='en')
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + result.text + '&appid=85f6ca196ec96174cb0374ff2ea990f7&lang=fa&units=metric'
        r = requests.get(url)
        d = json.loads(r.text)
        du = json.dumps(d)
        j = json.loads(du)
        del r
        del d
        del du
        del url
        msg = ''
        if str(j["cod"]) == '200':
            msg = 'وضعیت آب و هوا: '
            if 'cloud' in str(j["weather"][0]["main"]).lower():
                msg += 'ابری'
            elif 'rain' in str(j["weather"][0]["main"]).lower():
                msg += 'بارانی'
            elif 'sun' in str(j["weather"][0]["main"]).lower():
                msg += 'آفتابی'
            elif 'wind' in str(j["weather"][0]["main"]).lower():
                msg += 'بادی'
            elif 'sno' in str(j["weather"][0]["main"]).lower():
                msg += 'برفی'
            msg += '\n\nتوضیحات: ' + str(j["weather"][0]["description"]) + '\n\nدما: ' + str(
                j["main"]["temp"]) + '\n\nبیشترین دما: ' + str(j["main"]["temp_max"]) + '\n\nکمترین دما: ' + str(
                j["main"]["temp_min"]) + '\n\n فشار: ' + str(j["main"]["pressure"]) + '\n\n رطوبت: ' + str(
                j["main"]["humidity"]) + '\n\n سرعت باد: ' + str(j["wind"]["speed"]) + '\n\n درجه جهت وزش باد: °' + str(
                j["wind"]["deg"]) + '\n\n نام شهر: ' + translator.translate(str(j["name"]), src='en',
                                                                             dest='fa').text + '\n\n کد کشور: ' + str(
                j["sys"]["country"])+'\n\n طول جغرافیایی: '+str(j["coord"]["lon"])+'\n\n عرض جغرافیایی: '+str(j["coord"]["lat"])
        elif str(j["cod"]) == '404':
            msg = 'شهر مورد نظر یافت نشد'
        elif str(j["cod"]) == '503':
            msg = 'لطفا بعدا امتحان کنید'
        keyboards = [
            [InlineKeyboardButton('آب و هوا براساس نام شهر', callback_data='city')],
            [InlineKeyboardButton('آب و هوای محل من', callback_data='location')],
            [InlineKeyboardButton('تبلیغات', callback_data='ads'),
             InlineKeyboardButton('دیگر ربات های ما', callback_data='robots')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboards, one_time_keyboard=True)
        update.message.reply_text(msg)
        update.message.reply_text("لطفا گزینه مورد نظر خود را انتخاب کنید", reply_markup=reply_markup)
        del keyboards
        del reply_markup
        del msg
        del translator
        return MODE
    except Exception as ex:
        print(str(ex))


def location(bot, update):
    bot.delete_message(message_id=update.message.message_id,chat_id=update.message.chat.id)
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather?lat=' + str(
            update.message.location.latitude) + '&lon=' + str(
            update.message.location.longitude) + '&appid=85f6ca196ec96174cb0374ff2ea990f7&lang=fa&units=metric'
        r = requests.get(url)
        d = json.loads(r.text)
        du = json.dumps(d)
        j = json.loads(du)
        del url
        del r
        del d
        del du
        msg = ''
        if str(j["cod"]) == '200':
            translator = Translator()
            msg = 'وضعیت آب و هوا: '
            if 'cloud' in str(j["weather"][0]["main"]).lower():
                msg += 'ابری'
            elif 'rain' in str(j["weather"][0]["main"]).lower():
                msg += 'بارانی'
            elif 'sun' in str(j["weather"][0]["main"]).lower():
                msg += 'آفتابی'
            elif 'wind' in str(j["weather"][0]["main"]).lower():
                msg += 'بادی'
            elif 'sno' in str(j["weather"][0]["main"]).lower():
                msg += 'برفی'
            msg += '\n\nتوضیحات: ' + str(j["weather"][0]["description"]) + '\n\nدما: ' + str(
                j["main"]["temp"]) + '\n\nبیشترین دما: ' + str(j["main"]["temp_max"]) + '\n\nکمترین دما: ' + str(
                j["main"]["temp_min"]) + '\n\n فشار: ' + str(j["main"]["pressure"]) + '\n\n رطوبت: ' + str(
                j["main"]["humidity"]) + '\n\n سرعت باد: ' + str(j["wind"]["speed"]) + '\n\n درجه جهت وزش باد: °' + str(
                j["wind"]["deg"]) + '\n\n نام شهر: ' + translator.translate(str(j["name"]), src='en',
                                                                             dest='fa').text + '\n\n کد کشور: ' + str(
                j["sys"]["country"])+'\n\n طول جغرافیایی: '+str(j["coord"]["lon"])+'\n\n عرض جغرافیایی: '+str(j["coord"]["lat"])
        elif str(j["cod"]) == '404':
            msg = 'شهر مورد نظر یافت نشد'
        elif str(j["cod"]) == '503':
            msg = 'لطفا بعدا امتحان کنید'
        keyboards = [
            [InlineKeyboardButton('آب و هوا براساس نام شهر', callback_data='city')],
            [InlineKeyboardButton('آب و هوای محل من', callback_data='location')],
            [InlineKeyboardButton('تبلیغات', callback_data='ads'),
             InlineKeyboardButton('دیگر ربات های ما', callback_data='robots')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboards, one_time_keyboard=True)
        update.message.reply_text(msg)
        update.message.reply_text("لطفا گزینه مورد نظر خود را انتخاب کنید", reply_markup=reply_markup)
        del reply_markup
        del msg
        del keyboards
        return MODE
    except Exception as ex:
        print(str(ex))


def cancel(bot, update):
    update.message.reply_text("عملیات متوقف شد", reply_text=ReplyKeyboardRemove())
    keyboards = [
        [InlineKeyboardButton('آب و هوا براساس نام شهر', callback_data='city')],
        [InlineKeyboardButton('آب و هوای محل من', callback_data='location')],
        [InlineKeyboardButton('تبلیغات', callback_data='ads'),
         InlineKeyboardButton('دیگر ربات های ما', callback_data='robots')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboards, one_time_keyboard=True)
    update.message.reply_text("لطفا گزینه مورد نظر خود را انتخاب کنید", reply_markup=reply_markup)
    del keyboards
    del reply_markup
    return MODE


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_command)],
    states={
        MODE: [CallbackQueryHandler(inline_buttons),
               MessageHandler(Filters.regex('^توقف$'), cancel)],
        CITY: [MessageHandler(Filters.text, city),
               CallbackQueryHandler(inline_buttons)],
        LOCATION: [MessageHandler(Filters.location, location),
                   MessageHandler(Filters.regex('^توقف$'), cancel)]
    },
    fallbacks=[CommandHandler('cancel', inline_buttons)]
)

dp = updater.dispatcher

dp.add_handler(conv_handler)

updater.start_polling()

updater.idle()

# url='https://api.openweathermap.org/data/2.5/weather?q=Tehran&appid=85f6ca196ec96174cb0374ff2ea990f7&lang=fa'
# r=requests.get(url)
# j=r.json()
# print(str(j))
