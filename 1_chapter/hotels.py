from fastapi import FastAPI, Query, Body, APIRouter
from fastapi.params import Body
from pydantic import BaseModel

from support import select_hotel_by_signature, next_hotel_id
import time
import asyncio
import threading



router = APIRouter(prefix='/hotels', tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "h_name": "Sochi best resort"},
    {"id": 2, "title": "Дубай", "h_name": "Dubai abu Dabi"},
]

######################################
# нагрузка синхронными и асинхронными запросами

@router.get('/sync/{id}')
def sync_func(id: int):
    print("\n\n")
    print(f"sync: потоков {threading.active_count()}")
    print(f'sync начал {id}: {time.time():.2f}')
    time.sleep(3)
    print(f'sync закончил {id}: {time.time():.2f}')
    return {"sync slept for id": id}


@router.get('/async/{id}')
async def async_func(id: int):
    print("\n\n")
    print(f"async: потоков {threading.active_count()}")
    print(f'async начал {id}: {time.time():.2f}')
    await asyncio.sleep(3)
    print(f'async закончил {id}: {time.time():.2f}')
    return {"async slept for id": id}
######################################


class Hotel(BaseModel):
    title: str
    h_name: str



@router.post(
    '',
    summary="получение списка отелей",
    description="описание сложной бизнес логиги",
)
def create_hotel(hotel_data: Hotel):
    global hotels
    hotel_id = next_hotel_id(hotels)
    titleIsPresent = any([hotel['title'] for hotel in hotels if hotel_data.title.lower() == hotel['title'].lower()])
    if not titleIsPresent:
        hotels.append(
            {
                "id": hotel_id,
                "title": hotel_data.title,
                "h_name": hotel_data.h_name,
            }
        )
        return {"result": f'inserted hotel "{hotel_data.title}" with id {hotel_id}'}
    else:
        return {"result": "No data inserted"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    prev = len(hotels)
    del hotels[hotel_id]
    return {'previous_entries': prev, "last_entries": len(hotels)}


@router.get('')
def get_hotels(
        id: int | None = Query(None, description="id отеля"),
        title: str | None = Query(None, description="название отеля"),
):

    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue

        hotels_.append(hotel)

    return hotels_


@router.put('/{hotel_id}')
def modify_hotel(
        hotel_id: int,
        hotel_data: Hotel,
):
    global hotels

    search_hotel = select_hotel_by_signature(hotel_id, None, hotels)
    if search_hotel:
        for hotel in hotels:
            if hotel["id"] == search_hotel["id"]:
                hotel['h_name'] = hotel_data.h_name
                hotel['title'] = hotel_data.title
                return {'result': f'updated hotel id {hotel["id"]}'}


    return {'result': 'No data updated'}


@router.patch('/{hotel_id}')
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(default=None, embed=True, strict=False),
        h_name: str | None = Body(default=None, embed=True, strict=False),
):
    global hotels

    if not title and not h_name:
        return {'result': 'No data updated'}

    search_hotel = select_hotel_by_signature(hotel_id, None, hotels)

    if search_hotel:
        for hotel in hotels:
            if hotel["id"] == search_hotel["id"]:
                if title:
                    hotel["title"] = title
                if h_name:
                    hotel["h_name"] = h_name
                return {'result': f'updated hotel id {hotel["id"]}'}

    return {'result': 'No data updated'}