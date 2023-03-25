import asyncio
from typing import List
from email.message import EmailMessage

class EmailQueue:
    def __init__(self, emailer, max_workers: int = 10):
        self.emailer = emailer
        self.queue = asyncio.Queue()
        self.max_workers = max_workers

    async def _send_email(self, email):
        await self.emailer.send_email(email['to'], email['subject'], email['body'])

    async def _worker(self):
        while True:
            email = await self.queue.get()
            await self._send_email(email)
            self.queue.task_done()

    async def start(self):
        tasks = []
        for i in range(self.max_workers):
            task = asyncio.create_task(self._worker())
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def add_email(self, email):
        await self.queue.put(email)

    async def add_emails(self, emails):
        for email in emails:
            await self.queue.put(email)

    async def wait_empty(self):
        await self.queue.join()