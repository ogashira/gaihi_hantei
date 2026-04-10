from  datetime import date, timedelta
import warnings
import pandas as pd
from typing import List
from abc import ABC, abstractmethod

warnings.filterwarnings('ignore', category=UserWarning)

class IFetchData(ABC):

    @abstractmethod
    def fetch_data(self)-> pd.DataFrame:
        pass


class FetchHolidays(IFetchData):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn


    def fetch_data(self)-> pd.DataFrame:

        # cursor = cnxn.cursor()

        today = date.today()
        before30days = today - timedelta(days=30)
        after30days = today + timedelta(days=30)

        before30str = before30days.strftime('%Y/%m/%d')
        after30str = after30days.strftime('%Y/%m/%d')


        sqlQuery = ("SELECT KJ_DT" 
                    " From dbo.TM_KJ"
                    " WHERE KJ_DT > ? AND KJ_DT < ? AND DEL_FLG <> ?" 
                    " ORDER BY KJ_DT")
        
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=[before30str, after30str, '1'])
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_holiday')

        return df


class FetchYotei(IFetchData):

    def __init__(self, cnxn, yokujitu:str) -> None:
        self.cnxn = cnxn
        self.yokujitu = f'{yokujitu[:4]}{yokujitu[5:7]}{yokujitu[8:]}'


    def fetch_data(self)-> pd.DataFrame:

        # cursor = cnxn.cursor()
        sqlQuery = ("SELECT RJYUCD.RjcSKDay AS 'Date',"
                    " RJYUCD.RjcJCNo As 'JtyuNo',"
                    " RJYUCD.RjcJGNo As 'JtyuGyouNo',"
                    " RJYUCD.RjcTokCD AS 'TokuiCD',"
                    " RJYUCD.RjcNonyuCD AS 'NonyuCD',"
                    " RJYUCD.RjcHinCD AS 'Hinban',"
                    " RJYUCD.RjcJcSu AS 'Qty',"
                    " RJYUCD.RjcTniCD AS 'TaniCD'"
                    " FROM dbo.RJYUCD"
                    " WHERE RJYUCD.RjcSKDay = ?" 
                    " AND RJYUCD.RjcTokCD < ?"
                    " ORDER BY RJYUCD.RjcJCNo, RJYUCD.RjcJGNo"
                    )

        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                             params= [self.yokujitu, 'T6000'])
        except Exception as e:
            print(f'データベースfetch中に予期せぬエラーです fetch_yotei')
            print(e)

        return df


class FetchInspectProducts(IFetchData):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn


    def fetch_data(self)-> pd.DataFrame:
        '''
        TM_KS_NS: 検査日数表
        '''
        # cursor = cnxn.cursor()
        sqlQuery = ("SELECT ITEM_ID" 
                    " From dbo.TM_KS_NS"
                    " WHERE  DEL_FLG <> ?" 
                    " ORDER BY ITEM_ID")
        
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=['1'])
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_holiday')

        return df


class FetchUriageSumi(IFetchData):

    def __init__(self, cnxn, yokujitu:str) -> None:
        self.cnxn = cnxn
        self.yokujitu = f'{yokujitu[:4]}{yokujitu[5:7]}{yokujitu[8:]}'
        

    def fetch_data(self) -> pd.DataFrame:

        sqlQuery = ("SELECT RURIDT.RurUriDay AS 'Date'," 
                    " RURIDT.RurJCNo AS 'JtyuNo'," 
                    " RURIDT.RurJGNo AS 'JtyuGyouNo',"
                    " RURIDT.RurTokCD AS 'TokuiCD'," 
                    " RURIDT.RurNonyuCD AS 'NonyuCD',"
                    " RURIDT.RurHinCD AS 'Hinban',"
                    " RURIDT.RurUriSu AS 'Qty',"
                    " RURIDT.RurUriTniCD AS 'TaniCD'"
                    " FROM dbo.RURIDT"
                    " WHERE RURIDT.RurUriDay = ?" 
                    " AND RURIDT.RurTokCD < ?"
                    " ORDER BY RURIDT.RurJCNo, RURIDT.RurJGNo"
                    )

        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                             params= [self.yokujitu, 'T6000'])
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_UriageSumi')

        return df


class FetchInventory(IFetchData):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> pd.DataFrame:

        sqlQuery = ("SELECT ZaiHinCD AS 'Hinban',"
                    " ZaiBuCD AS '倉庫', ZaiLotNo AS 'Lot',"
                    " ZaiZaiSuG AS 'Qty'"
                    " From dbo.BZAIKO"
                    " WHERE (ZaiBuCD = 'S0001'"
                    " OR ZaiBuCD = 'S0021')"
                    " AND ZaiZaiSuG > 0"
                    )
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn)
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_inventory')

        return df


