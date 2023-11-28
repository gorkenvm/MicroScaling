# define class with some helper functions with self init gets all imported modules and variables from main.py 
from telebot import types
import telebot
from logging import Logger

import Classes.UserSession_API as UserSession_API
from Classes.UserSession_API import UserSessionData



admins = []
# check and create admins.txt file if not exists
try:
    with open("admins.txt", "r") as f:
        admins = f.read().splitlines()
except:
    with open("admins.txt", "w") as f:
        f.write("1569925904")
    admins = ['1569925904'] # default admin id

# erenizmirbot 6647924449:AAECe340pjpMWnoZFFORaR5TM4DsfdmiZm4
# microizmir 6472809175:AAEffcb3Y0cVkDN2951yea8M4Zx6QiLIpq4
# izbblog_bot 6622880820:AAGfl9vuw9habaF0ObK23gHOeoO2rh76JK0
TOKEN = "6622880820:AAGfl9vuw9habaF0ObK23gHOeoO2rh76JK0"

admin_bot = telebot.TeleBot(TOKEN)

class Helper:
    global admins
    def __init__(self, bot: telebot, logger: Logger, user_sessions: UserSession_API):
        self.bot = bot
        self.logging = logger
        self.UserSessions = user_sessions

    def delete_last_message(self,user: 'UserSessionData'):
        self.bot.delete_message(chat_id=user.last_message.chat.id, message_id=user.last_message.message_id)
        
    def inform_admins(self, error_message):
        for admin in admins:
            admin_bot.send_message(admin, error_message)
    
    def StartSession(self, message: 'telebot.types.Message'):
        user = self.UserSessions.create_new_user(message) # removes any existing session and create a new one
        self._StartSession(user)
        
    def StartSessionByUser(self, user):
        self._StartSession(user)
            
    def _StartSession(self, user: 'UserSessionData'):
        try:
            self.logging.info(f"{user.first_name} - {user.user_id} started a new session")
            # Create a custom keyboard markup for menu buttons
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            talep_gonder = types.KeyboardButton("TALEP GÖNDER")
            konum_button = types.KeyboardButton("🌍 KONUM GÖNDER", request_location=True)
            tarih_button = types.KeyboardButton("📅 TARİH SEÇ")
            yeniden_baslat = types.KeyboardButton("🔄 YENİDEN BAŞLAT")
            markup.add(konum_button, tarih_button, yeniden_baslat, talep_gonder)

            # Send the welcome message with menu buttons
            welcome_message = f"""
                👋 MERHABA  <b>{user.first_name}</b>!

                🤖 İZMİR BÜYÜKŞEHİR BELEDİYESİNİN GÜCÜYLE İZMİRİN KALBİNDEN ELDE ETTİĞİM BİLGİLER IŞIGINDA SİZLERE YARDIMCI OLACAĞIM.🚀
                    
                MİKRO ÖLÇEKLENDİRME YÖNTEMİYLE FALİYET RAPORLARINI VE HEMŞERİ İLETİŞİM MERKEZİNDEN GELEN VERİLERİ İNCELEYEREK SİZLERE ANLAMLI VERİLER SUNMAK İÇİN GÖREVLENDİRİLDİM.
                
                BUTONLAR VE AÇIKLAMALARI :  
                
                🌍 <b>KONUM GÖNDER</b> tuşuna basarak bulunduğunuz yer'i yada 📎 İşaretine basarak Haritadan Analiz Yapmak istediğiniz her hangi bir yeri göndermelisiniz. 📍

                📅 <b>TARİH SEÇ</b> : Analiz yapmak istediğiniz tarihi seçebilirsiniz. ❗❗

                🤖 <b>AI</b> :  Yapay Zeka ile istek içeriklerinin analiz edilmesi ve öneride bulunulması

                ↩️ <b>GERİ</b> : Bir Önceki Sayfaya gidilmesini sağlar.

                📂 <b>VERİ</b> : HİM verileri ve faaliyet raporları kullanılarak analizler yapılacaktır.

                🔄 <b><i>Tekrar Başlatmak için /start tuşuna basınız!</i></b> 🌟


            """
            self.bot.send_message(
                user.user_id, welcome_message, parse_mode="HTML", reply_markup=markup
            )
            self.inform_admins(f"User {user.first_name} - {user.user_id} started a new session")
            
        except Exception as e:
            self.logging.error(
                f"{user.first_name}_{user.user_id} - Error in StartSession: {e}"
            )
            self.inform_admins(f"User {user.first_name} - {user.user_id} started a new session but got an error: {e}")