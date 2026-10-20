"""Gera dados_eleicao_2026.js a partir de votacao_secao_2026_BR.csv.

O CSV de 2026 traz os votos de cada seção eleitoral, mas NÃO informa quando
cada seção foi apurada (todas as linhas têm o mesmo horário de geração).
Por isso a "linha do tempo" de 2026 é uma reconstrução:

1. Os votos são agregados por seção (FB=22, L=13, outros, brancos=95, nulos=96).
2. As seções são ordenadas de duas formas:
   - 'csv': ordem de primeira aparição no arquivo;
   - 'regional': ordem SIMULADA (sorteio com semente fixa + peso por UF que
     imita a sequência típica de chegada dos estados em 2022).
3. Para cada um dos 5.286 passos de 2022, soma-se a mesma fração das seções
   de 2026, alinhando as duas eleições pelo % de seções apuradas.

Só o resultado final (100%) é real; a trajetória depende da ordem escolhida.
"""
import csv
import json
import os
import random

# Load 2022 data to align the 5286 percentage steps
with open('dados_eleicao.js', 'r', encoding='utf-8') as f:
    raw_2022 = f.read().split('=', 1)[1].strip().rstrip(';')
    data_2022 = json.loads(raw_2022)

print(f"Loaded {len(data_2022)} steps from 2022.")

# Read 2026 CSV and aggregate by section: (SG_UF, CD_MUNICIPIO, NR_ZONA, NR_SECAO)
# Value: [first_idx, last_idx, fb_votes, l_votes, outros_votes, brancos, nulos, uf]
sec_data = {}

with open('votacao_secao_2026_BR.csv', 'r', encoding='latin1') as f:
    reader = csv.reader(f, delimiter=';')
    header = next(reader)
    for idx, row in enumerate(reader):
        uf = row[10]
        key = (uf, row[13], row[15], row[16])
        nr = row[19]
        qt = int(row[21])
        if key not in sec_data:
            sec_data[key] = [idx, idx, 0, 0, 0, 0, 0, uf]
        else:
            sec_data[key][1] = idx

        if nr == '22':
            sec_data[key][2] += qt
        elif nr == '13':
            sec_data[key][3] += qt
        elif nr == '95':
            sec_data[key][5] += qt
        elif nr == '96':
            sec_data[key][6] += qt
        else:
            sec_data[key][4] += qt

total_sec_2026 = len(sec_data)
print(f"Total unique sections in 2026: {total_sec_2026:,}")

sections_list = list(sec_data.values())

# 1. Native CSV order (by first appearance of each section in votacao_secao_2026_BR.csv)
by_first = sorted(sections_list, key=lambda x: x[0])

# 2. Simulated regional order (NOT the real 2026 arrival order): a per-UF bias that
#    mirrors 2022 regional arrival dynamics, mixed with a seeded random draw.
#    Lower bias = arrives earlier ('ZZ' = votes from abroad).
uf_speed_bias = {
    'ZZ': 0.05,
    'SC': 0.30, 'PR': 0.31, 'RS': 0.33, 'DF': 0.32,
    'MS': 0.34, 'GO': 0.36, 'MT': 0.36,
    'SP': 0.42, 'ES': 0.43, 'MG': 0.46, 'RJ': 0.47,
    'TO': 0.49, 'RO': 0.46, 'RR': 0.44, 'AC': 0.50, 'AP': 0.51,
    'RN': 0.56, 'PB': 0.57, 'SE': 0.58, 'AL': 0.59,
    'PE': 0.60, 'CE': 0.61, 'MA': 0.63, 'PI': 0.64, 'BA': 0.65,
    'PA': 0.62, 'AM': 0.63
}

rng = random.Random(20261004)
def regional_sort_key(s):
    uf = s[7]
    pos = s[0] / 3800511.0
    bias = uf_speed_bias.get(uf, 0.5)
    # Mix regional bias with wide beta distribution so all states participate from the start
    return 0.36 * bias + 0.59 * rng.betavariate(1.5, 1.5) + 0.05 * pos

