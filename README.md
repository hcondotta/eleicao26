# 🗳️ Apuração 2022 × 2026: a vantagem inicial se repete?

Painel interativo em HTML/JS puro que compara como a diferença entre o nº 22 e o nº 13 (L) mudou **durante a contagem dos votos** para presidente:

- **2022 (2º turno):** JB × L, com a linha do tempo real do TSE (5.286 atualizações do placar, das 17:00:51 às 00:18:04).
- **2026 (1º turno):** FB × L, com o resultado real por seção eleitoral e uma **ordem de chegada simulada** (veja [Metodologia e limitações](#-metodologia-e-limitações)).

---

## 🚀 Como abrir

Abra o [`index.html`](index.html) em qualquer navegador moderno. Funciona com duplo clique, sem servidor, porque os dados já estão compilados em [`dados_eleicao.js`](dados_eleicao.js) e [`dados_eleicao_2026.js`](dados_eleicao_2026.js).

Se preferir um servidor local:

```bash
python -m http.server 8000   # depois acesse http://localhost:8000
```

---

## 📖 Como ler o painel

1. **A contagem anda da esquerda para a direita**, de 0% a 100% das seções apuradas. Arraste a barra ou aperte ▶ para assistir.
2. **Cor = candidato, traço = ano:** JB em azul, FB em verde, L em vermelho. No gráfico, a linha tracejada é 2022 e a cheia é 2026.
3. **As duas eleições estão alinhadas pelo % de seções apuradas.** O horário mostrado é sempre o de 2022.
4. **A pergunta central:** nas duas eleições o nº 22 começa na frente. Essa vantagem encolhe da mesma forma? Em 2022, L virou e venceu; em 2026, FB terminou na frente.

O painel tem um guia "Como ler este painel", ícones ⓘ com explicações e uma frase que descreve, em linguagem simples, o que está acontecendo em cada ponto da contagem.

---

## 🔬 Metodologia e limitações

**Fontes**

- `Presidente_BR_2T_2022.csv`: boletim de totalização do TSE do 2º turno de 2022, com o placar acumulado a cada atualização (472.075 seções).
- `votacao_secao_2026_BR.csv`: votos por seção eleitoral do 1º turno de 2026 (499.206 seções, 3,8 milhões de linhas). O arquivo foi gerado de uma só vez (06/10/2026, 14:03:43) e **não informa quando cada seção foi apurada**.

**Como a curva de 2026 é montada** ([`process_2026.py`](process_2026.py))

1. Somam-se os votos de cada seção: FB (22), L (13), demais candidatos, brancos (95) e nulos (96).
2. As seções são postas em uma ordem de chegada:
   - **Simulada por região** (padrão): sorteio com semente fixa, com prioridade para os estados que chegaram antes em 2022 (Sul e Centro-Oeste primeiro, Nordeste e Norte depois);
   - **Ordem do arquivo**: a sequência das linhas do CSV.
3. Para cada uma das 5.286 atualizações de 2022, soma-se a mesma fração das seções de 2026.

**O que dá e o que não dá para concluir**

- ✅ A trajetória de 2022 e o **resultado final** de 2026 são reais.
- ⚠️ O caminho de 2026 até o resultado é **ilustrativo**: picos, viradas e momentos de liderança mudam conforme a ordem escolhida. Na ordem do arquivo, por exemplo, L lidera de 3,5% a 75,9% das seções.
- ⚠️ Na ordem simulada, os estados entram na sequência típica de 2022. Por isso, parte da semelhança entre as curvas é consequência da própria simulação.
- ⚠️ 2022 foi 2º turno (dois candidatos) e 2026 foi 1º turno (com outros candidatos, que somaram 7,81% dos válidos). A opção "Só FB e L (soma 100%)" compara os dois anos na mesma base.

---

## 📊 Recursos

- **Três modos:** comparar 2022 e 2026, ou ver cada eleição isolada.
- **Placar:** os dois candidatos de cada ano com o mesmo destaque, a barra com a marca de 50%, a vantagem em pontos percentuais e em votos.
- **Reprodução da apuração:** barra de tempo, ▶/⏸, velocidades de 1x a Máx.
  - Atalhos: `Espaço` reproduz/pausa, `←` `→` avançam passo a passo, `Home` e `End` vão para o início e o fim.
- **Momentos-chave calculados a partir dos dados:** maior vantagem, virada, metade das seções, resultado final. Os textos, os cards e as anotações do gráfico são recalculados quando se troca a ordem ou a base de 2026, por isso nunca contradizem o gráfico.
- **Gráfico:**
  - três visões: % de cada candidato, vantagem do nº 22 em p.p. e vantagem em votos;
  - zoom por trecho da contagem;
  - eixo horizontal em % apurado ou horário;
  - exportação em PNG.
- **Projeção "e se" (frágil):** escolha a vantagem de FB em um ponto da contagem e veja se, e quando, L passaria à frente caso a vantagem encolhesse como em 2022.
  - Modelo: resultado final = vantagem de FB no ponto escolhido − quanto a vantagem de JB caiu desse ponto até o fim em 2022.
  - Uma faixa ilustrativa mostra o efeito de uma queda 25% menor ou maior que a de 2022.
  - Um segundo gráfico mostra, para cada vantagem inicial de FB, com quantos % apurados L passaria.
  - Não é previsão: supõe a mesma ordem de chegada dos estados e uma diferença uniforme entre FB e JB, e não tem margem de erro calculável, porque há uma única apuração real de referência.
- **Tabela passo a passo:** busca por horário ou %, e filtro de momentos-chave.
- **Tema claro/escuro.** As cores dos candidatos foram validadas para daltonismo, e o ano também é indicado pelo traço da linha.

---

## 📁 Arquivos

| Arquivo | Para que serve |
|---|---|
| [`index.html`](index.html) | O painel (HTML, CSS e JS em um só arquivo). |
| [`dados_eleicao.js`](dados_eleicao.js) | 2022 compilado: 5.286 registros (`window.RAW_ELECTION_DATA`). |
| [`dados_eleicao_2026.js`](dados_eleicao_2026.js) | 2026 compilado nas duas ordens de chegada (`window.RAW_ELECTION_DATA_2026`). |
| [`process_data.py`](process_data.py) | Gera `dados_eleicao.js` a partir do CSV de 2022. |
| [`process_2026.py`](process_2026.py) | Gera `dados_eleicao_2026.js` a partir do CSV de 2026 (requer `dados_eleicao.js`). |
| [`check_milestones.py`](check_milestones.py) | Inspeção: imprime os marcos de 2022 (virada, picos, +1M, +2M). |
| [`inspect_start.py`](inspect_start.py) | Inspeção: picos e primeiros minutos de 2022. |

Os CSVs brutos não vão para o Git (veja [`.gitignore`](.gitignore)). Para regerar os dados, coloque-os na raiz e rode:

```bash
python process_data.py   # 2022
python process_2026.py   # 2026 (usa os passos de 2022)
```

### Campos dos registros

| Campo | Significado |
|---|---|
| `t` | Data e hora da atualização (em 2026, o horário de 2022 com a data trocada) |
| `p` | % das seções apuradas |
| `s`, `st` | Seções apuradas / total |
| `vt` | Total de votos (válidos + brancos + nulos) |
| `jp`, `lp` | % do nº 22 e de L considerando só os dois (soma 100%) |
| `jpv`, `lpv` | 2026: % do nº 22 e de L sobre todos os votos válidos |
| `jv`, `lv` | Votos do nº 22 e de L |
| `ov`, `bv`, `nv` | Votos em outros candidatos (2026), brancos e nulos |
