from telethon import TelegramClient, sync

# Вставляем api_id и api_hash
api_id = 662249
api_hash = '442c984dfc2052407aca6c178f6f90a4'

client = TelegramClient('session_name', api_id, api_hash)
client.start()
