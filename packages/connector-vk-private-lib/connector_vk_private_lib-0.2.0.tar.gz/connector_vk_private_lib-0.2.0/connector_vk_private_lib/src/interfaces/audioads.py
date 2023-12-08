from typing import Optional

from pydantic import BaseModel


class AudioAds(BaseModel):
    content_id: Optional[str]
    duration: Optional[str]
    account_age_type: Optional[str]
