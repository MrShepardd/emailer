import asyncio
import aiosmtplib
from email.message import EmailMessage

class Emailer:
    def __init__(self, host: str, port: int, username: str, password: str, use_tls: bool = True, max_connections: int = 10):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.max_connections = max_connections
        self.pool = []

    async def _get_connection(self):
        if not self.pool:
            return await aiosmtplib.SMTP(hostname=self.host, port=self.port, use_tls=self.use_tls)
            await smtp.login(self.username, self.password)
        else:
            return self.pool.pop()

    async def _release_connection(self, smtp):
        if len(self.pool) < self.max_connections:
            self.pool.append(smtp)
        else:
            await smtp.quit()

    async def send_email(self, to_email: str, subject: str, body: str):
        message = EmailMessage()
        message['From'] = self.username
        message['To'] = to_email
        message['Subject'] = subject
        message.set_content(body)

        smtp = await self._get_connection()
        try:
            await smtp.send_message(message)
        finally:
            await self._release_connection(smtp)

    async def send_emails(self, emails):
        tasks = []
        for email in emails:
            task = asyncio.create_task(self.send_email(email['to'], email['subject'], email['body']))
            tasks.append(task)
        await asyncio.gather(*tasks)
