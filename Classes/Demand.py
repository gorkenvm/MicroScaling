import pandas as pd
import os
import numpy as np
import telebot
import logging
import sys
import json
import requests
from typing import List,Optional,Dict,Union

from Modules.Person_informations import Name_No, Duty_Place_Name
from Modules.smsService import persons_info, send_multiple_sms

from Classes.UserSession_API import UserSessionData
from Classes.DbConnect import DbConnect
from Classes.helper import Helper

db_connector = DbConnect()
connection = db_connector.connect()
UserSessions = UserSessionData()

base_directory = "temp"
# Enable logging
log_file = "bot.log"
dateformat = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s  - %(message)s",
    level=logging.INFO,
    filename=log_file,
    datefmt=dateformat,
)

logger = logging.getLogger(__name__)

TOKEN = os.environ("TOKEN")
bot = telebot.TeleBot(TOKEN)
helper = Helper(bot, logger, UserSessions)


class Demand():

    def __init__(self):
        super().__init__()

    @classmethod
    def to_list(cls, array):
        if isinstance(array, (np.ndarray, pd.Series)):
            return array.tolist()
        else:
            raise TypeError("Input is not a NumPy array")

    @staticmethod
    def Name_No():

        query1 = """
                select ISYERI_ADI,GOREV_YERI_ADI,ADI_SOYADI,cep_telefonu 
                from probs.vew_bilgileri 
                where KURUM_ID=2 and FIILI_GOREVI_KODU=2975 and ayrildi=0
                order by ISYERI_ADI
                """

        cursor = connection.cursor()
        cursor.execute(query1)
        result1 = cursor.fetchall()
        cursor.close()
        result1 = [(item[0], *item[1:]) for item in result1]
        dataFrame1 = pd.DataFrame(result1, columns=['ISYERI_ADI','GOREV_YERI_ADI','ADI_SOYADI','CEP_TELEFONU'])  # Use result1 instead of res
        dataFrame1['ISYERI_ADI'] = dataFrame1['ISYERI_ADI'].str.replace(r'\s?\(.*\)|\s?GENEL MÜDÜRLÜĞÜ', '', regex=True)
        dataFrame1['ISYERI_ADI'] = dataFrame1['ISYERI_ADI'].str.replace('İZMİR BÜYÜKŞEHİR BELEDİYESİ', 'İZBB')
        kurum_adi = dataFrame1['ISYERI_ADI'].str.replace('İZMİR BÜYÜKŞEHİR BELEDİYESİ', 'İZBB').unique()
        
        return dataFrame1,kurum_adi

    @staticmethod
    def turkish_sort_key(word):
        # Define a dictionary that assigns a sorting value to each Turkish character
        turkish_sort_order = {
            "Ç": "C",
            "ç": "C",
            "Ğ": "F",
            "ğ": "F",
            "I": "H",
            "ı": "H",
            "İ": "I",
            "i": "I",
            "Ö": "O",
            "ö": "O",
            "Ş": "S",
            "ş": "S",
            "Ü": "U",
            "ü": "U",
        }

        # Convert the word to uppercase for consistency
        word_upper = word.upper()

        # Use the custom sorting value for Turkish characters, or the original character
        sort_key = "".join(turkish_sort_order.get(char, char) for char in word_upper)

        return sort_key

    @staticmethod
    def Duty_Place_Name(organisation):
        dataframe, org = Name_No()
        dataframe2 = dataframe.loc[dataframe['ISYERI_ADI'] == organisation]


        if organisation == 'ESHOT':
            dataframe2['GOREV_YERI_ADI'] = dataframe2['GOREV_YERI_ADI'].str.replace(f'{organisation} - ', '', regex=False)
            dataframe2['GOREV_YERI_ADI'] = dataframe2['GOREV_YERI_ADI'].str.replace(' DAİRESİ BAŞKANLIĞI', '', regex=False)

        elif organisation == 'İZBB':
            dataframe2['GOREV_YERI_ADI'] = dataframe2['GOREV_YERI_ADI'].str.replace(' DAİRESİ BAŞKANLIĞI', '', regex=False)

        else:
            None

        df = dataframe2.drop(columns=['ISYERI_ADI'])
        # # Convert the modified DataFrame to a JSON object
        json_output = df.to_json(orient='records', force_ascii=False)

        json_output = json.loads(json_output)

        return json_output 

    @staticmethod
    def send_OTP_sms(number, message):
        """
        Sends a one-time password message.

        Args:
            number (str): A phone number to send the OTP to.
            message (str): The message to send.

        Returns:
            Response: The response object from the API call.
        """

        # prepare the payload
        payload = {
            "content": message,
            "receiver": number
        }
        

        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json-patch+json'
        }

        # send the post request
        response = requests.post(
            
            headers = headers,
            data = json.dumps(payload)
        )

        # return the response
        return response

    @staticmethod
    def persons_info(persons_dict,message):
        for entry,number in persons_dict.items():
            department, name = entry.split('-')
            department = department+" DAİRE BAŞKANLIĞI"
            header = f"****BAŞKANIN MESAJI****\n\n{department} - {name} :\n\n{message}\n\n ****BAŞKANIN MESAJI****\n\n"

            number = number
            print(number)
            print(header)
            Demand.send_OTP_sms(number, header)
