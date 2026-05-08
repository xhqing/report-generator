# report-generator

MCP Server for generating market research reports in HTML format — a cross-market macro event and Hong Kong equity strategy report generator.

## Features

- Generate HTML research reports with parameterized templates
- Support empty template generation (placeholder structure)
- Compliant with financial research report formatting standards
- Includes: market data tables, event analysis, index/stock/ETF analysis, reasoning chains, references, disclaimers
- Auto-generate report filenames with timestamps (Beijing time)
- Save reports to local files

## Quick Start: Use in TRAE CN with uvx

The recommended way to use this MCP service is through [uvx](https://docs.astral.sh/uv/guides/tools/), which lets you run the service directly from GitHub **without manual installation**.

### Prerequisites

Install [uv](https://docs.astral.sh/uv/) (includes `uvx`):

```bash
# macOS
brew install uv

# Or with curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Configure MCP Service in TRAE CN

1. Open TRAE CN IDE
2. Click the **Agent** icon in the left sidebar
3. Click the **⚙️ Settings** icon next to the agent name
4. Select **MCP Servers** tab
5. Click **+ Add MCP Server**
6. Paste the following JSON configuration:

```json
{
  "mcpServers": {
    "report-generator": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/xhqing/report-generator.git", "report-generator"],
      "env": {
        "REPORT_OUTPUT_DIR": "/Users/yourname/Documents/reports",
        "TARGETS_JSON_PATH": "/Users/yourname/Documents/targets.json"
      }
    }
  }
}
```

> **Important**: Replace the paths with your actual absolute paths:
> - `REPORT_OUTPUT_DIR`: Directory where generated reports will be saved. This sets the default output directory, so you don't need to specify `output_dir` every time you call `generate_report`.
> - `TARGETS_JSON_PATH`: Path to your `targets.json` file, which defines the indices, stocks, and ETFs to include in the report analysis tables. Required for `generate_empty_template` and empty `generate_report` calls to pre-fill the analysis tables with your custom targets. If not set, the analysis tables will be empty.

7. Save — the MCP service status should show as **Connected** (green dot)

That's it! You can now use the report generation tools in your agent conversations. `uvx` will automatically fetch and run the latest version from GitHub every time the service starts.

### How uvx Works

- `uvx` is a zero-install runner: it creates an isolated virtual environment, installs the package from GitHub, and runs the command — all automatically
- No need to `pip install`, no need to manage Python environments, no need to worry about dependency conflicts
- Each run pulls the latest version from GitHub, so you always have the most up-to-date code

## Other Installation Methods

### Install via pip from GitHub

If you prefer a traditional installation:

```bash
pip install git+https://github.com/xhqing/report-generator.git
```

Then configure in TRAE CN:

```json
{
  "mcpServers": {
    "report-generator": {
      "command": "report-generator",
      "env": {
        "REPORT_OUTPUT_DIR": "/Users/yourname/Documents/reports",
        "TARGETS_JSON_PATH": "/Users/yourname/Documents/targets.json"
      }
    }
  }
}
```

### Install from Source

```bash
git clone https://github.com/xhqing/report-generator.git
cd report-generator
pip install .
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `uvx: command not found` | Install uv first: `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| `report-generator: command not found` (pip install) | Use `which report-generator` to find the path, then use the absolute path in the config |
| Python environment mismatch | Use the `uvx` method instead — it handles environments automatically |
| Connection shows red dot in TRAE CN | Check that `uv` is in the PATH that TRAE CN uses; restart TRAE CN after installing uv |
| Report analysis tables are empty | Ensure `TARGETS_JSON_PATH` is set in the MCP config `env`, pointing to a valid `targets.json` file |

## MCP Tools

### `generate_report`

Generate a complete HTML research report from structured data.

**Parameters:**
- `data` (string, optional): JSON string containing report data. When empty or `"{}"`, generates an empty template with the analysis tables pre-filled from `targets.json` (if configured via `TARGETS_JSON_PATH`).
- `output_dir` (string, optional): Absolute path to the output directory. Falls back to `REPORT_OUTPUT_DIR` env var.
- `targets_json_path` (string, optional): Absolute path to the `targets.json` file. Falls back to `TARGETS_JSON_PATH` env var.

**Example:**
```json
{
  "data": "{\"report_date\": \"2026-05-02\", \"generation_time\": \"2026-05-02 15:30:00\", \"index_data\": [{\"name\": \"Hang Seng Index\", \"code\": \"HSI\", \"price\": 22000.50, \"timestamp\": \"2026-05-02 16:00:00 (HKT)\", \"source\": \"https://example.com\"}]}"
}
```

### `generate_empty_template`

Generate an empty report template with targets pre-filled from a `targets.json` file.

**Parameters:**
- `targets_json_path` (string, optional): Absolute path to the `targets.json` file. Falls back to `TARGETS_JSON_PATH` env var. If neither is provided, the analysis tables will be empty.

Use this to quickly get a report skeleton with your custom targets pre-populated, then fill in the analysis data.

### `get_report_schema`

Get the JSON schema for report input data. No parameters required.

Use this to understand the full data structure expected by `generate_report`.

### `save_report`

Save HTML report content to a local file.

**Parameters:**
- `html_content` (string, required): The HTML content to save
- `output_dir` (string, optional): Directory to save the report. Defaults to `./YB_000X`
- `filename` (string, optional): Filename for the report. Defaults to auto-generated name like `YB_0001_20260502153000.html`

**Example:**
```json
{
  "html_content": "<html>...</html>",
  "output_dir": "/path/to/output",
  "filename": "YB_0001_20260502.html"
}
```

## Report Data Schema

The report data structure supports the following top-level fields:

| Field | Type | Description |
|-------|------|-------------|
| `report_date` | string | Report date, format: YYYY-MM-DD |
| `generation_time` | string | Report generation time, format: YYYY-MM-DD HH:MM:SS |
| `index_data` | array | Index market data (name, code, price, timestamp) |
| `stock_data` | array | Stock market data (name, code, price, currency, timestamp) |
| `etf_data` | array | ETF market data (name, code, price, currency, timestamp) |
| `future_events` | array | Upcoming week major events (title, time, overview, scenarios) |
| `index_analysis` | array | Index analysis (name, code, current, trend, trend_probs, trend_reasons, high, low, logic) |
| `stock_analysis` | array | Stock analysis (name, code, price, currency, trend, trend_probs, high, low, view, position, logic) |
| `etf_analysis` | array | ETF analysis (name, code, price, currency, trend, trend_probs, high, low, view, position, logic) |
| `reasoning` | object | Analysis reasoning (macro_chain, index_chain, stock_chain, assumptions, risks, diff_from_last) |
| `references` | object | References (macro_policy, geopolitics, industry, technical) |

Use the `get_report_schema` tool to get the complete JSON schema with all nested fields.

## targets.json 格式

`targets.json` 定义了报告中需要分析的指数、个股和 ETF 标的。文件结构如下：

```json
{
  "a_shares": {
    "index_major":   [{"name": "上证指数", "code": "000001.SH"}],
    "index_sector":  [{"name": "中证白酒", "code": "399997.SZ"}],
    "sse_stocks":    [{"name": "贵州茅台", "code": "600519.SH"}],
    "sse_etf":       [{"name": "沪深300ETF", "code": "510300.SH"}],
    "szse_stocks":   [{"name": "宁德时代", "code": "300750.SZ"}],
    "szse_etf":      [{"name": "创业板ETF", "code": "159915.SZ"}]
  },
  "hk_shares": {
    "index_major":   [{"name": "恒生指数", "code": "HSI"}],
    "index_sector":  [{"name": "恒生科技", "code": "HSTECH"}],
    "hkex_stocks":   [{"name": "腾讯控股", "code": "00700.HK"}],
    "hkex_etf":      [{"name": "盈富基金", "code": "02800.HK"}]
  },
  "us_shares": {
    "index_major":   [{"name": "标普500", "code": "SPX"}],
    "index_sector":  [{"name": "费城半导体", "code": "SOX"}],
    "stocks":        [{"name": "Apple", "code": "AAPL.US"}],
    "adr":           [{"name": "阿里巴巴", "code": "BABA.US"}],
    "etf":           [{"name": "SPY", "code": "SPY.US"}]
  }
}
```

> 每个列表项包含 `name`（标的名称）和 `code`（标的代码）。留空的 `{"name": "", "code": ""}` 项会被自动过滤掉。

## Typical Workflow

1. **Get the schema**: Call `get_report_schema` to understand the data structure
2. **Generate empty template**: Call `generate_empty_template` to preview the report layout
3. **Fill in data**: Prepare your report data as a JSON string
4. **Generate report**: Call `generate_report` with the data
5. **Save report**: Call `save_report` to save the HTML to a file

## Development

```bash
git clone https://github.com/xhqing/report-generator.git
cd report-generator
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Lint

```bash
ruff check src/
```

## License

This project is open-sourced under the [GNU Affero General Public License v3.0](LICENSE).
