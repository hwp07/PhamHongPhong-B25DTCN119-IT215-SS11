from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from database import Base, engine, get_db
import model
from schemas import ParkingSlotCreate
from services import create, show, show_by_id

Base.metadata.create_all(bind=engine)

app = FastAPI()


def response_json(statusCode, message, error, data, path):
    return {
        "statusCode": statusCode,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/parking-slots", status_code=status.HTTP_201_CREATED)
def create_slot(request: ParkingSlotCreate,http_request: Request,db: Session = Depends(get_db)):

    result = create(request, db)

    return response_json(
        statusCode=status.HTTP_201_CREATED,
        message="Thêm vị trí đỗ xe thành công",
        error=None,
        data={
            "id": result.id,
            "slot_code": result.slot_code,
            "zone_name": result.zone_name,
            "max_weight": result.max_weight,
            "is_available": result.is_available
        },
        path=http_request.url.path
    )


@app.get("/parking-slots", status_code=status.HTTP_200_OK)
def get_slots(http_request: Request,db: Session = Depends(get_db)):

    result = show(db)

    data = []

    for item in result:
        data.append({
            "id": item.id,
            "slot_code": item.slot_code,
            "zone_name": item.zone_name,
            "max_weight": item.max_weight,
            "is_available": item.is_available
        })

    return response_json(
        statusCode=status.HTTP_200_OK,
        message="Danh sách vị trí đỗ xe",
        error=None,
        data=data,
        path=http_request.url.path
    )


@app.get("/parking-slots/{slot_id}", status_code=status.HTTP_200_OK)
def get_slot(slot_id: int,http_request: Request,db: Session = Depends(get_db)):
    result = show_by_id(slot_id, db)

    return response_json(
        statusCode=status.HTTP_200_OK,
        message="Chi tiết vị trí đỗ xe",
        error=None,
        data={
            "id": result.id,
            "slot_code": result.slot_code,
            "zone_name": result.zone_name,
            "max_weight": result.max_weight,
            "is_available": result.is_available
        },
        path=http_request.url.path
    )