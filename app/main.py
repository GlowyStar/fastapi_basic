from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel, Field

from sqlalchemy.orm import configure_mappers
from app.orm import *
configure_mappers()

from app.bookings.router import router as router_bookings


app = FastAPI()

app.include_router(router_bookings)


class HotelsQP(BaseModel):
    location: str
    date_from: datetime
    date_to: datetime
    has_spa: Optional[bool] = False
    stars: Optional[int] = Query(None, ge=1, le=5)


class HotelSchema(BaseModel):
    address: str
    name: str
    stars: int = Field(ge=1, le=5)
    has_spa: Optional[bool] = False


@app.get("/hotels/")
def get_hotels(
        qp: HotelsQP = Depends()
) -> list[HotelSchema]:
    return [
        HotelSchema(
            address="123 Street",
            name=f"Hotel near {qp.location}",
            stars=qp.stars or 3,
            has_spa=qp.has_spa
        )
    ]
