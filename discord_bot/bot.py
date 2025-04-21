import sys, logging
import discord
import requests
import time
import threading

from discord_bot.load_commands import load_commands
from core.config import Config

# ロギング設定
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",  # +0900 を明示
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

Config.validate()  # 必須設定の検証

api_url: str = Config.API_URL
hf_token: str = Config.HF_TOKEN
keep_alive_interval: int = Config.KEEP_ALIVE_INTERVAL

headers: dict[str, str] = {"Authorization": f"Bearer {hf_token}"}

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


def _keep_alive_loop() -> None:
    """HF Spaceがスリープしないように定期Pingする関数"""
    while True:
        try:
            logging.info("[KeepAlive] Ping to HF Space")
            response = requests.post(
                api_url, headers=headers, json={"data": ["ping"]}, timeout=10
            )
            response.raise_for_status()  # HTTPエラーを検出
            logging.info("[KeepAlive] Response Status Code: %s", response.status_code)
            logging.info("[KeepAlive] Response Content: %s", response.text)
        except requests.exceptions.RequestException as e:
            logging.error("[KeepAlive] Request Error: %s", e, exc_info=True)
        finally:
            time.sleep(keep_alive_interval)


def start_keep_alive() -> None:
    threading.Thread(target=_keep_alive_loop, daemon=True).start()


@client.event
async def on_ready() -> None:
    commands = load_commands("discord_bot.commands")
    for register_command in commands:
        register_command(tree)
    await tree.sync()
    logging.info(f"[Discord] Logged in as {client.user}")
