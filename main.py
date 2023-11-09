import telebot
from telebot import types
import logging
import json
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from Classes.UserSession_API import UserSessionData
from Classes.DbConnect import DbConnect
from Classes.Him import Him
from Classes.Demand import Demand
from Classes.Activity import Activity
from Classes.helper import Helper

app = Flask(__name__)
CORS(app)

class TurkishJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs['ensure_ascii'] = False
        super(TurkishJSONEncoder, self).__init__(*args, **kwargs)

    def default(self, o):
        if isinstance(o, str):
            return o.encode('utf-8').decode('unicode-escape')
        return super(TurkishJSONEncoder, self).default(o)

app.json_encoder = TurkishJSONEncoder


db_connector = DbConnect()
connection = db_connector.connect()
UserSessions = UserSessionData()
him = Him()
demand = Demand()
activitiy = Activity()

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

TOKEN = "6647924449:AAECe340pjpMWnoZFFORaR5TM4DsfdmiZm4"
bot = telebot.TeleBot(TOKEN)
helper = Helper(bot, logger, UserSessions)

#_____________________________________________#
#_______________HİM___________________________#
#_____________________________________________#
@app.route('/Him/MainTopics', methods=['POST'])  # district, neighborhood
def GetMainTopics():
    try:
        json = request.get_json()
        user = UserSessionData.from_json(json)
        if user.district != ''  and  user.neighborhood != '' :
            df = him.complaint_query_1(user.district,user.neighborhood,user.startDate,user.endDate)
            return jsonify(df)
        else:
            return jsonify({"OK": "Required district and neighborhood Correctly parameters SET !"}), 200
    except Exception as e:
        logger.error(
            f"{user.username}_{GetMainTopics.__name__} Jsonify Error: %s",
            str(e),
        )
        helper.inform_admins(
            f"{user.username} ❌ Got Error ❌\n  {str(e)}"
        )

@app.route('/Him/MainImages', methods=['POST'])  # district, neighborhood
def GetMainImagesHim():
    try:
        json_data = request.get_json()
        user = UserSessionData.from_json(json_data)
        
        if user.district != '' and user.neighborhood != '':
            # PLOT
            him.plot_complaints(user.district, user.neighborhood)
            path_to_send = Him.create_zip_tosend()
            # Return the ZIP file as an attachment
            return send_file(path_to_send,  mimetype='application/zip',as_attachment=True, download_name='general_analysis_images.zip')
        else:
            return jsonify({"ERROR": "Required district and neighborhood parameters correctly SET!"})
    except Exception as e:
        logger.error(
            f"{GetMainImagesHim.__name__} Jsonify Or Location Error : %s",
            str(e),
        )
        helper.inform_admins(
            f"{GetMainImagesHim.__name__} ❌ Got Error ❌\n  {str(e)}"
        )

@app.route('/Him/MainTopicResults', methods=['POST'])  # district, neighborhood, startDate, endDate
def GetMainTopicResults():
        try:
            json_data = request.get_json()
            user = UserSessionData.from_json(json_data)
        
            if user.district != '' and user.neighborhood != '' and user.startDate != '' and user.endDate != '':
                # PLOT
                topic_results = him.MainIssues(user.district,user.neighborhood,user.startDate,user.endDate)

                # Return the ZIP file as an attachment
                return jsonify(topic_results)
            else:
                return jsonify({"ERROR": "Required district and neighborhood parameters correctly SET!"})
        except Exception as e:
            logger.error(
                f"{user.username} {GetMainTopicResults.__name__} Jsonify Error: %s",
                str(e),
            )
            helper.inform_admins(
                f"{user.username}  {GetMainTopicResults.__name__} ❌ Got Error ❌\n  {str(e)}"
            )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5500)






