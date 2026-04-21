"""TrueAchievements scraper for Xbox gamerscore + achievement tiers."""
from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup

from ..models import PlatformStats, SubStat
from ..services.normalize import parse_int
from .base import Provider, ProviderError

log = logging.getLogger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class XboxProvider(Provider):
    platform = "xbox"

    def xǁXboxProviderǁfetch__mutmut_orig(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_1(self, profile_url: str) -> PlatformStats:
        soup = None
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_2(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(None)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_3(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = None
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_4(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=None, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_5(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label=None)
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_6(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_7(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, )
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_8(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="XXGamerscoreXX")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_9(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_10(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="GAMERSCORE")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_11(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = None
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_12(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(None, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_13(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, None)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_14(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_15(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, )
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_16(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = None
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_17(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(None)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_18(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = None
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_19(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(None)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_20(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = None
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_21(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(None)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_22(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = None
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_23(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"XXta_scoreXX": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_24(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"TA_SCORE": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_25(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = None
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_26(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label=None, value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_27(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=None)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_28(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_29(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", )]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_30(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="XXTAXX", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_31(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="ta", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_32(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta and 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_33(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 1)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_34(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None or ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_35(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is not None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_36(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is not None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def xǁXboxProviderǁfetch__mutmut_37(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError(None)
        return stats

    def xǁXboxProviderǁfetch__mutmut_38(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("XXxbox: no recognizable stats on pageXX")
        return stats

    def xǁXboxProviderǁfetch__mutmut_39(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("XBOX: NO RECOGNIZABLE STATS ON PAGE")
        return stats
    
    xǁXboxProviderǁfetch__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁXboxProviderǁfetch__mutmut_1': xǁXboxProviderǁfetch__mutmut_1, 
        'xǁXboxProviderǁfetch__mutmut_2': xǁXboxProviderǁfetch__mutmut_2, 
        'xǁXboxProviderǁfetch__mutmut_3': xǁXboxProviderǁfetch__mutmut_3, 
        'xǁXboxProviderǁfetch__mutmut_4': xǁXboxProviderǁfetch__mutmut_4, 
        'xǁXboxProviderǁfetch__mutmut_5': xǁXboxProviderǁfetch__mutmut_5, 
        'xǁXboxProviderǁfetch__mutmut_6': xǁXboxProviderǁfetch__mutmut_6, 
        'xǁXboxProviderǁfetch__mutmut_7': xǁXboxProviderǁfetch__mutmut_7, 
        'xǁXboxProviderǁfetch__mutmut_8': xǁXboxProviderǁfetch__mutmut_8, 
        'xǁXboxProviderǁfetch__mutmut_9': xǁXboxProviderǁfetch__mutmut_9, 
        'xǁXboxProviderǁfetch__mutmut_10': xǁXboxProviderǁfetch__mutmut_10, 
        'xǁXboxProviderǁfetch__mutmut_11': xǁXboxProviderǁfetch__mutmut_11, 
        'xǁXboxProviderǁfetch__mutmut_12': xǁXboxProviderǁfetch__mutmut_12, 
        'xǁXboxProviderǁfetch__mutmut_13': xǁXboxProviderǁfetch__mutmut_13, 
        'xǁXboxProviderǁfetch__mutmut_14': xǁXboxProviderǁfetch__mutmut_14, 
        'xǁXboxProviderǁfetch__mutmut_15': xǁXboxProviderǁfetch__mutmut_15, 
        'xǁXboxProviderǁfetch__mutmut_16': xǁXboxProviderǁfetch__mutmut_16, 
        'xǁXboxProviderǁfetch__mutmut_17': xǁXboxProviderǁfetch__mutmut_17, 
        'xǁXboxProviderǁfetch__mutmut_18': xǁXboxProviderǁfetch__mutmut_18, 
        'xǁXboxProviderǁfetch__mutmut_19': xǁXboxProviderǁfetch__mutmut_19, 
        'xǁXboxProviderǁfetch__mutmut_20': xǁXboxProviderǁfetch__mutmut_20, 
        'xǁXboxProviderǁfetch__mutmut_21': xǁXboxProviderǁfetch__mutmut_21, 
        'xǁXboxProviderǁfetch__mutmut_22': xǁXboxProviderǁfetch__mutmut_22, 
        'xǁXboxProviderǁfetch__mutmut_23': xǁXboxProviderǁfetch__mutmut_23, 
        'xǁXboxProviderǁfetch__mutmut_24': xǁXboxProviderǁfetch__mutmut_24, 
        'xǁXboxProviderǁfetch__mutmut_25': xǁXboxProviderǁfetch__mutmut_25, 
        'xǁXboxProviderǁfetch__mutmut_26': xǁXboxProviderǁfetch__mutmut_26, 
        'xǁXboxProviderǁfetch__mutmut_27': xǁXboxProviderǁfetch__mutmut_27, 
        'xǁXboxProviderǁfetch__mutmut_28': xǁXboxProviderǁfetch__mutmut_28, 
        'xǁXboxProviderǁfetch__mutmut_29': xǁXboxProviderǁfetch__mutmut_29, 
        'xǁXboxProviderǁfetch__mutmut_30': xǁXboxProviderǁfetch__mutmut_30, 
        'xǁXboxProviderǁfetch__mutmut_31': xǁXboxProviderǁfetch__mutmut_31, 
        'xǁXboxProviderǁfetch__mutmut_32': xǁXboxProviderǁfetch__mutmut_32, 
        'xǁXboxProviderǁfetch__mutmut_33': xǁXboxProviderǁfetch__mutmut_33, 
        'xǁXboxProviderǁfetch__mutmut_34': xǁXboxProviderǁfetch__mutmut_34, 
        'xǁXboxProviderǁfetch__mutmut_35': xǁXboxProviderǁfetch__mutmut_35, 
        'xǁXboxProviderǁfetch__mutmut_36': xǁXboxProviderǁfetch__mutmut_36, 
        'xǁXboxProviderǁfetch__mutmut_37': xǁXboxProviderǁfetch__mutmut_37, 
        'xǁXboxProviderǁfetch__mutmut_38': xǁXboxProviderǁfetch__mutmut_38, 
        'xǁXboxProviderǁfetch__mutmut_39': xǁXboxProviderǁfetch__mutmut_39
    }
    
    def fetch(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁXboxProviderǁfetch__mutmut_orig"), object.__getattribute__(self, "xǁXboxProviderǁfetch__mutmut_mutants"), args, kwargs, self)
        return result 
    
    fetch.__signature__ = _mutmut_signature(xǁXboxProviderǁfetch__mutmut_orig)
    xǁXboxProviderǁfetch__mutmut_orig.__name__ = 'xǁXboxProviderǁfetch'

    def xǁXboxProviderǁ_extract_username__mutmut_orig(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_1(self, soup: BeautifulSoup, url: str) -> str:
        h1 = None
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_2(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find(None)
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_3(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.rfind("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_4(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("XXh1XX")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_5(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("H1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_6(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 or h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_7(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=None):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_8(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=False):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_9(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=None).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_10(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=False).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_11(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[1]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_12(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = None
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_13(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(None, url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_14(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", None)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_15(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_16(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", )
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_17(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"XX/gamer/([^/?#]+)XX", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_18(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_19(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/GAMER/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_20(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(None) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_21(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(2) if m else ""

    def xǁXboxProviderǁ_extract_username__mutmut_22(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else "XXXX"
    
    xǁXboxProviderǁ_extract_username__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁXboxProviderǁ_extract_username__mutmut_1': xǁXboxProviderǁ_extract_username__mutmut_1, 
        'xǁXboxProviderǁ_extract_username__mutmut_2': xǁXboxProviderǁ_extract_username__mutmut_2, 
        'xǁXboxProviderǁ_extract_username__mutmut_3': xǁXboxProviderǁ_extract_username__mutmut_3, 
        'xǁXboxProviderǁ_extract_username__mutmut_4': xǁXboxProviderǁ_extract_username__mutmut_4, 
        'xǁXboxProviderǁ_extract_username__mutmut_5': xǁXboxProviderǁ_extract_username__mutmut_5, 
        'xǁXboxProviderǁ_extract_username__mutmut_6': xǁXboxProviderǁ_extract_username__mutmut_6, 
        'xǁXboxProviderǁ_extract_username__mutmut_7': xǁXboxProviderǁ_extract_username__mutmut_7, 
        'xǁXboxProviderǁ_extract_username__mutmut_8': xǁXboxProviderǁ_extract_username__mutmut_8, 
        'xǁXboxProviderǁ_extract_username__mutmut_9': xǁXboxProviderǁ_extract_username__mutmut_9, 
        'xǁXboxProviderǁ_extract_username__mutmut_10': xǁXboxProviderǁ_extract_username__mutmut_10, 
        'xǁXboxProviderǁ_extract_username__mutmut_11': xǁXboxProviderǁ_extract_username__mutmut_11, 
        'xǁXboxProviderǁ_extract_username__mutmut_12': xǁXboxProviderǁ_extract_username__mutmut_12, 
        'xǁXboxProviderǁ_extract_username__mutmut_13': xǁXboxProviderǁ_extract_username__mutmut_13, 
        'xǁXboxProviderǁ_extract_username__mutmut_14': xǁXboxProviderǁ_extract_username__mutmut_14, 
        'xǁXboxProviderǁ_extract_username__mutmut_15': xǁXboxProviderǁ_extract_username__mutmut_15, 
        'xǁXboxProviderǁ_extract_username__mutmut_16': xǁXboxProviderǁ_extract_username__mutmut_16, 
        'xǁXboxProviderǁ_extract_username__mutmut_17': xǁXboxProviderǁ_extract_username__mutmut_17, 
        'xǁXboxProviderǁ_extract_username__mutmut_18': xǁXboxProviderǁ_extract_username__mutmut_18, 
        'xǁXboxProviderǁ_extract_username__mutmut_19': xǁXboxProviderǁ_extract_username__mutmut_19, 
        'xǁXboxProviderǁ_extract_username__mutmut_20': xǁXboxProviderǁ_extract_username__mutmut_20, 
        'xǁXboxProviderǁ_extract_username__mutmut_21': xǁXboxProviderǁ_extract_username__mutmut_21, 
        'xǁXboxProviderǁ_extract_username__mutmut_22': xǁXboxProviderǁ_extract_username__mutmut_22
    }
    
    def _extract_username(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁXboxProviderǁ_extract_username__mutmut_orig"), object.__getattribute__(self, "xǁXboxProviderǁ_extract_username__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_username.__signature__ = _mutmut_signature(xǁXboxProviderǁ_extract_username__mutmut_orig)
    xǁXboxProviderǁ_extract_username__mutmut_orig.__name__ = 'xǁXboxProviderǁ_extract_username'

    def xǁXboxProviderǁ_extract_avatar__mutmut_orig(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_1(self, soup: BeautifulSoup) -> str | None:
        og = None
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_2(self, soup: BeautifulSoup) -> str | None:
        og = soup.find(None, property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_3(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property=None)
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_4(self, soup: BeautifulSoup) -> str | None:
        og = soup.find(property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_5(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", )
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_6(self, soup: BeautifulSoup) -> str | None:
        og = soup.rfind("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_7(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("XXmetaXX", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_8(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("META", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_9(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="XXog:imageXX")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_10(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="OG:IMAGE")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_11(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og or og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_12(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get(None):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_13(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("XXcontentXX"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_14(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("CONTENT"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_15(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["XXcontentXX"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_16(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["CONTENT"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_17(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = None
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_18(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one(None)
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_19(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("XXimg.gamer-avatar, img.avatar, img[alt*='avatar' i]XX")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_20(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("IMG.GAMER-AVATAR, IMG.AVATAR, IMG[ALT*='AVATAR' I]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_21(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img or img.get("src"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_22(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get(None):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_23(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("XXsrcXX"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_24(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("SRC"):
            return img["src"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_25(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["XXsrcXX"]
        return None

    def xǁXboxProviderǁ_extract_avatar__mutmut_26(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["SRC"]
        return None
    
    xǁXboxProviderǁ_extract_avatar__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁXboxProviderǁ_extract_avatar__mutmut_1': xǁXboxProviderǁ_extract_avatar__mutmut_1, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_2': xǁXboxProviderǁ_extract_avatar__mutmut_2, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_3': xǁXboxProviderǁ_extract_avatar__mutmut_3, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_4': xǁXboxProviderǁ_extract_avatar__mutmut_4, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_5': xǁXboxProviderǁ_extract_avatar__mutmut_5, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_6': xǁXboxProviderǁ_extract_avatar__mutmut_6, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_7': xǁXboxProviderǁ_extract_avatar__mutmut_7, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_8': xǁXboxProviderǁ_extract_avatar__mutmut_8, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_9': xǁXboxProviderǁ_extract_avatar__mutmut_9, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_10': xǁXboxProviderǁ_extract_avatar__mutmut_10, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_11': xǁXboxProviderǁ_extract_avatar__mutmut_11, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_12': xǁXboxProviderǁ_extract_avatar__mutmut_12, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_13': xǁXboxProviderǁ_extract_avatar__mutmut_13, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_14': xǁXboxProviderǁ_extract_avatar__mutmut_14, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_15': xǁXboxProviderǁ_extract_avatar__mutmut_15, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_16': xǁXboxProviderǁ_extract_avatar__mutmut_16, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_17': xǁXboxProviderǁ_extract_avatar__mutmut_17, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_18': xǁXboxProviderǁ_extract_avatar__mutmut_18, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_19': xǁXboxProviderǁ_extract_avatar__mutmut_19, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_20': xǁXboxProviderǁ_extract_avatar__mutmut_20, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_21': xǁXboxProviderǁ_extract_avatar__mutmut_21, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_22': xǁXboxProviderǁ_extract_avatar__mutmut_22, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_23': xǁXboxProviderǁ_extract_avatar__mutmut_23, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_24': xǁXboxProviderǁ_extract_avatar__mutmut_24, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_25': xǁXboxProviderǁ_extract_avatar__mutmut_25, 
        'xǁXboxProviderǁ_extract_avatar__mutmut_26': xǁXboxProviderǁ_extract_avatar__mutmut_26
    }
    
    def _extract_avatar(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁXboxProviderǁ_extract_avatar__mutmut_orig"), object.__getattribute__(self, "xǁXboxProviderǁ_extract_avatar__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_avatar.__signature__ = _mutmut_signature(xǁXboxProviderǁ_extract_avatar__mutmut_orig)
    xǁXboxProviderǁ_extract_avatar__mutmut_orig.__name__ = 'xǁXboxProviderǁ_extract_avatar'

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_orig(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_1(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select(None):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_2(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("XXli, tr, divXX"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_3(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("LI, TR, DIV"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_4(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = None
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_5(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(None, strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_6(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=None)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_7(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_8(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", )
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_9(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text("XX XX", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_10(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=False)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_11(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(None, text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_12(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", None, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_13(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, None):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_14(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_15(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_16(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, ):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_17(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"XX\bGamerscore\bXX", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_18(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bgamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_19(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGAMERSCORE\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_20(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = None
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_21(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(None)
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_22(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace(None, ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_23(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", None))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_24(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace(""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_25(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_26(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("XXGamerscoreXX", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_27(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_28(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("GAMERSCORE", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_29(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", "XXXX"))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_30(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(None)

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_31(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(None, strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_32(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=None))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_33(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_34(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", ))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_35(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text("XX XX", strip=True))

    def xǁXboxProviderǁ_extract_gamerscore__mutmut_36(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=False))
    
    xǁXboxProviderǁ_extract_gamerscore__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁXboxProviderǁ_extract_gamerscore__mutmut_1': xǁXboxProviderǁ_extract_gamerscore__mutmut_1, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_2': xǁXboxProviderǁ_extract_gamerscore__mutmut_2, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_3': xǁXboxProviderǁ_extract_gamerscore__mutmut_3, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_4': xǁXboxProviderǁ_extract_gamerscore__mutmut_4, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_5': xǁXboxProviderǁ_extract_gamerscore__mutmut_5, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_6': xǁXboxProviderǁ_extract_gamerscore__mutmut_6, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_7': xǁXboxProviderǁ_extract_gamerscore__mutmut_7, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_8': xǁXboxProviderǁ_extract_gamerscore__mutmut_8, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_9': xǁXboxProviderǁ_extract_gamerscore__mutmut_9, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_10': xǁXboxProviderǁ_extract_gamerscore__mutmut_10, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_11': xǁXboxProviderǁ_extract_gamerscore__mutmut_11, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_12': xǁXboxProviderǁ_extract_gamerscore__mutmut_12, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_13': xǁXboxProviderǁ_extract_gamerscore__mutmut_13, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_14': xǁXboxProviderǁ_extract_gamerscore__mutmut_14, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_15': xǁXboxProviderǁ_extract_gamerscore__mutmut_15, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_16': xǁXboxProviderǁ_extract_gamerscore__mutmut_16, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_17': xǁXboxProviderǁ_extract_gamerscore__mutmut_17, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_18': xǁXboxProviderǁ_extract_gamerscore__mutmut_18, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_19': xǁXboxProviderǁ_extract_gamerscore__mutmut_19, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_20': xǁXboxProviderǁ_extract_gamerscore__mutmut_20, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_21': xǁXboxProviderǁ_extract_gamerscore__mutmut_21, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_22': xǁXboxProviderǁ_extract_gamerscore__mutmut_22, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_23': xǁXboxProviderǁ_extract_gamerscore__mutmut_23, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_24': xǁXboxProviderǁ_extract_gamerscore__mutmut_24, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_25': xǁXboxProviderǁ_extract_gamerscore__mutmut_25, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_26': xǁXboxProviderǁ_extract_gamerscore__mutmut_26, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_27': xǁXboxProviderǁ_extract_gamerscore__mutmut_27, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_28': xǁXboxProviderǁ_extract_gamerscore__mutmut_28, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_29': xǁXboxProviderǁ_extract_gamerscore__mutmut_29, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_30': xǁXboxProviderǁ_extract_gamerscore__mutmut_30, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_31': xǁXboxProviderǁ_extract_gamerscore__mutmut_31, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_32': xǁXboxProviderǁ_extract_gamerscore__mutmut_32, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_33': xǁXboxProviderǁ_extract_gamerscore__mutmut_33, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_34': xǁXboxProviderǁ_extract_gamerscore__mutmut_34, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_35': xǁXboxProviderǁ_extract_gamerscore__mutmut_35, 
        'xǁXboxProviderǁ_extract_gamerscore__mutmut_36': xǁXboxProviderǁ_extract_gamerscore__mutmut_36
    }
    
    def _extract_gamerscore(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁXboxProviderǁ_extract_gamerscore__mutmut_orig"), object.__getattribute__(self, "xǁXboxProviderǁ_extract_gamerscore__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_gamerscore.__signature__ = _mutmut_signature(xǁXboxProviderǁ_extract_gamerscore__mutmut_orig)
    xǁXboxProviderǁ_extract_gamerscore__mutmut_orig.__name__ = 'xǁXboxProviderǁ_extract_gamerscore'

    def xǁXboxProviderǁ_extract_ta_score__mutmut_orig(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_1(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select(None):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_2(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("XXli, tr, div, spanXX"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_3(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("LI, TR, DIV, SPAN"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_4(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = None
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_5(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(None, strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_6(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=None)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_7(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_8(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", )
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_9(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text("XX XX", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_10(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=False)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_11(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(None, text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_12(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", None, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_13(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, None):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_14(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_15(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_16(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, ):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_17(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"XXTrueAchievement\s*Score|\bTA\s*Score\bXX", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_18(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"trueachievement\s*score|\bta\s*score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_19(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TRUEACHIEVEMENT\s*SCORE|\bTA\s*SCORE\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_20(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = None
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_21(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(None, text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_22(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", None)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_23(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_24(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", )
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_25(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"XX([\d,]{3,})XX", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_26(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_27(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_28(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = None
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_29(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(None)
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_30(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(None))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_31(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(2))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_32(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_33(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = None
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_34(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(None, strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_35(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=None)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_36(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_37(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", )
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_38(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text("XX XX", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_39(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=False)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_40(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = None
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_41(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(None, page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_42(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", None)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_43(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_44(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", )
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_45(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"XX\bTA\b[^0-9]{0,12}([\d,]+)XX", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_46(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bta\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_47(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_48(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(None) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_49(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(None)) if m else None

    def xǁXboxProviderǁ_extract_ta_score__mutmut_50(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(2)) if m else None
    
    xǁXboxProviderǁ_extract_ta_score__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁXboxProviderǁ_extract_ta_score__mutmut_1': xǁXboxProviderǁ_extract_ta_score__mutmut_1, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_2': xǁXboxProviderǁ_extract_ta_score__mutmut_2, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_3': xǁXboxProviderǁ_extract_ta_score__mutmut_3, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_4': xǁXboxProviderǁ_extract_ta_score__mutmut_4, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_5': xǁXboxProviderǁ_extract_ta_score__mutmut_5, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_6': xǁXboxProviderǁ_extract_ta_score__mutmut_6, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_7': xǁXboxProviderǁ_extract_ta_score__mutmut_7, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_8': xǁXboxProviderǁ_extract_ta_score__mutmut_8, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_9': xǁXboxProviderǁ_extract_ta_score__mutmut_9, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_10': xǁXboxProviderǁ_extract_ta_score__mutmut_10, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_11': xǁXboxProviderǁ_extract_ta_score__mutmut_11, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_12': xǁXboxProviderǁ_extract_ta_score__mutmut_12, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_13': xǁXboxProviderǁ_extract_ta_score__mutmut_13, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_14': xǁXboxProviderǁ_extract_ta_score__mutmut_14, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_15': xǁXboxProviderǁ_extract_ta_score__mutmut_15, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_16': xǁXboxProviderǁ_extract_ta_score__mutmut_16, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_17': xǁXboxProviderǁ_extract_ta_score__mutmut_17, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_18': xǁXboxProviderǁ_extract_ta_score__mutmut_18, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_19': xǁXboxProviderǁ_extract_ta_score__mutmut_19, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_20': xǁXboxProviderǁ_extract_ta_score__mutmut_20, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_21': xǁXboxProviderǁ_extract_ta_score__mutmut_21, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_22': xǁXboxProviderǁ_extract_ta_score__mutmut_22, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_23': xǁXboxProviderǁ_extract_ta_score__mutmut_23, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_24': xǁXboxProviderǁ_extract_ta_score__mutmut_24, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_25': xǁXboxProviderǁ_extract_ta_score__mutmut_25, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_26': xǁXboxProviderǁ_extract_ta_score__mutmut_26, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_27': xǁXboxProviderǁ_extract_ta_score__mutmut_27, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_28': xǁXboxProviderǁ_extract_ta_score__mutmut_28, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_29': xǁXboxProviderǁ_extract_ta_score__mutmut_29, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_30': xǁXboxProviderǁ_extract_ta_score__mutmut_30, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_31': xǁXboxProviderǁ_extract_ta_score__mutmut_31, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_32': xǁXboxProviderǁ_extract_ta_score__mutmut_32, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_33': xǁXboxProviderǁ_extract_ta_score__mutmut_33, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_34': xǁXboxProviderǁ_extract_ta_score__mutmut_34, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_35': xǁXboxProviderǁ_extract_ta_score__mutmut_35, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_36': xǁXboxProviderǁ_extract_ta_score__mutmut_36, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_37': xǁXboxProviderǁ_extract_ta_score__mutmut_37, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_38': xǁXboxProviderǁ_extract_ta_score__mutmut_38, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_39': xǁXboxProviderǁ_extract_ta_score__mutmut_39, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_40': xǁXboxProviderǁ_extract_ta_score__mutmut_40, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_41': xǁXboxProviderǁ_extract_ta_score__mutmut_41, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_42': xǁXboxProviderǁ_extract_ta_score__mutmut_42, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_43': xǁXboxProviderǁ_extract_ta_score__mutmut_43, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_44': xǁXboxProviderǁ_extract_ta_score__mutmut_44, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_45': xǁXboxProviderǁ_extract_ta_score__mutmut_45, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_46': xǁXboxProviderǁ_extract_ta_score__mutmut_46, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_47': xǁXboxProviderǁ_extract_ta_score__mutmut_47, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_48': xǁXboxProviderǁ_extract_ta_score__mutmut_48, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_49': xǁXboxProviderǁ_extract_ta_score__mutmut_49, 
        'xǁXboxProviderǁ_extract_ta_score__mutmut_50': xǁXboxProviderǁ_extract_ta_score__mutmut_50
    }
    
    def _extract_ta_score(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁXboxProviderǁ_extract_ta_score__mutmut_orig"), object.__getattribute__(self, "xǁXboxProviderǁ_extract_ta_score__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_ta_score.__signature__ = _mutmut_signature(xǁXboxProviderǁ_extract_ta_score__mutmut_orig)
    xǁXboxProviderǁ_extract_ta_score__mutmut_orig.__name__ = 'xǁXboxProviderǁ_extract_ta_score'
