import json

with open('dados_eleicao.js', 'r', encoding='utf-8') as f:
    content = f.read()
    raw_json = content.split('=', 1)[1].strip().rstrip(';')
    data = json.loads(raw_json)

jb_lead_idx = next(i for i, r in enumerate(data) if r['jp'] > r['lp'])
max_jb_idx = min(range(len(data)), key=lambda i: data[i]['lv'] - data[i]['jv'])
virada_idx = next(i for i in range(max_jb_idx, len(data)) if data[i]['lp'] > data[i]['jp'])
lead_1m_idx = next(i for i in range(virada_idx, len(data)) if (data[i]['lv'] - data[i]['jv']) >= 1000000)
lead_2m_idx = next(i for i in range(virada_idx, len(data)) if (data[i]['lv'] - data[i]['jv']) >= 2000000)
end_idx = len(data) - 1

milestones = [
    ('start', 0),
    ('jb_lead', jb_lead_idx),
    ('max_jb', max_jb_idx),
    ('virada', virada_idx),
    ('lead_1m', lead_1m_idx),
    ('lead_2m', lead_2m_idx),
    ('end', end_idx)
]

for name, idx in milestones:
    item = data[idx]
    t = item['t']
    p = item['p']
    lp = item['lp']
    jp = item['jp']
    dif = item['lv'] - item['jv']
    print(f"{name:10}: idx={idx:4} time={t} urnas={p:6.2f}% L={lp:6.2f}% JB={jp:6.2f}% dif={dif:+12,d}")

