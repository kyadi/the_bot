# Trading Bot Project

## Overview
This project is an automated trading bot for the OANDA forex platform. It is designed to manage trades, calculate technical indicators, and log trading activity. The bot is modular, with components for API interaction, trade management, logging, and technical analysis.

## Features
- Automated trading using OANDA API
- Trade management with trailing stop loss and take profit
- Dynamic lot multiplier (Martingale logic) based on last trade result
- Persistent state tracking for each pair (multiplier and last outcome)
- Automatic trade result checking after close (TP hit or loss)
- Logging of all trading activity
- Technical indicator calculations
- Configurable trading pairs and settings

## Main Components
- **bot.py**: Main entry point for running the trading bot.
- **trade_manager.py**: Manages trade execution, lot sizing, and state persistence.
- **oanda_trades.py**: Analyzes trade history and determines the result of the most recent closed trade.
- **oanda_api.py**: Handles all communication with the OANDA API.
- **settings.py**: Loads and manages trading settings from `settings.json`.
- **log_wrapper.py**: Provides logging functionality for the bot and its components.
- **defs.py**: Stores constants and API credentials (ensure to secure this file!).
- **oanda_trade.py**: Represents individual trades and their properties.

## Requirements
- Python 3.x
- See `requirements.txt` for required packages (requests, pandas, etc.)

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your trading pairs and settings in `settings.json`.
3. Run the bot:
   ```bash
   python bot.py
   ```

## File Structure
- `bot.py` - Main trading bot logic
- `trade_manager.py` - Trade management and state
- `oanda_trades.py` - Trade result analysis and history
## Trade Multiplier & State Logic

This bot uses a Martingale-style multiplier for lot sizing:
- If the last trade for a pair hit take profit (TP), the multiplier resets to 1.
- If the last trade was a loss, the multiplier doubles for the next trade.
- The state for each pair (multiplier and last outcome) is stored in `pair_state.json` and is persistent across runs.
- After closing a trade, the bot checks the result using `oanda_trades.py` and updates the multiplier accordingly.

**Example `pair_state.json`:**
```json
{
   "EUR_USD": {"multiplier": 2, "last_outcome": "LOSS"},
   "GBP_USD": {"multiplier": 1, "last_outcome": "TP_HIT"}
}
```

This ensures the bot adapts its lot size based on recent performance, aiming to recover losses after a losing trade.
- `oanda_api.py` - OANDA API interface
- `settings.py` - Settings loader
- `log_wrapper.py` - Logging utility
- `defs.py` - Constants and credentials
- `oanda_trade.py` - Trade object
- `requirements.txt` - Python dependencies
- `settings.json` - Trading configuration
- `logs/` - Log files

## Security Note
**Do not share your `defs.py` file or API credentials.**

## License
This project is for educational and personal use. Please review OANDA's terms of service before live trading.
