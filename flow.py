import yaml
from typing import Dict, List, Any
from decimal import Decimal
from ui import run_ui
from instance_factory import InstanceFactory
from fetch_data_for_list import FetchComponentBreakdown, IFetchDataForList, FetchHinban, FetchPs
from list_to_dict import ListToDict
from composition import IComposition, Seihin, CompositionError


def start()-> None:
    '''
    dic_info = {'hinban': , 'date': , 'format': , 'addr': }
    '''
    with open('atena.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    # uiを立ち上げて、dic_infoに情報を詰めてもらう
    dic_info:Dict[str, str] = {}
    run_ui(dic_info, config)

    # sql_server, sql_server_tssのcnxnを作っておく
    InstanceFactory.get_sql_server_tss()
    InstanceFactory.get_sql_server_effit()

    # 品番マスタ取得
    fetchHinban:IFetchDataForList = InstanceFactory.get_fetchHinban()
    hinban_list: List[List[Any]] = fetchHinban.fetch_data()

    # PSマスタ取得
    fetchPs: IFetchDataForList = InstanceFactory.get_fetchPs()
    ps_list: List[List[Any]] = fetchPs.fetch_data()

    # 成分分解表取得
    fetchComponentBreakdown: IFetchDataForList = \
                        InstanceFactory.get_fetchComponentBreakdown()
    breakdown_list: List[List[Any]] = fetchComponentBreakdown.fetch_data() 

    # リストを辞書に変換
    listToDict: ListToDict = InstanceFactory.get_listToDict()
    hinban_hinmoku1: Dict[str, str] = \
                                   listToDict.create_dict_Any(hinban_list, 0, 1)
    hinban_tani: Dict[str, str] = \
                                   listToDict.create_dict_Any(hinban_list, 0, 2)
    hinban_tnju: Dict[str, Decimal] = \
                                   listToDict.create_dict_Any(hinban_list, 0, 3)
    hinban_real: Dict[str, str] = \
                                   listToDict.create_dict_Any(hinban_list, 0, 4)
    hinban_harikae: Dict[str, str] = \
                                   listToDict.create_dict_Any(hinban_list, 0, 5)
    ps: Dict[str, Dict[str, Decimal]] = \
                                   listToDict.create_dict_dict(ps_list, 0, 1, 2)
    breakdown: Dict[str, Dict[str, Decimal]] = \
                            listToDict.create_dict_dict(breakdown_list, 0, 1, 2)
    
    # 入力されたhinbanを配合が存在する品番に変換する。
    # まず、-EX-ENG, -1-U などを　-EX, -U にする
    hinban = dic_info['hinban']
    if hinban in hinban_real:
        hinban = hinban_real[hinban]
    # 次に、張替え製品を配合製品にする S9-GH200-TH -> S9-U100-TH
    if hinban in hinban_harikae:
        hinban = hinban_harikae[hinban]

    # Seihinのインスタンスを生成すると、Sikakari, Gt, Genryouが次々出来上がる
    try:
        seihin: IComposition = Seihin(hinban, hinban_tnju[hinban], 
                                    hinban_hinmoku1, hinban_tani, ps, breakdown)
    except KeyError as e:
        print('入力した品番がありません')
        print(e)
        InstanceFactory.delete_cnxn()
        return
        
    except CompositionError as e: #自作のException
        print(f"エラー: {e}")
        # 接続を解除してから return
        InstanceFactory.delete_cnxn()
        return

    seihin.show_compositon()
    brokendown_composition: Dict[str, Decimal] = {}

    seihin.breakdown_composition(breakdown, brokendown_composition)

    print(brokendown_composition)
    sum: Decimal = Decimal(0)
    for _, val in brokendown_composition.items():
        sum += val

    print(sum)



    # 最後にsql_server, sql_server_tssのcnxnを削除する
    InstanceFactory.delete_cnxn()
