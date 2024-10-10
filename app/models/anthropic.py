# https://docs.anthropic.com/en/docs/about-claude/models

ANTHROPIC = {
    "default_model": "claude-3-5-sonnet-20241022",
    "models": {
        "claude-3-5-sonnet-20241022": {
            "costs": {
                "input": "0.000003",
                "output": "0.000015",
            },
            "capabilities": {
                "structured_outputs": False,
                "json_mode": False,
            },
        },
        "claude-3-5-sonnet-20240620": {
            "costs": {
                "input": "0.000003",
                "output": "0.000015",
            },
            "capabilities": {
                "structured_outputs": False,
                "json_mode": False,
            },
        },
        "claude-3-sonnet-20240229": {
            "costs": {
                "input": "0.000003",
                "output": "0.000015",
            },
            "capabilities": {
                "structured_outputs": False,
                "json_mode": False,
            },
        },
        "claude-3-haiku-20240307": {
            "costs": {
                "input": "0.00000025",
                "output": "0.00000125",
            },
            "capabilities": {
                "structured_outputs": False,
                "json_mode": False,
            },
        },
        "claude-3-opus-20240229": {
            "costs": {
                "input": "0.000015",
                "output": "0.000075",
            },
            "capabilities": {
                "structured_outputs": False,
                "json_mode": False,
            },
        },
    },
}
