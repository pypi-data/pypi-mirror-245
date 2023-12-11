from pydantic import BaseModel
from pydantic import Field
from typing import Optional, Union, List

class SMSSendSingleMessagePost(BaseModel):
    message: str
    success: bool
    message_id: str


class SMSGetBalance(BaseModel):
    balance: float
    currency: str


class _SMSGetCampaignsData(BaseModel):
    id: str
    type: str
    user_id: int
    sender_id: str
    template_id: Optional[Union[str, int]]
    message: str
    list_id: Optional[Union[str, int]]
    status: str
    client_total_cost: float
    estimated_cost: float
    delivered_messages: int
    failed_messages: int
    pending_messages: int
    sent_messages: int
    bypass_optout: int
    callback_url: str
    scheduled_for: int
    timezone: str
    created_at: str
    updated_at: str
    sms_count: int
    is_api: int
    canceled_at: str
    
class _SMSGetCampaignsLink(BaseModel):
    url: Optional[str]
    label: str
    active: bool
    

class SMSGetCampaigns(BaseModel):
    success: bool
    data: List[_SMSGetCampaignsData]
    links: List[_SMSGetCampaignsLink]
    current_page: int
    from_: int = Field(alias='from')
    last_page: int
    path: str
    per_page: int
    to: int
    total: int
    