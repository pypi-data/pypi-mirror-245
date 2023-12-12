from sdk.src.utilities import create_http_headers
from url_local.url_circlez import OurUrl
from url_local.action_name_enum import ActionName
from url_local.entity_name_enum import EntityName
from url_local.component_name_enum import ComponentName
from logger_local.Logger import Logger
from event_constants import EventRemoteConstants
from util import EventRemoteUtil
import importlib
import requests
import os
import sys
from dotenv import load_dotenv
load_dotenv()
external_event_module = importlib.import_module("event-external-local.external_event_local_class")  # noqa
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
event_external_local = external_event_module.ExternalEventsLocal()

BRAND_NAME = os.getenv("BRAND_NAME")
ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME")
EVENT_API_VERSION = 1


class EventRemote:

    def __init__(self):
        self.url_circlez = OurUrl()
        self.logger = Logger.create_logger(
            object=EventRemoteConstants.EVENT_REMOTE_CODE_LOGGER_OBJECT)
        self.brand_name = BRAND_NAME
        self.env_name = ENVIRONMENT_NAME

    def get_url_by_action_name(self, action_name: ActionName,
                               path_parameters: dict = None):
        # optional query_parameters can be added if needed
        return self.url_circlez.endpoint_url(
            brand_name=self.brand_name,
            environment_name=self.env_name,
            component_name=ComponentName.EVENT.value,
            entity_name=EntityName.EVENT.value,
            version=EVENT_API_VERSION,
            action_name=action_name.value,
            path_parameters=path_parameters if path_parameters else None
        )

    def create(self, location_id: int, organizers_profile_id: int,
               website_url: str, facebook_event_url: str = '',
               meetup_event_url: str = '', registration_url: str = ''):
        event_payload_json = {
            'location_id': location_id,
            'organizers_profile_id': organizers_profile_id,
            'website_url': website_url,
            'facebook_event_url': facebook_event_url,
            'meetup_event_url': meetup_event_url,
            'registration_url': registration_url
        }
        self.logger.start("Start create event", object=event_payload_json)
        try:
            url = self.get_url_by_action_name(ActionName.CREATE_EVENT)

            self.logger.info(
                "Endpoint event  - createEvent action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())
            response = requests.post(
                url=url, json=event_payload_json, headers=headers)
            self.logger.end(
                f"End create event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            raise

    def create_external_events(self, external_events_details: list):
        external_events = {
            'external_events_details': external_events_details
        }
        self.logger.start("Start create external events",
                          object=external_events)
        try:
            url = self.get_url_by_action_name(ActionName.CREATE_EVENT)

            # temp
            url = "https://nw5y0kykwi.execute-api.us-east-1.amazonaws.com/play1/api/v1/event/createEvent"

            self.logger.info(
                "Endpoint event  - createEvent action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())
            for external_event in external_events_details:
                event_payload_json = EventRemoteUtil.create_event_from_external_event(external_event=external_event)  # noqa
                event_response = requests.post(url=url,  # noqa
                                               json=event_payload_json,
                                               headers=headers)

                event_id = event_response.json().get('event_id')   # noqa

                external_event_response = event_external_local.insert(system_id=external_event.get('system_id'),  # noqa
                                                                      subsystem_id=external_event.get('subsystem_id', None),  # noqa
                                                                      url=external_event.get('url'),  # noqa
                                                                      external_event_identifier=external_event.get('external_event_identifier'),  # noqa
                                                                      environment_id=external_event.get('environment_id', 1))  # noqa
                # TODO add list of event_id and external_id list to return
                # should be here insert into event_external_event_table

            self.logger.end("End create events-remote")
            return

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            raise

    def get_event_by_event_id(self, event_id: int):
        path_parameters = {
            'event_id': event_id
        }
        self.logger.start("Start get event-remote", object=path_parameters)
        try:
            url = self.get_url_by_action_name(
                ActionName.GET_EVENT_BY_ID, path_parameters=path_parameters)

            self.logger.info(
                "Endpoint event - getEventById action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())
            response = requests.get(url=url, headers=headers)
            self.logger.end(
                f"End get event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            raise

    def delete_event_by_id(self, event_id: int):
        path_parameters = {
            'event_id': event_id
        }
        self.logger.start("Start delete event-remote", object=path_parameters)
        try:
            url = self.get_url_by_action_name(
                ActionName.DELETE_EVENT_BY_ID, path_parameters=path_parameters)

            self.logger.info(
                "Endpoint event - deleteEventById action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())

            response = requests.delete(url=url, headers=headers)
            self.logger.end(
                f"End delete event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            raise

    def update_event_by_id(self, event_id: int, location_id: int,
                           organizers_profile_id: int, website_url: str,
                           facebook_event_url: str = '',
                           meetup_event_url: str = '',
                           registration_url: str = ''):

        object_start = {
            'event_id': event_id,
            'location_id': location_id,
            'organizers_profile_id': organizers_profile_id,
            'website_url': website_url,
            'facebook_event_url': facebook_event_url,
            'meetup_event_url': meetup_event_url,
            'registration_url': registration_url
        }
        self.logger.start("Start update event-remote", object=object_start)
        try:
            path_parameters = {
                'event_id': event_id
            }
            url = self.get_url_by_action_name(
                ActionName.UPDATE_EVENT_BY_ID, path_parameters=path_parameters)

            event_payload_json = {
                "location_id": location_id,
                "organizers_profile_id": organizers_profile_id,
                "website_url": website_url,
                "facebook_event_url": facebook_event_url,
                "meetup_event_url": meetup_event_url,
                "registration_url": registration_url
            }

            self.logger.info(
                "Endpoint event - updateEventById action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())

            response = requests.put(
                url=url, json=event_payload_json, headers=headers)
            self.logger.end(
                f"End update event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            raise
