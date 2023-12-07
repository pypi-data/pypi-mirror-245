#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : copilot
# @Time         : 2023/12/6 13:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.uniform_queue import UniformQueue

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

requests.get = retrying(requests.get)
requests.post = retrying(requests.post)


class Completions(object):
    def __init__(self, **client_params):
        self.client_params = client_params
        api_key = self.client_params.get('api_key')
        self.access_token = self.get_access_token(api_key)

    def create(self, messages: List[Dict[str, Any]], **kwargs):
        """
                messages=messages,
                model=model,
                stream=stream
        :param messages:
        :param kwargs:
        :return:
        """

        data = {
            "model": 'gpt-4',
            "messages": messages,
            **kwargs
        }
        interval = 0.01
        if data['model'].startswith("gpt-4"):
            data['model'] = "gpt-4"
            interval = 0.05

        # logger.debug(data)

        if data.get('stream'):

            return UniformQueue(self._stream_create(**data)).consumer(interval=interval)

            # return self._stream_create(**data)
        else:
            return self._create(**data)

    def _create(self, **data):
        data = data or {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "你是谁"}]
        }
        response = self._post(**data)

        response = response.json()
        response['model'] = data.get('model', 'gpt-4')
        response['object'] = 'chat.completion'

        return ChatCompletion.model_validate(response)

    def _stream_create(self, **data):
        data = data or {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "你是谁"}],
            "stream": True
        }
        response = self._post(**data)

        buffer = b''  # 用于缓存不完整的行
        for chunk in response.iter_content(chunk_size=1024 * 8):  # , decode_unicode=True
            # logger.debug(chunk)

            if chunk:
                buffer += chunk
                lines = buffer.split(b'\n\n')  # 按照两个换行符切分
                buffer = lines.pop()  # 最后一行可能不完整，保存到 buffer 中
                for line in lines:

                    # logger.debug(line)

                    if line == b'data: [DONE]':
                        break

                    line = line.strip(b"data: ")  # line.decode('utf-8').strip("data: ")
                    line = json.loads(line)
                    line['model'] = data.get('model', "gpt-4")
                    line['object'] = "chat.completion.chunk"
                    line['choices'][0]['finish_reason'] = line['choices'][0].get('finish_reason')  # 最后一个应为 "stop"

                    line = ChatCompletionChunk.model_validate(line)
                    line.choices[0].delta.role = 'assistant'

                    # logger.debug(line)
                    # logger.debug(line.model_dump_json())
                    # logger.debug(line.choices[0].finish_reason)
                    if not line.choices[0].finish_reason and line.choices[0].delta.content:
                        yield line
        yield None

    def _post(self, **data):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            # 'X-Request-Id': str(uuid.uuid4()),
            # 'Vscode-Sessionid': str(uuid.uuid4()) + str(int(datetime.datetime.utcnow().timestamp() * 1000)),
            # 'vscode-machineid': machine_id,
            'Editor-Version': 'vscode/1.84.2',
            'Editor-Plugin-Version': 'copilot-chat/0.10.2',
            'Openai-Organization': 'github-copilot',
            'Openai-Intent': 'conversation-panel',
            'Content-Type': 'application/json',
            'User-Agent': 'GitHubCopilotChat/0.10.2',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        response = requests.post(
            'https://api.githubcopilot.com/chat/completions',
            json=data,
            headers=headers,
            stream=data.get('stream')
        )

        return response

    @staticmethod
    @ttl_cache(ttl=60)
    def get_access_token(api_key: Optional[str] = None):
        api_key = api_key or os.getenv("GITHUB_COPILOT_TOKEN")
        assert api_key

        headers = {
            'Host': 'api.github.com',
            'authorization': f'token {api_key}',
            "Editor-Version": "vscode/1.84.2",
            "Editor-Plugin-Version": "copilot/1.138.0",
            "User-Agent": "GithubCopilot/1.138.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close"
        }
        response = requests.get('https://api.github.com/copilot_internal/v2/token', headers=headers)
        return response.json()['token']

    @staticmethod
    def break_fn(line: ChatCompletionChunk):
        return line.choices[0].finish_reason


if __name__ == '__main__':
    # print(Completions()._create())

    data = {'model': 'gpt-xx', 'messages': [{'role': 'user', 'content': '讲个故事'}], 'stream': True}
    _ = Completions().create(**data)

    for i in _:
        print(i.choices[0].delta.content, end='')

