import os
from environ import Env

env = Env()

env_file = os.path.join(os.path.dirname(__file__), "../../.env")
if os.path.exists(env_file):
    env.read_env(env_file)

BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", default="")
PROVIDER_TOKEN = env("PROVIDER_TOKEN", default="")