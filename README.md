# Discord Bot mit CRCON-Integration

Ein Discord-Bot zur Verwaltung von Servereinstellungen des CRCON-Tools, einschließlich der Funktionen:

- Anwenden von Servereinstellungen (`/apply_settings`)
- Leeren des Server-Caches (`/clear_cache`)

## Voraussetzunge.

1. **Python:** Version 3.8 oder höher.
2. **CRCON-API:** Zugang zu einem CRCON-Server mit gültigem API-Key.
3. **Discord Bot:** Erstelle einen Bot im [Discord Developer Portal](https://discord.com/developers/applications).
4. **JSON-Konfigurationsdateien:** Stelle sicher, dass die Dateien `public_settings.json` und `competitive_settings.json` korrekt konfiguriert sind.

## Installation

### 1. Repository klonen

```bash
# Klone das Projekt-Repository
git clone <REPOSITORY_URL>
cd <REPOSITORY_ORDNER>
```

### 2. Virtuelle Umgebung erstellen und aktivieren

```bash
python3 -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Umgebungsvariablen konfigurieren

Erstelle eine `.env`-Datei im Projektverzeichnis mit folgendem Inhalt:

```env
DISCORD_BOT_TOKEN=<DISCORD_BOT_TOKEN>
CRCON_API_URL=http://<CRCON_API_URL>:<PORT>/api
CRCON_API_KEY=<CRCON_API_KEY>
```

Ersetze die Platzhalter durch die tatsächlichen Werte:

- `<DISCORD_BOT_TOKEN>`: Token deines Discord-Bots.
- `<CRCON_API_URL>`: Basis-URL der CRCON-API.
- `<CRCON_API_KEY>`: API-Key für die Authentifizierung.

### 5. Konfigurationsdateien vorbereiten

Erstelle die Dateien `public_settings.json` und `competitive_settings.json` im Projektordner mit den gewünschten Servereinstellungen, z. B.:

#### `public_settings.json`

```json
{
  "type": "public",
  "friendly_fire": false,
  "max_players": 100,
  "allow_vote_kick": true
}
```

#### `competitive_settings.json`

```json
{
  "type": "competitive",
  "friendly_fire": true,
  "max_players": 80,
  "allow_vote_kick": false
}
```

## Verwendung

### Bot starten

```bash
python bot.py
```

### Verfügbare Befehle

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

- **Discord:** [Dein Discord-Name]
- **E-Mail:** [Deine E-Mail-Adresse]
