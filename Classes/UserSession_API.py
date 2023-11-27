from typing import Optional, List

class UserSessionData:
    # Initializing the UserSessionData class with default values
    def __init__(
        self,
        username: str = '',
        district: str = '',
        neighborhood: str = '',
        startDate:  str = '',
        endDate: str = '',
        MainTopic: str = '',
        SubTopic: str = '',
        Stratejik_Alan : list = [],
        Durum : list = [],
        Organisation: str = '', 
        Messages : list = [],
        Persons : dict = {}
    ):
        self.username = username
        self.district = district
        self.neighborhood = neighborhood
        self.startDate = startDate         # ("%d.%m.%Y")
        self.endDate = endDate


        self.MainTopic = MainTopic        # HİM
        self.SubTopic = SubTopic          # HİM

        self.Stratejik_Alan = Stratejik_Alan          # HİM
        self.Durum = Durum          # HİM

        self.Organisation = Organisation  # DEMAND
        self.Messages = Messages          # DEMAND
        self.Persons = Persons            # DEMAND

        self.sessions = [] 
    
       

    @classmethod
    def from_json(cls, json) -> 'UserSessionData' :
        # Create a new instance of UserSessionData and populate it from the JSON data
        instance  = cls(
            username=json.get('username', ''),
            district=json.get('district', ''),
            neighborhood=json.get('neighborhood', ''),
            startDate=json.get('startDate', ''),
            endDate=json.get('endDate', ''),
            MainTopic=json.get('MainTopic', ''),
            SubTopic=json.get('SubTopic', ''),
            Organisation=json.get('Organisation', ''),
            Messages=json.get('Messages', ''),
            Persons=json.get('Persons', ''),
            Stratejik_Alan=json.get('Stratejik_Alan', ''),
            Durum=json.get('Durum', '')
            
        )
            
        

        instance.sessions.append({
            'username': instance.username,
            'district': instance.district,
            'neighborhood': instance.neighborhood,
            'startDate': instance.startDate,
            'endDate': instance.endDate,
            'MainTopic': instance.MainTopic,
            'SubTopic': instance.SubTopic,
            'Organisation': instance.Organisation,
            'Messages': instance.Messages,
            'Persons': instance.Persons,
            'Stratejik_Alan': instance.Stratejik_Alan,
            'Durum': instance.Durum
        })

        return instance 

    def create_new_user(self, userSessionData) -> 'UserSessionData':

        self.sessions.append(userSessionData)
        # return as UserSessionData object
        return userSessionData


    # Method to get a user session
    def get_user_session(self, message) -> 'UserSessionData':
        # check if user is in sessions
        for session in self.sessions:
            if session.user_id == message.from_user.id:
                return session
        # if user is not in sessions, create new user
        return self.create_new_user(message)
 
    
    # Method to get user session index
    def get_user_session_index(self, message) -> int:
        return self.sessions.index(self.get_user_session(message))

    # Method to get user session by index
    def get_user_session_by_index(self, index):
        return self.sessions[index]

    # Method to get user session by user id
    def get_user_session_by_user_id(self, user_id) -> Optional['UserSessionData']:
        for session in self.sessions:
            if session.user_id == user_id:
                return session
        return None    

    # Method to remove a user session
    def remove_user_session(self, message) -> None:
        self.sessions.remove(self.get_user_session(message))

    # Method to check if user has set location
    def check_user_set_location(self, user) -> bool:
        if user.neighborhood == '' or user.district == '':
            return False
        else:
            special_mapping = str.maketrans({"i": "İ", "ı": "I"})
            user.neighborhood = user.neighborhood.translate(special_mapping).upper()
            user.district = user.district.translate(special_mapping).upper()
            return True


    


    
        # if user.district != ''  and  user.neighborhood != '' :
        #     df = him.complaint_query_1('KONAK','ALSANCAK')
        #     return jsonify(df)

        # elif user.lat != 0.0 and user.lon != 0.0 :
        #     return jsonify({"İNFO": "GOOGLE API YE GİT!"}), 400
        
        # elif user.lat == 0.0 or user.lon == 0.0 :
        #     return jsonify({"error": "district-neighborhood OR lat-lon SET!"}), 400
        # else:
        #     return jsonify({"OK": "Required parameters SET !"}), 200