"""
echo_message_command.py

このモジュールは、Discordボット用の`Echo`コンテキストメニューコマンドを定義します。
ユーザーが選択したメッセージを引用し、メンション付きで同じチャンネルに送信します。

使用例:
    from discord.app_commands import CommandTree
    from echo_message_command import register_command

    tree = CommandTree(client)
    register_command(tree)

ライセンス:
    このソースコードはMITライセンスの下で提供されています。
"""

import logging

from discord import Interaction, AllowedMentions, Message
from discord.app_commands import CommandTree

# 定数定義
ERROR_GENERIC = "エラーが発生しました。管理者にお問い合わせください。"


def register_command(tree: CommandTree) -> None:
    """
    Message コンテキストメニュー Ask (echo) を登録します。

    Args:
        tree (CommandTree): DiscordのCommandTreeオブジェクト。
    """

    @tree.context_menu(name="Echo")
    async def message_echo(interaction: Interaction, message: Message) -> None:
        """
        コンテキストメニュー「Echo」の実装。

        ユーザーが右クリックメニューから選択したメッセージを引用し、
        メンション付きで同じチャンネルに送信します。

        Args:
            interaction (Interaction): Discordのインタラクションオブジェクト。
            message (Message): 対象のDiscordメッセージ。

        Returns:
            None
        """
        try:
            # 応答を遅延（非同期処理のため）
            await interaction.response.defer(ephemeral=False)

            logging.info(f"[Bot] Echoing message: {message.content}")
            # メンション＋対象のメッセージの本文を新規メッセージとして送信
            await interaction.followup.send(
                content=f"{message.author.mention}\n> {message.content}",
                allowed_mentions=AllowedMentions(
                    users=True, roles=False, everyone=False
                ),
            )
        except Exception as e:
            logging.error(f"[Bot] Error in echo context command: {e}", exc_info=True)
            await interaction.followup.send(ERROR_GENERIC, ephemeral=True)
