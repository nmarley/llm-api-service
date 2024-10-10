# Demo Repo - Python LLM API Wrapper Service

This is a demo of a robust Python-based LLM API wrapper service that integrates multiple providers (Anthropic, OpenAI, and xAI), implements fallback mechanisms for enhanced reliability, and delivers diverse endpoints for tasks such as generating email responses, rewriting messages, and summarizing text. The service is designed to be highly configurable, with support for custom tool configurations and precise cost accounting.

## Install

```bash
python3 -mvenv ./.venv
./.venv/bin/pip install -r requirements.txt
```

## Format / Lint Check

```bash
./.venv/bin/ruff  format
15 files left unchanged

./.venv/bin/ruff  check
All checks passed!
```

## Set API keys

Copy the `.env.example` file to `.env` and fill in the values for your API
keys. Currently OpenAI, Anthropic, and xAI are supported.

## Start dev server

```bash
./.venv/bin/python3 run.py
```

## Start server with Gunicorn, use this for prod deployment behind nginx

```bash
./.venv/bin/gunicorn --config gunicorn.conf.py
```

## Using the API, Examples

### Email Response Generation

Generate a response to an email, using the Anthropic API w/the default model:

```bash
curl --include --header 'Content-type: application/json' --request POST \
 --data '{"email": "Hello, how are you? Please respond with your earliest availability"}' \
 http://localhost:6000/anthropic/email

HTTP/1.1 200 OK
Server: Werkzeug/3.0.4 Python/3.12.7
Date: Tue, 15 Jan 2025 05:02:56 GMT
Content-Type: application/json
Content-Length: 677
Access-Control-Allow-Origin: *
Connection: close

{"data":{"costs":{"input_cost":"0.002307","input_token_cost":"0.000003","output_cost":"0.002325","output_token_cost":"0.000015","total_cost":"0.004632"},"model":"claude-3-5-sonnet-20241022","result":{"body":"Hi there,\n\nThank you for reaching out. I hope you're doing well too.\n\nPlease let me know what type of availability you're looking for, and I'll be happy to provide my schedule. This will help me share the most relevant time slots with you.\n\nLooking forward to your response.\n\nBest regards","enthusiasm_level":"medium","subject":"Re: Availability","tone":"semi-formal"},"timestamp":"2025-01-21T02:00:57.866201","usage":{"input_tokens":769,"output_tokens":155}}}
```

### Text Summarization

Summarize a text using the OpenAI API w/a specific model:

```bash
curl --include --header 'Content-type: application/json' --request POST \
 --data '{"text": "Johannes Gutenberg (1398 – 1468) was a German goldsmith and publisher who introduced printing to Europe. His introduction of mechanical movable type printing to Europe started the Printing Revolution and is widely regarded as the most important event of the modern period. It played a key role in the scientific revolution and laid the basis for the modern knowledge-based economy and the spread of learning to the masses", "model": "gpt-4-turbo"}' \
http://localhost:6000/openai/summarize

HTTP/1.1 200 OK
Server: Werkzeug/3.0.4 Python/3.12.7
Date: Tue, 21 Jan 2025 02:06:38 GMT
Content-Type: application/json
Content-Length: 727
Access-Control-Allow-Origin: *
Connection: close

{"data":{"costs":{"input_cost":"0.00210","input_token_cost":"0.00001","output_cost":"0.00255","output_token_cost":"0.00003","total_cost":"0.00465"},"model":"gpt-4-turbo-2024-04-09","result":{"text_summary":"Johannes Gutenberg (1398 \u2013 1468) was a German goldsmith and publisher who introduced printing to Europe. His introduction of mechanical movable type printing to Europe started the Printing Revolution and is widely regarded as the most important event of the modern period. It played a key role in the scientific revolution and laid the basis for the modern knowledge-based economy and the spread of learning to the masses"},"timestamp":"2025-01-21T02:06:38.885834","usage":{"input_tokens":210,"output_tokens":85}}}
```

### Professional Message Rewrite

Rewrite a message:

```bash
curl --include --header 'Content-type: application/json' --request POST \
 --data '{"message": "Yo dawg! :D I need a job pretty bad, you got any leads for a good gig?"}' \
 http://localhost:6000/openai/rewrite

HTTP/1.1 200 OK
Server: Werkzeug/3.0.4 Python/3.12.7
Date: Tue, 21 Jan 2025 02:49:57 GMT
Content-Type: application/json
Content-Length: 522
Access-Control-Allow-Origin: *
Connection: close

{"data":{"costs":{"input_cost":"0.0005750","input_token_cost":"0.0000025","output_cost":"0.00043","output_token_cost":"0.00001","total_cost":"0.0010050"},"model":"gpt-4o-2024-11-20","result":{"rewritten_message":"Hello, I hope you're doing well. I am currently seeking employment opportunities and was wondering if you could provide any leads or suggestions for potential positions. Your assistance would be greatly appreciated."},"timestamp":"2025-01-21T02:49:57.627636","usage":{"input_tokens":230,"output_tokens":43}}}
```

### Basic Prompt Passthru

Write any prompt, in this case request a haiku about tea and Unix, using the Claude 3 Haiku model

```bash
curl --include --header 'Content-type: application/json' --request POST \
 --data '{"message": "Write me a haiku about tea and unix", "model": "claude-3-haiku-20240307"}' \
 http://localhost:6000/anthropic/prompt_response
HTTP/1.1 200 OK
Server: Werkzeug/3.0.4 Python/3.12.7
Date: Tue, 21 Jan 2025 02:53:57 GMT
Content-Type: application/json
Content-Length: 414
Access-Control-Allow-Origin: *
Connection: close

{"data":{"costs":{"input_cost":"0.00011625","input_token_cost":"0.00000025","output_cost":"0.00007875","output_token_cost":"0.00000125","total_cost":"0.00019500"},"model":"claude-3-haiku-20240307","result":{"summary":"Haiku about tea and Unix:\n\nSteaming cup of tea,\nTerminal commands flow swift,\nUnix, nature blends."},"timestamp":"2025-01-21T02:53:57.226603","usage":{"input_tokens":465,"output_tokens":63}}}
```
