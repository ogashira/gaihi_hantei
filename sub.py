import sys

# 引数を受け取る (引数がない場合の対策も含む)
passed_text = sys.argv[1] if len(sys.argv) > 1 else "データがありません"

# ","で分割してリストへ
items = passed_text.split(",")
print(items)

# 辞書コンプレヘンションで展開
result_dict = {item.split(":", 1)[0]: item.split(":", 1)[1] for item in items}

print(result_dict)
