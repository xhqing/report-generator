# report-generator

MCP Server for generating market research reports in HTML format — 跨市场重大事件与港股龙头策略研判报告生成器。

## Features

- Generate HTML research reports with parameterized templates
- Support empty template generation (placeholder structure)
- Compliant with financial research report formatting standards
- Includes: market data tables, event analysis, index/stock/ETF analysis, reasoning chains, references, disclaimers
- Auto-generate report filenames with timestamps (Beijing time)
- Save reports to local files

## Installation

### Install from GitHub (Recommended)

```bash
pip install git+https://github.com/xhqing/report-generator.git
```

### Install from Source

```bash
git clone https://github.com/xhqing/report-generator.git
cd report-generator
pip install .
```

### Verify Installation

```bash
report-generator --help
```

## Configure MCP Service in TRAE CN

TRAE CN is an AI-powered IDE that supports MCP (Model Context Protocol) services. Follow these steps to configure the report-generator MCP service for your agent:

### Step 1: Install the package

Make sure you have installed `report-generator` using one of the methods above, and the `report-generator` command is available in your terminal.

### Step 2: Open Agent MCP Settings

1. Open TRAE CN IDE
2. Click the **Agent** icon in the left sidebar (or press the shortcut)
3. Click the **⚙️ Settings** icon next to the agent name
4. Select **MCP Servers** tab
5. Click **+ Add MCP Server**

### Step 3: Add Configuration

Choose **Command (Stdio)** mode and fill in:

| Field | Value |
|-------|-------|
| **Name** | `report-generator` |
| **Command** | `report-generator` |

Or paste the following JSON directly into the configuration file:

```json
{
  "mcpServers": {
    "report-generator": {
      "command": "report-generator"
    }
  }
}
```

### Step 4: Verify Connection

After adding, the MCP service status should show as **Connected** (green dot). You can now use the report generation tools in your agent conversations.

### Troubleshooting

If the connection fails:

1. **Check if `report-generator` is in PATH**: Run `which report-generator` in terminal
2. **Use absolute path**: If the command is not found, use the full path instead:
   ```json
   {
     "mcpServers": {
       "report-generator": {
         "command": "/absolute/path/to/report-generator"
       }
     }
   }
   ```
   You can find the path by running: `which report-generator`
3. **Check Python environment**: Make sure the Python environment where you installed the package is the same one TRAE CN uses
4. **Use uvx (alternative)**: If you have [uv](https://docs.astral.sh/uv/) installed, you can use:
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
