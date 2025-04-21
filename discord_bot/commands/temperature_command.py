"""
temperature_command.py

このモジュールは、Discordボット用の`/temperature`コマンドを定義します。
指定された地域（アッツ島とサムイ島）の現在の天気と気温を取得し、ユーザーに表示します。

使用例:
    from discord.app_commands import CommandTree
    from temperature_command import register_command

    tree = CommandTree(client)
    register_command(tree)

ライセンス:
    このソースコードはMITライセンスの下で提供されています。
"""

import asyncio
import logging
import os

import aiohttp
from discord import Interaction
from discord.app_commands import CommandTree

# API関連
OPEN_WEATHER_API_TOKEN: str = os.environ.get("OPEN_WEATHER_API_TOKEN", "")

# アッツ島とサムイ島の緯度と経度
weather_locations = {
    "アッツ島": {"lat": 52.8413, "lon": 173.1700},
    "サムイ島": {"lat": 9.5120, "lon": 100.0136},
}

# 定数定義
ERROR_GENERIC = "エラーが発生しました。管理者にお問い合わせください。"
ERROR_NO_TOKEN = "APIキーが設定されていません。環境変数 `OPEN_WEATHER_API_TOKEN` を確認してください。"


async def fetch_weather(
    session: aiohttp.ClientSession, name: str, coords: dict[str, float]
) -> tuple:
    """
    指定された地域の天気情報を取得します。

    Args:
        session (aiohttp.ClientSession): 非同期HTTPセッション。
        name (str): 地域名。
        coords (dict): 緯度と経度の辞書。

    Returns:
        tuple: 地域名、気温、天気の説明。
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={coords['lat']}&lon={coords['lon']}&units=metric&appid={OPEN_WEATHER_API_TOKEN}&lang=ja"
    )
    # 非同期でHTTPリクエストを送信
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            logging.info(f"{name}: {temp}°C, {weather}")
            return name, temp, weather
        else:
            logging.error(
                f"{name}: データ取得に失敗しました（ステータスコード: {response.status}）"
            )
            return name, None, None


def register_command(tree: CommandTree) -> None:
    """
    DiscordChatbotコマンドを登録します。

    Args:
        tree (CommandTree): DiscordのCommandTreeオブジェクト。
    """

    @tree.command(name="temperature", description="現在の天気と気温を表示します。")
    async def temperature(interaction: Interaction) -> None:
        """
        スラッシュコマンド `/temperature` の応答処理。

        指定された地域（アッツ島とサムイ島）の現在の天気と気温を取得し、
        ユーザーに表示します。

        Args:
            interaction (Interaction): Discordのインタラクションオブジェクト。

        Returns:
            None
        """
        try:
            if not OPEN_WEATHER_API_TOKEN:
                logging.error("[Bot] APIキーが設定されていません。")
                await interaction.response.send_message(ERROR_NO_TOKEN)
                return
            # 応答を遅延
            await interaction.response.defer()
            # 非同期で天気情報を取得
            async with aiohttp.ClientSession() as session:
                results = await asyncio.gather(
                    *[
                        fetch_weather(session, name, coords)
                        for name, coords in weather_locations.items()
                    ]
                )

            # 結果をフォーマットして送信
            response_message = "```"
            for name, temp, weather in results:
                if temp is not None and weather is not None:
                    response_message += f"- {name}：{weather}（{temp}°C）\n"
                else:
                    response_message += f"{name}：データ取得に失敗しました。\n"
            response_message += "```"

            logging.info(f"[Bot] 送信内容: {response_message}")
            await interaction.followup.send(response_message)
        except Exception as e:
            logging.error(f"[Bot] エラー: {e}")
            await interaction.followup.send(ERROR_GENERIC)
