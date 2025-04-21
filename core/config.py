import os


class Config:
    """アプリケーション全体の設定を管理するクラス"""

    # Discord関連
    DISCORD_TOKEN: str = os.environ.get("DISCORD_TOKEN", "")
    HF_TOKEN: str = os.environ.get("HF_TOKEN", "")
    # API関連
    API_URL: str = os.environ.get("API_URL", "")

    KEEP_ALIVE_INTERVAL: int = int(
        os.environ.get("KEEP_ALIVE_INTERVAL", 1800)
    )  # 秒単位 (デフォルト: 30分)

    # ログ設定
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> None:
        """必須設定の検証"""
        missing_vars = []
        if not cls.DISCORD_TOKEN:
            missing_vars.append("DISCORD_TOKEN")
        if not cls.HF_TOKEN:
            missing_vars.append("HF_TOKEN")
        if not cls.API_URL:
            missing_vars.append("API_URL")
        if missing_vars:
            raise EnvironmentError(
                f"以下の環境変数が設定されていません: {', '.join(missing_vars)}"
            )
