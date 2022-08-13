from environs import Env
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

PAYMENT_TOKEN = env.str("PAYMENT_TOKEN")

host = env.str("host")

port = env.str("port")

user = env.str("user")

password = env.str("password")

database_name = env.str("database_name")

ADMIN_ID = env.str("ADMIN_ID")