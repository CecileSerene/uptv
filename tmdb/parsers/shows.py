"""Parsers of show objects."""

from datetime import datetime
from typing import Union

from .mixins import ImageParserMixin, ImageSize
from .base import Parser, ParserGroup
from ..datatypes import Show


class BaseShowParser(ImageParserMixin, Parser[Show]):
    """Abstract parser class for show objects.

    Defines a few utility methods, but concrete subclasses must implement
    the .get_kwargs() method.
    """

    object_class = Show

    def _get_logo_path(self, data: dict, size: ImageSize) -> str:
        return self.get_image_or_placeholder_url(data['poster_path'], size=size)

    def _get_small_logo_path(self, data: dict):
        return self._get_logo_path(data, size=ImageSize.SMALL)

    def _get_big_logo_path(self, data: dict):
        return self._get_logo_path(data, size=ImageSize.BIG)

    @staticmethod
    def _parse_date(date: Union[str, None]) -> datetime.date:
        """Parse a date (which might be null) as returned by the API."""
        if date is None:
            return None
        return datetime.strptime(date, '%Y-%m-%d')


class ShowListParser(BaseShowParser):
    """Parser of Show objects suited for displaying them in lists."""

    def get_kwargs(self, data: dict) -> dict:
        return {
            'id': data['id'],
            'title': data['name'],
            'small_logo_path': self._get_small_logo_path(data),
        }


class ShowDetailParser(ShowListParser):
    """Parser of Show objects with all their details."""

    def _get_next_episode_date(self, data: dict) -> Union[datetime.date, None]:
        next_episode: dict = data['next_episode_to_air'] or {}
        return self._parse_date(next_episode.get('air_date'))

    def get_kwargs(self, data: dict) -> dict:
        return {
            **super().get_kwargs(data),
            'synopsis': data['overview'],
            'big_logo_path': self._get_big_logo_path(data),
            'genres': [genre['name'] for genre in data['genres']],
            'directors': [director['name'] for director in data['created_by']],
            'creation_date': self._parse_date(data['first_air_date']),
            'last_episode_date': self._parse_date(data['last_air_date']),
            'next_episode_date': self._get_next_episode_date(data),
            'number_of_seasons': data['number_of_seasons'],
        }


class ShowParser(ParserGroup[Show]):
    """Parser of show objects.

    Defines how to parse lists and details of shows.
    """

    list_parser_class = ShowListParser
    detail_parser_class = ShowDetailParser
