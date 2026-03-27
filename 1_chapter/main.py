from unicodedata import name

from fastapi import FastAPI, Query, Body
import uvicorn
from fastapi.params import Body

from support import select_hotel_by_signature

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "h_name": "Sochi best resort"},
    {"id": 2, "title": "Дубай", "h_name": "Dubai abu Dabi"},
]





@app.get('/')
def func():
    return {'hello': 'world!!!fffff'}


@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    titleIsPresent = any([hotel['title'] for hotel in hotels if title.lower() == hotel['title'].lower()])
    if not titleIsPresent:
        hotels.append(
            {
                "id": hotels[-1]["id"] + 1,
                "title": title
            }
        )
        return {"result": f'inserted hotel "{title}" with id {hotels[-1]["id"]}'}
    else:
        return {"result": "No data inserted"}


@app.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int):
    prev = len(hotels)
    del hotels[hotel_id]
    return {'previous_entries': prev, "last_entries": len(hotels)}


@app.get('/hotels')
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


@app.put('/hotels/{hotel_id}')
def modify_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        h_name: str = Body(embed=True),
):
    global hotels

    search_hotel = select_hotel_by_signature(hotel_id, None, hotels)
    if search_hotel:
        for hotel in hotels:
            if hotel["id"] == search_hotel["id"]:
                hotel['h_name'] = h_name
                hotel['title'] = title
                return {'result': f'updated hotel id {hotel["id"]}'}


    return {'result': 'No data updated'}


@app.patch('/hotels/{hotel_id}')
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


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)