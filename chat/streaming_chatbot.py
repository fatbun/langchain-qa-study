#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Project : langchang-openai
# @Time : 2023/8/18 16:04
# @Author : Ben Li.
# @File: streaming_chatbot.py
import gradio as gr
from streaming_chat import stream_sse
from condense_chat import condense_question
from qa_retrive_prompt import get_prompt

with gr.Blocks() as demo:
    gr.Markdown("# <center>ChatGLM-6B</center>")
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")


    def user(user_message, history):
        return "", history + [[user_message, None]]


    def bot(history):
        query = history[-1][0]
        history[-1][1] = ""

        # 根据历史记录，重新生成问题
        question = condense_question(query, history)
        # 结合本地知识库，重新生成prompt
        prompt = get_prompt(question)
        # 调用 chatglm6b 流式接口
        chunk = stream_sse(input=prompt)
        for character in chunk:
            history[-1][1] = character
            yield history


    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch()
