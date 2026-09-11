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
                    " HinMokCD1 AS 'hinmoku1',"
                    " HinTniCD AS 'Tni',"
                    " HinTju AS 'Tju',"
                    " HinFree11 AS 'RealHinban',"
                    " HinFree20 AS 'Harikae'"
                    " From dbo.MHINCD"
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
            # cnxnは呼び出しもとでクローズ

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
            # cnxnは呼び出しもとでクローズ

        return data_list


class FetchComponentBreakdown(IFetchDataForList):
    '''
    成分分解表の取得
    '''
    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> List[List[Any]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT ITEM_ID AS 'parent',"
                    " ZAIRYO AS 'child',"
                    " ZAIRYO_PERCENT AS 'percent'"
                    " From dbo.TM_SBBK"
                    " ORDER BY ITEM_ID"
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
            # cnxnは呼び出しもとでクローズ

        return data_list


class FetchDb(IFetchDataForList):
    '''
    成分分解表の取得
    '''
    def __init__(self, cnxn, hinban) -> None:
        self.cnxn = cnxn
        self._hinban = hinban
        

    def fetch_data(self) -> List[List[Any]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT ITEM_ID AS 'hinban',"
                    " LBL_HYOJI_NM AS 'display_name'"
                    " From dbo.TF_DB"
                    f" WHERE ITEM_ID = '{self._hinban}'"
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
            # cnxnは呼び出しもとでクローズ

        return data_list
