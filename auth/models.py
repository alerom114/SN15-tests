from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel, EmailStr, validator, Field

class HotkeyType(Enum):
    MINER = "miner"
    VALIDATOR = "validator"


class Axon(BaseModel):
    ip: str
    port: int
    ip_type: int
    
class Hotkey(BaseModel):
    hotkey: str
    coldkey: str
    uid: int
    netuid: int
    rank: float
    emission: float
    incentive: float
    consensus: float
    trust: float
    validator_trust: float
    dividends: float
    last_update: int
    validator_permit: bool
    axon: Axon
    
    hotkeyMetadata: Optional[Dict]
    hotkeyType: str = HotkeyType.MINER.value

    @validator('hotkeyType', pre=True)
    def convert_type_to_string(cls, v):
        if isinstance(v, HotkeyType):
            return v.value
        return v
    
    @staticmethod
    def from_neuron(neuron):
        return Hotkey(
            hotkey=neuron.hotkey,
            coldkey = neuron.coldkey,
            uid = neuron.uid,
            netuid = neuron.netuid,
            rank = neuron.rank,
            emission = neuron.emission,
            incentive = neuron.incentive,
            consensus = neuron.consensus,
            trust = neuron.trust,
            validator_trust = neuron.validator_trust,
            dividends = neuron.dividends,
            last_update = neuron.last_update,
            validator_permit = neuron.validator_permit,
            axon = Axon(
                ip = neuron.axon_info.ip,
                port = neuron.axon_info.port,
                ip_type = neuron.axon_info.ip_type,
            )
        )


class UserRegistrationModel(BaseModel):
    userName: str
    email: EmailStr
    password: str

class UserResponseModel(BaseModel):
    userId: Optional[str] = Field(None, alias="_id")
    userName: str
    email: EmailStr
    hotkeys: List[Hotkey] = []
    jwtRefreshTokens: Optional[List[str]] = []


class ForgotPasswordModel(BaseModel):
    email: EmailStr


class ResetPasswordModel(BaseModel):
    token: str
    new_password: str