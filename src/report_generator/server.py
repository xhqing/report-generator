import json
import logging
import os

from mcp.server.fastmcp import FastMCP

from report_generator.models import REPORT_DATA_SCHEMA, get_empty_data
from report_generator.template import render_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_DIR = os.environ.get("REPORT_OUTPUT_DIR", "")

mcp = FastMCP(
    "report-generator",
    instructions="Market research report generator MCP Server. Generates HTML research reports from structured data. Supports empty template generation when no data is provided.",
)


def _resolve_output_dir(output_dir: str) -> str:
    if not output_dir:
        output_dir = DEFAULT_OUTPUT_DIR
    if not output_dir:
        return ""
    if not os.path.isabs(output_dir):
        return ""
    return output_dir


@mcp.tool()
def generate_report(data: str = "{}", output_dir: str = "", targets_json_path: str = "") -> str:
    """Generate a complete HTML research report from structured data and save to file.

    Args:
        data: JSON string containing report data. When empty or "{}", generates an empty template
              with placeholder structure. The data should follow the report data schema
              (use get_report_schema to see the full schema).
        output_dir: Absolute path to the directory where the report will be saved.
                    If not provided, falls back to the REPORT_OUTPUT_DIR environment variable.
                    One of them must be set to a valid absolute path.
        targets_json_path: Absolute path to the targets.json file. Required for empty template
                          generation to pre-fill analysis tables with target names and codes.

    Returns:
        JSON string with the saved file path or error message.
    """
    resolved = _resolve_output_dir(output_dir)
    if not resolved:
        hint = "Set output_dir parameter or configure REPORT_OUTPUT_DIR env var in mcp.json"
        return json.dumps({"error": f"output_dir is required and must be an absolute path. {hint}"}, ensure_ascii=False)

    try:
        parsed = json.loads(data) if data else {}
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON input: {e}"}, ensure_ascii=False)

    if not parsed:
        parsed = get_empty_data(targets_json_path)

    try:
        html_content = render_report(parsed)
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return json.dumps({"error": f"Report generation failed: {e}"}, ensure_ascii=False)

    try:
        os.makedirs(resolved, exist_ok=True)
        from datetime import datetime
        import pytz

        bj_tz = pytz.timezone("Asia/Shanghai")
        now_bj = datetime.now(bj_tz)
        existing = [f for f in os.listdir(resolved) if f.startswith("YB_") and f.endswith(".html")]
        next_num = len(existing) + 1
        timestamp_str = now_bj.strftime("%Y%m%d%H%M%S")
        filename = f"YB_{next_num:04d}_{timestamp_str}.html"
        filepath = os.path.join(resolved, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        return json.dumps({"success": True, "filepath": filepath, "filename": filename}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Report save failed: {e}")
        return json.dumps({"error": f"Report save failed: {e}"}, ensure_ascii=False)


@mcp.tool()
def generate_empty_template(targets_json_path: str) -> str:
    """Generate an empty report template with targets pre-filled from a targets.json file.

    Args:
        targets_json_path: Absolute path to the targets.json file containing the indices,
                          stocks, and ETFs to include in the analysis tables.

    Returns:
        HTML report template with target names, codes, and empty trend probabilities pre-filled.
    """
    empty_data = get_empty_data(targets_json_path)
    return render_report(empty_data)


@mcp.tool()
def get_report_schema() -> str:
    """Get the JSON schema for report input data.

    Use this to understand the expected data structure for the generate_report tool.

    Returns:
        JSON schema describing all supported fields in the report data.
    """
    return json.dumps(REPORT_DATA_SCHEMA, ensure_ascii=False, indent=2)


@mcp.tool()
def save_report(html_content: str, output_dir: str = "", filename: str = "") -> str:
    """Save HTML report content to a file.

    Args:
        html_content: The HTML content to save.
        output_dir: Absolute path to the directory where the report will be saved.
                    If not provided, falls back to the REPORT_OUTPUT_DIR environment variable.
                    One of them must be set to a valid absolute path.
        filename: Filename for the report. Defaults to auto-generated name with timestamp.

    Returns:
        JSON with the saved file path or error message.
    """
    resolved = _resolve_output_dir(output_dir)
    if not resolved:
        hint = "Set output_dir parameter or configure REPORT_OUTPUT_DIR env var in mcp.json"
        return json.dumps({"error": f"output_dir is required and must be an absolute path. {hint}"}, ensure_ascii=False)

    os.makedirs(resolved, exist_ok=True)

    if not filename:
        from datetime import datetime
        import pytz

        bj_tz = pytz.timezone("Asia/Shanghai")
        now_bj = datetime.now(bj_tz)
        existing = [f for f in os.listdir(resolved) if f.startswith("YB_") and f.endswith(".html")]
        next_num = len(existing) + 1
        timestamp_str = now_bj.strftime("%Y%m%d%H%M%S")
        filename = f"YB_{next_num:04d}_{timestamp_str}.html"

    filepath = os.path.join(resolved, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        return json.dumps({"success": True, "filepath": filepath, "filename": filename}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
