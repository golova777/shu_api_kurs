from fastapi import FastAPI, Query
import uvicorn



app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Дубай"},
]



@app.get('/')
def func():
    return {'hello': 'world!!!fffff'}


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


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)