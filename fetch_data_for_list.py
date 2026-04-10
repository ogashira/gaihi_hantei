from  datetime import date, timedelta
import warnings
import pandas as pd
from typing import List, Any
from abc import ABC, abstractmethod

warnings.filterwarnings('ignore', category=UserWarning)

class IFetchDataForList(ABC):

    @abstractmethod
    def fetch_data(self)-> List[List[Any]]:
        pass


class FetchHinban(IFetchDataForList):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> List[List[Any]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT HinHinCD AS 'Hinban',"
                    " HinTniCD AS 'Tni',"
                    " HinTju AS 'Tju',"
                    " HinFree11 AS 'RealHinban',"
                    " HinFree20 AS 'Harikae'"
                    " From dbo.MHINCD"
                    " WHERE HinSeiKBN = '7'"
                    )

        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_hinban')
        finally:
            cursor.close()
            self.cnxn.close()

        return data_list


class FetchPs(IFetchDataForList):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> List[List[Any]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT PsmHinCDO AS 'parent',"
                    " PsmHinCDK AS 'child',"
                    " PsmInsS AS 'weight'"
                    " From dbo.MPSMST"
                    " ORDER BY PsmHinCDO, PsmHinCDK"
                    )

        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_hinban')
        finally:
            cursor.close()
            self.cnxn.close()

        return data_list
