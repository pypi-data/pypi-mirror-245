'''Scrape Webtoons from Naver Webtoon.'''

from __future__ import annotations
from itertools import count
import logging
from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING, ClassVar

from typing_extensions import override

from .A_scraper import Scraper, reload_manager
from ..exceptions import InvalidPlatformError, UnsupportedWebtoonRating


class NaverWebtoonScraper(Scraper[int]):
    '''Scrape webtoons from Naver Webtoon.'''
    BASE_URL = 'https://comic.naver.com/webtoon'
    IS_CONNECTION_STABLE = True
    TEST_WEBTOON_ID = 809590  # 이번 생
    IS_BEST_CHALLENGE: ClassVar[bool] = False
    # 네이버 웹툰과 베스트 도전은 selector가 다르기 때문에 필요함.
    EPISODE_IMAGES_URL_SELECTOR: ClassVar[str] = '#sectionContWide > img'
    URL_REGEX: str = r"(?:https?:\/\/)?(?:m[.])?comic[.]naver[.]com\/webtoon\/list\?(?:.*&)*titleId=(?P<webtoon_id>\d+)(?:&.*)*"
    seamless_redirect = True

    def __new__(cls, *args, _seamless_redirect: bool | None = None, **kwargs) -> Scraper:
        self = super().__new__(cls)
        self.__init__(*args, **kwargs)
        if _seamless_redirect is False or not cls.seamless_redirect:
            return self

        try:
            self.fetch_webtoon_information()
        except InvalidPlatformError:
            try:
                alternative_platforms = [
                    platform
                    for platform in NAVER_WEBTOON_CLASSES
                    if platform.IS_BEST_CHALLENGE is not cls.IS_BEST_CHALLENGE
                ]
            except AttributeError as e:
                raise ValueError(
                    "class inside NAVER_WEBTOON_CLASSES should has `IS_BEST_CHALLENGE` attribute.") from e

            if len(alternative_platforms) != 1:
                raise ValueError(
                    f"Length of alternative platforms({alternative_platforms}) should be 1. "
                    "If you want to make a subclass of NaverWebtoonScraper or "
                    "BestChallengeScraper, there's a few solutions.\n"
                    "1. Change `seamless_redirect` to False.\n"
                    f"2. Replace `NAVER_WEBTOON_CLASSES` as your class "
                    "at `WebtoonScraper/scrapers/B_naver_webtoon.py`."
                ) from None
            alternative_platform, = alternative_platforms
            logging.info(f"Redirect to `{alternative_platform}` due to `seamless_redirect`.")

            self = alternative_platform.__new__(
                alternative_platform,
                *args,
                _seamless_redirect=False,  # type: ignore
                **kwargs
            )
            return self
        else:
            return self

    @reload_manager
    def fetch_webtoon_information(self, *, reload: bool = False) -> None:
        webtoon_json_info = self.requests.get(f'https://comic.naver.com/api/article/list/info?titleId={self.webtoon_id}').json()
        # webtoon_json_info['thumbnailUrl']  # 정사각형 썸네일
        webtoon_thumbnail = webtoon_json_info['sharedThumbnailUrl']  # 실제로 웹툰 페이지에 사용되는 썸네일
        title = webtoon_json_info['titleName']  # 제목
        is_best_challenge = webtoon_json_info['webtoonLevelCode']  # BEST_CHALLENGE or WEBTOON

        if webtoon_json_info['age']['type'] == "RATE_18":
            raise UnsupportedWebtoonRating(f"Webtoon {title} is adult webtoon, which is not supported in NaverWebtoonScraper. "
                                           "Thus cannot download this webtoon.")

        self.webtoon_thumbnail = webtoon_thumbnail
        self.title = title
        self.is_best_challenge = is_best_challenge == 'BEST_CHALLENGE'

        if self.is_best_challenge is not self.IS_BEST_CHALLENGE:
            platform_name = 'Best Challenge' if is_best_challenge else 'Naver Webtoon'
            raise InvalidPlatformError(f"Use {platform_name} Scraper to download {platform_name}.")

    @reload_manager
    def fetch_episode_informations(self, *, reload: bool = False) -> None:
        prev_articleList = []
        subtitles = []
        episode_ids = []
        for i in count(1):
            url = f"https://comic.naver.com/api/article/list?titleId={self.webtoon_id}&page={i}&sort=ASC"
            try:
                res = self.requests.get(url).json()
            except JSONDecodeError:
                raise ValueError('Naver Webtoon changed their api specification. Contect developer to update get_title. '
                                 '...Or just webtoon you tried to download invalid or adult webtoon. '
                                 'WebtoonScraper currently not support downloading adult webtoon.')

            curr_articleList = res["articleList"]
            if prev_articleList == curr_articleList:
                break
            for article in curr_articleList:
                # subtitles[article["no"]] = article["subtitle"]
                subtitles.append(article["subtitle"])
                episode_ids.append(article["no"])

            prev_articleList = curr_articleList

        self.episode_titles = subtitles
        self.episode_ids = episode_ids

    def get_episode_image_urls(self, episode_no) -> list[str]:
        # sourcery skip: de-morgan
        episode_id = self.episode_ids[episode_no]
        url = f'{self.BASE_URL}/detail?titleId={self.webtoon_id}&no={episode_id}'
        episode_image_urls_raw = self.requests.get(url).soup_select(self.EPISODE_IMAGES_URL_SELECTOR)
        episode_image_urls = [
            element['src'] for element in episode_image_urls_raw
            if not ('agerate' in element['src'] or 'ctguide' in element['src'])
        ]

        if TYPE_CHECKING:
            episode_image_urls = [
                url
                for url in episode_image_urls
                if isinstance(url, str)
            ]

        return episode_image_urls

    def check_if_legitimate_webtoon_id(self) -> str | None:
        return super().check_if_legitimate_webtoon_id((InvalidPlatformError, UnsupportedWebtoonRating))


class BestChallengeScraper(NaverWebtoonScraper):
    BASE_URL = 'https://comic.naver.com/bestChallenge'
    TEST_WEBTOON_ID = 809971  # 까마귀
    IS_BEST_CHALLENGE = True
    EPISODE_IMAGES_URL_SELECTOR = '#comic_view_area > div > img'
    URL_REGEX: str = r"(?:https?:\/\/)?comic[.]naver[.]com\/bestChallenge\/list\?(?:.*&)*titleId=(?P<webtoon_id>\d+)(?:&.*)*"


NAVER_WEBTOON_CLASSES: set[type[NaverWebtoonScraper]] = {NaverWebtoonScraper, BestChallengeScraper}
