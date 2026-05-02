# report-generator

MCP Server for generating market research reports in HTML format — 跨市场重大事件与港股龙头策略研判报告生成器。

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
      "args": ["--from", "git+https://github.com/xhqing/report-generator.git", "report-generator"]
    }
  }
}
```

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
      "command": "report-generator"
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

## MCP Tools

### `generate_report`

Generate a complete HTML research report from structured data.

**Parameters:**
- `data` (string, optional): JSON string containing report data. When empty or `"{}"`, generates an empty template with placeholder structure.

**Example:**
```json
{
  "data": "{\"report_date\": \"2026年05月02日\", \"generation_time\": \"2026-05-02 15:30:00\", \"index_data\": [{\"name\": \"恒生指数\", \"code\": \"HSI\", \"price\": 22000.50, \"timestamp\": \"2026-05-02 16:00:00 (HKT)\", \"source\": \"https://example.com\"}]}"
}
```

### `generate_empty_template`

Generate an empty report template with placeholder structure. No parameters required.

Use this to quickly get a report skeleton, then fill in the data sections.

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
| `report_date` | string | 报告日期，格式：YYYY年MM月DD日 |
| `generation_time` | string | 报告生成时间，格式：YYYY-MM-DD HH:MM:SS |
| `index_data` | array | 指数行情数据表（name, code, price, timestamp, source） |
| `stock_data` | array | 个股行情数据表（name, code, price, timestamp, source） |
| `etf_data` | array | ETF行情数据表（name, code, price, timestamp, source） |
| `future_events` | array | 未来一周重大事件分析（title, time, overview, scenarios） |
| `index_analysis` | array | 指数研判（name, code, current, trend, trend_probs, trend_reasons, high, low, logic） |
| `stock_analysis` | array | 个股分析（name, code, price, trend, trend_probs, high, low, view, position, logic） |
| `etf_analysis` | array | ETF分析（name, code, price, trend, trend_probs, high, low, view, position, logic） |
| `reasoning` | object | 分析推理过程（macro_chain, index_chain, stock_chain, assumptions, risks, diff_from_last） |
| `references` | object | 参考资料（macro_policy, geopolitics, industry, technical） |

Use the `get_report_schema` tool to get the complete JSON schema with all nested fields.

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

AGPL-3.0
