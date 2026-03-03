#!/usr/bin/env python3
import asyncio
import aiohttp
import random
import string
import os
import json
from typing import List
from dataclasses import dataclass

@dataclass
class Proxy:
    ip: str
    port: int

class VanitySniper:
    def __init__(self, token: str, guild_id: str):
        self.token = token
        self.guild_id = guild_id
        self.ua_pool = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        ]
    
    async def create_session(self):
        headers = {
            "Authorization": self.token,
            "User-Agent": random.choice(self.ua_pool),
            "Content-Type": "application/json"
        }
        return aiohttp.ClientSession(headers=headers)
    
    async def check_vanity(self, session, vanity):
        try:
            async with session.get(f"https://discord.com/api/v9/invites/{vanity}") as resp:
                if resp.status == 404:
                    return True
                return False
        except:
            return False
    
    async def claim_vanity(self, session, vanity):
        payload = {"code": vanity}
        try:
            async with session.patch(
                f"https://discord.com/api/v9/guilds/{self.guild_id}/vanity-url",
                json=payload
            ) as resp:
                if resp.status == 200:
                    print(f"🎉 PENTEST SUCCESS: CLAIMED {vanity}")
                    return True
            return False
        except Exception as e:
            print(f"Claim failed: {e}")
            return False
    
    async def snipe(self):
        session = await self.create_session()
        try:
            for i in range(1000):  # 1000 attempts
                vanity = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                print(f"Checking: {vanity}")
                
                if await self.check_vanity(session, vanity):
                    print(f"✅ {vanity} AVAILABLE - CLAIMING...")
                    if await self.claim_vanity(session, vanity):
                        return True
                
                await asyncio.sleep(0.1)  # Rate limit safe
        finally:
            await session.close()

async def main():
    token = os.getenv("TOKEN")
    guild_id = os.getenv("GUILD_ID")
    
    print(f"Pentest starting: Guild {guild_id}")
    sniper = VanitySniper(token, guild_id)
    await sniper.snipe()

if __name__ == "__main__":
    asyncio.run(main())
