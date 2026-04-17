from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING, Any, List
import platform
import sys
from fetch_data_for_list import IFetchDataForList
from list_to_dict import ListToDict

# 実行時にはインポートせず、型チェックの為だけに書く
if TYPE_CHECKING:
    from soukoidou2.effitA import EffitA
    from cybozu import ICybozu
    from recorder import Recorder


class InstanceFactory:
    '''
    各モジュールのインポートは必要な時にメソッド内で行う。
    冒頭でまとめてやると実行速度が急激に遅くなったため
    '''

    _sqlServerTss: Any = None
    _sqlServerEffit: Any = None
    _cnxn_tss = None
    _cnxn_effit = None

    _instances: Dict[str, Any] = {}

    @classmethod
    def _setup_sql_path(cls) -> None:
        """SQLサーバー用モジュールのパスを通す (一度だけ実行)"""
        if 'sql_path_setup' in cls._instances:
            return
            
        shared_folder_path: str = r'./'
        if platform.system() == 'Linux':
            shared_folder_path = \
                r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sql_python_module'
        elif platform.system() == 'Windows':
            shared_folder_path = \
                r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sql_python_module'
        
        if shared_folder_path not in sys.path:
            sys.path.append(shared_folder_path)
        cls._instances['sql_path_setup'] = True

    @classmethod
    def get_sql_server_tss(cls) -> None:
        if cls._sqlServerTss is None:
            cls._setup_sql_path()
            from sql_server_tss_addmin import SqlServer as SqlServerTss 
            cls._sqlServerTss = SqlServerTss()
            cls._cnxn_tss = cls._sqlServerTss.get_cnxn()

    @classmethod
    def get_sql_server_effit(cls) -> None:
        if cls._sqlServerEffit is None:
            cls._setup_sql_path()
            from sql_server import SqlServer as SqlServerEffit
            cls._sqlServerEffit = SqlServerEffit()
            cls._cnxn_effit = cls._sqlServerEffit.get_cnxn()

    @classmethod
    def delete_cnxn(cls) -> None:
        if cls._sqlServerTss:
            cls._sqlServerTss.close()
        if cls._sqlServerEffit:
            cls._sqlServerEffit.close()


    @classmethod
    def get_fetchHinban(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchHinban
        ins_name: str = 'fetchHinban'
        if ins_name not in cls._instances:
            cls.get_sql_server_effit()
            cls._instances[ins_name] = FetchHinban(cls._cnxn_effit)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchPs(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchPs
        ins_name: str = 'fetchPs'
        if ins_name not in cls._instances:
            cls.get_sql_server_effit()
            cls._instances[ins_name] = FetchPs(cls._cnxn_effit)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchComponentBreakdown(cls) -> IFetchDataForList:#成分分解表
        from fetch_data_for_list import FetchComponentBreakdown
        ins_name: str = 'FetchComponentBreakdown'
        if ins_name not in cls._instances:
            cls.get_sql_server_effit()
            cls._instances[ins_name] = FetchComponentBreakdown(cls._cnxn_tss)
        return cls._instances[ins_name]


    @classmethod
    def get_listToDict(cls) -> ListToDict:
        from list_to_dict import ListToDict
        ins_name: str = 'listToDict'
        if ins_name not in cls._instances:
            cls._instances[ins_name] = ListToDict()
        return cls._instances[ins_name]
