"""PSNProfiles scraper for PlayStation trophy counts."""
from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup

from ..models import PlatformStats, SubStat
from ..services.normalize import parse_int
from .base import Provider, ProviderError

log = logging.getLogger(__name__)


_TIERS = ("platinum", "gold", "silver", "bronze")
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


class PsnProvider(Provider):
    platform = "psn"

    def xǁPsnProviderǁfetch__mutmut_orig(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_1(self, profile_url: str) -> PlatformStats:
        soup = None
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_2(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(None)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_3(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = None
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_4(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=None, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_5(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label=None)
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_6(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_7(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, )
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_8(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="XXTrophiesXX")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_9(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_10(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="TROPHIES")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_11(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = None
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_12(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(None, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_13(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, None)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_14(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_15(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, )
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_16(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = None

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_17(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(None)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_18(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = None
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_19(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(None)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_20(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = None

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_21(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=None, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_22(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=None) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_23(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_24(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, ) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_25(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(None, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_26(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, None)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_27(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_28(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, )) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_29(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 1)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_30(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = None
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_31(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get(None, 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_32(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", None)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_33(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get(0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_34(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", )
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_35(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("XXplatinumXX", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_36(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("PLATINUM", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_37(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 1)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_38(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_39(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_40(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_41(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(None):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def xǁPsnProviderǁfetch__mutmut_42(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError(None)
        return stats

    def xǁPsnProviderǁfetch__mutmut_43(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("XXpsn: no trophy counts foundXX")
        return stats

    def xǁPsnProviderǁfetch__mutmut_44(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("PSN: NO TROPHY COUNTS FOUND")
        return stats
    
    xǁPsnProviderǁfetch__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPsnProviderǁfetch__mutmut_1': xǁPsnProviderǁfetch__mutmut_1, 
        'xǁPsnProviderǁfetch__mutmut_2': xǁPsnProviderǁfetch__mutmut_2, 
        'xǁPsnProviderǁfetch__mutmut_3': xǁPsnProviderǁfetch__mutmut_3, 
        'xǁPsnProviderǁfetch__mutmut_4': xǁPsnProviderǁfetch__mutmut_4, 
        'xǁPsnProviderǁfetch__mutmut_5': xǁPsnProviderǁfetch__mutmut_5, 
        'xǁPsnProviderǁfetch__mutmut_6': xǁPsnProviderǁfetch__mutmut_6, 
        'xǁPsnProviderǁfetch__mutmut_7': xǁPsnProviderǁfetch__mutmut_7, 
        'xǁPsnProviderǁfetch__mutmut_8': xǁPsnProviderǁfetch__mutmut_8, 
        'xǁPsnProviderǁfetch__mutmut_9': xǁPsnProviderǁfetch__mutmut_9, 
        'xǁPsnProviderǁfetch__mutmut_10': xǁPsnProviderǁfetch__mutmut_10, 
        'xǁPsnProviderǁfetch__mutmut_11': xǁPsnProviderǁfetch__mutmut_11, 
        'xǁPsnProviderǁfetch__mutmut_12': xǁPsnProviderǁfetch__mutmut_12, 
        'xǁPsnProviderǁfetch__mutmut_13': xǁPsnProviderǁfetch__mutmut_13, 
        'xǁPsnProviderǁfetch__mutmut_14': xǁPsnProviderǁfetch__mutmut_14, 
        'xǁPsnProviderǁfetch__mutmut_15': xǁPsnProviderǁfetch__mutmut_15, 
        'xǁPsnProviderǁfetch__mutmut_16': xǁPsnProviderǁfetch__mutmut_16, 
        'xǁPsnProviderǁfetch__mutmut_17': xǁPsnProviderǁfetch__mutmut_17, 
        'xǁPsnProviderǁfetch__mutmut_18': xǁPsnProviderǁfetch__mutmut_18, 
        'xǁPsnProviderǁfetch__mutmut_19': xǁPsnProviderǁfetch__mutmut_19, 
        'xǁPsnProviderǁfetch__mutmut_20': xǁPsnProviderǁfetch__mutmut_20, 
        'xǁPsnProviderǁfetch__mutmut_21': xǁPsnProviderǁfetch__mutmut_21, 
        'xǁPsnProviderǁfetch__mutmut_22': xǁPsnProviderǁfetch__mutmut_22, 
        'xǁPsnProviderǁfetch__mutmut_23': xǁPsnProviderǁfetch__mutmut_23, 
        'xǁPsnProviderǁfetch__mutmut_24': xǁPsnProviderǁfetch__mutmut_24, 
        'xǁPsnProviderǁfetch__mutmut_25': xǁPsnProviderǁfetch__mutmut_25, 
        'xǁPsnProviderǁfetch__mutmut_26': xǁPsnProviderǁfetch__mutmut_26, 
        'xǁPsnProviderǁfetch__mutmut_27': xǁPsnProviderǁfetch__mutmut_27, 
        'xǁPsnProviderǁfetch__mutmut_28': xǁPsnProviderǁfetch__mutmut_28, 
        'xǁPsnProviderǁfetch__mutmut_29': xǁPsnProviderǁfetch__mutmut_29, 
        'xǁPsnProviderǁfetch__mutmut_30': xǁPsnProviderǁfetch__mutmut_30, 
        'xǁPsnProviderǁfetch__mutmut_31': xǁPsnProviderǁfetch__mutmut_31, 
        'xǁPsnProviderǁfetch__mutmut_32': xǁPsnProviderǁfetch__mutmut_32, 
        'xǁPsnProviderǁfetch__mutmut_33': xǁPsnProviderǁfetch__mutmut_33, 
        'xǁPsnProviderǁfetch__mutmut_34': xǁPsnProviderǁfetch__mutmut_34, 
        'xǁPsnProviderǁfetch__mutmut_35': xǁPsnProviderǁfetch__mutmut_35, 
        'xǁPsnProviderǁfetch__mutmut_36': xǁPsnProviderǁfetch__mutmut_36, 
        'xǁPsnProviderǁfetch__mutmut_37': xǁPsnProviderǁfetch__mutmut_37, 
        'xǁPsnProviderǁfetch__mutmut_38': xǁPsnProviderǁfetch__mutmut_38, 
        'xǁPsnProviderǁfetch__mutmut_39': xǁPsnProviderǁfetch__mutmut_39, 
        'xǁPsnProviderǁfetch__mutmut_40': xǁPsnProviderǁfetch__mutmut_40, 
        'xǁPsnProviderǁfetch__mutmut_41': xǁPsnProviderǁfetch__mutmut_41, 
        'xǁPsnProviderǁfetch__mutmut_42': xǁPsnProviderǁfetch__mutmut_42, 
        'xǁPsnProviderǁfetch__mutmut_43': xǁPsnProviderǁfetch__mutmut_43, 
        'xǁPsnProviderǁfetch__mutmut_44': xǁPsnProviderǁfetch__mutmut_44
    }
    
    def fetch(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPsnProviderǁfetch__mutmut_orig"), object.__getattribute__(self, "xǁPsnProviderǁfetch__mutmut_mutants"), args, kwargs, self)
        return result 
    
    fetch.__signature__ = _mutmut_signature(xǁPsnProviderǁfetch__mutmut_orig)
    xǁPsnProviderǁfetch__mutmut_orig.__name__ = 'xǁPsnProviderǁfetch'

    def xǁPsnProviderǁ_extract_username__mutmut_orig(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_1(self, soup: BeautifulSoup, url: str) -> str:
        name_el = None
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_2(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") and soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_3(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one(None) or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_4(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("XXspan.usernameXX") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_5(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("SPAN.USERNAME") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_6(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find(None)
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_7(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.rfind("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_8(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("XXh1XX")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_9(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("H1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_10(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el or name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_11(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=None):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_12(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=False):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_13(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=None)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_14(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=False)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_15(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = None
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_16(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(None, url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_17(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", None)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_18(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_19(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", )
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_20(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"XXpsnprofiles\.com/([^/?#]+)XX", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_21(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_22(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"PSNPROFILES\.COM/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_23(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(None) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_24(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(2) if m else ""

    def xǁPsnProviderǁ_extract_username__mutmut_25(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else "XXXX"
    
    xǁPsnProviderǁ_extract_username__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPsnProviderǁ_extract_username__mutmut_1': xǁPsnProviderǁ_extract_username__mutmut_1, 
        'xǁPsnProviderǁ_extract_username__mutmut_2': xǁPsnProviderǁ_extract_username__mutmut_2, 
        'xǁPsnProviderǁ_extract_username__mutmut_3': xǁPsnProviderǁ_extract_username__mutmut_3, 
        'xǁPsnProviderǁ_extract_username__mutmut_4': xǁPsnProviderǁ_extract_username__mutmut_4, 
        'xǁPsnProviderǁ_extract_username__mutmut_5': xǁPsnProviderǁ_extract_username__mutmut_5, 
        'xǁPsnProviderǁ_extract_username__mutmut_6': xǁPsnProviderǁ_extract_username__mutmut_6, 
        'xǁPsnProviderǁ_extract_username__mutmut_7': xǁPsnProviderǁ_extract_username__mutmut_7, 
        'xǁPsnProviderǁ_extract_username__mutmut_8': xǁPsnProviderǁ_extract_username__mutmut_8, 
        'xǁPsnProviderǁ_extract_username__mutmut_9': xǁPsnProviderǁ_extract_username__mutmut_9, 
        'xǁPsnProviderǁ_extract_username__mutmut_10': xǁPsnProviderǁ_extract_username__mutmut_10, 
        'xǁPsnProviderǁ_extract_username__mutmut_11': xǁPsnProviderǁ_extract_username__mutmut_11, 
        'xǁPsnProviderǁ_extract_username__mutmut_12': xǁPsnProviderǁ_extract_username__mutmut_12, 
        'xǁPsnProviderǁ_extract_username__mutmut_13': xǁPsnProviderǁ_extract_username__mutmut_13, 
        'xǁPsnProviderǁ_extract_username__mutmut_14': xǁPsnProviderǁ_extract_username__mutmut_14, 
        'xǁPsnProviderǁ_extract_username__mutmut_15': xǁPsnProviderǁ_extract_username__mutmut_15, 
        'xǁPsnProviderǁ_extract_username__mutmut_16': xǁPsnProviderǁ_extract_username__mutmut_16, 
        'xǁPsnProviderǁ_extract_username__mutmut_17': xǁPsnProviderǁ_extract_username__mutmut_17, 
        'xǁPsnProviderǁ_extract_username__mutmut_18': xǁPsnProviderǁ_extract_username__mutmut_18, 
        'xǁPsnProviderǁ_extract_username__mutmut_19': xǁPsnProviderǁ_extract_username__mutmut_19, 
        'xǁPsnProviderǁ_extract_username__mutmut_20': xǁPsnProviderǁ_extract_username__mutmut_20, 
        'xǁPsnProviderǁ_extract_username__mutmut_21': xǁPsnProviderǁ_extract_username__mutmut_21, 
        'xǁPsnProviderǁ_extract_username__mutmut_22': xǁPsnProviderǁ_extract_username__mutmut_22, 
        'xǁPsnProviderǁ_extract_username__mutmut_23': xǁPsnProviderǁ_extract_username__mutmut_23, 
        'xǁPsnProviderǁ_extract_username__mutmut_24': xǁPsnProviderǁ_extract_username__mutmut_24, 
        'xǁPsnProviderǁ_extract_username__mutmut_25': xǁPsnProviderǁ_extract_username__mutmut_25
    }
    
    def _extract_username(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPsnProviderǁ_extract_username__mutmut_orig"), object.__getattribute__(self, "xǁPsnProviderǁ_extract_username__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_username.__signature__ = _mutmut_signature(xǁPsnProviderǁ_extract_username__mutmut_orig)
    xǁPsnProviderǁ_extract_username__mutmut_orig.__name__ = 'xǁPsnProviderǁ_extract_username'

    def xǁPsnProviderǁ_extract_avatar__mutmut_orig(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_1(self, soup: BeautifulSoup) -> str | None:
        og = None
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_2(self, soup: BeautifulSoup) -> str | None:
        og = soup.find(None, property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_3(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property=None)
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_4(self, soup: BeautifulSoup) -> str | None:
        og = soup.find(property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_5(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", )
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_6(self, soup: BeautifulSoup) -> str | None:
        og = soup.rfind("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_7(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("XXmetaXX", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_8(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("META", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_9(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="XXog:imageXX")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_10(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="OG:IMAGE")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_11(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og or og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_12(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get(None):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_13(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("XXcontentXX"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_14(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("CONTENT"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_15(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["XXcontentXX"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_16(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["CONTENT"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_17(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = None
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_18(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one(None)
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_19(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("XXimg.avatar, div.avatar imgXX")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_20(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("IMG.AVATAR, DIV.AVATAR IMG")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_21(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img or img.get("src"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_22(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get(None):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_23(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("XXsrcXX"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_24(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("SRC"):
            return img["src"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_25(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["XXsrcXX"]
        return None

    def xǁPsnProviderǁ_extract_avatar__mutmut_26(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["SRC"]
        return None
    
    xǁPsnProviderǁ_extract_avatar__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPsnProviderǁ_extract_avatar__mutmut_1': xǁPsnProviderǁ_extract_avatar__mutmut_1, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_2': xǁPsnProviderǁ_extract_avatar__mutmut_2, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_3': xǁPsnProviderǁ_extract_avatar__mutmut_3, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_4': xǁPsnProviderǁ_extract_avatar__mutmut_4, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_5': xǁPsnProviderǁ_extract_avatar__mutmut_5, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_6': xǁPsnProviderǁ_extract_avatar__mutmut_6, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_7': xǁPsnProviderǁ_extract_avatar__mutmut_7, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_8': xǁPsnProviderǁ_extract_avatar__mutmut_8, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_9': xǁPsnProviderǁ_extract_avatar__mutmut_9, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_10': xǁPsnProviderǁ_extract_avatar__mutmut_10, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_11': xǁPsnProviderǁ_extract_avatar__mutmut_11, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_12': xǁPsnProviderǁ_extract_avatar__mutmut_12, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_13': xǁPsnProviderǁ_extract_avatar__mutmut_13, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_14': xǁPsnProviderǁ_extract_avatar__mutmut_14, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_15': xǁPsnProviderǁ_extract_avatar__mutmut_15, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_16': xǁPsnProviderǁ_extract_avatar__mutmut_16, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_17': xǁPsnProviderǁ_extract_avatar__mutmut_17, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_18': xǁPsnProviderǁ_extract_avatar__mutmut_18, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_19': xǁPsnProviderǁ_extract_avatar__mutmut_19, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_20': xǁPsnProviderǁ_extract_avatar__mutmut_20, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_21': xǁPsnProviderǁ_extract_avatar__mutmut_21, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_22': xǁPsnProviderǁ_extract_avatar__mutmut_22, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_23': xǁPsnProviderǁ_extract_avatar__mutmut_23, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_24': xǁPsnProviderǁ_extract_avatar__mutmut_24, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_25': xǁPsnProviderǁ_extract_avatar__mutmut_25, 
        'xǁPsnProviderǁ_extract_avatar__mutmut_26': xǁPsnProviderǁ_extract_avatar__mutmut_26
    }
    
    def _extract_avatar(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPsnProviderǁ_extract_avatar__mutmut_orig"), object.__getattribute__(self, "xǁPsnProviderǁ_extract_avatar__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_avatar.__signature__ = _mutmut_signature(xǁPsnProviderǁ_extract_avatar__mutmut_orig)
    xǁPsnProviderǁ_extract_avatar__mutmut_orig.__name__ = 'xǁPsnProviderǁ_extract_avatar'

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_orig(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_1(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = None
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_2(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = None
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_3(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(None)
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_4(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = None
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_5(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(None)
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_6(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(None, strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_7(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=None))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_8(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_9(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", ))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_10(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text("XX XX", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_11(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=False))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_12(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_13(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = None
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_14(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    break

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_15(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = None
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_16(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(None, soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_17(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", None, re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_18(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), None)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_19(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_20(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_21(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), )
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_22(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(None, strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_23(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=None), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_24(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_25(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", ), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_26(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text("XX XX", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_27(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=False), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_28(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = None
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_29(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(None)
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_30(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(None))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_31(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(2))
                if n is not None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_32(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is None:
                    counts[tier] = n
        return counts

    def xǁPsnProviderǁ_extract_trophy_counts__mutmut_33(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = None
        return counts
    
    xǁPsnProviderǁ_extract_trophy_counts__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPsnProviderǁ_extract_trophy_counts__mutmut_1': xǁPsnProviderǁ_extract_trophy_counts__mutmut_1, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_2': xǁPsnProviderǁ_extract_trophy_counts__mutmut_2, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_3': xǁPsnProviderǁ_extract_trophy_counts__mutmut_3, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_4': xǁPsnProviderǁ_extract_trophy_counts__mutmut_4, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_5': xǁPsnProviderǁ_extract_trophy_counts__mutmut_5, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_6': xǁPsnProviderǁ_extract_trophy_counts__mutmut_6, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_7': xǁPsnProviderǁ_extract_trophy_counts__mutmut_7, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_8': xǁPsnProviderǁ_extract_trophy_counts__mutmut_8, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_9': xǁPsnProviderǁ_extract_trophy_counts__mutmut_9, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_10': xǁPsnProviderǁ_extract_trophy_counts__mutmut_10, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_11': xǁPsnProviderǁ_extract_trophy_counts__mutmut_11, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_12': xǁPsnProviderǁ_extract_trophy_counts__mutmut_12, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_13': xǁPsnProviderǁ_extract_trophy_counts__mutmut_13, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_14': xǁPsnProviderǁ_extract_trophy_counts__mutmut_14, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_15': xǁPsnProviderǁ_extract_trophy_counts__mutmut_15, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_16': xǁPsnProviderǁ_extract_trophy_counts__mutmut_16, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_17': xǁPsnProviderǁ_extract_trophy_counts__mutmut_17, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_18': xǁPsnProviderǁ_extract_trophy_counts__mutmut_18, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_19': xǁPsnProviderǁ_extract_trophy_counts__mutmut_19, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_20': xǁPsnProviderǁ_extract_trophy_counts__mutmut_20, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_21': xǁPsnProviderǁ_extract_trophy_counts__mutmut_21, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_22': xǁPsnProviderǁ_extract_trophy_counts__mutmut_22, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_23': xǁPsnProviderǁ_extract_trophy_counts__mutmut_23, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_24': xǁPsnProviderǁ_extract_trophy_counts__mutmut_24, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_25': xǁPsnProviderǁ_extract_trophy_counts__mutmut_25, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_26': xǁPsnProviderǁ_extract_trophy_counts__mutmut_26, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_27': xǁPsnProviderǁ_extract_trophy_counts__mutmut_27, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_28': xǁPsnProviderǁ_extract_trophy_counts__mutmut_28, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_29': xǁPsnProviderǁ_extract_trophy_counts__mutmut_29, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_30': xǁPsnProviderǁ_extract_trophy_counts__mutmut_30, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_31': xǁPsnProviderǁ_extract_trophy_counts__mutmut_31, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_32': xǁPsnProviderǁ_extract_trophy_counts__mutmut_32, 
        'xǁPsnProviderǁ_extract_trophy_counts__mutmut_33': xǁPsnProviderǁ_extract_trophy_counts__mutmut_33
    }
    
    def _extract_trophy_counts(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPsnProviderǁ_extract_trophy_counts__mutmut_orig"), object.__getattribute__(self, "xǁPsnProviderǁ_extract_trophy_counts__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_trophy_counts.__signature__ = _mutmut_signature(xǁPsnProviderǁ_extract_trophy_counts__mutmut_orig)
    xǁPsnProviderǁ_extract_trophy_counts__mutmut_orig.__name__ = 'xǁPsnProviderǁ_extract_trophy_counts'
