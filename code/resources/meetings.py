import datetime
from flask_restful import Resource, reqparse
from models.meetings import MeetingModel

class Meeting(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('scheduled_on',
                        type = str,
                        required = True,
                        help = "This field is Required.")
    
    parser.add_argument('start_time',
                        type = datetime,
                        required = True,
                        help = "This field is Required.")

    parser.add_argument('end_time',
                        type = datetime,
                        required = True,
                        help = "This field is Required.")

    parser.add_argument('subject',
                        type = str,
                        required = True,
                        help = "This field is Required.")

    def get(self, created_by, date):
        meeting = MeetingModel.find_by_creator(created_by, date)
        if meeting:
            return meeting.json()
        return {'message': 'meet not found'}, 404

    def post(self):
        data = Meeting.parser.parse_args()

        meet = MeetingModel(**data)

        try:
            meet.save_to_db()
        except:
            return {"message": "An error occurred inserting the meet."}, 500

        return meet.json(), 201

    def delete(self, created_by, scheduled_on, start_time, end_time):
        meet = MeetingModel.find_by_time(created_by, scheduled_on, start_time, end_time)
        if meet:
            meet.delete_from_db()
            return {'message': 'meet deleted.'}
        return {"message": "meet not found."}, 404

    def put(self, scheduled_on, start_time, end_time):
        data = Meeting.parser.parse_args()

        meet = MeetingModel.find_by_time(scheduled_on, start_time, end_time)

        if meet:
            meet.scheduled_on = data['scheduled_on']
            meet.start_time = data['start_time']
            meet.end_time = data['end_time']
            meet.subject = data['subject']
        else:
            meet = MeetingModel(**data)

        meet.save_to_db()

        return meet.json()

    
class MeetingsList(Resource):
    def get(self):
        return {'Meetings': list(map(lambda x: x.json(), MeetingModel.query.all()))}