Telegram bot that monitors our reward distribution process and sends daily statistics to our group.

Bot Functionality:
- The bot reads events from the contract that occurred in the last 24 hours.

Requirements:
- Calculate and send the daily sum of all four parameters through the bot to a Telegram chat.
- The bot should not only listen for messages but also fetch history, as it may not operate continuously (e.g., during reboots) and should be able to backfill history, especially on the first launch.
- Ideally, record all events in a PostgreSQL database for future statistical analysis and report generation.
- Generate and send reports every four hours.

Example Report Format:

Daily $AIX Stats:
- First TX: 23h50m ago
- Last TX: 1h30m ago
- AIX processed: 2,068,102.33
- AIX distributed: 79,473.32
- ETH bought: 149.71
- ETH distributed: 149.71
        
Distributor wallet: `wallet address`  
Distributor balance: `Distributor balance ETH`  
