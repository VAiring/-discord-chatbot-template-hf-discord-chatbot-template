import sys, logging
import asyncio
from fastapi import FastAPI, Request
from core.config import Config
from discord_bot.bot import client, start_keep_alive

# ロギング設定
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",  # +0900 を明示
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

app = FastAPI()


@app.post("/keep_alive")
async def keep_alive_endpoint(request: Request):
    """KeepAliveリクエストを受け取るエンドポイント"""
    try:
        data = await request.json()
        logging.info("[KeepAlive] Received data: %s", data)
        return {"status": "success", "message": "KeepAlive received"}
    except Exception as e:
        logging.error("[KeepAlive] Error processing request: %s", e, exc_info=True)
        return {"status": "error", "message": "Invalid request"}


async def run_uvicorn():
    """Uvicornを非同期で実行"""
    import uvicorn

    await asyncio.to_thread(
        uvicorn.run,
        app,
        host="0.0.0.0",
        port=7860,
    )


async def main() -> None:
    start_keep_alive()  # HF Ping スレッド開始
    await asyncio.gather(
        client.start(Config.DISCORD_TOKEN),  # Discord ボット起動
        run_uvicorn(),  # FastAPI サーバー起動
    )


if __name__ == "__main__":
    asyncio.run(main())
