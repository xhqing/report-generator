REPORT_DATA_SCHEMA = {
    "type": "object",
    "properties": {
        "report_date": {
            "type": "string",
            "description": "报告日期，格式：YYYY年MM月DD日",
        },
        "generation_time": {
            "type": "string",
            "description": "报告生成时间，格式：YYYY-MM-DD HH:MM:SS",
        },
        "index_data": {
            "type": "array",
            "description": "指数行情数据表",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "指数名称"},
                    "code": {"type": "string", "description": "指数代码"},
                    "price": {"type": ["number", "string"], "description": "当前最新点数"},
                    "timestamp": {"type": "string", "description": "时间戳（含时区标注）"},
                    "source": {"type": "string", "description": "数据来源链接"},
                },
            },
        },
        "stock_data": {
            "type": "array",
            "description": "个股行情数据表",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "股票名称"},
                    "code": {"type": "string", "description": "股票代码"},
                    "price": {"type": ["number", "string"], "description": "当前最新价格(HKD)"},
                    "timestamp": {"type": "string", "description": "时间戳（含时区标注）"},
                    "source": {"type": "string", "description": "数据来源链接"},
                },
            },
        },
        "etf_data": {
            "type": "array",
            "description": "ETF行情数据表",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "ETF名称"},
                    "code": {"type": "string", "description": "ETF代码"},
                    "price": {"type": ["number", "string"], "description": "当前最新价格(HKD)"},
                    "timestamp": {"type": "string", "description": "时间戳（含时区标注）"},
                    "source": {"type": "string", "description": "数据来源链接"},
                },
            },
        },
        "future_events": {
            "type": "array",
            "description": "未来一周重大事件分析",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "事件标题"},
                    "time": {"type": "string", "description": "预计时间（含时区标注）"},
                    "overview": {"type": "string", "description": "事件概述"},
                    "scenarios": {
                        "type": "array",
                        "description": "情景分析",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "description": "情景类型：base/optimistic/pessimistic"},
                                "label": {"type": "string", "description": "情景标签：基准情景/乐观情景/悲观情景"},
                                "probability": {"type": "number", "description": "概率值(%)"},
                                "description": {"type": "string", "description": "情景描述"},
                            },
                        },
                    },
                },
            },
        },
        "index_analysis": {
            "type": "array",
            "description": "指数研判",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "指数名称"},
                    "code": {"type": "string", "description": "指数代码"},
                    "current": {"type": ["number", "string"], "description": "当前点位"},
                    "trend": {"type": "string", "description": "趋势判断"},
                    "trend_probs": {
                        "type": "object",
                        "description": "趋势概率分布",
                        "properties": {
                            "震荡上行": {"type": "number"},
                            "震荡偏强": {"type": "number"},
                            "震荡偏弱": {"type": "number"},
                            "震荡下行": {"type": "number"},
                            "直接上行": {"type": "number"},
                            "直接下行": {"type": "number"},
                        },
                    },
                    "trend_reasons": {
                        "type": "object",
                        "description": "趋势情景理由",
                        "additionalProperties": {"type": "string"},
                    },
                    "high": {"type": "number", "description": "最高目标点数"},
                    "low": {"type": "number", "description": "最低目标点数"},
                    "logic": {"type": "string", "description": "核心逻辑"},
                },
            },
        },
        "stock_analysis": {
            "type": "array",
            "description": "个股分析",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "股票名称"},
                    "code": {"type": "string", "description": "股票代码"},
                    "price": {"type": ["number", "string"], "description": "当前最新价格(HKD)"},
                    "trend": {"type": "string", "description": "趋势判断"},
                    "trend_probs": {
                        "type": "object",
                        "description": "趋势概率分布",
                    },
                    "high": {"type": "number", "description": "最高目标价"},
                    "low": {"type": "number", "description": "最低目标价"},
                    "view": {"type": "string", "description": "看多看空观点：看多/看空/中性"},
                    "position": {"type": "string", "description": "仓位调整建议"},
                    "logic": {"type": "string", "description": "核心逻辑"},
                },
            },
        },
        "etf_analysis": {
            "type": "array",
            "description": "ETF分析",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "ETF名称"},
                    "code": {"type": "string", "description": "ETF代码"},
                    "price": {"type": ["number", "string"], "description": "当前最新价格"},
                    "trend": {"type": "string", "description": "趋势判断"},
                    "trend_probs": {
                        "type": "object",
                        "description": "趋势概率分布",
                    },
                    "high": {"type": "number", "description": "最高目标价"},
                    "low": {"type": "number", "description": "最低目标价"},
                    "view": {"type": "string", "description": "看多看空观点"},
                    "position": {"type": "string", "description": "仓位调整建议"},
                    "logic": {"type": "string", "description": "核心逻辑"},
                },
            },
        },
        "reasoning": {
            "type": "object",
            "description": "分析推理过程",
            "properties": {
                "macro_chain": {"type": "string", "description": "宏观判断链"},
                "index_chain": {"type": "string", "description": "指数推导链"},
                "stock_chain": {"type": "string", "description": "个股推导链"},
                "assumptions": {
                    "type": "array",
                    "description": "关键假设",
                    "items": {"type": "string"},
                },
                "risks": {
                    "type": "array",
                    "description": "风险提示",
                    "items": {"type": "string"},
                },
                "diff_from_last": {"type": "string", "description": "与上一份研报的不同之处"},
            },
        },
        "references": {
            "type": "object",
            "description": "参考资料",
            "properties": {
                "macro_policy": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"},
                            "source": {"type": "string"},
                        },
                    },
                },
                "geopolitics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"},
                            "source": {"type": "string"},
                        },
                    },
                },
                "industry": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"},
                            "source": {"type": "string"},
                        },
                    },
                },
                "technical": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"},
                            "source": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
}


def get_empty_data():
    return {
        "report_date": "",
        "generation_time": "",
        "index_data": [],
        "stock_data": [],
        "etf_data": [],
        "future_events": [],
        "index_analysis": [],
        "stock_analysis": [],
        "etf_analysis": [],
        "reasoning": {
            "macro_chain": "",
            "index_chain": "",
            "stock_chain": "",
            "assumptions": [],
            "risks": [],
            "diff_from_last": "",
        },
        "references": {
            "macro_policy": [],
            "geopolitics": [],
            "industry": [],
            "technical": [],
        },
    }
