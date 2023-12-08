from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass
class NaceCode:
    number: str
    description: str
    is_correted: bool = False
    correction_ranking: Optional[int] = None


@dataclass
class Address:
    street: Optional[str] = None
    number: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    additionnal_address_info: Optional[str] = None
    scraped_address: Optional[str] = None
    last_update: Optional[str] = None

@dataclass
class BoardMember:
    is_company: bool
    function: str
    name: str
    start_date: str
    linked_company_number: Optional[str] = None

@dataclass
class SocialNetwork:
    name: str
    url: str

@dataclass
class Establishment:
    company_inoopa_id: str
    establishment_number: str
    status: Optional[str] = None
    start_date: Optional[str] = None
    country: Literal["BE"] = "BE"
    address: Optional[Address] = None
    name: Optional[str] = None
    name_fr: Optional[str] = None
    name_nl: Optional[str] = None
    name_last_update: Optional[str] = None
    social_networks: Optional[List[SocialNetwork | None]] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    end_date: Optional[str] = None
    website_url: Optional[str] = None
    nace_codes: Optional[List[NaceCode | None]] = None
    is_nace_codes_corrected: Optional[bool] = False

@dataclass
class Company:
    inoopa_id: str
    company_number: str
    country: Literal["BE"] = "BE"
    legal_situation: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[str] = None
    entity_type: Optional[str] = None
    legal_form: Optional[str] = None
    name: Optional[str] = None
    name_fr: Optional[str] = None
    name_nl: Optional[str] = None
    name_last_update: Optional[str] = None
    address: Optional[Address] = None
    social_networks: Optional[List[SocialNetwork | None]] = None
    number_of_establishments: Optional[int] = None
    establishments: Optional[List[Establishment | None]] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    end_date: Optional[str] = None
    website_url: Optional[str] = None
    legal_situation_last_update: Optional[str] = None
    legal_form_last_update: Optional[str] = None
    board_members: Optional[List[BoardMember | None]] = None
    nace_codes: Optional[List[NaceCode | None]] = None
    is_nace_codes_corrected: Optional[bool] = False
    employee_category_code: Optional[int] = None
    employee_category_formatted: Optional[str] = None
