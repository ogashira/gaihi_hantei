from abc import ABC, abstractmethod 
from decimal import Decimal
from typing import Dict
from decimal import Decimal, ROUND_UP
import math
import win32com.client
from gaihi_hantei import hantei


def put_maru_on_該_or_非(ws, cell_address: str, 
                                            gaihi: str) -> None:
        # cell_address = H39 など
        # gaihi = '該' など

        ''' セルからの移動pxを設定'''
        to_right: int = 0
        to_down: int = 0
        if gaihi == '該':
            to_right = 13
            to_down = -1

        if gaihi == '非':
            to_right = 55
            to_down = -1

        # ※位置やサイズをいったん「0」や「-1（元のサイズ）」で仮置きします
        shape_path = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\200. effit_data\ﾏｽﾀ\該非判定書自動作成関連\ﾌｫｰﾏｯﾄ\maru.png'
        shape = ws.Shapes.AddPicture(shape_path, LinkToFile=False, SaveWithDocument=True, Left=0, Top=0, Width=-1, Height=-1)

        # 5. 画像の位置やサイズを調整する
        # 例：D5セルの位置にぴったり合わせる場合
        target_cell = ws.Range(cell_address)
        shape.Left = target_cell.Left + to_right   # セルの左端から5ポイント右へ移動
        shape.Top = target_cell.Top + to_down     # セルの上端から5ポイント下へ移動
        # サイズを変更したい場合（アスペクト比を維持する場合は片方だけ調整）
        #shape.LockAspectRatio = True        # 縦横比を固定
        #shape.Width = 30                   # 横幅を150ポイントに設定（縦は自動調整されます）

def put_daen_on_35_3(ws, cell_address: str)-> None:
        # ※位置やサイズをいったん「0」や「-1（元のサイズ）」で仮置きします
        shape_path = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\200. effit_data\ﾏｽﾀ\該非判定書自動作成関連\ﾌｫｰﾏｯﾄ\daen.png'
        shape = ws.Shapes.AddPicture(shape_path, LinkToFile=False, SaveWithDocument=True, Left=0, Top=0, Width=-1, Height=-1)

        # 5. 画像の位置やサイズを調整する
        # 例：D5セルの位置にぴったり合わせる場合
        target_cell = ws.Range(cell_address)
        shape.Left = target_cell.Left + 67   # セルの左端から5ポイント右へ移動
        shape.Top = target_cell.Top + (-2)     # セルの上端から5ポイント下へ移動


def round_up_significant_digits(x: Decimal, digits: int = 3) -> Decimal:
    '''
    有効桁数を指定して、指定した桁の有効桁に丸める
    '''
    if x == 0:
        return Decimal('0')
    
    # 0より大きい正の数を想定
    # 最上位の桁の位置（10の何乗か）を計算
    # 例: 35.3456 -> 1 (10^1の位), 0.0002343422 -> -4 (10^-4の位)
    exponent = math.floor(math.log10(abs(x)))
    
    # 丸めたい位置の単位を計算
    # 例: 35.3456 で有効3桁なら、10^(1 - 3 + 1) = 10^-1 = 0.1 の位で丸める
    # 例: 0.0002343422 なら、10^(-4 - 3 + 1) = 10^-6 = 0.000001 の位で丸める
    target_unit = Decimal(10) ** (exponent - digits + 1)
    
    # quantizeで切り上げを実行
    return x.quantize(target_unit, rounding=ROUND_UP)


