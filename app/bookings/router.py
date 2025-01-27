from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_session
from app.bookings.schemas import BookingCreate, BookingUpdate, BookingResponse
from app.bookings.service import BookingService
from app.bookings.repository import BookingRepository


repository = BookingRepository()
service = BookingService(repository=repository)
router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[BookingResponse])
async def get_all_bookings(
    session: AsyncSession = Depends(get_session)
):
    return await service.get_all(session)


@router.get("/search", response_model=List[BookingResponse])
async def get_filtered_bookings(
    session: AsyncSession = Depends(get_session),
    user_id: Optional[int] = None,
    room_id: Optional[int] = None,
):
    return await service.get_filtered(session, user_id=user_id, room_id=room_id)


@router.get("/id/{booking_id}", response_model=BookingResponse)
async def get_booking_by_id(
    booking_id: int,
    session: AsyncSession = Depends(get_session)
):
    booking = await service.get_by_id(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found.",
        )
    return booking



@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    session: AsyncSession = Depends(get_session)
):
    return await service.create(session, booking_data)


@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    update_data: BookingUpdate,
    session: AsyncSession = Depends(get_session)
):
    updated_booking = await service.update(session, booking_id, update_data)
    if not updated_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found.",
        )
    return updated_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_session)
):
    success = await service.delete(session, booking_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found.",
        )