by_regional = sorted(sections_list, key=regional_sort_key)

def build_series(ordered_sections):
    n = len(ordered_sections)
    pref_fb = [0] * (n + 1)
    pref_l = [0] * (n + 1)
    pref_ot = [0] * (n + 1)
    pref_br = [0] * (n + 1)
    pref_nu = [0] * (n + 1)

    for i, s in enumerate(ordered_sections, 1):
        pref_fb[i] = pref_fb[i-1] + s[2]
        pref_l[i] = pref_l[i-1] + s[3]
        pref_ot[i] = pref_ot[i-1] + s[4]
        pref_br[i] = pref_br[i-1] + s[5]
        pref_nu[i] = pref_nu[i-1] + s[6]

    series = []
    for step in data_2022:
        frac = step['s'] / step['st']
        idx = max(1, min(n, round(frac * n)))
        fb_v = pref_fb[idx]
        l_v = pref_l[idx]
        ot_v = pref_ot[idx]
        br_v = pref_br[idx]
        nu_v = pref_nu[idx]
        val_v = fb_v + l_v + ot_v
        tot_v = val_v + br_v + nu_v
        two_v = fb_v + l_v

        fb_p2 = round((fb_v / two_v) * 100, 3) if two_v > 0 else 50.0
        l_p2 = round((l_v / two_v) * 100, 3) if two_v > 0 else 50.0

        fb_pval = round((fb_v / val_v) * 100, 3) if val_v > 0 else 0.0
        l_pval = round((l_v / val_v) * 100, 3) if val_v > 0 else 0.0

        t_2026 = step['t'].replace('30/10/2022', '04/10/2026').replace('31/10/2022', '05/10/2026')

        series.append({
            't': t_2026,
            'p': round((idx / n) * 100, 4),
            's': idx,
            'st': n,
            'vt': tot_v,
            'lp': l_p2,
            'jp': fb_p2,
            'lpv': l_pval,
            'jpv': fb_pval,
            'lv': l_v,
            'jv': fb_v,
            'ov': ot_v,
            'bv': br_v,
            'nv': nu_v
        })
    return series

s_csv = build_series(by_first)
s_reg = build_series(by_regional)

for name, s in [('csv_order', s_csv), ('regional_2022_pace', s_reg)]:
    max_fb = max(s, key=lambda x: x['jp'])
    print(f"\nMode: {name}")
    print(f"  Start (idx 0): FB={s[0]['jp']}% (val {s[0]['jpv']}%) vs L={s[0]['lp']}% (val {s[0]['lpv']}%)")
    print(f"  Max FB %: {max_fb['jp']}% (val {max_fb['jpv']}%) at {max_fb['t']} (idx {s.index(max_fb)}, {max_fb['p']}% urnas)")
    for check_idx in [10, 50, 140, 500, 1387, 2500, 3190, 4000, 5285]:
        r = s[check_idx]
        print(f"  Idx {check_idx:4d} ({r['t']} | {r['p']:6.2f}%): FB={r['jp']:6.3f}% (val {r['jpv']:6.3f}%) | L={r['lp']:6.3f}% (val {r['lpv']:6.3f}%) | Dif(FB-L)={r['jv']-r['lv']:+10,d}")

payload = {
    'csv': s_csv,
    'regional': s_reg,
    'summary': {
        'total_secoes': total_sec_2026,
        'fb_votos': s_csv[-1]['jv'],
        'l_votos': s_csv[-1]['lv'],
        'outros_votos': s_csv[-1]['ov'],
        'brancos_votos': s_csv[-1]['bv'],
        'nulos_votos': s_csv[-1]['nv'],
        'total_votos': s_csv[-1]['vt']
    }
}

with open('dados_eleicao_2026.js', 'w', encoding='utf-8') as f:
    f.write('window.RAW_ELECTION_DATA_2026 = ' + json.dumps(payload, separators=(',', ':')) + ';')

sz = os.path.getsize('dados_eleicao_2026.js')
print(f"\nSaved dados_eleicao_2026.js ({sz:,} bytes / {sz/1024:.1f} KB)")

