# https://openai.com/api/pricing/

OPENAI = {
    "default_model": "gpt-4o-2024-11-20",
    "models": {
        "gpt-4o-2024-11-20": {
            "costs": {
                "input": "0.0000025",
                "input_cached": "0.00000125",
                "output": "0.00001",
            },
            "capabilities": {
                "structured_outputs": True,
                "json_mode": True,
            },
        },
        "gpt-4o-2024-08-06": {
            "costs": {
                "input": "0.0000025",
                "input_cached": "0.00000125",
                "output": "0.00001",
            },
            "capabilities": {
                "structured_outputs": True,
                "json_mode": True,
            },
        },
        "gpt-4o": {
            "costs": {
                "input": "0.0000025",
                "input_cached": "0.00000125",
                "output": "0.00001",
            },
            "capabilities": {
                "structured_outputs": True,
                "json_mode": True,
            },
        },
        "gpt-4o-mini": {
            "costs": {
                "input": "0.00000015",
                "input_cached": "0.000000075",
                "output": "0.0000006",
            },
            "capabilities": {
                "structured_outputs": True,
                "json_mode": True,
            },
        },
        "gpt-4-turbo": {
            "costs": {
                "input": "0.00001",
                "output": "0.00003",
            },
            "capabilities": {
                "structured_outputs": False,
                "json_mode": True,
            },
        },
        "gpt-4": {
            "costs": {
                "input": "0.00003",
                "output": "0.00006",
            },
            "capabilities": {
                "structured_outputs": False,
                "json_mode": True,
            },
        },
        "gpt-4-32k": {
            "costs": {
                "input": "0.00006",
                "output": "0.00012",
            },
            "capabilities": {
                "structured_outputs": False,
                "json_mode": True,
            },
        },
    },
}
