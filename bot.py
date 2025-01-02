import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from api_client import APIClient
import json
import asyncio

# Umgebungsvariablen laden
load_dotenv()

def load_language(lang_code: str) -> dict:
    """Lädt die Sprachdatei basierend auf dem angegebenen Sprachcode."""
    with open("languages.json", "r", encoding="utf-8") as lang_file:
        languages = json.load(lang_file)
    print(f"Verfügbare Sprachen: {list(languages.keys())}")  # Debug-Ausgabe
    return languages.get(lang_code, languages["en"])  # Fallback auf Englisch

# Konfiguration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ALLOWED_ROLE_IDS = list(map(int, os.getenv('ALLOWED_ROLE_IDS', '').split(',')))  # Liste von Rollen-IDs
LANGUAGE = os.getenv("LANGUAGE", "en").strip().lower()  # Sprache aus .env laden und bereinigen
print(f"LANGUAGE aus .env: '{LANGUAGE}'")  # Debug-Ausgabe
LANG_STRINGS = load_language(LANGUAGE)
print(f"Geladene Sprachstrings: {LANG_STRINGS}")  # Debug-Ausgabe


# Bot-Klasse
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.guilds = True  # Für Zugriff auf Rollen erforderlich
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        # Slash-Befehle synchronisieren
        await self.tree.sync()

# Bot-Instanz erstellen
bot = MyBot()

# Rollenüberprüfung
def has_required_role(interaction: discord.Interaction) -> bool:
    """Prüft, ob der Nutzer mindestens eine der erlaubten Rollen besitzt."""
    user_roles = {role.id for role in interaction.user.roles}
    return any(role_id in user_roles for role_id in ALLOWED_ROLE_IDS)

# View mit Dropdown-Menü erstellen
class SettingsDropdown(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SettingsSelect())

class SettingsSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Public", description=LANG_STRINGS["settings_applied"].format(setting_type="Public"), value="public"),
            discord.SelectOption(label="Competitive", description=LANG_STRINGS["settings_applied"].format(setting_type="Competitive"), value="competitive"),
        ]
        super().__init__(placeholder=LANG_STRINGS["apply_settings_prompt"], min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Defer the interaction to allow follow-up messages
        await interaction.response.defer()

        setting_type = self.values[0].lower()
        file_name = f"{setting_type}_settings.json"
        if not os.path.exists(file_name):
            followup_message = await interaction.followup.send(
                LANG_STRINGS["file_not_found"].format(file_name=file_name), ephemeral=True
            )
            await asyncio.sleep(60)
            await followup_message.delete()
            return

        with open(file_name, "r") as file:
            settings = json.load(file)

        response = APIClient.apply_settings(settings)
        if response and not response.get("failed", True):
            followup_message = await interaction.followup.send(
                LANG_STRINGS["settings_applied"].format(setting_type=setting_type)
            )
        else:
            error_message = response.get("error", LANG_STRINGS["error_occurred"].format(error_message="Unknown Error"))
            followup_message = await interaction.followup.send(
                LANG_STRINGS["settings_apply_failed"].format(error_message=error_message)
            )

        await asyncio.sleep(60)
        await followup_message.delete()

# Slash-Befehl: Dropdown-Menü anzeigen
@bot.tree.command(name="apply_settings", description=LANG_STRINGS["apply_settings_prompt"])
async def apply_settings_command(interaction: discord.Interaction):
    if not has_required_role(interaction):
        await interaction.response.send_message(LANG_STRINGS["no_permission"], ephemeral=True)
        await asyncio.sleep(60)
        return

    view = SettingsDropdown()
    await interaction.response.send_message(LANG_STRINGS["apply_settings_prompt"], view=view)
    await asyncio.sleep(60)

# Slash-Befehl: Cache leeren
@bot.tree.command(name="clear_cache", description="Clear the server cache.")
async def clear_cache_command(interaction: discord.Interaction):
    if not has_required_role(interaction):
        await interaction.response.send_message(LANG_STRINGS["no_permission"], ephemeral=True)
        await asyncio.sleep(60)
        return

    try:
        cache_response = APIClient.clear_cache()
        if cache_response and not cache_response.get("failed", True):
            result = cache_response.get("result", 0)
            await interaction.response.send_message(
                LANG_STRINGS["cache_cleared"].format(result=result), ephemeral=False
            )
        else:
            await interaction.response.send_message(LANG_STRINGS["error_occurred"].format(error_message="Unknown Error"), ephemeral=True)

        await asyncio.sleep(60)
        try:
            original_message = await interaction.original_response()
            await original_message.delete()
        except Exception as e:
            print(f"Fehler beim Löschen der Nachricht: {e}")

    except Exception as e:
        error_message = LANG_STRINGS["error_occurred"].format(error_message=str(e))
        await interaction.response.send_message(error_message, ephemeral=True)
        await asyncio.sleep(60)

# Slash-Befehl: Aktuelle Autosettings anzeigen
@bot.tree.command(name="get_autosettings", description="Show current auto settings.")
async def get_autosettings_command(interaction: discord.Interaction):
    try:
        response = APIClient.get_auto_settings()
        if not response or response.get("failed", False):
            error_message = LANG_STRINGS["error_occurred"].format(error_message="Unknown Error")
            await interaction.response.send_message(error_message, ephemeral=True)
            await asyncio.sleep(60)
            return

        settings_json = json.dumps(response, indent=2, ensure_ascii=False)
        temp_file_path = "autosettings.json"
        with open(temp_file_path, "w", encoding="utf-8") as file:
            file.write(settings_json)

        await interaction.response.send_message(
            LANG_STRINGS["autosettings_retrieved"], file=discord.File(temp_file_path)
        )

        os.remove(temp_file_path)
        await asyncio.sleep(60)

        try:
            original_message = await interaction.original_response()
            await original_message.delete()
        except Exception as e:
            print(f"Fehler beim Löschen der Originalnachricht: {e}")

    except Exception as e:
        error_message = LANG_STRINGS["error_occurred"].format(error_message=str(e))
        await interaction.response.send_message(error_message, ephemeral=True)
        await asyncio.sleep(60)

# Bot starten
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
