import csv
import json
import os

def parse_num(s):
    return float(s.replace(',', '.'))

records = []
with open('Presidente_BR_2T_2022.csv', mode='r', encoding='latin1') as f:
    reader = csv.reader(f, delimiter=';')
    header = [c.strip() for c in next(reader)]
    for r in reader:
        if not r or len(r) < len(header):
            continue
        d = {header[i]: r[i].strip() for i in range(len(header))}
        dt = d['DT_TOTALIZACAO']
        pe_sec = round(parse_num(d['PE_SECOES_TOT_ACUMULADO']) * 100, 4)
        sec_acum = int(d['QT_SECOES_TOT_ACUMULADO'])
        sec_tot = int(d['QT_SECOES_TOTAL'])
        votos_tot = int(d['QT_VOTOS_TOTAL_ACUMULADO'])
        l_pct = round(parse_num(d['L_PE_VOTOS_TOT_ACUMULADO']) * 100, 3)
        jb_pct = round(parse_num(d['JB_PE_VOTOS_TOT_ACUMULADO']) * 100, 3)
        l_votos = int(d['L_QT_VOTOS_TOT_ACUMULADO'])
        jb_votos = int(d['JB_QT_VOTOS_TOT_ACUMULADO'])
        br_votos = int(d['BRANCO_QT_VOTOS_TOT_ACUMULADO'])
        nu_votos = int(d['NULO_QT_VOTOS_TOT_ACUMULADO'])
        records.append({
            't': dt,
            'p': pe_sec,
            's': sec_acum,
            'st': sec_tot,
            'vt': votos_tot,
            'lp': l_pct,
            'jp': jb_pct,
            'lv': l_votos,
            'jv': jb_votos,
            'bv': br_votos,
            'nv': nu_votos,
        })

print(f"Total records processed: {len(records)}")

with open('dados_eleicao.js', 'w', encoding='utf-8') as f:
    f.write('window.RAW_ELECTION_DATA = ' + json.dumps(records, separators=(',', ':')) + ';')

size = os.path.getsize('dados_eleicao.js')
print(f"File dados_eleicao.js created: {size} bytes ({size / 1024:.1f} KB)")

