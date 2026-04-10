import tkinter as tk
import subprocess
import sys
from datetime import datetime  # 日付取得用
import yaml
from typing import Dict
import frow

def toggle_entry():
    # 状態を切り替え（Textウィジェットは "disabled" か "normal"）
    if radio_addr_var.get() == 1:
        text_addr.config(state="normal", bg="white")
    else:
        text_addr.config(state="disabled", bg="#f0f0f0")

def show_atena():
    with open('atena.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    atesaki = radio_fmt_var.get()
    atena = config['atena'][atesaki]

    if text_addr.cget("state") == "disabled":
        text_addr.config(state="normal")
        text_addr.delete("1.0", "end")
        text_addr.insert("1.0", atena)
        text_addr.config(state="disabled")
    else:
        text_addr.delete("1.0", "end")
        text_addr.insert("1.0", atena)


def launch_sub():
    # 各入力値を取得
    pno = entry_pno.get()
    date = entry_date.get()
    fmt = radio_fmt_var.get()
    # Textウィジェットからの取得は "1.0"（1行目の0文字目）から "end-1c"（最後から1文字前まで）
    addr = text_addr.get("1.0", "end-1c")
    
    data = f"品番:{pno},日付:{date},フォーマット:{fmt},宛名:{addr}"
    
    subprocess.Popen([sys.executable, "sub.py", data])
    root.destroy()


def launch_frow():
    dic_info: Dict = {}
    pno = entry_pno.get()
    date = entry_date.get()
    fmt = radio_fmt_var.get()
    # Textウィジェットからの取得は "1.0"（1行目の0文字目）から "end-1c"（最後から1文字前まで）
    addr = text_addr.get("1.0", "end-1c")

    dic_info['hinban'] = pno
    dic_info['date'] = date
    dic_info['format'] = fmt
    dic_info['addr'] = addr
    
    frow.start(dic_info)
    root.destroy()


def run_ui():
    global root, entry_pno, entry_date, radio_fmt_var, text_addr, radio_addr_var

    root = tk.Tk()
    root.title("該非判定書自動作成")
    root.geometry("450x550") # 高さを少し広げました

    # --- 1. 基本情報入力エリア ---
    frame_basic = tk.LabelFrame(root, text="基本情報", padx=10, pady=10)
    frame_basic.pack(padx=20, pady=10, fill="x")

    # 品番
    tk.Label(frame_basic, text="品番:").grid(row=0, column=0, sticky="e", pady=5)
    entry_pno = tk.Entry(frame_basic, width=30)
    entry_pno.grid(row=0, column=1, padx=10, pady=5)

    # 作成日（今日の日付をデフォルト挿入）
    tk.Label(frame_basic, text="作成日:").grid(row=1, column=0, sticky="e", pady=5)
    entry_date = tk.Entry(frame_basic, width=30)
    entry_date.grid(row=1, column=1, padx=10, pady=5)

    today = datetime.now().strftime("%Y/%m/%d") # 今日の日付を取得
    entry_date.insert(0, today) # 入力欄の先頭(0)に挿入


    # --- 2. フォーマット選択エリア ---
    frame_fmt = tk.LabelFrame(root, text="フォーマット選択", padx=10, pady=10)
    frame_fmt.pack(padx=20, pady=10, fill="x")

    radio_fmt_var = tk.StringVar(value="toyotu")
    tk.Radiobutton(frame_fmt, text="豊通", variable=radio_fmt_var, value="toyotu", command=show_atena).pack(side="left", padx=20)
    tk.Radiobutton(frame_fmt, text="長瀬", variable=radio_fmt_var, value="nagase", command=show_atena).pack(side="left", padx=20)


    # --- 3. 宛名設定エリア ---
    frame_addr = tk.LabelFrame(root, text="宛名設定", padx=10, pady=10)
    frame_addr.pack(padx=20, pady=10, fill="x")

    radio_addr_var = tk.IntVar(value=0)
    sub_frame_radio = tk.Frame(frame_addr)
    sub_frame_radio.pack(fill="x")
    tk.Radiobutton(sub_frame_radio, text="変更無し", variable=radio_addr_var, value=0, command=toggle_entry).pack(side="left", padx=10)
    tk.Radiobutton(sub_frame_radio, text="変更あり", variable=radio_addr_var, value=1, command=toggle_entry).pack(side="left", padx=10)

    # 宛名入力欄（5行分の高さに設定）
    # height=5 で5行分、width=40 で幅を指定
    text_addr = tk.Text(frame_addr, height=5, width=40, state="disabled", bg="#f0f0f0")
    text_addr.pack(pady=10)


    # --- 実行ボタン ---
    btn_submit = tk.Button(root, text="該非判定書を作成する", command=launch_frow, 
                           bg="#2196F3", fg="white", font=("", 10, "bold"), pady=10)
    btn_submit.pack(pady=20, padx=20, fill="x")

    root.mainloop()

if __name__ == "__main__":
    run_ui()
