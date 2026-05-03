import html


def _esc(val):
    if val is None:
        return ""
    return html.escape(str(val))


def _fmt_price(val):
    if val is None or val == "":
        return "-"
    try:
        return f"{float(val):,.2f}"
    except (ValueError, TypeError):
        return _esc(val)


def _fmt_pct(current, target):
    if current is None or target is None:
        return "-"
    try:
        c, t = float(current), float(target)
        if c == 0:
            return "-"
        pct = (t - c) / c * 100
        return f"{pct:.2f}%"
    except (ValueError, TypeError):
        return "-"


def _make_source_link(val, source):
    if not source:
        return _esc(val) if val else "-"
    url = str(source)
    if url.startswith("http"):
        return f'<a href="{_esc(url)}" target="_blank">{_esc(val) if val else "来源"}</a>'
    return _esc(val) if val else "-"


def _format_trend_probs(probs):
    if not probs:
        return ""
    trend_order = ["震荡上行", "震荡偏强", "震荡偏弱", "震荡下行", "直接上行", "直接下行"]
    parts = []
    for trend in trend_order:
        prob = probs.get(trend, 0)
        parts.append(f"{trend}({prob}%)")
    return "<br>".join(parts)


CSS_STYLES = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; line-height: 1.8; color: #2c3e50; background: #f8f9fa; }
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }
.header { background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; text-align: center; }
.header h1 { font-size: 2em; margin-bottom: 10px; letter-spacing: 2px; }
.header .date { font-size: 1.1em; opacity: 0.9; }
.toc { background: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
.toc h2 { color: #1a237e; margin-bottom: 20px; border-bottom: 2px solid #1a237e; padding-bottom: 10px; }
.toc ul { list-style: none; padding-left: 0; }
.toc li { margin: 8px 0; }
.toc a { color: #3949ab; text-decoration: none; font-size: 1.05em; transition: color 0.2s; }
.toc a:hover { color: #1a237e; text-decoration: underline; }
.toc .sub { padding-left: 25px; }
.toc .sub a { font-size: 0.95em; color: #5c6bc0; }
.section { background: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
.section h2 { color: #1a237e; margin-bottom: 20px; border-bottom: 2px solid #e8eaf6; padding-bottom: 10px; font-size: 1.5em; }
.section h3 { color: #283593; margin: 20px 0 15px; font-size: 1.2em; }
.section h4 { color: #3949ab; margin: 15px 0 10px; font-size: 1.05em; }
.data-table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.9em; }
.data-table th { background: #e8eaf6; color: #1a237e; padding: 12px 8px; text-align: center; font-weight: 600; border: 1px solid #c5cae9; }
.data-table td { padding: 10px 8px; text-align: center; border: 1px solid #e0e0e0; }
.data-table tr:nth-child(even) { background: #f5f5f5; }
.data-table tr:hover { background: #e8eaf6; }
.data-table a { color: #3949ab; text-decoration: underline; }
.event-card { background: #f8f9fa; border-left: 4px solid #3949ab; padding: 15px 20px; margin: 15px 0; border-radius: 0 8px 8px 0; }
.event-card h4 { color: #1a237e; margin-bottom: 8px; }
.event-card .time { color: #e65100; font-weight: 600; font-size: 0.9em; }
.scenario { display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 0.85em; margin: 3px; }
.scenario.base { background: #e3f2fd; color: #1565c0; }
.scenario.optimistic { background: #e8f5e9; color: #2e7d32; }
.scenario.pessimistic { background: #fce4ec; color: #c62828; }
.index-card { margin-bottom: 25px; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #1a237e; }
.index-card h4 { color: #1a237e; margin-bottom: 10px; }
.reasoning-chain { background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 15px 0; }
.reasoning-chain h4 { color: #6a1b9a; }
.ref-list { font-size: 0.9em; }
.ref-list li { margin: 8px 0; }
.ref-list a { color: #3949ab; }
.footer { text-align: center; color: #9e9e9e; padding: 20px; font-size: 0.85em; }
.disclaimer { background: #fff3e0; padding: 15px; border-radius: 8px; margin: 20px 0; font-size: 0.85em; color: #e65100; }
.placeholder { color: #9e9e9e; font-style: italic; }
"""


def _build_header(data):
    report_date = data.get("report_date", "") or '<span class="placeholder">[报告日期]</span>'
    return f"""
<div class="header">
<h1>全球金融市场标的定制化深度分析报告</h1>
<div class="date">报告日期：{report_date}（北京时间）</div>
</div>"""


def _build_toc(data):
    items = [
        '<li><a href="#section1">一、市场数据</a></li>',
        '<li><a href="#section2">二、未来一周重大事件分析</a></li>',
        '<li><a href="#section3">三、指数研判</a></li>',
        '<li><a href="#section4">四、ETF分析</a></li>',
        '<li><a href="#section5">五、个股分析</a></li>',
        '<li><a href="#section6">六、分析推理过程</a></li>',
        '<li><a href="#section7">七、参考资料</a></li>',
    ]

    return f"""
<div class="toc">
<h2>目录</h2>
<ul>
{"".join(items)}
</ul>
</div>"""


def _build_market_data_section(data):
    index_rows = ""
    for item in data.get("index_data", []):
        price_val = _fmt_price(item.get("price"))
        source_link = _make_source_link(price_val, item.get("source"))
        index_rows += f"""<tr>
<td>{_esc(item.get("name"))}</td>
<td>{_esc(item.get("code"))}</td>
<td>{source_link}</td>
<td>{_esc(item.get("timestamp"))}</td>
<td>{_make_source_link("来源", item.get("source"))}</td>
</tr>"""

    stock_rows = ""
    for item in data.get("stock_data", []):
        stock_rows += f"""<tr>
<td>{_esc(item.get("name"))}</td>
<td>{_esc(item.get("code"))}</td>
<td>{_fmt_price(item.get("price"))}</td>
<td>{_esc(item.get("timestamp"))}</td>
<td>{_make_source_link("来源", item.get("source"))}</td>
</tr>"""

    etf_rows = ""
    for item in data.get("etf_data", []):
        etf_rows += f"""<tr>
<td>{_esc(item.get("name"))}</td>
<td>{_esc(item.get("code"))}</td>
<td>{_fmt_price(item.get("price"))}</td>
<td>{_esc(item.get("timestamp"))}</td>
<td>{_make_source_link("来源", item.get("source"))}</td>
</tr>"""

    if not index_rows:
        index_rows = '<tr><td colspan="5" class="placeholder">[指数数据待填充]</td></tr>'
    if not stock_rows:
        stock_rows = '<tr><td colspan="5" class="placeholder">[个股数据待填充]</td></tr>'
    if not etf_rows:
        etf_rows = '<tr><td colspan="5" class="placeholder">[ETF数据待填充]</td></tr>'

    return f"""
<div class="section" id="section1">
<h2>一、市场数据</h2>

<h3>1.1 指数数据</h3>
<table class="data-table">
<thead>
<tr><th>指数名称</th><th>指数代码</th><th>当前最新点数</th><th>时间戳</th><th>数据来源</th></tr>
</thead>
<tbody>
{index_rows}
</tbody>
</table>

<h3>1.2 个股数据</h3>
<table class="data-table">
<thead>
<tr><th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th><th>时间戳</th><th>数据来源</th></tr>
</thead>
<tbody>
{stock_rows}
</tbody>
</table>

<h3>1.3 ETF数据</h3>
<table class="data-table">
<thead>
<tr><th>ETF名称</th><th>ETF代码</th><th>当前最新价格(HKD)</th><th>时间戳</th><th>数据来源</th></tr>
</thead>
<tbody>
{etf_rows}
</tbody>
</table>
</div>"""


def _build_events_section(data):
    events = data.get("future_events", [])
    if not events:
        return """
<div class="section" id="section2">
<h2>二、未来一周重大事件分析</h2>
<p class="placeholder">[重大事件分析待填充]</p>
</div>"""

    cards = ""
    for i, event in enumerate(events, 1):
        scenarios_html = ""
        for s in event.get("scenarios", []):
            s_type = s.get("type", "base")
            s_label = s.get("label", "")
            s_prob = s.get("probability", 0)
            s_desc = s.get("description", "")
            scenarios_html += f'<p><span class="scenario {s_type}">{s_label}（概率{s_prob}%）：{s_desc}</span></p>'

        cards += f"""
<div class="event-card">
<h4>{i}. {_esc(event.get("title"))}</h4>
<p class="time">预计时间：{_esc(event.get("time"))}</p>
<p><strong>事件概述：</strong>{_esc(event.get("overview"))}</p>
<p><strong>可能的市场影响情景分析：</strong></p>
{scenarios_html}
</div>"""

    return f"""
<div class="section" id="section2">
<h2>二、未来一周重大事件分析</h2>
{cards}
</div>"""


def _build_index_analysis_section(data):
    items = data.get("index_analysis", [])
    if not items:
        return """
<div class="section" id="section3">
<h2>三、指数研判</h2>
<p class="placeholder">[指数研判待填充]</p>
</div>"""

    cards = ""
    for ia in items:
        probs = ia.get("trend_probs", {})
        reasons = ia.get("trend_reasons", {})
        trend_items = []
        for scenario, prob in probs.items():
            reason = reasons.get(scenario, "")
            if reason:
                trend_items.append(f"<li><strong>{scenario}（{prob}%）</strong>：{_esc(reason)}</li>")
            else:
                trend_items.append(f"<li><strong>{scenario}（{prob}%）</strong></li>")

        trend_list = "\n".join(trend_items)
        current = _fmt_price(ia.get("current"))
        high = _fmt_price(ia.get("high"))
        low = _fmt_price(ia.get("low"))
        high_pct = _fmt_pct(ia.get("current"), ia.get("high"))
        low_pct = _fmt_pct(ia.get("current"), ia.get("low"))

        cards += f"""
<div class="index-card">
<h4>{_esc(ia.get("name"))}（{_esc(ia.get("code"))}）| 当前点位：{current}</h4>
<p style="margin: 8px 0;"><strong>未来半年趋势预判：</strong></p>
<ul style="margin: 8px 0 8px 25px; padding-left: 0;">{trend_list}</ul>
<p style="margin: 8px 0;"><strong>截止年底最高目标点数：</strong>{high}（涨幅 {high_pct}）</p>
<p style="margin: 8px 0;"><strong>截止年底最低目标点数：</strong>{low}（跌幅 {low_pct}）</p>
<p style="margin: 8px 0;"><strong>核心逻辑：</strong>{_esc(ia.get("logic"))}</p>
</div>"""

    return f"""
<div class="section" id="section3">
<h2>三、指数研判</h2>
{cards}
</div>"""


def _build_stock_analysis_section(data):
    items = data.get("stock_analysis", [])
    if not items:
        return '<div class="section" id="section5"><h2>五、个股分析</h2><p class="placeholder">[个股分析待填充]</p></div>'

    rows = ""
    for sa in items:
        high_rise = _fmt_pct(sa.get("price"), sa.get("high"))
        low_fall = _fmt_pct(sa.get("price"), sa.get("low"))
        trend_display = f"{_esc(sa.get('trend'))}<br>{_format_trend_probs(sa.get('trend_probs'))}"
        rows += f"""<tr>
<td>{_esc(sa.get("name"))}</td>
<td>{_esc(sa.get("code"))}</td>
<td>{_fmt_price(sa.get("price"))}</td>
<td>{trend_display}</td>
<td>{_fmt_price(sa.get("high"))}</td>
<td>{high_rise}</td>
<td>{_fmt_price(sa.get("low"))}</td>
<td>{low_fall}</td>
<td>{_esc(sa.get("view"))}</td>
<td>{_esc(sa.get("position"))}</td>
<td>{_esc(sa.get("logic"))}</td>
</tr>"""

    return f"""
<div class="section" id="section5">
<h2>五、个股分析</h2>
<table class="data-table">
<thead>
<tr>
<th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th>
<th>未来半年趋势预判</th><th>截止年底最高目标价</th><th>最高目标价涨幅</th>
<th>截止年底最低目标价</th><th>最低目标价跌幅</th>
<th>当前看多看空观点</th><th>当前仓位调整建议</th>
<th>核心逻辑</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>"""


def _build_etf_analysis_section(data):
    items = data.get("etf_analysis", [])
    if not items:
        return '<div class="section" id="section4"><h2>四、ETF分析</h2><p class="placeholder">[ETF分析待填充]</p></div>'

    rows = ""
    for ea in items:
        high_rise = _fmt_pct(ea.get("price"), ea.get("high"))
        low_fall = _fmt_pct(ea.get("price"), ea.get("low"))
        trend_display = f"{_esc(ea.get('trend'))}<br>{_format_trend_probs(ea.get('trend_probs'))}"
        rows += f"""<tr>
<td>{_esc(ea.get("name"))}</td>
<td>{_esc(ea.get("code"))}</td>
<td>{_fmt_price(ea.get("price"))}</td>
<td>{trend_display}</td>
<td>{_fmt_price(ea.get("high"))}</td>
<td>{high_rise}</td>
<td>{_fmt_price(ea.get("low"))}</td>
<td>{low_fall}</td>
<td>{_esc(ea.get("view"))}</td>
<td>{_esc(ea.get("position"))}</td>
<td>{_esc(ea.get("logic"))}</td>
</tr>"""

    return f"""
<div class="section" id="section4">
<h2>四、ETF分析</h2>
<table class="data-table">
<thead>
<tr>
<th>ETF名称</th><th>ETF代码</th><th>当前最新价格</th>
<th>未来半年趋势预判</th><th>截止年底最高目标价</th><th>最高目标价涨幅</th>
<th>截止年底最低目标价</th><th>最低目标价跌幅</th>
<th>当前看多看空观点</th><th>当前仓位调整建议</th>
<th>核心逻辑</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>"""


def _build_reasoning_section(data):
    r = data.get("reasoning", {})
    if not r:
        r = {}

    macro = r.get("macro_chain", "")
    index_chain = r.get("index_chain", "")
    stock_chain = r.get("stock_chain", "")
    assumptions = r.get("assumptions", [])
    risks = r.get("risks", [])
    diff = r.get("diff_from_last", "")

    has_content = any([macro, index_chain, stock_chain, assumptions, risks, diff])

    if not has_content:
        return """
<div class="section" id="section6">
<h2>六、分析推理过程</h2>
<p class="placeholder">[分析推理过程待填充]</p>
</div>"""

    assumptions_html = ""
    for i, a in enumerate(assumptions, 1):
        assumptions_html += f"<p>① {_esc(a)}</p>" if i == 1 else f"<p>{'①②③④⑤⑥⑦⑧⑨⑩'[i-1]} {_esc(a)}</p>"

    risks_html = ""
    for i, rk in enumerate(risks, 1):
        risks_html += f"<p>{'①②③④⑤⑥⑦⑧⑨⑩'[i-1]} <strong>{_esc(rk)}</strong></p>"

    sections = ""
    if macro:
        sections += f"""
<div class="reasoning-chain">
<h4>1. 宏观判断链</h4>
<p><strong>重大事件 → 宏观环境影响 → 市场整体方向</strong></p>
<p>{_esc(macro)}</p>
</div>"""
    if index_chain:
        sections += f"""
<div class="reasoning-chain">
<h4>2. 指数推导链</h4>
<p><strong>宏观判断 → 各指数差异化表现</strong></p>
<p>{_esc(index_chain)}</p>
</div>"""
    if stock_chain:
        sections += f"""
<div class="reasoning-chain">
<h4>3. 个股推导链</h4>
<p><strong>宏观+行业+个股事件 → 个股趋势判断</strong></p>
<p>{_esc(stock_chain)}</p>
</div>"""
    if assumptions:
        sections += f"""
<div class="reasoning-chain">
<h4>4. 关键假设</h4>
{assumptions_html}
</div>"""
    if risks:
        sections += f"""
<div class="reasoning-chain">
<h4>5. 风险提示</h4>
{risks_html}
</div>"""
    if diff:
        sections += f"""
<div class="reasoning-chain">
<h4>6. 与上一份研报的不同之处</h4>
<p>{_esc(diff)}</p>
</div>"""

    return f"""
<div class="section" id="section6">
<h2>六、分析推理过程</h2>
{sections}
</div>"""


def _build_references_section(data):
    refs = data.get("references", {})
    if not refs:
        refs = {}

    categories = [
        ("macro_policy", "宏观政策类"),
        ("geopolitics", "地缘政治类"),
        ("industry", "行业/公司类"),
        ("technical", "技术分析类"),
    ]

    has_any = any(refs.get(k) for k, _ in categories)
    if not has_any:
        return """
<div class="section" id="section7">
<h2>七、参考资料</h2>
<p class="placeholder">[参考资料待填充]</p>
</div>"""

    sections = ""
    for key, label in categories:
        items = refs.get(key, [])
        if not items:
            continue
        lis = ""
        for item in items:
            title = item.get("title", "")
            url = item.get("url", "")
            source = item.get("source", "")
            if url:
                lis += f'<li><a href="{_esc(url)}" target="_blank">{_esc(title)}</a>'
                if source:
                    lis += f" — {_esc(source)}"
                lis += "</li>"
            else:
                lis += f"<li>{_esc(title)}"
                if source:
                    lis += f" — {_esc(source)}"
                lis += "</li>"

        sections += f"""
<h3>{label}</h3>
<ul class="ref-list">
{lis}
</ul>"""

    return f"""
<div class="section" id="section7">
<h2>七、参考资料</h2>
{sections}
</div>"""


def _build_disclaimer():
    return """
<div class="disclaimer">
<strong>免责声明：</strong>本报告仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。报告中的观点和预测基于当前市场信息和分析师判断，可能随市场变化而调整。过往业绩不代表未来表现。
</div>"""


def _build_footer(data):
    gen_time = data.get("generation_time", "") or '<span class="placeholder">[生成时间]</span>'
    return f"""
<div class="footer">
<p>全球金融市场标的定制化深度分析报告 | 报告生成时间：{gen_time}（北京时间）</p>
<p>数据来源：Longport API、新华网、财联社、新浪财经、东方财富网、Nasdaq官网、AP News等</p>
</div>"""


def render_report(data):
    header = _build_header(data)
    toc = _build_toc(data)
    market_data = _build_market_data_section(data)
    events = _build_events_section(data)
    index_analysis = _build_index_analysis_section(data)
    etf_analysis = _build_etf_analysis_section(data)
    stock_analysis = _build_stock_analysis_section(data)
    reasoning = _build_reasoning_section(data)
    references = _build_references_section(data)
    disclaimer = _build_disclaimer()
    footer = _build_footer(data)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全球金融市场标的定制化深度分析报告 - {data.get('report_date', '')}</title>
<style>
{CSS_STYLES}
</style>
</head>
<body>
<div class="container">

{header}

{toc}

{market_data}

{events}

{index_analysis}

{etf_analysis}

{stock_analysis}

{reasoning}

{references}

{disclaimer}

{footer}

</div>
</body>
</html>"""
