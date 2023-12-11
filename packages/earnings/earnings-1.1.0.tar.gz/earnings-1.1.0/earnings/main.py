from .utils import *


class Ticker:
    __slots__ = ("ticker",)
    BLANK_TICKER: str = "BLANK_TICKER"

    def __init__(self, sym: str = "") -> None:
        self.ticker: Union[str, None] = Ticker.BLANK_TICKER
        self.setTicker(_sym=sym)

    def setTicker(self, _sym: str = "") -> str:
        self.ticker = str(_sym).upper() if _sym != "" else Ticker.BLANK_TICKER
        return self.ticker

    def getTicker(self) -> str:
        return self.ticker

    def isBlankTicker(self) -> bool:
        return self.ticker == Ticker.BLANK_TICKER


class Portfolio:
    __slots__ = ("tickers",)

    def __init__(self, *args, **kwargs) -> None:
        self.tickers: list = []
        if len(args) > 0 and all([type(e) == str for e in args]):
            _ = [self.addTicker(sym=e) for e in args]

    def addTicker(self, sym: Union[str, Ticker] = Ticker.BLANK_TICKER) -> bool:
        t = Generic.getCleanTicker(sym)
        if t.isBlankTicker():
            return False
        if t not in self.tickers:
            self.tickers.append(t)
            return True
        return False

    def removeTicker(self, sym: Union[str, Ticker] = Ticker.BLANK_TICKER) -> bool:
        t = Generic.getCleanTicker(sym)
        if t.isBlankTicker():
            return False
        l1: int = len(self.tickers)
        self.tickers = list(set(list(filter(lambda x: x.getTicker() == t.getTicker(), self.tickers))))
        l2: int = len(self.tickers) - l1
        return l2 == 1

    def getTickers(self) -> list:
        return list(set(self.tickers))

    def importTickers(self, filename: str = "") -> bool:
        try:
            with open(file=filename, mode="r") as f:
                l: list = f.readlines()
                if len(l) == 0:
                    return False
                l = list(map(lambda x: x.replace("\n", ""), l))
                _ = list(map(lambda x: self.addTicker(sym=x), l))
            return True
        except FileNotFoundError as e:
            print(f"Portfolio file (.pff) not found\n--> {e}")
            return False


class Generic:
    @staticmethod
    def getHeatmap(mode: Heatmap = Heatmap.PRICES_MOVES) -> dict:
        assert isinstance(mode, Heatmap) #type(mode) == Heatmap
        _p: str = "?cat=rev" if mode == Heatmap.ESTIMATE_MOVES else ""
        r = get(f"{MAIN_URL}/api/getheatmap{_p}")
        return r.json()["children"]

    @staticmethod
    @outputFormat
    def getSPY() -> dict:
        """
        Returning the last 6-month daily candle OHLC data
        :return: dict
        """
        r = get(f"{MAIN_URL}/api/getspydata")
        return r.json()

    @staticmethod
    @outputFormat
    def checkSymbol(_sym: str = "") -> bool:
        try:
            r = post(f"{MAIN_URL}/api/tickers", {"symbol":_sym})
        except Exception as e:
            print(f"Exception (error: {e})")
            return False
        if r.status_code == 200:  # // 100 == 2:
            return len([k for k in r.json() if k["ticker"] == str(_sym).upper()]) == 1
        return False

    @staticmethod
    @outputFormat
    def getCleanTicker(sym: Union[str, Ticker] = Ticker.BLANK_TICKER) -> Ticker:
        if isinstance(sym, str):
            t: Ticker = Ticker(sym)
        elif isinstance(sym, Ticker):
            t: Ticker = sym
        return t


@addFunc("setOutputFormat", "setOutputFormat")
class Calendar:
    __slots__ = ("outputType",)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Calendar, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self) -> None:
        self.outputType: Output = Output.DICT

    @outputFormat
    def getEarningsByDay(self, day: Union[str, datetime.datetime, datetime.date]) -> dict:
        if isinstance(day, str):
            day = datetime.date.fromisoformat(day)
        elif isinstance(day, datetime.datetime):
            day = day.date()
        assert type(day) == datetime.date
        if day.weekday() in [5, 6]:
            raise Exception("weekend")
        r = get(f"{MAIN_URL}/api/caldata/{day.isoformat().replace('-', '')}")
        return r.json()

    @outputFormat
    def getConfirmedUpcomingEarningsBySector(self, sector: Sector = Sector.ALL) -> dict:
        """
        Returning the confirmed upcoming earnings by sector
        :return: dict
        """
        assert isinstance(sector, Sector)
        r = get(f"{MAIN_URL}/api/upcomingsectors")
        res = r.json()
        if sector != Sector.ALL:
            res = list(filter(lambda x: x["sector"] == sector.name, res))
        return res


