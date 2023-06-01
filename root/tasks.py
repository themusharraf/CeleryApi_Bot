import requests
from celery import shared_task

GROUP_ID = -620660762 # Group id qo'yish kerak
BOT_API = 'https://api.telegram.org/bot6040781764:AAGCW7OLL25tngh9Mgqw7XPBOL3nN6J47vo/sendMessage'
# bor token olish keyin botni group ga qushish kerak keyin ishlaydi


@shared_task
def notify_telegram_group():
    data = {
        'chat_id': GROUP_ID,
        'text': 'Message yuborildi by Celery Team'
    }
    response = requests.post(BOT_API, data)
    print(response.status_code, response.json())


# CELERY_BROKER_URL = 'amqp://localhost'            # settings ga qushish kerak rammitq uchun
# docker run --name rabbitmq -p 5672:5672 rabbitmq
# celery -A root worker -l info
# celery -A root flower --port=5566
