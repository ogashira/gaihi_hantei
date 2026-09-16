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
        self._cell_addresses['reg1-4-6'] = 'H29'
        self._cell_addresses['not_reg1-4-6'] = 'I29'
        self._cell_addresses['reg2-21-3'] = 'H39'
        self._cell_addresses['not_reg2-21-3'] = 'I39'
        self._cell_addresses['reg2-35-3'] = 'H41'
        self._cell_addresses['not_reg2-35-3'] = 'I41'
        self._cell_addresses['substance_name_col'] = '1'
        self._cell_addresses['substance_percent_col'] = '8'
        self._cell_addresses['substance_row'] = '51'

        self._dic_info: Dict[str, str] = dic_info
        self._regs: List[IJudgmentGaihi] = regs

        self._excel_app = None
        self._wb = None
        self._ws = None
        self._pid = None


        try:
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
            reg.input_to_excel_toyotu(self._ws, self._cell_addresses)


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
        
        '''Excelフォーマットの入力セルのアドレス'''
        self._cell_addresses: Dict[str, str] = {}
        self._cell_addresses['date'] = 'T1'
        self._cell_addresses['atena1'] = 'A2'
        self._cell_addresses['atena2'] = 'A3'
        self._cell_addresses['atena3'] = 'A4'
        self._cell_addresses['atena4'] = 'A5'
        self._cell_addresses['display_name'] = 'J19'
        self._cell_addresses['check_box_gaitou'] = 'B23'
        self._cell_addresses['check_box_higaitou'] = 'B27'
        self._cell_addresses['check_box_taisyougai'] = 'C29'
        self._cell_addresses['check_box_higaitou_percent'] = 'C31'

        self._cell_addresses['gaitou_kouban_row'] = '23'
        self._cell_addresses['gaitou_kouban_col'] = '8'
        self._cell_addresses['gaitou_kouban_last_row'] = '26'

        self._cell_addresses['higaitou_substance_row'] = '33'
        self._cell_addresses['higaitou_substance_col'] = '8'
        self._cell_addresses['higaitou_substance_last_row'] = '36'

        self._cell_addresses['higaitou_percent_row'] = '33'
        self._cell_addresses['higaitou_percent_col'] = '18'
        self._cell_addresses['higaitou_percent_last_row'] = '36'
        '''
        check_boxにcheckを入れる条件
        True => 文字が入力されている
        False => 文字が入力されていない（空白）
        H23=False and H33=False -> C29 checked, B27 checked
        H23=False and H33= True -> C31 checked, B27 checked
        H23= True and H33=False -> B23 checked
        H23= True and H33= True -> C31 checked, B23 checked
        '''

        self._dic_info: Dict[str, str] = dic_info
        self._regs: List[IJudgmentGaihi] = regs

        self._excel_app = None
        self._wb = None
        self._ws = None
        self._pid = None


        try:
            self._excel_app = win32com.client.DispatchEx("Excel.Application")
            self._excel_app.Visible = False
            self._excel_app.DisplayAlerts = False  # アラートを非表示

            path = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\200. effit_data\ﾏｽﾀ\該非判定書自動作成関連\ﾌｫｰﾏｯﾄ\nagase.xlsx'
            self._wb = self._excel_app.Workbooks.Open(path)
            self._ws = self._wb.sheets("nagase")  # 1番目のシート
        except Exception as e:
            print(f"Excelフォーマットの立ち上げでエラーが発生しました: {e}")
            self._kill_processes()


    def _check_to_checkbox(self, row: int, col: int) -> None:
        # チェックボックスにチェックを入れる
        self._ws.Cells(row, col).Value = 1 #1=オン
        # セルに入った1の文字を透明にする
        self._ws.Cells(row, col).NumberFormatLocal = ";;;"

    def _check_to_checkboxes(self) -> None:
        # チェックボックスにチェックを入れる
        '''
        H23=False and H33=False -> C29 checked, B27 checked
        H23=False and H33= True -> C31 checked, B27 checked
        H23= True and H33=False -> B23 checked
        H23= True and H33= True -> C31 checked, B23 checked
        '''
        
        gaitou_row: int = int(self._cell_addresses['gaitou_kouban_row'])
        gaitou_col: int = int(self._cell_addresses['gaitou_kouban_col'])
        higaitou_row: int = int(self._cell_addresses['higaitou_substance_row'])
        higaitou_col: int = int(self._cell_addresses['higaitou_substance_col'])

        checkbox_c29_row: int = 29
        checkbox_c31_row: int = 31
        checkbox_b23_row: int = 23
        checkbox_b27_row: int = 27
        checkbox_b_col: int = 2
        checkbox_c_col: int = 3

        if (self._ws.Cells(gaitou_row, gaitou_col).Value is None and
            self._ws.Cells(higaitou_row, higaitou_col).Value is None):
            # c29, b27チェックボックスにチェックを入れる
            self._check_to_checkbox(checkbox_c29_row, checkbox_c_col)
            self._check_to_checkbox(checkbox_b27_row, checkbox_b_col)
            return

        if (self._ws.Cells(gaitou_row, gaitou_col).Value is None and
            self._ws.Cells(higaitou_row, higaitou_col).Value is not None):
            # c31, b27チェックボックスにチェックを入れる
            self._check_to_checkbox(checkbox_c31_row, checkbox_c_col)
            self._check_to_checkbox(checkbox_b27_row, checkbox_b_col)
            return
        
        if (self._ws.Cells(gaitou_row, gaitou_col).Value is not None and
            self._ws.Cells(higaitou_row, higaitou_col).Value is None):
            # b23チェックボックスにチェックを入れる
            self._check_to_checkbox(checkbox_b23_row, checkbox_b_col)
            return

        if (self._ws.Cells(gaitou_row, gaitou_col).Value is not None and
            self._ws.Cells(higaitou_row, higaitou_col).Value is not None):
            # c31, b23チェックボックスにチェックを入れる
            self._check_to_checkbox(checkbox_c31_row, checkbox_c_col)
            self._check_to_checkbox(checkbox_b23_row, checkbox_b_col)
            return


    def _remove_empty_row(self, stt_row: int, col: int, last_row: int) -> None:

        # 空白のセルを行ごと削除する
        def delete_row(row: int, col: int) -> None:
            if self._ws.Cells(row, col).Value is None:
                self._ws.Rows(row).Delete()

        # stt_rowの一つ下の行までを削除する(stt_rowは含まれない)
        for i in range(last_row, stt_row, -1):
            delete_row(i, col)


    def input_to_excel_format(self) -> None:
        # 年月日とあて名と商品名を入力
        self._ws.Range(self._cell_addresses['date']).Value = \
                                               self._dic_info['date']
        self._ws.Range(self._cell_addresses['display_name']).Value = \
                                               self._dic_info['display_name']

        addrs = self._dic_info['addr'].split('\n')
        for i, addr in enumerate(addrs):
            self._ws.Range(self._cell_addresses['atena'+str(i+1)]).Value = \
                                               addr

        # 以降はIJudgmentGaihiクラスに任せる
        for reg in self._regs:
            reg.input_to_excel_nagase(self._ws, self._cell_addresses)

        # チェックボックスにチェックを入れる
        self._check_to_checkboxes()

        # 空白のセルを行ごと削除する
        self._remove_empty_row(
                int(self._cell_addresses['higaitou_substance_row']),
                int(self._cell_addresses['higaitou_substance_col']),
                int(self._cell_addresses['higaitou_substance_last_row'])
        )

        self._remove_empty_row (
                int(self._cell_addresses['gaitou_kouban_row']),
                int(self._cell_addresses['gaitou_kouban_col']),
                int(self._cell_addresses['gaitou_kouban_last_row'])
        )



    def save_file(self) -> None:
        '''excel_fileを保存'''

        today: str = datetime.datetime.today().strftime('%Y%m%d')
        try:
            path = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\40. 輸出関係\70.該非判定書類\1.自動作成\自動作成_for_python\excel_files'
            file = fr'{path}\nagase_{self._dic_info["hinban"]}_{today}.xlsx'
            self._wb.SaveAs(file, FileFormat=51) # 51:xlsx

            pdf_path = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\40. 輸出関係\70.該非判定書類\1.自動作成\自動作成_for_python\pdf_files'
            pdf_file = fr'{pdf_path}\nagase_{self._dic_info["hinban"]}_{today}.pdf'
            self._ws.ExportAsFixedFormat(Type = 0,   # 0 = PDF
                                         Filename = pdf_file, 
                                         Quality = 0, # 0 = standard
                                         IncludeDocProperties = True,
                                         IgnorePrintAreas = False,
                                         OpenAfterPublish=False)
            print()
            print("PDFへの変換が完了しました！")
        except Exception as e:
            print(f"ファイル保存時でエラー: {e}")
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
