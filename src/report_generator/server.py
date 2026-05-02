import json
import logging
import os

from mcp.server.fastmcp import FastMCP

from report_generator.models import REPORT_DATA_SCHEMA, get_empty_data
from report_generator.template import render_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    "report-generator",
    instructions="Market research report generator MCP Server. Generates HTML research reports from structured data. Supports empty template generation when no data is provided.",
)


@mcp.tool()
def generate_report(data: str = "{}") -> str:
    """Generate a complete HTML research report from structured data.

    Args:
        data: JSON string containing report data. When empty or "{}", generates an empty template
              with placeholder structure. The data should follow the report data schema
              (use get_report_schema to see the full schema).

    Returns:
        Complete HTML research report as a string.
    """
    try:
        parsed = json.loads(data) if data else {}
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON input: {e}"}, ensure_ascii=False)

    if not parsed:
        parsed = get_empty_data()

    try:
        html_content = render_report(parsed)
        return html_content
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return json.dumps({"error": f"Report generation failed: {e}"}, ensure_ascii=False)


@mcp.tool()
def generate_empty_template() -> str:
    """Generate an empty report template with placeholder structure.

    Returns:
        HTML report template with placeholder markers for each section.
    """
    empty_data = get_empty_data()
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
        output_dir: Directory to save the report. Defaults to the current working directory/YB_000X.
        filename: Filename for the report. Defaults to auto-generated name with timestamp.

    Returns:
        JSON with the saved file path or error message.
    """
    if not output_dir:
        output_dir = os.path.join(os.getcwd(), "YB_000X")

    os.makedirs(output_dir, exist_ok=True)

    if not filename:
        from datetime import datetime
        import pytz

        bj_tz = pytz.timezone("Asia/Shanghai")
        now_bj = datetime.now(bj_tz)
        existing = [f for f in os.listdir(output_dir) if f.startswith("YB_") and f.endswith(".html")]
        next_num = len(existing) + 1
        timestamp_str = now_bj.strftime("%Y%m%d%H%M%S")
        filename = f"YB_{next_num:04d}_{timestamp_str}.html"

    filepath = os.path.join(output_dir, filename)

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