def put_substance_name_and_percent(ws, cell_addresses, component_percent)-> None:
    substance_name_col = int(cell_addresses['substance_name_col'])
    substance_percent_col = int(cell_addresses['substance_percent_col'])
    substance_row = int(cell_addresses['substance_row'])

    for substance_key, substance_val in component_percent.items():
        if substance_val <= Decimal(0): # 含有量が0の場合は、スルー
            continue

        # 化学物質名と含有量を入力
        row = substance_row
        while True:
            name_cell = ws.Cells(row, substance_name_col)
            percent_cell = ws.Cells(row, substance_percent_col)
            
            # セルの値を取得
            cell_val = name_cell.Value
            
            # 値が None または 空文字（スペースを除いた状態）か判定
            if cell_val is None or str(cell_val).strip() == "":
                # 空のセルが見つかったので substance_name を入力
                name_cell.Value = substance_key
                percent_cell.Value = "< " + str(round_up_significant_digits(substance_val, 3))
                # 目的を達成したので while ループを抜ける
                break
                
            # データが入っていた場合は、次の行（1つ下）へ進む
            row += 1


def put_on_higaitou_nagase(substance: str, percent: Decimal, 
                           higai_set: Dict[str, int],
                           ws: object) -> None:

    stt_row = higai_set['higai_stt_row']
    last_row = higai_set['higai_last_row']
    substance_col = higai_set['higai_col']
    percent_col = higai_set['higai_percent_col']

    if percent <= Decimal('0'):
        return

    i = stt_row
    # セルにデータが入っていてlast_rowより小さい間は場合はrowをインクリ
    while ws.Cells(i, substance_col).Value is not None and i < last_row:
        i += 1

    up_percent = round_up_significant_digits(percent, 3)
    ws.Cells(i, substance_col).Value = substance
    ws.Cells(i, percent_col).Value = "< " + str(up_percent)


def put_on_gaitou_nagase(substance: str, percent: Decimal, 
                         gai_set: Dict[str, int], ws: object, 
                         koumoku: str)-> None:

    stt_row = gai_set['gai_stt_row']
    last_row = gai_set['gai_last_row']
    col = gai_set['gai_col']

    i = stt_row
    # セルにデータが入っていてlast_rowより小さい間は場合はrowをインクリ
    while ws.Cells(i, col).Value is not None and i < last_row:
        i += 1

    up_percent = round_up_significant_digits(percent, 3)
    txt = f'{koumoku}  ({substance}  < {up_percent}%)'
    ws.Cells(i, col).Value = txt


def put_on_gaitou_or_higaitou_nagase(substance: str, percent: Decimal, 
                                     gai_set: Dict[str,int], 
                                     higai_set: Dict[str, int], ws: object,
                                     koumoku: str, reg_dic: Dict)-> None:


    threshold_gaitou_over: float = int(reg_dic[substance]['threshold_gaitou_over'])
    if percent <= Decimal('0'):
        return
    if percent >= Decimal(threshold_gaitou_over):
        # 50以上の場合は、該当欄に入力する
        put_on_gaitou_nagase(substance, percent, gai_set, ws, koumoku)
        return

    # 0以下でも50以上でもない場合
    put_on_higaitou_nagase(substance, percent, higai_set, ws)
    return


