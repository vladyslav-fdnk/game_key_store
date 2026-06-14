import httpx
import os

BACKEND_API_URL = os.getenv("BACKEND_URL", "http://backend:8000") + "/api"


class BackendAPIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=BACKEND_API_URL, timeout=10.0)

    async def get_games(self) -> list:
        response = await self.client.get("games/")
        if response.status_code == 200:
            return response.json()
        return []

    async def get_or_create_user(self, telegram_id: int, username: str, first_name: str, last_name: str = "") -> dict:
        response = await self.client.get(f"users/{telegram_id}/")
        if response.status_code == 404:
            create_res = await self.client.post("users/", json={
                "telegram_id": telegram_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            })
            return create_res.json()
        return response.json()

    async def create_order(self, user_id: int, game_id: int) -> dict:
        response = await self.client.post("orders/", json={
            "user": user_id,
            "game": game_id,
            "status": "PENDING"
        })
        return {"status_code": response.status_code, **response.json()}

    async def check_order_keys(self, order_id: int) -> dict:
        response = await self.client.get(f"orders/{order_id}/check_keys/")
        return response.json()

    async def complete_payment(self, order_id: int, transaction_id: str) -> dict:
        response = await self.client.post(f"orders/{order_id}/complete_payment/", json={
            "transaction_id": transaction_id
        })
        return {"status_code": response.status_code, **response.json()}

    async def get_profile(self, tg_id: int) -> dict:
        response = await self.client.get(f"profile/{tg_id}/")
        return response.json()

    async def close(self):
        await self.client.aclose()