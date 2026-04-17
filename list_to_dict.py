from typing import List, Dict, Any
from decimal import Decimal

class ListToDict:

    def __init__(self) -> None:
        pass

    def create_dict_dict(self, list_list: List[List[Any]],
                         parent_key_idx: int, 
                         child_key_idx: int,
                         value_idx: int) -> Dict[str, Dict[str, Decimal]]:
        
        # raw_data: SQLから取得した2次元リスト

        result = {}
        for row in list_list:
            parent_key: str = row[parent_key_idx]  # 'AAA' など
            child_key: str  = row[child_key_idx]  # 'abc' など
            value: Decimal  = row[value_idx]  # 15 など

            # 親キーがなければ新しい辞書を作る
            if parent_key not in result:
                result[parent_key] = {}
            
            # 子キーが存在していれば、valueをプラス
            if child_key in result[parent_key]:
                result[parent_key][child_key] = result[parent_key][child_key] + value
            else:
                result[parent_key][child_key] = value

        return result


    def create_dict_Any(self, list_list: List[List[Any]],
                    key_idx: int, value_idx: int) -> Dict[str, Any]:
        '''
        品番マスタのListがわたってくるので、keyが重複することは無い
        valueは単位または単重
        '''
        result = {}
        for row in list_list:
            key: str = row[key_idx]  
            value: Any = row[value_idx]
            if value == ' ' or value == '':
                continue

            result[key] = value

        return result





            


        
