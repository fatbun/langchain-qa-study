#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Project : langchain-qa-study
# @Time : 2023/8/17 15:30
# @Author : Ben Li.
# @File: chatbot.py
import gradio as gr
from embedded_chat import chat, chat_history


def random_response(message, history):
    print("Message: ", message)
    print("History: ", history)

    return chat_history(message, history)


demo = gr.ChatInterface(random_response)

demo.launch()
