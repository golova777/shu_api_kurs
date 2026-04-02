from fastapi import FastAPI, Query, Body, APIRouter


from support import select_hotel_by_signature, next_hotel_id, get_last_page
import time
import asyncio
import threading

from schemas.hotels import Hotel, HotelPATCH
from api_examples.post_endpoints import post_create_hotel


router = APIRouter(prefix='/hotels', tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "h_name": "Sochi best resort"},
    {"id": 2, "title": "Дубай", "h_name": "Dubai abu Dabi"},
    {"id": 3, "title": "Шелестоф", "h_name": "Костромской отель"},
    {"id": 4, "title": "Москва", "h_name": "Лучшее в москвке"},
    {"id": 5, "title": "Ярославль-сити", "h_name": "Маленький отель в Ярославле"},
    {"id": 6, "title": "Саратовские ждуны", "h_name": "Саратов отдыхает"},
    {"id": 7, "title": "Лещ да рыбалка", "h_name": "в романтикой рыбалки"},
    {"id": 8, "title": "Мария", "h_name": "Дорошлй отель в Костроме"},
    {"id": 9, "title": "Гос-отель", "h_name": "Всё регламентировано!"},
]

DEFAULT_PER_PAGE = 3
DEFAULT_PAGE = 1

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


@router.post(
    '',
    summary="получение списка отелей",
    description="описание сложной бизнес логиги",
)
def create_hotel(
        hotel_data: Hotel = Body(openapi_examples=post_create_hotel)
):
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
        hotel_id: int | None = Query(None, description="id отеля"),
        title: str | None = Query(None, description="название отеля"),
        page: int | None = Query(None, description="страница списка отелей"),
        per_page: int | None = Query(None, description="количество отелей на страницу (1-5)")
):
    if not per_page:
        per_page = DEFAULT_PER_PAGE
    if per_page > 5:
        per_page = DEFAULT_PER_PAGE

    last_page_num = get_last_page(len(hotels), per_page)

    if not page:
        page = DEFAULT_PAGE

    if page > last_page_num:
        page = DEFAULT_PAGE

    hotels_ = []
    for hotel in hotels:
        if hotel_id and hotel['id'] != hotel_id:
            continue
        if title and hotel['title'] != title:
            continue

        hotels_.append(hotel)

    if len(hotels_) == 1:
        return hotels_
    else:
        # пагинация
        start_pos = (page - 1) * per_page
        end_pos = start_pos + per_page

        return hotels_[start_pos: end_pos]


@router.put('/{hotel_id}')
def modify_hotel(hotel_id: int, hotel_data: Hotel):
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
        hotel_data: HotelPATCH,
):
    global hotels

    if not hotel_data.title and not hotel_data.h_name:
        return {'result': 'No data updated'}

    search_hotel = select_hotel_by_signature(hotel_id, None, hotels)

    if search_hotel:
        for hotel in hotels:
            if hotel["id"] == search_hotel["id"]:
                if hotel_data.title:
                    hotel["title"] = hotel_data.title
                if hotel_data.h_name:
                    hotel["h_name"] = hotel_data.h_name
                return {'result': f'updated hotel id {hotel["id"]}'}

    return {'result': 'No data updated'}