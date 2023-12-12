import asyncio
import flet as ft
from ..vrobots_bridge import WebSocketList

class StatusText(ft.UserControl):
    def __init__(self, vrobot_name):
        super().__init__()
        self.vrobot_name = vrobot_name

    async def did_mount_async(self):
        self.running = True
        asyncio.create_task(self.update_timer())

    async def will_unmount_async(self):
        self.running = False

    async def update_timer(self):
        while self.running:
            self.countdown.value = f"Inactive"
            self.countdown.color = "#e02869"
            self.countdown.weight = ft.FontWeight.W_500
            self.countdown.size = 14
            for ws in WebSocketList:
                if (ws.name == self.vrobot_name):
                    self.countdown.value = f"Active"
                    self.countdown.color = "#059669"
            await self.update_async()
            await asyncio.sleep(0.2)
            
    def build(self):
        self.countdown = ft.Text()
        return self.countdown