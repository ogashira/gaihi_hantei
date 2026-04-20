from abc import ABC, abstractmethod 
from decimal import Decimal
from typing import Dict
from gaihi_hantei import hantei

class IJudgmentGaihi(ABC):

    @abstractmethod
    def get_component_percent(self) -> Dict[str, Decimal]:
        pass

    @abstractmethod
    def judgment_gaihi(self) -> Dict[str, str]:
        pass


class Reg2_21_3(IJudgmentGaihi):
    '''
    トルエン、MEK
    '''

    def __init__(self, reg_dic: Dict, 
                 brokendown_composition: Dict[str, Decimal])-> None:
        '''
        reg_dic = 
        {'composit1': {'hinban': 'G-TOL', 'name': 'トルエン', 'threshold': 
        {'対象外': 'x == 0', '非': 'x > 0 and x < 50', '該': 'x >= 50 and x <= 100'}}, 
        'composit2': {'hinban': 'G-MEK', 'name': 'エチルメチルケトン', 'threshold': 
        {'対象外': 'x == 0', '非': 'x > 0 and x < 50', '該': 'x >= 50'}}
        '''
        self._reg_dic: Dict = reg_dic
        self._composition: Dict[str,Decimal] = brokendown_composition
        self._component_percent: Dict[str, Decimal] = self.get_component_percent()
        self._gaihi: Dict[str, str] = self.judgment_gaihi()

        print(self._component_percent)
        print(self._gaihi)

        

    def get_component_percent(self) -> Dict[str, Decimal]:
        component_percent: Dict[str, Decimal] = {}
        for key, val in self._reg_dic.items():
            hinban = val['hinban'] # G-TOL, G-MEK
            name = val['name'] # トルエン、エチルメチルケトン
            component_percent[name] = \
                    self._composition.get(hinban, Decimal(0)) * Decimal(100)

        return component_percent


    def judgment_gaihi(self) -> Dict[str, str]:

        component_gaihi_dic = {}
        for _, val in self._reg_dic.items():
            name = val['name'] # トルエン、エチルメチルケトン
            d = val['threshold'] # {'対象外': 'x = 0 ...} 
            percent = self._component_percent.get(name, Decimal(0))
            component_gaihi_dic[name] = hantei(d, percent)

        # gaihi_component_dic = {'トルエン':'該', 'エチルメチルケトン':'非'}
        # gaihi_list = ['該', '非']
        # gaihi_dic = {'reg2-21-3': '該'}
        gaihi_list = []
        for _, val in component_gaihi_dic.items():
            gaihi_list.append(val)

        gaihi_dic = {}
        if all(x == '対象外' for x in gaihi_list):
            gaihi_dic = {'reg2-21-3': '対象外'} # 全て対象外なら対象外
        elif any(x == '該' for x in gaihi_list):
            gaihi_dic = {'reg2-21-3': '該'} # 一つでも該があれば該
        else:
            gaihi_dic = {'reg2-21-3': '非'} # それ以外は非

        return gaihi_dic



class Reg1_4_1(IJudgmentGaihi):
    '''
    ミサイル（ポリブタ）
    '''

    def __init__(self, reg_dic: Dict, 
                 brokendown_composition: Dict[str, Decimal])-> None:
        '''
        reg_dic = 
        {'composit1': {'hinban': 
        ['G-G-2000', 'G-G-3000', 'G-T-4000', 'G-TP-2000'], 
        'name': '末端に水酸基を有するポリブタジエン', 'threshold': 
        {'対象外': 'x == 0', '非': 'x > 0 and x <= 100', '該': 'False'}}
        '''
        self._reg_dic: Dict = reg_dic
        self._composition: Dict[str,Decimal] = brokendown_composition
        self._component_percent: Dict[str, Decimal] = self.get_component_percent()
        self._gaihi: Dict[str, str] = self.judgment_gaihi()

        print(self._component_percent)
        print(self._gaihi)


    def get_component_percent(self) -> Dict[str, Decimal]:
        component_percent: Dict[str, Decimal] = {}
        for key, val in self._reg_dic.items():
            hinbans = val['hinban'] # [G-G-2000, G-G-3000, G-T-4000, G-TP-2000]
            name = val['name'] # 末端に水酸基を有するポリブタジエン
            for hinban in hinbans:
                component_percent[name] = \
                    component_percent.get(name, Decimal(0)) + \
                    self._composition.get(hinban, Decimal(0)) * Decimal(100)

        return component_percent
        

    def judgment_gaihi(self) -> Dict[str, str]:
        gaihi_dic = {}
        for _, val in self._reg_dic.items():
            name = val['name'] # 末端に水酸基を有するポリブタジエン
            d = val['threshold'] # {'対象外': 'x = 0 ...} 
            percent = self._component_percent.get(name, Decimal(0))
            gaihi_dic['reg1-4-1'] = hantei(d, percent)

        return gaihi_dic



class Reg2_35_3(IJudgmentGaihi):
    '''
    トリブチルスズ化合物
    '''

    def __init__(self, reg_dic: Dict, 
                 brokendown_composition: Dict[str, Decimal])-> None:
        '''
        {'composit1': {'hinban': 'G-DI-PN', '含有': 0.0003, 'name': 
        'トリブチルスズ化合物', 'threshold': {'対象外': 'x == 0', 
        '非': 'x > 0 and x < 0.05', '該': 'x >= 0.05'}}
        '''
        self._reg_dic: Dict = reg_dic
        self._composition: Dict[str,Decimal] = brokendown_composition
        self._component_percent: Dict[str, Decimal] = self.get_component_percent()
        self._gaihi: Dict[str, str] = self.judgment_gaihi()

        print(self._component_percent)
        print(self._gaihi)


    def get_component_percent(self) -> Dict[str, Decimal]:
        component_percent: Dict[str, Decimal] = {}
        for _, val in self._reg_dic.items():
            hinban = val['hinban'] # G-DI-PN
            name = val['name'] # トリブチルスズ化合物
            component_percent[name] = \
                self._composition.get(hinban, Decimal(0)) \
                                * Decimal(100) * Decimal(0.0003)

        return component_percent


    def judgment_gaihi(self) -> Dict[str, str]:
        gaihi_dic = {}
        for _, val in self._reg_dic.items():
            name = val['name'] # トリブチルスズ化合物
            d = val['threshold'] # {'対象外': 'x = 0 ...} 
            percent = self._component_percent.get(name, Decimal(0))
            gaihi_dic['reg2-35-3'] = hantei(d, percent)

        return gaihi_dic

