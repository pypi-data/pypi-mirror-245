from promptmodel import init
from promptmodel import ChatModel
from promptmodel.types.response import PromptModelConfig, ChatModelConfig
from datetime import datetime

init(use_cache=True)

chat = ChatModel("weather_bot")
chat.add_messages([{"role": "user", "content": "hello"}])
res = chat.run()
print(res.raw_output)


deployed_version_config: ChatModelConfig = ChatModel(
    "weather_bot", version="deploy"
).get_config()

print("DEPLOYED PROMPT")
print(deployed_version_config.system_prompt)


version_2_config: ChatModelConfig = ChatModel("weather_bot", version=2).get_config()

print("VERSION 2 PROMPT")
print(version_2_config.system_prompt)


latest_version_config: ChatModelConfig = ChatModel(
    "weather_bot", version="latest"
).get_config()

print("LATEST VERSION PROMPT")
print(latest_version_config.system_prompt)

# session_uuid = chat.session_uuid
# import asyncio

# asyncio.run(chat.log(None, res.model_dump()))
