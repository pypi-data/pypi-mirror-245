__ALL__ = ()

from requests import post, get

from ..exceptions import BadRequest, APINotImplemented
from .models import SMSSendSingleMessagePost, SMSGetBalance, SMSGetCampaigns


class SMS:
    def __init__(self, token):
        self._token = token
        self._basic_headers = {'Authorization': f'Bearer {self._token}',
                               'Content-Type': 'application/json'}

    def send_single_message(self,
                    message: str,
                    to: str,
                    bypass_optout: bool = None,
                    sender_id: str = None,
                    callback_url: str = None
                    ) -> models.SMSSendSingleMessagePost:
        """Send single message to a number

        Args:
            message (str): Your message
            to (str): Phone number
            bypass_optout (bool, optional): True will bypass optouts. Defaults to None.
            sender_id (str, optional): The displayed value of who sent the message. Defaults to None.
            callback_url (str, optional): A callback URL that will be used to send back information about updates of message status. Defaults to None.

        Raises:
            BadRequest

        Returns:
            models.SMSSendSingleMessagePost
        """
        
        
        URL = 'https://api.sms.to/sms/send'
        r = post(URL,
                 json={
                     'message': message,
                     'to': to,
                     'bypass_optout': bypass_optout if bypass_optout is not None else None,
                     'sender_id': sender_id if sender_id is not None else None,
                     'callback_url': callback_url if callback_url is not None else None,
                 },
                 headers=self._basic_headers)
        if r.status_code == 400:
            raise BadRequest(r.json()['message'], r)

        return SMSSendSingleMessagePost.model_validate(r.json())

    def get_balance(self) -> SMSGetBalance:
        """Get the current balance of your SMS.to account

        Raises:
            BadRequest

        Returns:
            SMSGetBalance
        """
        
        
        URL = 'https://auth.sms.to/api/balance'
        r = get(URL, headers=self._basic_headers)
        if r.status_code == 400:
            raise BadRequest(r.json()['message'], r)
        return SMSGetBalance.model_validate(r.json())
    
    def get_messages(limit: int = 15, 
                     order_direction: str = 'desc', 
                     order_by: str = 'created_at', 
                     status: str = None, 
                     to: str = None, 
                     create_at_from: str = None, 
                     create_at_to: str = None):
        URL = 'https://api.sms.to/v2/messages'
        raise APINotImpemented
        
    def get_campaigns(limit: int = 100,
                      page: int = 1,
                      search: str = None) -> SMSGetCampaigns:
        """Fetch paginated campaigns list

        Args:
            limit (int, optional): The number of campaigns per page. Defaults to 100.
            page (int, optional): The page number. Defaults to 1.
            search (str, optional): Keywords to search for. This parameter can be used to filter campaigns by phone number, specific date, source type. Defaults to None.

        Raises:
            BadRequest

        Returns:
            SMSGetCampaigns: _description_
        """
        URL = 'https://api.sms.to/v2/campaigns'
        r = get(URL, params={
            'limit': limit,
            'page': page,
            'search': search if search is not None else None
        })
        if r.status_code == 400:
            raise BadRequest(r.json()['message', r])
        
        return SMSGetCampaigns.model_validate(r.json())
    
    def get_campaign_by_id():
        URL = 'https://api.sms.to/v2/campaigns/[id]'
        raise APINotImplemented
    
    def get_last_campaign():
        URL = 'https://api.sms.to/v2/last/campaign'
        raise APINotImplemented
    
    def get_last_message():
        URL = 'https://api.sms.to/v2/last/message'
        raise APINotImplemented
    
    def get_recent_incoming_sms():
        URL = 'https://sms.to/v1/recent/inbound-sms'
        raise APINotImplemented
    
    def get_message_by_id():
        URL = 'https://api.sms.to/message/[id]'
        raise APINotImplemented
    
    def estimate_personalized_message(messages: list, 
                                      sender_id: str = None):
        URL = 'https://api.sms.to/sms/estimate'
        raise APINotImplemented
    
    def estimate_campaign_message(message: str, 
                                  to: list, 
                                  sender_id: str = None):
        URL = 'https://api.sms.to/sms/estimate'
        raise APINotImplemented
    
    def estimate_single_message(message: str,
                                to: str,
                                sender_id: str = None):
        URL = 'https://api.sms.to/sms/estimate'
        raise APINotImplemented
    
    def send_campaign_message(message: str,
                              to: list,
                              bypass_optout: bool = None,
                              sender_id: str = None,
                              callback_url: str = None):
        URL = 'https://api.sms.to/sms/send'
        raise APINotImplemented
    
    def estimate_list_message(message: str,
                              list_id: str,
                              sender_id: str = None):
        URL = 'https://api.sms.to/sms/estimate'
        raise APINotImplemented
    
    def send_message_to_list(message: str,
                             list_id: str,
                             bypass_optout: bool = None,
                             sender_id: str = None,
                             callback_url: str = None):
        URL = 'https://api.sms.to/sms/send'
        raise APINotImplemented
    
    def send_personalized_messages(messages: list,
                                   sender_id: str = None,
                                   callback_url: str = None):
        URL = 'https://api.sms.to/sms/send'
        raise APINotImplemented
    
    def schedule_sending_messages(messages: list,
                                  sender_id: str = None,
                                  scheduled_for: str = None,
                                  timezone: str = None,
                                  bypass_optout: bool = None):
        URL = 'https://api.sms.to/sms/send'
        raise APINotImplemented
    
    def send_flash_message(message: str,
                           to: str,
                           bypass_optout: bool = None,
                           sender_id: str = None,
                           callback_url: str = None):
        URL = 'https://api.sms.to/fsms/send'
        raise APINotImplemented
    