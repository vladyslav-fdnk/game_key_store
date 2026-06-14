import httpx

BASE_URL = "http://backend:8000"

async def get_profile(tg_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/api/profile/{tg_id}/")
        return r.json()