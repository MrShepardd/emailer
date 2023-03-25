import asyncio
from emailer import Emailer
from emailqueue import EmailQueue

emails = [
    {
        'to': 'user1@example.com',
        'subject': 'Test email 1',
        'body': 'Hello, this is a test email 1'
    },
    {
        'to': 'user2@example.com',
        'subject': 'Test email 2',
        'body': 'Hello, this is a test email 2'
    },
    {
        'to': 'user3@example.com',
        'subject': 'Test email 3',
        'body': 'Hello, this is a test email 3'
    }
]

async def main():
    emailer = Emailer('smtp.gmail.com', 587, 'user@gmail.com', 'password')
    email_queue = EmailQueue(emailer)
   
    await email_queue.add_emails(emails)
    await email_queue.start()
    await email_queue.wait_empty()

if __name__ == "__main__":
	asyncio.run(main())
