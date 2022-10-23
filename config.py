from pymongo import MongoClient
from pymongo.server_api import ServerApi
# подключение базы данных
conn_str = "mongodb+srv://timeDev:timeDevPassword@timedev22.gxnyxls.mongodb.net/?retryWrites=true&w=majority"
# даётся 5 секунд на подключение
client = MongoClient(conn_str, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Не удалось подключиться к серверу MongoDB")
    exit()
db = client['data']
tasks = db['tasks']

BOT_TOKEN = '5302865425:AAFD3befoEEcqZWPJtkrMN5E6tKH_wa-JfY'