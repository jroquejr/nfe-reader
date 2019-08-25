import locale

from .ba.crawler import Crawler as BA_Crawler

locale.setlocale(locale.LC_ALL, "pt_BR")

UF_CRAWLERS = {"ba": BA_Crawler}
