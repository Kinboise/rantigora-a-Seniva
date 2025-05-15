import re

temp = '''
                <tr>
                    <td><code>{code}</code></td>
                    <td>{snv}</td>
                    <td>{han}</td>
                    <td>{count}</td>
                </tr>
'''
with open('Seniva.db', 'r', -1, 'utf-8') as f:
    text = f.read()

pat = r'\\nt 词源: ([A-Z]{3}([A-Z:]{4})?)|(新造)'
alllangs = [x[0] if x[0] != '' else x[2] for x in re.findall(pat, text)]
langs = list(set(alllangs))
langs.sort()

with open('zune.csv', 'r', -1, 'utf-8') as f:
    zunes = [x.strip().split(',') for x in f.readlines()]

diff = list(set(langs) - set([x[0] for x in zunes]))

if diff != []:
    with open('zune.csv', 'a', -1, 'utf-8') as f:
        f.write('\n,,'.join(diff))
else:
    dic = []
    for zune in zunes:
        if zune[0] == '新造':
            dic.append({
            'code': '-',
            'snv': '-',
            'han': '新造',
            'count': alllangs.count(zune[0])
            })
        else:
            dic.append({
                'code': zune[0].lower(),
                'snv': zune[1],
                'han': f'<u>{zune[2]}</u>语',
                'count': alllangs.count(zune[0])
            })
    data = ''
    dic.sort(key=lambda x: x['count'], reverse=True)
    for lang in dic:
        data += temp.format_map(lang)
    with open('template.html', 'r', -1, 'utf-8') as f:
        template = f.read()
    with open('about.html', 'w', -1, 'utf-8') as f:
        f.write(re.sub(r'\{data\}', data, template))