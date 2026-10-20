import json

with open('dados_eleicao.js', 'r', encoding='utf-8') as f:
    d = json.loads(f.read().split('=', 1)[1].rstrip(';'))

top_jb = sorted(enumerate(d), key=lambda x: x[1]['jp'], reverse=True)[:5]
print("Top 5 JB %:")
for i, r in top_jb:
    print(f"  idx {i:4d}: {r['t']} urnas={r['p']:6.2f}% JB={r['jp']:6.3f}% L={r['lp']:6.3f}% JB_votos={r['jv']:,} L_votos={r['lv']:,}")

top_l = sorted(enumerate(d), key=lambda x: x[1]['lp'], reverse=True)[:5]
print("\nTop 5 L %:")
for i, r in top_l:
    print(f"  idx {i:4d}: {r['t']} urnas={r['p']:6.2f}% L={r['lp']:6.3f}% JB={r['jp']:6.3f}% L_votos={r['lv']:,} JB_votos={r['jv']:,}")

# Let's inspect the timeline from 17:00 to 17:30
print("\nTimeline 17:00 to 17:30 samples:")
for i in [0, 4, 20, 50, 100, 140, 180, 250, 350, 500]:
    if i < len(d):
        r = d[i]
        print(f"  idx {i:4d}: {r['t']} urnas={r['p']:6.2f}% L={r['lp']:6.2f}% JB={r['jp']:6.2f}%")

