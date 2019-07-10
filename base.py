from abc import ABCMeta, abstractmethod
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()


class BaseScrapper(object):
    url = None
    _data = []
    as_json = False
    next_selector = None
    follow = False
    filename = None
    save_as_file = False
    parser = "html.parser"

    __metaclass__ = ABCMeta

    def get_url(self):
        assert self.url is not None, (
            '`url` can not be None'
        )

        return self.url

    def get_next_selector(self):
        assert self.follow, (
            '`follow` need to be set as True'
        )
        assert self.next_selector is not None, (
            'You have set `follow` as True, so `next_selector` can not be None'
        )
        return self.next_selector

    def get_filename(self):
        assert self.save_as_file, (
            '`save_as_file` need to be set as True'
        )
        assert self.filename is not None, (
            'You have set `save_as_file` as True, so `filename` can not be None'
        )
        return self.filename

    def perform_request(self):
        return requests.get(self.get_url())

    def get_html(self):
        return self.perform_request().content

    def get_soup(self):
        return BeautifulSoup(self.get_html(), self.parser)

    def get_next_url(self):
        try:
            return self.get_soup().select_one(self.get_next_selector()).attrs.get('href')
        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def reproduce(cls, url):
        cls.url = url
        return cls()

    def __del__(self):
        scrapped_data = list(self.scrap(self.get_soup()))
        self._data.extend(scrapped_data)

        if self.follow:
            if self.get_next_url():
                self.url = self.get_next_url()
                return self.reproduce(self.url)

        if self.as_json:
            from json import dumps
            self._data = dumps(self._data)

        if self.save_as_file:
            open(self.get_filename(), 'w').write(self._data)

    def get_data(self):
        return self._data

    @abstractmethod
    def scrap(self, soup):
        ...
