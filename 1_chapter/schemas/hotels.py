from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    h_name: str



class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    h_name: str | None = Field(None)