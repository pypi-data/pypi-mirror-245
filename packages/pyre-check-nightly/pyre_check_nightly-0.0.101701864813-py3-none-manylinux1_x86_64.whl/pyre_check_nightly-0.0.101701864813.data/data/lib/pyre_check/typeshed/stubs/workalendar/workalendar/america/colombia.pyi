from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Colombia(WesternCalendar):
    FIXED_HOLIDAYS: Incomplete
    include_labour_day: ClassVar[bool]
    include_palm_sunday: ClassVar[bool]
    include_holy_thursday: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    include_easter_sunday: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    def get_epiphany(self, year): ...
    def get_saint_joseph(self, year): ...
    def get_ascension(self, year): ...
    def get_corpus_christi(self, year): ...
    def get_sacred_heart(self, year): ...
    def get_saint_peter_and_saint_paul(self, year): ...
    def get_assumption(self, year): ...
    def get_day_of_the_races(self, year): ...
    def get_all_saints(self, year): ...
    def get_cartagena_independence(self, year): ...
    def get_variable_days(self, year): ...
