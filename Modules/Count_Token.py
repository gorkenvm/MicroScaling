import tiktoken
import openai
import random
import cx_Oracle
import pandas as pd
import openai
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)

from Modules.direct import Gpt_Maintopic_Analysis

def connect():
    dsn = cx_Oracle.makedsn(
        host='_______',  # Replace with the hostname or IP address of the Oracle server *** 19C 'ibbdb-scan'
        port='_______',      # Replace with the port number of the Oracle server
        service_name='_______'  # Replace with the service name or SID of the Oracle database *** 19C ibbdb
    )

    connection = cx_Oracle.connect(
        user='_______',      # Replace with your Oracle username
        password='_______',  # Replace with your Oracle password
        dsn=dsn,
        encoding='_______'
    )
    return connection



def Gpt_Maintopic_Data(district:str, neighborhood:str, StartDate:str, EndDate:str,MainTopic:str):

    MainTopic = MainTopic+"\n"

    query1 = """
        select ISTEK_OZETI FROM WISH4
            where ISTEK_OZETI is not null and (basvuru_no,basvuru_yili) IN 
            (
            SELECT basvuru_no,EXTRACT(YEAR FROM application_date) AS application_date
            FROM COMPLAINT3
            WHERE DISTRICT = :1 AND NEIGHBOURHOOD = :2 AND APPLICATION_DATE > :3 AND APPLICATION_DATE < :4 AND  MAIN_TOPIC = :5 )
            """

    params = []

    params.append(district)
    params.append(neighborhood)
    params.append(StartDate)
    params.append(EndDate)
    params.append(MainTopic)
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query1, params)
    result1 = cursor.fetchall()
    cursor.close()

    result1 = [(item[0].rstrip('\n'), *item[1:]) for item in result1]

    df1 = pd.DataFrame(result1, columns=['ISTEK_OZETI'])  # Use result1 instead of res

    return df1

# wishes_for_gpt = Gpt_Maintopic_Data("KONAK","ALSANCAK","01.01.2022","01.01.2023","ZABITA")

def num_tokens_from_list(list: list, encoding_name: str = "cl100k_base") -> int:

    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = []
    count_token = 0

    for index, message in enumerate(list):
        count_token = count_token + (len(encoding.encode(message)) + len(message.split(" ")))
        num_tokens.append({index:count_token})

    return num_tokens

def find_max_index_below_threshold(lst : list, threshold : int):
    max_index = -1
    max_value = 0

    for d in lst:
        index, value = next(iter(d.items()))

        if value < threshold and index > max_index:
            max_index = index
            max_value = value

    if max_index != -1:
        return max_index, max_value
    else:
        return None, None

# finds only one point for chatgpt token limit.
def subtract_value_from_list(lst : list, value : int):
    return [{k: v - value} for d in lst for k, v in d.items()]

# Find all points for chatgpt token limit
def find_and_store_pairs(lst : list, threshold : int):
    result_dict = {}
    i = 0
    keys = [key for item in lst for key in item.keys()]
    if len(keys) == 0:
        return result_dict
    key = keys[-1]

    while True :

        if lst[-1][key]> threshold:
            max_index, max_value = find_max_index_below_threshold(lst, threshold)
            result_dict[max_index] = max_value

            if max_index is None:

                break

            lst = subtract_value_from_list(lst[max_index+1 :], max_value)

            print(f"--\n{result_dict}--\n")
            all_above_threshold = all(v >= threshold for d in lst for v in d.values())

            if all_above_threshold:
                lst = subtract_value_from_list(lst[max_index + 2:], max_value)

                all_above_threshold2 = all(v >= threshold for d in lst for v in d.values())
                if all_above_threshold2:
                    break

            if lst[-1][key] < threshold:
                break
        else:
            break

    return result_dict

# BU ARAYA SAMPLİNG GELECEK

# # wishes_for_gpt = Gpt_Maintopic_Data(district="KONAK", neighborhood="KONAK", 
#                                     StartDate='01.01.2022',
#                                     EndDate='01.01.2023',
#                                     main_topic="ULAŞIM")


# main_data = wishes_for_gpt['ISTEK_OZETI'].tolist()



def token(main_data):

    token = num_tokens_from_list(main_data)

    key_points = find_and_store_pairs(token,13500)

    key_points_keys = list(key_points.keys())

    key_points_keys = [0] + [key + 1 for key in key_points_keys]

    chunk_wishes = []
    for index, key in enumerate(key_points_keys):
        if index == len(key_points_keys) - 1:
            globals()[f'liste{key}'] = main_data[key:]
            chunk_wishes.append(f'liste{key}')
        else:
            next_key = key_points_keys[index + 1]
            globals()[f'liste{key}'] = main_data[key:next_key]
            chunk_wishes.append(f'liste{key}')

            print(f"key: {key}\nnext_key:{next_key}")
    
    random_selected = random.choice(chunk_wishes)

    selected_list = globals()[random_selected]

    return selected_list


#x = token(main_data_for_gpt)

def get_completion(prompt, model="gpt-3.5-turbo-16k"):
    messages = [{"role":"user", "content":prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop = ["#", ";"]
    )
    return response.choices[0].message["content"]



def print_list(list_name):
    # Use globals() to access the variable by name
    if list_name in globals():
        print(globals()[list_name])
        print(f"----------------------------------------------\n")
    else:
        print(f"************************************************\n")

        print(f"Variable '{list_name}' not found.")


