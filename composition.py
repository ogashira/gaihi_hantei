import warnings
from typing import List, Dict, Optional, Any
from decimal import Decimal
from abc import ABC, abstractmethod

warnings.filterwarnings('ignore', category=UserWarning)


class CompositionError(Exception):
    """配合が見つからない場合のエラー"""
    pass


class IComposition(ABC):

    @abstractmethod
    def show_compositon(self)-> None:
        pass

    @abstractmethod
    def insert_composition_to_list(self, l: List[List[Any]])-> None:
        pass

    @abstractmethod
    def breakdown_composition(self, d: Dict[str, Dict[str, Decimal]], 
                              d2: Dict[str, Decimal])-> None:
        pass


class Seihin(IComposition):

    def __init__(self, hinban: str, tnju: Decimal,
                 hinban_hinmoku1: Dict[str, str],
                 hinban_tani: Dict[str, str], 
                 ps: Dict[str, Dict[str, Decimal]],
                 breakdown: Dict[str, Dict[str, Decimal]]) -> None:

        self._hinban = hinban
        self._tnju = tnju
        self._hinmoku1: Dict[str, str] = hinban_hinmoku1
        self._tani: Dict[str, str] = hinban_tani
        self._ps: Dict[str, Dict[str, Decimal]] = ps
        self._breakdown: Dict[str, Dict[str, Decimal]] = breakdown


        self._composits:List[IComposition] = self._get_composits()


    def _get_composits(self)-> List[IComposition]:
        result: List[IComposition] = []
        if self._hinban not in self._ps:
            raise CompositionError(f'品番 {self._hinban} がPSマスタにありません')

        # もとのデータが仕掛品 + 缶の形でないと処理できないようにした
        if len(self._ps[self._hinban]) != 2:
            raise CompositionError(f'品番 {self._hinban} は計算できない構成' \
                                   f'（仕掛品+缶以外）です')
        child_dict: Dict[str, Decimal] = self._ps[self._hinban]
        for key, val in child_dict.items():
            if self._hinmoku1.get(key) == 'GK':
                result.append(Can(key, self._hinban))
                # canは内容物の重量ではないのでis_net = False
                continue
            result.append(Sikakari(key, # hinban
                                   self._hinban, # parent_hinban 
                                   self._tnju / Decimal(1000), 
                                   self._tani, 
                                   self._ps,
                                   self._breakdown)
                          )
        return result


    def show_compositon(self)-> None:
        for ins in self._composits:
            ins.show_compositon()


    def insert_composition_to_list(self, l: List[List[Any]])-> None:
        for ins in self._composits:
            ins.insert_composition_to_list(l)


    def breakdown_composition(self, d: Dict[str, Dict[str, Decimal]], 
                              d2: Dict[str, Decimal])-> None:
        for ins in self._composits:
            ins.breakdown_composition(d, d2)


class Can(IComposition):

    def __init__(self, 
                 hinban: str, 
                 parent_hinban: str, 
                 ) -> None:

        self._hinban = hinban
        self._parent_hinban = parent_hinban
        self._qty: int = 1

        # このインスタンスのqtyの割合を求める。psマスタの小品番の合計
        # に対しての割合
        # psマスタの子品番の合計
        # 成分の合計を求める


    def show_compositon(self)-> None:
        print(f'{self._parent_hinban}, {self._hinban}, {self._qty}缶')


    def insert_composition_to_list(self, l: List[List[Any]])-> None:
        inner_list: List[Any] = [self._parent_hinban, self._hinban, self._qty]
        l.append(inner_list)


    def breakdown_composition(self, d: Dict[str, Dict[str, Decimal]], 
                              d2: Dict[str, Decimal])-> None:
        pass


class Sikakari(IComposition):

    def __init__(self, 
                 hinban: str, 
                 parent_hinban: str, 
                 qty: Decimal, 
                 hinban_tani: Dict[str, str], 
                 ps: Dict[str, Dict[str, Decimal]],
                 breakdown: Dict[str, Dict[str, Decimal]]) -> None:

        self._hinban = hinban
        self._parent_hinban = parent_hinban
        self._net = qty
        self._hinban_tani = hinban_tani
        self._ps = ps
        self._breakdown: Dict[str, Dict[str, Decimal]] = breakdown

        # このインスタンスのqtyの割合を求める。psマスタの小品番の合計
        # に対しての割合
        # psマスタの子品番の合計
        # 成分の合計を求める
        child_dict: Optional[Dict[str, Decimal]] = ps.get(hinban)
        if child_dict is None:
            raise CompositionError(f'仕掛品 {hinban} の配合がありません')

        total: Decimal = self._calc_total(child_dict)
        self._ratio = self._net / total

        self._composits:List[IComposition] = self._get_composits(child_dict)


    def _calc_total(self, child_dict) -> Decimal:
        total: Decimal = Decimal(0)
        for key, val in child_dict.items():
            if self._hinban_tani.get(key) == 'G': 
                total += val / Decimal(1000)
                continue
            total += val

        return total


    def _get_composits(self, child_dict)-> List[IComposition]:
        result: List[IComposition] = []
        # psの親品番にkeyが存在していたらGtのインスタンスを
        # 存在していなかったらGenryouのインスタンスを生成する
        for key, val in child_dict.items():
            if self._hinban_tani.get(key) == 'G':
                 val = val / Decimal(1000)
            genryou_qty: Decimal = val * self._ratio
            if key not in self._ps: 
                result.append(Genryou(key, self._hinban, genryou_qty, 
                                      self._breakdown, self._net)) 
                # 仕掛品は内容物の重量なのでis_net = True
                continue

            result.append(Gt(key, # hinban
                                   self._hinban, # parent_hinban 
                                   genryou_qty,
                                   self._hinban_tani, 
                                   self._ps,
                                   self._breakdown,
                                   self._net)
                         )
        return result


    def show_compositon(self)-> None:
        for ins in self._composits:
            ins.show_compositon()


    def insert_composition_to_list(self, l: List[List[Any]])-> None:
        for ins in self._composits:
            ins.insert_composition_to_list(l)


    def breakdown_composition(self, d: Dict[str, Dict[str, Decimal]], 
                              d2: Dict[str, Decimal])-> None:
        for ins in self._composits:
            ins.breakdown_composition(d, d2)


