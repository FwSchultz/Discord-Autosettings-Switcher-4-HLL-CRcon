
<h1 align="center" style="font-weight: bold;">Discord - Autosettings Switcher for Hell Let Loose CRcon</h1>

<p align="center">This is a Discord bot for switching between different autosettings (public and competitive) in the CRCON tool.</p>

<h2 id="layout"></h2>

<p align="center">
<img src="https://i.imgur.com/8XmDwWF.png" alt="Random Image" width="250px">
</p>

## Requirements

1. **Python:** Version 3.12 or higher.
2. **CRCON-API:** Access to a CRCON server with a valid API key.
3. **Discord Bot:** Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications).
4. **JSON Configuration Files:** Ensure the files `public_settings.json` and `competitive_settings.json` are correctly configured.

## Installation

### 1. Clone the Repository

```bash
# Clone the project repository
git clone https://github.com/FwSchultz/Discord-Autosettings-Switcher-4-HLL-CRcon
cd Discord-Autosettings-Switcher-4-HLL-CRcon
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a Discord Bot

3.1 Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications).

3.2 Go to the `OAuth2` tab and grant the bot the following permissions under `Scopes` and `Bot Permissions`:

```discord bot permissions
SCOPES: applications.commands and bot
PERMISSIONS: READ MESSAGE HISTORY, SEND MESSAGES, ATTACH FILES, EMBED LINKS, and USE SLASH COMMANDS
```

3.3 Navigate to the `Bot` tab:

```
Enable the "Message Content Intent" under Privileged Gateway Intents.
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory with the following content:

```env
DISCORD_BOT_TOKEN=<DISCORD_BOT_TOKEN>
CRCON_API_URL=http://<CRCON_API_URL>:<PORT>
CRCON_API_KEY=<CRCON_API_KEY>
ALLOWED_ROLE_IDS=<ROLE_ID1,ROLE_ID2,...>
LANGUAGE=<LANGUAGE>
```

Replace the placeholders with your actual values:

- `<DISCORD_BOT_TOKEN>`: Your Discord bot token.
- `<CRCON_API_URL>`: Base URL of the CRCON API.
- `<CRCON_API_KEY>`: API key for authentication.
- `<ROLE_ID1,ROLE_ID2,...>`: Discord Role ID that can use that Tool
- `<LANGUAGE>`: Available languages: [‘de’, ‘en’, ‘fr’, ‘es’]

> [!TIP]
> A `.env` file template is already provided; you just need to modify it:

```shell
cp .env.dev .env
```

### 5. Prepare Configuration Files

The files `public_settings.json` and `competitive_settings.json` are already included in the folder. You just need to add or modify the desired server settings.

> [!TIP]
> Documentation for the autosettings can be found in the [HLL RCON Tool Wiki](https://github.com/MarechJ/hll_rcon_tool/wiki/User-Guide-%E2%80%90-Main-interface-%E2%80%90-Settings-%E2%80%90-Autosettings).

## Usage

### Start the Bot

```bash
python bot.py
```

### Available Commands in Discord

#### 1. `/apply_settings`

Applies settings from the JSON files to the server and clears the cache afterward.

- **Syntax:** `/apply_settings <public|competitive>`
- **Example:** `/apply_settings public`

#### 2. `/clear_cache`

Clears the server cache.

- **Syntax:** `/clear_cache`

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or issues, contact the project maintainer:

- **Discord:** [Fw.Schultz](https://discord.gg/tKhMCr2ZYZ)
