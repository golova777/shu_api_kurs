from typing import Dict, List


def get_last_page(all_entries_len: int, per_page: int):
    DEFAULT_LAST_PAGE: int = 1
    ostatok = all_entries_len % per_page

    if type(all_entries_len) is not int:
        return DEFAULT_LAST_PAGE
    if type(per_page) is not int:
        return DEFAULT_LAST_PAGE
    if not all_entries_len or not per_page:
        return DEFAULT_LAST_PAGE
    if all_entries_len < per_page:
        return DEFAULT_LAST_PAGE

    if ostatok == 0:
        return all_entries_len // per_page
    else:
        return all_entries_len // per_page + 1


def next_hotel_id(hotels: list) -> int:
    # выдаёт следующий свободгный id для нового отеля
    max_hotel_id = 0
    for hotel in hotels:
        h_id = hotel.get("id", None)
        if h_id:
            if h_id > max_hotel_id:
                max_hotel_id = h_id

    return max_hotel_id + 1



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