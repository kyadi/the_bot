# Trading Bot Project

## Overview
This project is an automated trading bot for the OANDA forex platform. It is designed to manage trades, calculate technical indicators, and log trading activity. The bot is modular, with components for API interaction, trade management, logging, and technical analysis.

## Features
- Automated trading using OANDA API
- Trade management with trailing stop loss and take profit
- Logging of all trading activity
- Technical indicator calculations
- Configurable trading pairs and settings

## Main Components
- **bot.py**: Main entry point for running the trading bot.
- **trade_manager.py**: Manages trade execution, lot sizing, and state persistence.
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
