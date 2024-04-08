import re


def name_check(text: str):
    if all(ch.isdigit() for ch in text):
        raise ValueError
    return re.sub(r'[^a-zA-Zа-яА-Я0-9 ]', '', text)


def name_phone_check(text: str):
    if all(ch.isdigit() for ch in text) and len(text) == 7 or len(text) == 11:
        return text
    else:
        return re.sub(r'[^a-zA-Zа-яА-Я0-9 ]', '', text)


def phone_check(text: str):
    if all(ch.isdigit() for ch in text) and len(text) == 7 or len(text) == 11:
        return text
    raise ValueError


def address_check(text: str):
    if all(ch.isdigit() for ch in text) or all(ch.isalpha() for ch in text):
        raise ValueError
    return text


def model_check(text: str):
    if all(ch.isalpha() for ch in text):
        raise ValueError
    return text


def defect_check(text: str):
    if all(ch.isdigit() for ch in text):
        raise ValueError
    return text


def price_check(text: str):
    if all(ch.isdigit() for ch in text):
        return text
    raise ValueError
