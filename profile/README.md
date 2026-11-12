<div align="center">

<img src="banner.svg" alt="funnest — Every moment of investing, more fun" width="100%">

<br>

[![Website](https://img.shields.io/badge/funnest.xyz-6C4DFF?style=flat-square)](https://funnest.xyz)&nbsp;[![Terminal](https://img.shields.io/badge/Open_the_terminal-14121F?style=flat-square)](https://funnest.xyz/trade/)&nbsp;[![Charts](https://img.shields.io/badge/charts.funnest.xyz-14121F?style=flat-square)](https://charts.funnest.xyz)&nbsp;[![npm](https://img.shields.io/npm/v/@funnest/charts-react?style=flat-square&color=6C4DFF&label=%40funnest%2Fcharts)](https://www.npmjs.com/package/@funnest/charts-react)&nbsp;[![Stars](https://img.shields.io/github/stars/funnest-xyz/funnest-charts?style=flat-square&color=FFD43B&labelColor=14121F)](https://github.com/funnest-xyz/funnest-charts)

</div>

<br>

**Funnest** is making investing more fun.
Watch the markets, practice with virtual money and share the indicators you build, all in one place.

<br>

## 📈 What we build

<table>
<tr>
<td width="50%" valign="top">

### Funnest Terminal

**[funnest.xyz/trade](https://funnest.xyz/trade/)**

- Korean and US stocks and crypto (Upbit, Bithumb, Binance Futures, Hyperliquid) on one screen
- Paper trading in stocks, crypto and futures with virtual money
- A community to share and backtest your own indicators, and follow the people behind them
- Live chat while the market moves

</td>
<td width="50%" valign="top">

### Funnest Charts

**[funnest-xyz/funnest-charts](https://github.com/funnest-xyz/funnest-charts)** · Apache-2.0

- A trading chart for investment apps that runs in your page, not an iframe
- Lightweight SVG charts for dashboards
- Korean market defaults: KST, KRX tick sizes, red up · blue down
- A CLI and an MCP server, so AI agents can draw charts too

</td>
</tr>
</table>

<br>

## 📦 Packages

| Package | What it does |
|---|---|
| [`@funnest/charts`](https://www.npmjs.com/package/@funnest/charts) | Canvas charting engine for financial charts |
| [`@funnest/charts-ui`](https://www.npmjs.com/package/@funnest/charts-ui) | Pro trading UI: toolbar, drawing tools, sheets. Framework-agnostic |
| [`@funnest/charts-react`](https://www.npmjs.com/package/@funnest/charts-react) | React bindings: the trading widget plus SVG line, area and bar charts |
| [`@funnest/charts-viz`](https://www.npmjs.com/package/@funnest/charts-viz) | Chart math (scales, ticks, paths, scrubbing) shared by web and React Native |
| [`@funnest/charts-cli`](https://www.npmjs.com/package/@funnest/charts-cli) | Render SVG/PNG/HTML, validate specs, suggest charts, generate React code |
| [`@funnest/charts-mcp`](https://www.npmjs.com/package/@funnest/charts-mcp) | MCP server: rendering, chart suggestions, Datafeed templates |

```bash
npm i @funnest/charts-react
```

```tsx
import { FnChart } from '@funnest/charts-react';

<FnChart datafeed={myDatafeed} symbol="005930" resolution="1D" />
```

Read the [docs](https://charts.funnest.xyz/docs/) to connect your own data.

<br>

## 💬 Get involved

- Found a bug in the charts or have an idea? Open an [issue](https://github.com/funnest-xyz/funnest-charts/issues). Pull requests are welcome.
- Feedback on the terminal goes to **고객센터** (Support) at the bottom of its right rail. We read every note.

<br>

<details>
<summary><b>한국어</b></summary>

<br>

**Funnest**는 투자를 더 재밌게 만들고 있어요. 차트를 보고, 가상 자금으로 연습하고, 내가 만든 지표를 나누는 일을 한 곳에서 할 수 있게요.

- **[Funnest 터미널](https://funnest.xyz/trade/)**: 국내·미국 주식과 코인(업비트, 빗썸, 바이낸스 선물, 하이퍼리퀴드)을 한 화면에서 보고, 가상 자금으로 모의투자하고, 직접 만든 지표를 공유·백테스트하고, 실시간 채팅으로 함께 시장을 봐요.
- **[Funnest Charts](https://github.com/funnest-xyz/funnest-charts)**: 투자 앱에 넣는 Apache-2.0 금융 차트예요. 내 페이지 안에서 도는 트레이딩 차트, 대시보드용 SVG 차트, CLI와 MCP 서버가 있어요. 문서는 [charts.funnest.xyz](https://charts.funnest.xyz)에 있어요.

</details>

<br>

<div align="center">
<img src="mascot.svg" width="56" alt="The Funnest mascot">
<br>
<sub>Have fun out there.</sub>
</div>