class FetchHinban(IFetchData):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> pd.DataFrame:

        sqlQuery = ("SELECT HinHinCD AS 'Hinban',"
                    " HinTniCD AS 'Tni',"
                    " HinTju AS 'Tju',"
                    " HinFree11 AS 'RealHinban',"
                    " HinFree20 AS 'Harikae'"
                    " From dbo.MHINCD"
                    " WHERE HinSeiKBN = '7'"
                    )
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn)
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_hinban')

        return df


class FetchHk(IFetchData):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn


    def fetch_data(self)-> pd.DataFrame:
        '''
        TF_HS: 品質管理
        '''
        # cursor = cnxn.cursor()
        sqlQuery = ("SELECT ITEM_ID as 'Hinban', LOT, KANRI_QTY as 'Cans'," 
                    " USER_NM_SEI as 'User'" 
                    " From dbo.TF_HS"
                    " LEFT JOIN dbo.TM_USER"
                    " ON TF_HS.KS_TT_USER = TM_USER.USER_ID"
                    " WHERE  TF_HS.DEL_FLG <> ?" 
                    " AND END_SHIKEN_KBN IS NULL"
                    " ORDER BY TF_HS.UPD_DTTM")
        
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=['1'])
        except Exception as e:
            print(f'データベースfetch中に予期せぬエラーです fetch_TF_HS')
            print(e)

        return df


class FetchMhk(IFetchData):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn


    def fetch_data(self)-> pd.DataFrame:
        '''
        TF_MHS: メタル品質管理
        '''
        # cursor = cnxn.cursor()
        sqlQuery = ("SELECT ITEM_ID as 'Hinban', LOT, KAN_QTY as 'Cans'" 
                    " From dbo.TF_MHS"
                    " WHERE DEL_FLG <> ?" 
                    " AND HANTEI IS NULL"
                    " ORDER BY UPD_DTTM")
        
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=['1'])
        except Exception as e:
            print(f'データベースfetch中に予期せぬエラーです fetch_TF_HS')
            print(e)

        return df


class FetchHkLot(IFetchData):

    def __init__(self, cnxn, six_months_ago) -> None:
        self.cnxn = cnxn
        self.six_months_ago = six_months_ago


    def fetch_data(self)-> pd.DataFrame:
        '''
        TF_HS: 品質管理
        '''
        # cursor = cnxn.cursor()
        sqlQuery = ("SELECT  LOT" 
                    " From dbo.TF_HS"
                    " WHERE  TF_HS.DEL_FLG <> ?" 
                    " AND INS_DTTM >= ?"
                    " ORDER BY LOT")
        
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=['1', self.six_months_ago])
        except Exception as e:
            print(f'データベースfetch中に予期せぬエラーです fetch_TF_HS_LOT')
            print(e)

        return df


class FetchMhkLot(IFetchData):

    def __init__(self, cnxn, six_months_ago) -> None:
        self.cnxn = cnxn
        self.six_months_ago = six_months_ago


    def fetch_data(self)-> pd.DataFrame:
        '''
        TF_MHS: メタル品質管理
        '''
        # cursor = cnxn.cursor()
        sqlQuery = ("SELECT LOT" 
                    " From dbo.TF_MHS"
                    " WHERE TF_MHS.DEL_FLG <> ?" 
                    " AND INS_DTTM >= ?"
                    " ORDER BY LOT")
        
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=['1', self.six_months_ago])
        except Exception as e:
            print(f'データベースfetch中に予期せぬエラーです fetch_TF_MHS_LOT')
            print(e)

        return df


class FetchHkNotSumi(IFetchData):
    '''
    NULLで合格、または、中で合格、または、特。
    IDOU= {'01':'中', '02':'済', '03':'特'}
    '''

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn


    def fetch_data(self)-> pd.DataFrame:
        '''
        TF_HS: 品質管理
        IDOU <> '02'　02以外としてもNULLは取得できない。
        従って(IDOU IS NULL OR IDOU <> '02')とした
        '''
        # cursor = cnxn.cursor()
        sqlQuery = ("SELECT ITEM_ID as 'Hinban', LOT, KANRI_QTY as 'Cans'," 
                    " USER_NM_SEI as 'User'" 
                    " From dbo.TF_HS"
                    " LEFT JOIN dbo.TM_USER"
                    " ON TF_HS.KS_TT_USER = TM_USER.USER_ID"
                    " WHERE  TF_HS.DEL_FLG <> ?" 
                    " AND (((IDOU IS NULL OR IDOU <> '02' )AND HANTEI='合格') OR IDOU = '03')"
                    " ORDER BY TF_HS.UPD_DTTM")
        
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=['1'])
        except Exception as e:
            print(f'データベースfetch中に予期せぬエラーです FetchHkNotSumi')
            print(e)

        return df


