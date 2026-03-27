from typing import Dict, List

def select_hotel_by_signature(
        hotel_id: int | None,
        hotel_title: str | None,
        hotels: List[Dict],
):
    # ничего не указано
    if not hotel_id and not hotel_title:
        return None

    # указаны и ID отлея, и Title отеля
    if hotel_id and hotel_title:
        for hotel in hotels:
            if hotel["id"] == hotel_id and hotel["title"] == hotel_title:
                return hotel

    # указан только ID отеля
    if hotel_id and not hotel_title:
        for hotel in hotels:
            if hotel["id"] == hotel_id:
                return hotel

    # указан только Title отеля
    if not hotel_id and hotel_title:
        for hotel in hotels:
            if hotel["title"] == hotel_title:
                return hotel

    # обработаем иные случаи
    return None