@addFunc("setOutputFormat", "setOutputFormat")
class Earnings:
    __slots__ = ("outputType", "_sym", "stockData", "earningsDates", "dtInstance",)
    output: Output = Output.DICT

    def __init__(self, sym: str = "", preRetrieval: bool = False) -> None:
        self.outputType: Output = Output.DICT
        self._sym = str(sym).upper()
        self.dtInstance: datetime.datetime = datetime.datetime.now().replace(microsecond=0)
        self.stockData: Union[dict, None] = None
        self.earningsDates: dict = {"last": None, "next": None}
        if bool(preRetrieval):
            self.getCompanyInfo(_full=True)

    def _premCheck(self) -> bool:
        return Generic.checkSymbol(self._sym)

    def __str__(self) -> str:
        return f"Earnings ({self._sym})"

    def __repr__(self) -> None:
        print(self.__str__())

    def __hash__(self) -> int:
        return hash(self._sym)

    def getTicker(self) -> str:
        return self._sym

    def __eq__(self, other: object) -> bool:
        return self._sym == other._sym and self.dtInstance == other.dtInstance

    @outputFormat
    def getEarningsDates(self):
        if self.earningsDates["last"] is None or self.earningsDates["next"] is None:
            if self.stockData is None:
                self.getCompanyInfo(full=False)
            if self.stockData["lastEPSTime"] is not None:
                if "." not in self.stockData["lastEPSTime"]:
                    self.stockData["lastEPSTime"] += ".00"
            if self.stockData["nextEPSDate"] is not None:
                if "." not in self.stockData["nextEPSDate"]:
                    self.stockData["nextEPSDate"] += ".00"
            if self.stockData["confirmDate"] is not None:
                if "." not in self.stockData["confirmDate"]:
                    self.stockData["confirmDate"] += ".00"
            self.earningsDates["last"] = {
                "event_dt": datetime.datetime.strptime(self.stockData["lastEPSTime"], '%Y-%m-%dT%H:%M:%S.%f') if self.stockData["lastEPSTime"] is not None else None
            }
            self.earningsDates["next"] = {
                "event_dt": datetime.datetime.strptime(self.stockData["nextEPSDate"], '%Y-%m-%dT%H:%M:%S.%f') if self.stockData["nextEPSDate"] is not None else None,
                "confirm_dt": datetime.datetime.strptime(self.stockData["confirmDate"], '%Y-%m-%dT%H:%M:%S.%f') if self.stockData["confirmDate"] is not None else None,
                "release_counter": int(self.stockData["releaseTime"])
            }
        return self.earningsDates

    def getLastEarningsDate(self) -> datetime.datetime:
        if self.earningsDates["last"] is None:
            self.getEarningsDates()
        return self.earningsDates["last"]["event_dt"]

    def getNextEarningsDate(self) -> Union[datetime.datetime, str]:
        if self.earningsDates["next"] is None:
            self.getEarningsDates()
        if self.earningsDates["next"]["event_dt"] < datetime.datetime.now():
            return f"TBN"
        return self.earningsDates["next"]["event_dt"]

    @outputFormat
    def getCompanyInfo(self, full: bool = True) -> dict:
        if self.stockData is None:
            r = get(f"{MAIN_URL}/api/getstocksdata/{self._sym}")
            self.stockData = r.json()
            if full and "website" not in self.stockData:
                self.stockData["website"] = get(f"{MAIN_URL}/api/gotowebsite/{self._sym}").url
        return self.stockData

    @outputFormat
    def getQuotes(self) -> dict:
        r = get(f"{MAIN_URL}/api/getquotes/{self._sym}")
        return r.json()[self._sym]

    def getExpectedPriceAction(self) -> list:
        r = post(f"{MAIN_URL}/api/vote",
                 {
                     "ticker": self._sym,
                     "vote": DEFAULT_POST_OPTIONS["vote"]
                 })
        res = r.json()
        res[-1]["totalHolds"] -= 1
        return res

    @outputFormat
    def getExpectedPriceAction(self) -> list:
        r = post(f"{MAIN_URL}/api/expect",
                 {
                     "ticker": self._sym,
                     "vote": DEFAULT_POST_OPTIONS["expect"]
                 })
        res = r.json()
        res[-1]["meet"] -= 1
        res[-1]["total"] -= 1
        return res

    @outputFormat
    def getLastEarningsDetails(self) -> dict:
        r = get(f"{MAIN_URL}/api/epsdetails/{self._sym}")
        res = r.json()
        res["article"] = get(f"{MAIN_URL}/api/newsarticle/{self._sym}/{r.json()['fileName']}").json()
        return res

    @outputFormat
    def getChartData(self, freq: Frequency = Frequency.DAILY) -> dict:
        f_url: str = "weekly" if freq == Frequency.WEEKLY else ""
        r = get(f"{MAIN_URL}/api/get{f_url}chartdata/{self._sym}")
        return r.json()

    @outputFormat
    def getNews(self) -> dict:
        """
        Returning news articles (in time-descending order)
        :return:
        """
        r = get(f"{MAIN_URL}/api/getnews/{self._sym}")
        return r.json()

    @outputFormat
    def getArticle(self, articleId: int) -> dict:
        r = get(f"{MAIN_URL}/api/newsarticle/{self._sym}/{articleId}")
        return r.json()

    @outputFormat
    def getPivotPoints(self) -> dict:
        r = get(f"{MAIN_URL}/api/pivotpoints/{self._sym}/")
        return r.json()

    @outputFormat
    def getCandleCurrentQuarter(self) -> dict:
        r = get(f"{MAIN_URL}/api/getqhist/{self._sym}/")
        return r.json()

    @outputFormat
    def getWeeklyNetBuyRating(self) -> dict:
        r = get(f"{MAIN_URL}/api/anrechist?symbol={self._sym}")
        return r.json()