class IJudgmentGaihi(ABC):

    @abstractmethod
    def get_component_percent(self) -> Dict[str, Decimal]:
        pass

    @abstractmethod
    def judgment_gaihi(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def input_to_excel_toyotu(self, ws, cell_addresses: Dict[str, str]) -> None:
        pass

    @abstractmethod
    def input_to_excel_nagase(self, ws, cell_addresses: Dict[str, str]) -> None:
        pass


class Reg2_21_3(IJudgmentGaihi):
    '''
    トルエン、MEK
    '''
    def __init__(self, reg_dic: Dict, 
                 brokendown_composition: Dict[str, Decimal])-> None:
        '''
        reg_dic = 
        {'トルエン': {'hinban': 'G-TOL', 'name': 'トルエン', 'threshold': 
        {'対象外': 'x == 0', '非': 'x > 0 and x < 50', '該': 'x >= 50 and x <= 100'},
        'threshold_gaitou_over': "50"}, 
        'エチルメチルケトン': {'hinban': 'G-MEK', 'name': 'エチルメチルケトン', 'threshold': 
        {'対象外': 'x == 0', '非': 'x > 0 and x < 50', '該': 'x >= 50'},
        'threshold_gaitou_over': "50"}
        '''
        self._reg_dic: Dict = reg_dic
        self._composition: Dict[str,Decimal] = brokendown_composition
        self._component_percent: Dict[str, Decimal] = self.get_component_percent()
        self._gaihi: Dict[str, str] = self.judgment_gaihi()

        print(self._component_percent)
        # {'トルエン': Decimal('43.47772137248343989458942229'), 'エチルメチルケトン': Decimal('0')}
        print(self._gaihi)
        # {'reg2-21-3': '非'}
        

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


    def input_to_excel_toyotu(self, ws, 
                              cell_addresses: Dict[str, str]) -> None:

        if self._gaihi['reg2-21-3'] == '対象外':
            ws.Range(cell_addresses['not_reg2-21-3']).Value = "◯"
            return

        # 該または非の上に◯を置く
        cell_address: str = cell_addresses['reg2-21-3'] # H39
        gaihi = self._gaihi['reg2-21-3']
        put_maru_on_該_or_非(ws, cell_address, gaihi)

        # 化学物質名と含有量を入力
        put_substance_name_and_percent(ws, cell_addresses, self._component_percent)


    def input_to_excel_nagase(self, ws, 
                              cell_addresses: Dict[str, str]) -> None:

        if self._gaihi['reg2-21-3'] == '対象外':
            return

        gai_set: Dict[str, int] = {
            'gai_stt_row': int(cell_addresses['gaitou_kouban_row']),
            'gai_col': int(cell_addresses['gaitou_kouban_col']),
            'gai_last_row': int(cell_addresses['gaitou_kouban_last_row'])
        }

        higai_set: Dict[str, int] = {
            'higai_stt_row': int(cell_addresses['higaitou_substance_row']),
            'higai_col': int(cell_addresses['higaitou_substance_col']),
            'higai_last_row': int(cell_addresses['higaitou_substance_last_row']),
            'higai_percent_col': int(cell_addresses['higaitou_percent_col'])
        }

        for substance, percent in self._component_percent.items():
            if self._gaihi['reg2-21-3'] == '該':
                # 該の場合の入力はpercentによって該当欄か非該当欄かに分かれる
                put_on_gaitou_or_higaitou_nagase(substance, percent, 
                                                 gai_set, higai_set, 
                                                 ws, '別表2-21-3 ',
                                                 self._reg_dic)
                continue

            if self._gaihi['reg2-21-3'] == '非':
                put_on_higaitou_nagase(substance, percent, higai_set, ws)


class Reg1_4_6(IJudgmentGaihi):
    '''
    ミサイル（ポリブタ）
    '''

    def __init__(self, reg_dic: Dict, 
                 brokendown_composition: Dict[str, Decimal])-> None:
        '''
        reg_dic = 
        {'末端に水酸基を有するポリブタジエン': {'hinban': 
        ['G-G-2000', 'G-G-3000', 'G-T-4000', 'G-TP-2000'], 
        'name': '末端に水酸基を有するポリブタジエン', 'threshold': 
        {'対象外': 'x == 0', '非': 'x > 0 and x <= 100', '該': 'False'},
        'threshold_gaitou_over': "101"}
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
            gaihi_dic['reg1-4-6'] = hantei(d, percent)

        return gaihi_dic

    def input_to_excel_toyotu(self, ws, 
                              cell_addresses: Dict[str, str]) -> None:
        if self._gaihi['reg1-4-6'] == '対象外':
            ws.Range(cell_addresses['not_reg1-4-6']).value = "◯"
            return

        # 該または非の上に◯を置く
        cell_address: str = cell_addresses['reg1-4-6'] # H29
        gaihi = self._gaihi['reg1-4-6']
        put_maru_on_該_or_非(ws, cell_address, gaihi)
        # 化学物質名と含有量を入力
        put_substance_name_and_percent(ws, cell_addresses, self._component_percent)


    def input_to_excel_nagase(self, ws, 
                              cell_addresses: Dict[str, str]) -> None:

        if self._gaihi['reg1-4-6'] == '対象外':
            return

        gai_set: Dict[str, int] = {
            'gai_stt_row': int(cell_addresses['gaitou_kouban_row']),
            'gai_col': int(cell_addresses['gaitou_kouban_col']),
            'gai_last_row': int(cell_addresses['gaitou_kouban_last_row'])
        }

        higai_set: Dict[str, int] = {
            'higai_stt_row': int(cell_addresses['higaitou_substance_row']),
            'higai_col': int(cell_addresses['higaitou_substance_col']),
            'higai_last_row': int(cell_addresses['higaitou_substance_last_row']),
            'higai_percent_col': int(cell_addresses['higaitou_percent_col'])
        }

        for substance, percent in self._component_percent.items():
            if self._gaihi['reg1-4-6'] == '該':
                # 該の場合の入力はpercentによって該当欄か非該当欄かに分かれる
                put_on_gaitou_or_higaitou_nagase(substance, percent, 
                                                 gai_set, higai_set, 
                                                 ws, '別表1-4-6 ', 
                                                 self._reg_dic)
                continue

            if self._gaihi['reg1-4-6'] == '非':
                put_on_higaitou_nagase(substance, percent, higai_set, ws)


    
    
class Reg2_35_3(IJudgmentGaihi):
    '''
    トリブチルスズ化合物
    '''

    def __init__(self, reg_dic: Dict, 
                 brokendown_composition: Dict[str, Decimal])-> None:
        '''
        {'トリブチルスズ化合物': {'hinban': 'G-DI-PN', '含有': 0.0003, 'name': 
        'トリブチルスズ化合物', 'threshold': {'対象外': 'x == 0', 
        '非': 'x > 0 and x < 0.05', '該': 'x >= 0.05'},
        'threshold_gaitou_over': "0.05"}
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

    def input_to_excel_toyotu(self, ws, 
                              cell_addresses: Dict[str, str]) -> None:
        if self._gaihi['reg2-35-3'] == '対象外':
            ws.Range(cell_addresses['not_reg2-35-3']).value = "◯"
            return

        # 該または非の上に◯を置く
        cell_address: str = cell_addresses['reg2-35-3'] # H41
        gaihi = self._gaihi['reg2-35-3'] # 該または非
        put_maru_on_該_or_非(ws, cell_address, gaihi)

        # 35の3項の上に楕円を置く
        cell_address: str = "D40"
        put_daen_on_35_3(ws, cell_address)

        # 化学物質名と含有量を入力
        put_substance_name_and_percent(ws, cell_addresses, self._component_percent)

    
    def input_to_excel_nagase(self, ws, 
                              cell_addresses: Dict[str, str]) -> None:

        if self._gaihi['reg2-35-3'] == '対象外':
            return

        gai_set: Dict[str, int] = {
            'gai_stt_row': int(cell_addresses['gaitou_kouban_row']),
            'gai_col': int(cell_addresses['gaitou_kouban_col']),
            'gai_last_row': int(cell_addresses['gaitou_kouban_last_row'])
        }

        higai_set: Dict[str, int] = {
            'higai_stt_row': int(cell_addresses['higaitou_substance_row']),
            'higai_col': int(cell_addresses['higaitou_substance_col']),
            'higai_last_row': int(cell_addresses['higaitou_substance_last_row']),
            'higai_percent_col': int(cell_addresses['higaitou_percent_col'])
        }

        for substance, percent in self._component_percent.items():
            if self._gaihi['reg2-35-3'] == '該':
                # 該の場合の入力はpercentによって該当欄か非該当欄かに分かれる
                put_on_gaitou_or_higaitou_nagase(substance, percent, 
                                                 gai_set, higai_set, 
                                                 ws, '別表2-35-3 ',
                                                 self._reg_dic)
                continue

            if self._gaihi['reg2-35-3'] == '非':
                put_on_higaitou_nagase(substance, percent, higai_set, ws)
