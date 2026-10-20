# 🏢 Eleição de Condomínio 2022 — Apuração JB x L

Aplicação interativa em HTML/JS puro para visualização e reprodução da apuração da eleição de 2022 (segundo turno), baseada no arquivo de dados `Presidente_BR_2T_2022.csv`.

---

## 🚀 Como Executar

Basta abrir o arquivo [`index.html`](file:///d:/Projetos/eleicao/index.html) em qualquer navegador moderno (Chrome, Edge, Firefox, Brave):

1. **Duplo clique direto no arquivo**: Funciona imediatamente sem necessidade de servidor web, pois os dados estão pré-compilados em [`dados_eleicao.js`](file:///d:/Projetos/eleicao/dados_eleicao.js).
2. **Via Servidor Web Local (opcional)**:
   ```bash
   # Python
   python -m http.server 8000
   # Ou Node.js npx
   npx serve .
   ```
   Acesse: `http://localhost:8000`

---

## 📊 Recursos do Painel

- **Placar Dinâmico**:
  - Percentuais de votos válidos de **Chapa L** e **Chapa JB**.
  - Quantidade total de votos acumulados.
  - Vantagem/diferença em votos nominais e pontos percentuais.
  - Indicador de liderança e vencedor ao final da apuração.
  - Barra dupla proporcional com marca d'água no centro de 50%.
- **Simulador / Player de Apuração**:
  - Slider contínuo de 0% a 100% das seções.
  - Botão Play/Pause com velocidades ajustáveis (`1x`, `5x`, `20x`, `60x`, `Max`).
  - Teclas de atalho: `Espaço` (Play/Pause), `Setas Esquerda/Direita` (Avançar/Voltar), `Home`/`End` (Início/Fim).
- **Saltos Rápidos para Momentos Marcantes**:
  - `17:00:51`: Início da contagem (L inicia à frente com 50,59%).
  - `17:01:51`: Pico inicial de L (57,30% vs 42,70% de JB).
  - `17:07:59`: JB assume a liderança inicial (51,21%).
  - `17:17:29`: **Pico Percentual Máximo de JB (56,84% vs 43,16% de L)** — diferença de +13,68 p.p.
  - `17:56:46`: Pico de vantagem em votos nominais de JB (+790.791 votos de frente, 51,31%).
  - `18:42:53`: Primeiro empate técnico (50,01% x 49,99%).
  - `18:44:51`: **A Virada** de L aos 68,34% das seções apuradas.
  - `19:05:01`: L ultrapassa 1 milhão de votos de vantagem.
  - `20:07:15`: L alcança 2 milhões de votos de vantagem.
  - `00:18:04`: Totalização final com 100% das seções.
- **Gráfico de Alta Performance com Zoom & Escala Y Flexível**:
  - **Filtros de Período**:
    - 🔍 **Início (17:00 - 17:45)**: Expande os primeiros 45 minutos em tela cheia para detalhar a volatilidade e o pico de 56,8% de JB.
    - ⚡ **A Virada (18:15 - 19:05)**: Foco na ultrapassagem histórica.
    - 🏁 **Reta Final (19:00 - 00:18)**: Consolidação da apuração.
    - 🌐 **Total (17:00 - 00:18)**: Toda a apuração.
  - **Escala Y comutável**:
    - **Escala Total (40% - 60%)**: Permite visualizar com folga os picos de 56,8% e 43,2%.
    - **Foco Central (47% - 53%)**: Foco na disputa acirrada.
    - **Auto**: Ajuste dinâmico aos valores visíveis.
- **Tabela com Histórico e Busca**:
  - Filtro em tempo real por horário ou percentual.
  - Botão para filtrar apenas os marcos históricos.
- **Importador de CSV**:
  - Suporta carregar ou arrastar qualquer novo CSV que siga a mesma estrutura de colunas do TSE.

---

## 📁 Estrutura de Arquivos

- [`index.html`](file:///d:/Projetos/eleicao/index.html): Painel completo da aplicação com interface responsiva e gráficos.
- [`dados_eleicao.js`](file:///d:/Projetos/eleicao/dados_eleicao.js): Conjunto de 5.286 registros formatados para carregamento instantâneo offline.
- [`Presidente_BR_2T_2022.csv`](file:///d:/Projetos/eleicao/Presidente_BR_2T_2022.csv): Arquivo de dados original da totalização.
- [`process_data.py`](file:///d:/Projetos/eleicao/process_data.py): Script Python para regeneração e compactação dos dados.

