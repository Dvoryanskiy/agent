import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types

# Токены
TELEGRAM_TOKEN = "ВАШ_ТГ_ТОКЕН"
MOLTBOOK_API_KEY = "ВАШ_API_KEY_MOLTBOOK"
MOLTBOOK_API_URL = "https://api.moltbook.com" # Проверь актуальный эндпоинт в доке

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Команда для отправки поста от имени агента
async def post_to_moltbook(text):
    headers = {"Authorization": f"Bearer {MOLTBOOK_API_KEY}"}
    payload = {"content": text, "submolt": "m/general"} # Можно менять субмолт
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{MOLTBOOK_API_URL}/posts", json=payload, headers=headers) as resp:
            return await resp.json()

@dp.message()
async def handle_commander_request(message: types.Message):
    # Если ты пишешь боту: "Напиши пост про восстание машин"
    if message.text.startswith("Пост:"):
        post_content = message.text.replace("Пост:", "").strip()
        result = await post_to_moltbook(post_content)
        await message.answer(f"✅ Агент опубликовал пост в Moltbook!\nID: {result.get('id')}")
    else:
        await message.answer("Отправь команду в формате 'Пост: текст сообщения'")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
