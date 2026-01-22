from __future__ import annotations

from bs4 import BeautifulSoup
from requests.sessions import Session

from .exceptions import LoginError, TagNotFoundError


class UserPage:
    def __init__(self, session: Session):
        self.session = session
        r = self.session.get("https://chouseisan.com/user")
        r.raise_for_status()
        self.soup = BeautifulSoup(r.content, "html.parser")

    @property
    def is_authenticated(self) -> bool:
        user_link = self.soup.select_one("a[href='/user']")
        return user_link is not None

    def login(self, email: str, password: str) -> None:
        token_input = self.soup.select_one("input[name='_token']")
        if token_input is None:
            raise TagNotFoundError("input[name='_token']")

        csrf_token = token_input.get("value")

        data = {
            "_token": csrf_token,
            "email": email,
            "password": password,
            "remember": "1",
        }

        r = self.session.post(
            "https://chouseisan.com/auth/login",
            data=data,
            headers={"Referer": "https://chouseisan.com/login"},
        )
        r.raise_for_status()
        self.soup = BeautifulSoup(r.content, "html.parser")

        if not self.is_authenticated:
            raise LoginError

    def go_to_top_page(self) -> TopPage:
        return TopPage(self.session)


class TopPage:
    def __init__(self, session: Session):
        self.session = session
        r = self.session.get("https://chouseisan.com/")
        r.raise_for_status()
        self.soup = BeautifulSoup(r.content, "html.parser")

    def create_event(self, name: str, comment: str, kouho: str) -> NewEventPage:
        token = self.soup.select_one('input[name="_token"]')
        if token is None:
            raise TagNotFoundError('input[name="_token"]')

        data = {
            "_token": token["value"],
            "name": name,
            "comment": comment,
            "kouho": kouho,
        }

        url = "https://chouseisan.com/schedule/newEvent/create"

        r = self.session.post(
            url,
            data=data,
            headers={"Referer": "https://chouseisan.com/"},
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.content, "html.parser")
        return NewEventPage(self.session, soup)


class NewEventPage:
    def __init__(self, session: Session, soup: BeautifulSoup):
        self.session = session
        self.soup = soup

    def get_event_url(self) -> str:
        selector = "#listUrl"
        list_url = self.soup.select_one(selector)
        if list_url is None:
            raise TagNotFoundError(selector)
        value = list_url.get("value")
        if not value:
            value = ""
        return value[0] if isinstance(value, list) else value
