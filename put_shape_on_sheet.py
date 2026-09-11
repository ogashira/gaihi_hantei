from typing import Dict

def put_maru_on_該_or_非(ws, cell_addresses: Dict[str, str]) -> None:
        cell_address: str = cell_addresses['reg2-21-3'] # H39
        ''' H39からの移動pxを設定'''
        to_right: int = 0
        to_down: int = 0
        if self._gaihi['reg2-21-3'] == '該':
            to_right = 13
            to_down = -1

        if self._gaihi['reg2-21-3'] == '非':
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

