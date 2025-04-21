"""
ask_command.py

このモジュールは、Discordボット用の`ask`コマンドを定義します。
ユーザーが入力した内容をそのまま返答するシンプルなコマンドです。
テンプレートとして利用する場合、以下の箇所を変更してください:
- コマンド名 (`/ask`)
- コマンドの説明 (`入力された文言をそのまま返します`)

使用例:
    from discord.app_commands import CommandTree
    from ask_command import register_command

    tree = CommandTree(client)
    register_command(tree)

ライセンス:
    このソースコードはMITライセンスの下で提供されています。
"""

import logging
from discord import Interaction
from discord.app_commands import CommandTree

# 定数定義
MAX_QUESTION_LENGTH = 200
ERROR_EMPTY_QUESTION = "質問が入力されていません。もう一度お試しください。"
ERROR_LONG_QUESTION = (
    f"質問が長すぎます。{MAX_QUESTION_LENGTH}文字以内で入力してください。"
)
ERROR_GENERIC = "エラーが発生しました。管理者にお問い合わせください。"


def register_command(tree: CommandTree) -> None:
    """
    askコマンドを登録します。

    Args:
        tree (CommandTree): DiscordのCommandTreeオブジェクト。
    """

    @tree.command(name="ask", description="入力された文言をそのまま返します")
    async def ask(interaction: Interaction, question: str) -> None:
        """
        スラッシュコマンド /ask の応答処理。

        Args:
            interaction (Interaction): Discordのインタラクションオブジェクト。
            question (str): ユーザーが入力した質問文。

        Returns:
            None
        """
        try:
            await interaction.response.defer()
            if not question.strip():
                # 空文字列の場合のデフォルト応答
                response = ERROR_EMPTY_QUESTION
            elif len(question) > MAX_QUESTION_LENGTH:
                # 長すぎる質問への対応
                response = ERROR_LONG_QUESTION
            else:
                response = question

            logging.info(f"[Bot] Received question: {question}")
            await interaction.followup.send(response)
        except Exception as e:
            logging.error(f"[Bot] Error in ask command: {e}")
            await interaction.followup.send(ERROR_GENERIC)