class FetchMhkNotSumi(IFetchData):
    '''
    NULLで合格、または、中で合格、または、特。
    IDOU= {'01':'中', '02':'済', '03':'特'}
    '''

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn


    def fetch_data(self)-> pd.DataFrame:
        '''
        TF_HS: 品質管理
        IDOU <> '02'　02以外としてもNULLは取得できない。
        従って(IDOU IS NULL OR IDOU <> '02')とした
        '''
        # cursor = cnxn.cursor()
        
        sqlQuery = ("SELECT ITEM_ID as 'Hinban', LOT, KAN_QTY as 'Cans'" 
                    " From dbo.TF_MHS"
                    " WHERE DEL_FLG <> ?" 
                    " AND (((IDOU IS NULL OR IDOU <> '02' )AND HANTEI='合格') OR IDOU = '03')"
                    " ORDER BY UPD_DTTM")

        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=['1'])
        except Exception as e:
            print(f'データベースfetch中に予期せぬエラーです FetchMhkNotSumi')
            print(e)

        return df


class FetchKoitoKensa(IFetchData):
    '''
    小糸coa発行が必要なデータをfetchする
    NULLで合格でAorB、または、中で合格でAorB、または、特で合格でAorB。
    IDOU= {'01':'中', '02':'済', '03':'特'}
    '''

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn


    def fetch_data(self)-> pd.DataFrame:
        '''
        TF_HS: 品質管理
        IDOU <> '02'　02以外としてもNULLは取得できない。
        従って(IDOU IS NULL OR IDOU <> '02')とした
        '''
        # cursor = cnxn.cursor()
        sqlQuery = ("SELECT ITEM_ID as 'Hinban', LOT, KANRI_QTY as 'Cans'," 
                    " SHIKEN, IDOU"
                    " From dbo.TF_HS"
                    " WHERE  TF_HS.DEL_FLG <> ?" 
                    " AND (SHIKEN='01' OR SHIKEN='02')"
                    " AND HANTEI='合格'"
                    " ORDER BY TF_HS.LOT")
        
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=['1'])
        except Exception as e:
            print(f'データベースfetch中に予期せぬエラーです FetchHkIdou')
            print(e)

        return df


class FetchSyukko(IFetchData):

    def __init__(self, cnxn, honjitu) -> None:
        self.cnxn = cnxn
        self.honjitu = f'{honjitu[:4]}{honjitu[5:7]}{honjitu[8:]}'


    def fetch_data(self)-> pd.DataFrame:
        '''
        TF_HS: 品質管理
        IDOU <> '02'　02以外としてもNULLは取得できない。
        従って(IDOU IS NULL OR IDOU <> '02')とした
        '''
        # cursor = cnxn.cursor()
        sqlQuery = ("SELECT RsySKDay AS '出庫日',"
                    " RsyHinNam AS '品名',"
                    " RsyHinCD AS '品番',"
                    " RsySKSu AS '出庫数量',"
                    " RsyTehaiCD '出庫先コード',"
                    " RsyLotNo 'ロットＮＯ',"
                    " RsySokoFrom '出庫元倉庫',"
                    " RsySKNo '出庫ＮＯ',"
                    " RsySKGNo '出庫行ＮＯ'"
                    " From dbo.RSYUKO"
                    " WHERE RsySKDay = ?" 
                    " AND ((RsySokoFrom = 'S0008' AND RsyTehaiCD = 'S0001')"
                    " OR (RsySokoFrom = 'S0012' AND RsyTehaiCD = 'S0013')"
                    " OR (RsySokoFrom = 'S0028' AND RsyTehaiCD = 'S0021')"
                    " OR (RsySokoFrom = 'S0032' AND RsyTehaiCD = 'S0033')"
                    " OR (RsySokoFrom = 'S0038' AND RsyTehaiCD = 'S0031')"
                    " OR (RsySokoFrom = 'S0010' AND RsyTehaiCD = 'S0004')"
                    " OR (RsySokoFrom = 'S0030' AND RsyTehaiCD = 'S0024'))"
                )
        
        df: pd.DataFrame = pd.DataFrame()
        try:
            df = pd.read_sql(sqlQuery, self.cnxn, 
                                       params=[self.honjitu])
        except Exception as e:
            print(f'データベースfetch中に予期せぬエラーです FetchHkIdou')
            print(e)

        return df
