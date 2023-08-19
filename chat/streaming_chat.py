import requests


def stream_sse(url="http://127.0.0.1:8000/stream_chat", input=""):
    data = {
        "input": input
    }
    headers = {
        "Content-Type": "application/json"
    }
    # 使用POST方法连接到SSE流式接口
    response = requests.post(url=url, json=data, headers=headers, stream=True)

    # 循环监听服务器发送的消息
    for line in response.iter_lines():
        # 过滤掉空行
        if line:
            decoded_line = line.decode('utf-8')

            # 只处理以"data:"开头的行，这是SSE的标准格式
            if decoded_line.startswith("data:"):
                chunk = f"\r{decoded_line[len('data:'):].strip()}"
                print(chunk, end="", flush=True)
                yield chunk
    print()  # 添加一个换行符，以便在流结束后移至下一行


if __name__ == "__main__":
    g = stream_sse(input="hi there")
    for i in g:
        next(g)
