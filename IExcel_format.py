import subprocess
from typing import Dict, List
from abc import ABC, abstractmethod
import win32com.client
import datetime

from IJudgment_gaihi import IJudgmentGaihi


class IExcelFormat(ABC):

    @abstractmethod
    def input_to_excel_format(self)-> None:
        pass

    @abstractmethod
    def save_file(self)-> None:
        pass


class ToyotuFormat(IExcelFormat):

    def __init__(self, dic_info: Dict[str, str], 
                                regs: List[IJudgmentGaihi]) -> None:

        '''Excelフォーマットの入力セルのアドレス'''
        self._cell_addresses: Dict[str, str] = {}
        self._cell_addresses['date'] = 'G1'
        self._cell_addresses['atena'] = 'A2'
        self._cell_addresses['display_name'] = 'B9'
        self._cell_addresses['reg1-4-1'] = 'H29'
        self._cell_addresses['not_reg1-4-1'] = 'I29'
        self._cell_addresses['reg2-21-3'] = 'H39'
        self._cell_addresses['not_reg2-21-3'] = 'I39'
        self._cell_addresses['reg2-35-3'] = 'H41'
        self._cell_addresses['not_reg2-35-3'] = 'I41'
        self._cell_addresses['substance_name_cols'] = '1'
        self._cell_addresses['substance_percent_cols'] = '8'
        self._cell_addresses['substance_rows'] = '51'

        self._dic_info: Dict[str, str] = dic_info
        self._regs: List[IJudgmentGaihi] = regs

        self._excel_app = None
        self._wb = None
        self._ws = None
        self._pid = None


        try:
            # DispatchEx により既存のExcelとは別の新しい独立プロセスを起動
            self._excel_app = win32com.client.DispatchEx("Excel.Application")
            self._excel_app.Visible = False
            self._excel_app.DisplayAlerts = False  # アラートを非表示

            path = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\200. effit_data\ﾏｽﾀ\該非判定書自動作成関連\ﾌｫｰﾏｯﾄ\toyotu.xlsx'
            self._wb = self._excel_app.Workbooks.Open(path)
            self._ws = self._wb.sheets("toyotu")  # 1番目のシート
        except Exception as e:
            print(f"Excelフォーマットの立ち上げでエラーが発生しました: {e}")
            self._kill_processes()



    def input_to_excel_format(self) -> None:
        # 年月日とあて名と商品名を入力
        self._ws.Range(self._cell_addresses['date']).Value = \
                                               self._dic_info['date']
        self._ws.Range(self._cell_addresses['atena']).Value = \
                                               self._dic_info['addr']
        self._ws.Range(self._cell_addresses['display_name']).Value = \
                                               self._dic_info['display_name']

        # 以降はIJudgmentGaihiクラスに任せる
        for reg in self._regs:
            reg.input_to_excel_format(self._ws, self._cell_addresses)


    def save_file(self) -> None:
        '''excel_fileを保存'''

        today: str = datetime.datetime.today().strftime('%Y%m%d')
        try:
            path = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\40. 輸出関係\70.該非判定書類\1.自動作成\自動作成_for_python\excel_files'
            file = fr'{path}\toyotu_{self._dic_info["hinban"]}_{today}.xlsx'
            self._wb.SaveAs(file, FileFormat=51) # 51:xlsx

            pdf_path = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\40. 輸出関係\70.該非判定書類\1.自動作成\自動作成_for_python\pdf_files'
            pdf_file = fr'{pdf_path}\toyotu_{self._dic_info["hinban"]}_{today}.pdf'
            self._ws.ExportAsFixedFormat(Type = 0,   # 0 = PDF
                                         Filename = pdf_file, 
                                         Quality = 0, # 0 = standard
                                         IncludeDocProperties = True,
                                         IgnorePrintAreas = False,
                                         OpenAfterPublish=False)
            print()
            print("PDFへの変換が完了しました！")
        finally:
            self._kill_processes()


    def _kill_processes(self) -> None:
        if self._wb is not None:
            self._wb.Close(SaveChanges=False)

        if self._excel_app is not None:
            self._excel_app.Quit()

        self._ws = None
        self._wb = None
        self._excel_app = None

class NagaseFormat(IExcelFormat):

    def __init__(self, dic_info: Dict[str, str], 
                                regs: List[IJudgmentGaihi]) -> None:
        pass

    def input_to_excel_format(self) -> None:
        pass

    def save_file(self) -> None:
        pass
