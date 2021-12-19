from flask_restful import Resource, reqparse
import sqlalchemy
from models.users import UserModel
from models.meetings import MeetingModel
import datetime

class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('first_name',
                        type = str,
                        required = True,
                        help = "This field is Required.")

    parser.add_argument('last_name',
                        type = str,
                        required = True,
                        help = "This field is Required.")

    parser.add_argument('username',
                        type = str,
                        required = True,
                        help = "This field is Required.")

    parser.add_argument('email',
                        type = str,
                        required = True,
                        help = "This field is Required.")

    parser.add_argument('password',
                        type = str,
                        required = True,
                        help = "This field is Required.")\

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with username already exists. Please select different username"}

        user = UserModel(data['first_name'], data['last_name'], data['username'], data['email'], data['password'])

        user.save_to_db()

        return {"message": "User created successfuly."}
    
    #get all meetings
    def get(self, user_id, scheduled_on):
        meetings = MeetingModel.num_of_meets_for_user(user_id, scheduled_on)

        return meetings.json()

class UserMeeting(Resource):
    #get total Meets
    def get(self, user_id, scheduled_on, start_time, end_time):
        meetings = MeetingModel.num_of_meets_for_user(user_id, scheduled_on)

        meets = meetings.json()
        total_meets = 0
        for meet in meets:
            if meet['end_time']>=datetime.strptime(start_time, '%d-%m-%Y') and meet['start_time']<=datetime.strptime(end_time, '%d-%m-%Y'):
                total_meets+=1
        
        if total_meets:
            return {"message": "Total meets in requested time frames are {}".format(total_meets)}
        return{"message": "There are no meets for requested time frame."}

class UserMeetCount(Resource):
    #total number of meets
    def get_meeting_count(self, user_id, scheduled_on):
        meetings = MeetingModel.num_of_meets_for_user(user_id, scheduled_on)
        meetings_count = meetings.json()
        total = len(meetings_count)
        if len:
            return {"message": "User have {} number of meetings.".format(total)}, 200
        return {"message": "No meetings scheduled for today"}, 200

class UserMeetTime(Resource):
    #total time spent
    def get(self, user_id, scheduled_on):
        meetings = MeetingModel.num_of_meets_for_user(user_id, scheduled_on)
        total_time = meetings.json()

        time_count = 0
        for time in total_time:
            time_count+=time['total_time']
        total_hours = time_count//60
        return {"message":"Totday you have to spend {} mins and {} hrs in meetings".format(time_count, total_hours)}
    