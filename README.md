# Inference Policy Gate

Rate limiting and content policy for LLMs

## Features

- Rate limiting by user/API key
- Token counting (word-based estimator)
- Budget management per user
- Token bucket algorithm (per-minute and per-hour limits)
- JSON file configuration persistence
- CLI for configuration management

## Usage

```bash
# Initialize config
python -m src.cli init --requests 60 --requests-hour 1000 --tokens 100000

# Show config
python -m src.cli show

# Check if request is allowed
python -m src.cli check user1 100

# Check user status
python -m src.cli status user1

# Reset user limits
python -m src.cli reset user1
```

## Testing

```bash
pytest tests/ -v
```

## Security

- Uses synthetic/test data only
- No real credentials or production systems

## License

MIT
