# 該非判定書自動作成アプリ
## システム概要
### 動作環境
- OS  
    - Windows11(pushd \\wsl$\Ubuntu\home\oga\projects\gaihi_hantei\main.py)
    - Linux(WSL)は不可（Tkinterを使っているため）
- インストール先
    - 和泉PC, 徳武PC
    - 尾頭PC(toyo-pc12) WSL2(Ubuntu)で開発
### 構築システム
- メインシステム: Python3.10
- Windowsスクリプト(gaihi.bat)
### ソースコード
GitHub Publicリポジトリで公開</br>
[GitHub_ https://github.com/ogashira/gaihi_hantei](https://github.com/ogashira/gaihi_hantei)
### 起動方法
##### soukoidou
- `Winボタン+R -> gaihi入力 -> Enter`または`pushd \\wsl$\Ubuntu\home\oga\projects\gaihi_hantei\`デイレクトリ内にて`python main.py`で実行
### 動作
#### GUI表示 「該非判定書自動作成」画面
- 品番、作成日を入力
- フォーマット選択（豊通 or 長瀬）
- フォーマットに応じて宛名が表示される。
- 「変更あり」ラジオボタンで宛先を修正できる
- 「該非判定書を作成する」をクリックでプログラムスタート
#### 配合計算
1. 製品 -> 缶 -> 仕掛かり品 -> GT品 -> 原料　に全て分解する
1. 原料分解表から、原料を更に分解する
#### 該非判定
##### Reg2_21_3
1. component_percent = {'トルエン': 25(%), 'エチルメチルケトン':10(%)} を求める
1. gaihi = {'reg2_21_3': '非'} を求める
##### Reg1_4_1
1. component_percent = {'末端に水酸基を有するポリブタジエン': 25(%)} を求める
1. gaihi = {'reg1_4_1': '非'} を求める
##### Reg2_35_3
1. component_percent = {'トリブチルスズ化合物': 25(%)} を求める
1. gaihi = {'reg2_35_3': '非'} を求める
### クラス図
```mermaid
---
title: インスタンス生成
---
classDiagram
direction LR 

class Main{
    + main()None
}
class Flow{
    + start()None
}
class InstanceFactory{
    - _sqlServerTss: Any
    - _sqlServerEffit: Any
    - _cnxn_tss
    - _cnxn_effit
    - _instances: Dict~str,Any
    + _setup_sql_path()None*
    + get_instance()instance*
}
class IFetchDataForList{
    <<interface>>
    + fetch_data()List~List~Any~~*
}
class FetchHinban{
    - cnxn
    + fetch_data()List~List~Any~~
}
class FetchPs{
    - cnxn
    + fetch_data()List~List~Any~~
}
class FetchComponentBreakdown{
    - cnxn
    + fetch_data()List~List~Any~~
}
Main --> Flow
Flow --> InstanceFactory
InstanceFactory --> IFetchDataForList
IFetchDataForList <|.. FetchHinban
IFetchDataForList <|.. FetchPs
IFetchDataForList <|.. FetchComponentBreakdown
```
```mermaid
---
title: 成分分解
---
classDiagram
direction TB:w
class Main{
    + main()None
}
class Flow{
    + start()None
}
class IComposition{
    <<interface>>
    + show_composition()None*
    + insert_compositon_to_list(List~List~Any~~)None*
    + breakdown_composition(Dict[str,Dict[str,Decimal]], Dict[str, Decimal])None*
}
class Seihin{
    - hinban:str
    - tnju:Decimal
    - hinmoku1:Dict[str,str]
    - tani:Dict[str,str]
    - ps:Dict[str,Dict[str,Decimal]]
    - breakdown:Dict[str,Dict[str,Decimal]]
    - composits:List[IComposition]
    + show_composition()None
    + insert_compositon_to_list(List~List~Any~~)None
    + breakdown_composition(Dict[str,Dict[str,Decimal]], Dict[str, Decimal])None
    - _get_composits(Dict)List~IComposition~
}
class Can{
    - hinban: str
    - parent_hinban:str
    - qty: int
    + show_composition()None
    + insert_compositon_to_list(List~List~Any~~)None
    + breakdown_composition(Dict[str,Dict[str,Decimal]], Dict[str, Decimal])None
}
class Sikakari{
    - hinban:str
    - parent_hinban:str
    - net: Decimal
    - hinban_tani: Dict[str, str]
    - ps:Dict[str,Dict[str,Decimal]]
    - breakdown:Dict[str,Dict[str,Decimal]]
    - ratio:Decimal
    - composits:List~IComposition~
    + show_composition()None
    + insert_compositon_to_list(List~List~Any~~)None
    + breakdown_composition(Dict[str,Dict[str,Decimal]], Dict[str, Decimal])None
    - _calc_total(Dict)Decimal
    - _get_composits(Dict)List~IComposition~
}
class Gt{
    - hinban:str
    - parent_hinban:str
    - hinban_tani:Dict[str,str]
    - ps:Dict[str,Dict[str,Decimal]]
    - breakdown:Dict[str,Dict[str,Decimal]]
    - net:Decimal
    - ratio:Decimal
    - composits:List~IComposition~
    + show_composition()None
    + insert_compositon_to_list(List~List~Any~~)None
    + breakdown_composition(Dict[str,Dict[str,Decimal]], Dict[str, Decimal])None
    - _calc_total(Dict)Decimal
    - _get_composits(Dict)List~IComposition~
}
class Genryou{
    - hinban:str
    - parent_hinban:str
    - qty:Decimal
    - breakdown:Dict[str,Dict[str,Decimal]]
    - qty_per_net:Decimal
    + show_composition()None
    + insert_compositon_to_list(List~List~Any~~)None
    + breakdown_composition(Dict[str,Dict[str,Decimal]], Dict[str, Decimal])None
}
Main --> Flow
Flow --> IComposition
IComposition <|.. Seihin
IComposition <|.. Can
IComposition <|.. Sikakari
IComposition <|.. Gt
IComposition <|.. Genryou
Seihin "1" o-- "1" Sikakari
Seihin "1" o-- "1" Can
Sikakari "1" o-- "1..n" Gt
Sikakari "1" o-- "1..n" Genryou
Gt "1" o-- "1..n" Gt
Gt "1" o-- "1..n" Genryou
```

```mermaid
---
title: 該非判定
---
classDiagram
direction TB 

class Main{
    + main()None
}
class Flow{
    + start()None
}
class InstanceFactory{
    - _sqlServerTss: Any
    - _sqlServerEffit: Any
    - _cnxn_tss
    - _cnxn_effit
    - _instances: Dict~str,Any
    + _setup_sql_path()None*
    + get_instance()instance*
}
class IJudgmentGaihi{
    <<interface>>
    + get_component_percent()Dict[str,Decimal]*
    + judgment_gaihi()Dict[str,str]*
    + input_to_excel_format()None*
}
class Reg2_21_3{
    - reg_dic:Dict
    - composition:Dict[str,Decimal]
    - component_percent:Dict[str,Decimal]
    - gaihi:Dict[str,str]
    + get_component_percent()Dict[str,Decimal]*
    + judgment_gaihi()Dict[str,str]*
    + input_to_excel_format()None
}
class Reg1_4_1{
    - reg_dic:Dict
    - composition:Dict[str,Decimal]
    - component_percent:Dict[str,Decimal]
    - gaihi:Dict[str,str]
    + get_component_percent()Dict[str,Decimal]*
    + judgment_gaihi()Dict[str,str]*
    + input_to_excel_format()None
}
class Reg2_35_3{
    - reg_dic:Dict
    - composition:Dict[str,Decimal]
    - component_percent:Dict[str,Decimal]
    - gaihi:Dict[str,str]
    + get_component_percent()Dict[str,Decimal]*
    + judgment_gaihi()Dict[str,str]*
    + input_to_excel_format()None
}
class IExcelFormat{
    <<interface>>
    + input_to_excel_format()*
}
class ToyotuFormat{
    - dic_info: Dict[str, str]
    - regs: List~IJudgmentGaihi~
    + input_to_excel_format()None
}
class NagaseFormat{
    - dic_info: Dict[str, str]
    - regs: List~IJudgmentGaihi~
    + input_to_excel_format()None
}
Main --> Flow
Flow --> InstanceFactory
InstanceFactory --> IJudgmentGaihi
InstanceFactory --> IExcelFormat
IJudgmentGaihi <|.. Reg2_21_3
IJudgmentGaihi <|.. Reg1_4_1
IJudgmentGaihi <|.. Reg2_35_3
IExcelFormat <|.. ToyotuFormat
IExcelFormat <|.. NagaseFormat
IExcelFormat o-- IJudgmentGaihi
```
