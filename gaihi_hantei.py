'''
文字列をそのまま比較演算式、論理演算式にする

d = {'対象外': 'x == 0', '非': 'x > 0 and x < 50', '該': 'x >= 50'}

x = 含有量%
'''

def hantei(d, x):
    if eval(d['対象外']):
            return '対象外'
    elif eval(d['非']):
            return '非'
    elif eval(d['該']):     

            return '該'
    else:
            return 'nodata'
