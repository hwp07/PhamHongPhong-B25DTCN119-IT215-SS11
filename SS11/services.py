from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, status

from model import ParkingSlotModel
from schemas import ParkingSlotCreate


def create(request: ParkingSlotCreate, db: Session):
    slot = db.query(ParkingSlotModel).filter(ParkingSlotModel.slot_code == request.slot_code).first()

    if slot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot code already exists"
        )

    new_slot = ParkingSlotModel(
        slot_code=request.slot_code,
        zone_name=request.zone_name,
        max_weight=request.max_weight,
        is_available=request.is_available
    )

    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return new_slot

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot code already exists"
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )


def show(db: Session):
    return db.query(ParkingSlotModel).all()


def show_by_id(slot_id: int, db: Session):
    slot = db.query(ParkingSlotModel).filter(ParkingSlotModel.id == slot_id).first()

    if slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking slot not found"
        )

    return slot