class Gt(IComposition):

    def __init__(self, 
                 hinban: str, 
                 parent_hinban: str, 
                 qty: Decimal, 
                 hinban_tani: Dict[str, str], 
                 ps: Dict[str, Dict[str, Decimal]],
                 breakdown: Dict[str, Dict[str, Decimal]],
                 net: Decimal) -> None: # 入れ目

        self._hinban: str = hinban
        self._parent_hinban: str = parent_hinban
        self._hinban_tani: Dict[str, str] = hinban_tani
        self._ps: Dict[str, Dict[str, Decimal]]= ps
        self._breakdown: Dict[str, Dict[str, Decimal]] = breakdown
        self._net: Decimal = net

        # このインスタンスのqtyの割合を求める。psマスタの小品番の合計
        # に対しての割合
        # psマスタの子品番の合計
        # 成分の合計を求める
        child_dict: Optional[Dict[str, Decimal]] = ps.get(hinban)
        if child_dict is None:
            raise CompositionError(f'GT {hinban} の配合がありません')

        total: Decimal = self._calc_total(child_dict)
        self._ratio = qty / total

        self._composits:List[IComposition] = self._get_composits(child_dict)


    def _calc_total(self, child_dict) -> Decimal:
        total: Decimal = Decimal(0)
        for key, val in child_dict.items():
            if self._hinban_tani.get(key) == 'G': 
                total += val / Decimal(1000)
                continue
            total += val

        return total


    def _get_composits(self, child_dict)-> List[IComposition]:
        result: List[IComposition] = []
        # psの親品番にkeyが存在していたらGtのインスタンスを
        # 存在していなかったらGenryouのインスタンスを生成する
        for key, val in child_dict.items():
            if self._hinban_tani.get(key) == 'G':
                 val = val / Decimal(1000)
            genryou_qty: Decimal = val * self._ratio
            if key not in self._ps: 
                result.append(Genryou(key, self._hinban, genryou_qty, 
                                      self._breakdown, self._net)
                             )
                continue

            result.append(Gt(key, # hinban
                             self._hinban, # parent_hinban 
                             genryou_qty,
                             self._hinban_tani, 
                             self._ps,
                             self._breakdown,
                             self._net)
                         )
        return result


    def show_compositon(self)-> None:
        for ins in self._composits:
            ins.show_compositon()



    def insert_composition_to_list(self, l: List[List[Any]])-> None:
        for ins in self._composits:
            ins.insert_composition_to_list(l)


    def breakdown_composition(self, d: Dict[str, Dict[str, Decimal]], 
                              d2: Dict[str, Decimal])-> None:
        for ins in self._composits:
            ins.breakdown_composition(d, d2)


class Genryou(IComposition):

    def __init__(self, hinban: str, parent_hinban: str, qty: Decimal, 
                          breakdown: Dict[str, Dict[str, Decimal]],
                                                    net: Decimal) -> None:
        self._hinban: str = hinban
        self._parent_hinban: str = parent_hinban
        self._qty: Decimal = qty
        self._breakdown = breakdown
        self._qty_per_net: Decimal = self._qty / net
        

    def show_compositon(self)-> None:
        print(f'{self._parent_hinban}, {self._hinban}, {self._qty_per_net * 100}%')


    def insert_composition_to_list(self, l: List[List[Any]])-> None:
        inner_list: List[Any] = [self._parent_hinban, self._hinban, self._qty]
        l.append(inner_list)


    def breakdown_composition(self, d: Dict[str, Dict[str, Decimal]], 
                              d2: Dict[str, Decimal])-> None:
        # d = breakdown成分分解データ、d2 = brokendown_composition（分解成分の辞書）
        inner_dic: Optional[Dict[str, Decimal]] = d.get(self._hinban)
        if inner_dic is not None:
            for key, val in inner_dic.items():
                if key in d2:
                    d2[key] = d2[key] + (Decimal(val) * self._qty_per_net) 
                    continue
                d2[key] = Decimal(val) * self._qty_per_net



