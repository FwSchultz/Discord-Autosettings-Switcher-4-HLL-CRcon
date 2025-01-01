<h1 align="center" style="font-weight: bold;">Discord  - Autosettings Switcher 4 Hell let Loose CRcon</h1>


<p align="center">Dies ist ein  Discord-Bot zum switchen von verschiedenen Autosettings (public und competitive) im CRCON-Tools.</p>



<h2 id="layout"></h2>

<p align="center">

<img src="https://i.imgur.com/8XmDwWF.png" alt="Random Image" width="400px">
</p>

## Voraussetzunge.

1. **Python:** Version 3.12 oder höher.
2. **CRCON-API:** Zugang zu einem CRCON-Server mit gültigem API-Key.
3. **Discord Bot:** Erstelle einen Bot im [Discord Developer Portal](https://discord.com/developers/applications).
4. **JSON-Konfigurationsdateien:** Stelle sicher, dass die Dateien `public_settings.json` und `competitive_settings.json` korrekt konfiguriert sind.

## Installation

### 1. Repository klonen

```bash
# Klone das Projekt-Repository
git clone https://github.com/FwSchultz/Discord-Autosettings-Switcher-4-HLL-CRcon
cd Discord-Autosettings-Switcher-4-HLL-CRcon
```

### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3. Discord-Bot erstellen

3.1 Erstelle einen Bot unter [Discord Developer Portal](https://discord.com/developers/applications).

3.2 geht zum Reiter `Installation` und gebt dem Bot folgende Rechte unter Guild Install

```discord bot rechte
SCOPES: applications.commands und bot
PERMISSIONS: READ MESSAGE HISTORY, SEND MESSAGES, ATTACH FILES, EMBED LINKS und USE SLASH COMMANDS
```

3.3 geht zum Reiter `Bot`

```
Unter Privileged Gateway Intents: Message Content Intent aktivieren
```

### 4. CRCON-User-Rechte

Welches Konto Du auch verwendest, es muss mindestens über diese Berechtigungen verfügen:

```
- api|rcon user| Can clear the CRCON Redis cache
- api|rcon user| Can change auto settings
- api|rcon user| Can view auto settings
```

### 5. Umgebungsvariablen konfigurieren

Erstelle eine `.env`-Datei im Projektverzeichnis mit folgendem Inhalt:

```env
DISCORD_BOT_TOKEN=<DISCORD_BOT_TOKEN>
CRCON_API_URL=http://<CRCON_API_URL>:<PORT>
CRCON_API_KEY=<CRCON_API_KEY>
```

Ersetze die Platzhalter durch die tatsächlichen Werte:

- `<DISCORD_BOT_TOKEN>`: Token deines Discord-Bots.
- `<CRCON_API_URL>`: Basis-URL der CRCON-API.
- `<CRCON_API_KEY>`: API-Key für die Authentifizierung.

> [!TIP]
> eine .env ist schon vorhanden die muss nur angepasst werden.

>```shell
>cp .env.dev .env
>```

### 6. Konfigurationsdateien vorbereiten

Die Dateien `public_settings.json` und `competitive_settings.json` sind im Ordner schon vorhanden. Ihr müsst nur eure gewünschten Servereinstellungen hinzufügen bzw. abändern

> [!TIP]
> Eine Doku für die Autosettings findet ihr unter [HLL-RCON-Tool-Wiki](https://github.com/MarechJ/hll_rcon_tool/wiki/User-Guide-%E2%80%90-Main-interface-%E2%80%90-Settings-%E2%80%90-Autosettings)


## Verwendung

### Bot starten

```bash
python bot.py
```

### Verfügbare Befehle im Discord

#### 1. `/apply_settings`

Wendet die Einstellungen aus den JSON-Dateien auf den Server an und leert anschließend den Cache.

- **Syntax:** `/apply_settings <public|competitive>`
- **Beispiel:** `/apply_settings public`

#### 2. `/clear_cache`

Leert den Server-Cache.

- **Syntax:** `/clear_cache`

## Fehlerbehebung

### 1. Bot reagiert nicht auf Befehle

- Stelle sicher, dass der Bot die erforderlichen Berechtigungen hat (z. B. `application.commands`).
- Überprüfe, ob der Bot im Discord-Developer-Portal korrekt registriert ist.

### 2. API-Fehler

- **500-Fehler:** Überprüfe die Struktur der JSON-Dateien und stelle sicher, dass sie mit den API-Erwartungen übereinstimmen.
- **404-Fehler:** Vergewissere dich, dass die `CRCON_API_URL` korrekt ist.

### 3. Cache wird nicht geleert

- Stelle sicher, dass der Cache-Endpunkt `/api/clear_cache` verfügbar ist und einen leeren Payload akzeptiert (`{}`).

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe die `LICENSE`-Datei für weitere Details.

## Kontakt

Bei Fragen oder Problemen kannst du dich an den Projektmaintainer wenden:

- **Discord:** [Fw.Schultz](https://discord.gg/tKhMCr2ZYZ)
