from event_constants import EventRemoteConstants
from dotenv import load_dotenv
load_dotenv()
from logger_local.Logger import Logger  # noqa

logger = Logger.create_logger(object=EventRemoteConstants.EVENT_REMOTE_CODE_LOGGER_OBJECT) # noqa


class EventRemoteUtil:
    @staticmethod
    def create_event_from_external_event(external_event: dict):
        event = {
            'location_id': 1,  # temp
            'organizers_profile_id': 1,  # temp
            'website_url': external_event.get('url'),
            'facebook_event_url': "",  # temp
            'meetup_event_url': "",  # temp
            'registration_url': ""  # temp
        }
        return event
