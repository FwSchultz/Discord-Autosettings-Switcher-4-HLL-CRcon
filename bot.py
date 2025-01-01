import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import os
import asyncio
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()

# Konfiguration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CRCON_API_URL = os.getenv('CRCON_API_URL')
CRCON_API_KEY = os.getenv('CRCON_API_KEY')

HEADERS = {
    "Authorization": f"Bearer {CRCON_API_KEY}",
    "Content-Type": "application/json"
}

# Bot-Klasse
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        # Slash-Befehle synchronisieren
        await self.tree.sync()

# Bot-Instanz erstellen
bot = MyBot()

# Funktion zur Fehlerbehandlung
async def handle_api_response(response):
    try:
        print(f"Statuscode: {response.status_code}")
        print(f"Antwort: {response.text}")
        response.raise_for_status()
        return response.json() if response.text.strip() else None
    except requests.exceptions.RequestException as e:
        print(f"HTTP-Fehler: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON-Fehler: {e}")
        return None

# Cache-Funktion
async def clear_cache():
    try:
        response = requests.post(
            url=f"{CRCON_API_URL}/api/clear_cache",
            headers=HEADERS
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Fehler beim Leeren des Caches: {e}")
        return False

# Slash-Befehl: Einstellungen anwenden
@bot.tree.command(name="apply_settings", description="Wendet Server-Einstellungen an (public oder competitive) und leert den Cache.")
async def apply_settings(interaction: discord.Interaction, setting_type: str):
    if setting_type.lower() not in ["public", "competitive"]:
        await interaction.response.send_message("Ungültiger Setting-Typ. Verwende `public` oder `competitive`.")
        return

    # Lade die entsprechende Konfigurationsdatei
    file_name = f"{setting_type.lower()}_settings.json"
    if not os.path.exists(file_name):
        await interaction.response.send_message(f"Die Datei `{file_name}` wurde nicht gefunden.")
        return

    with open(file_name, "r") as file:
        settings = json.load(file)

    try:
        # Konvertiere die Einstellungen in einen JSON-String
        payload = json.dumps({"settings": json.dumps(settings)})

        # Sende die Anfrage an den Server
        response = requests.post(
            url=f"{CRCON_API_URL}/api/set_auto_settings",
            headers=HEADERS,
            data=payload  # Sende den JSON-String direkt
        )

        # Prüfe die Antwort des Servers
        if response.status_code == 200 and not response.json().get("failed", True):
            await interaction.response.send_message(f"Die `{setting_type}`-Einstellungen wurden erfolgreich angewendet.")
            
            # Führe anschließend clear_cache aus
            cache_response = requests.post(
                url=f"{CRCON_API_URL}/api/clear_cache",
                headers=HEADERS,
                json={}  # Leerer JSON-Body für clear_cache
            )

            if cache_response.status_code == 200 and not cache_response.json().get("failed", True):
                await interaction.followup.send("Der Cache wurde erfolgreich geleert.")
            else:
                await interaction.followup.send(
                    f"Die Einstellungen wurden angewendet, aber das Leeren des Caches ist fehlgeschlagen. Serverantwort: {cache_response.status_code} - {cache_response.text}"
                )
        else:
            error_message = response.json().get("error", "Unbekannter Fehler")
            await interaction.response.send_message(
                f"Fehler beim Anwenden der Einstellungen. Serverantwort: {response.status_code} - {error_message}"
            )
    except Exception as e:
        await interaction.response.send_message(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


@bot.tree.command(name="clear_cache", description="Leert den gesamten Redis-Cache des Servers.")
async def clear_cache_command(interaction: discord.Interaction):
    try:
        response = requests.post(
            url=f"{CRCON_API_URL}/api/clear_cache",
            headers=HEADERS,
            json={}  # Leerer JSON-Payload
        )
        if response.status_code == 200 and not response.json().get("failed", True):
            result = response.json().get("result", 0)
            await interaction.response.send_message(f"Der Cache wurde erfolgreich geleert. Gelöschte Einträge: {result}.")
        else:
            await interaction.response.send_message(
                f"Fehler beim Leeren des Caches. Serverantwort: {response.status_code} - {response.text}"
            )
    except Exception as e:
        await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {e}")

# Slash-Befehl: Servereinstellungen abrufen
@bot.tree.command(name="get_settings", description="Zeigt die aktuellen Server-Einstellungen an.")
async def get_settings(interaction: discord.Interaction):
    try:
        response = requests.get(
            url=f"{CRCON_API_URL}/api/get_server_settings",
            headers=HEADERS
        )
        data = await handle_api_response(response)
        if data:
            await interaction.response.send_message(f"Aktuelle Server-Einstellungen:\n```json\n{json.dumps(data, indent=4)}\n```")
        else:
            await interaction.response.send_message("Fehler beim Abrufen der Server-Einstellungen.")
    except Exception as e:
        await interaction.response.send_message(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

# Bot starten
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
