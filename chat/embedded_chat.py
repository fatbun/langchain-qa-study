#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Project : langchang-openai
# @Time : 2023/8/13 09:38
# @Author : Ben Li.
# @File: embedded_chat.py
from langchain import PromptTemplate
from langchain.llms import ChatGLM
# 向量数据库
from langchain.vectorstores import Chroma
# 文本转换为向量的嵌入引擎
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

import langchain

# 打开langchain debug
langchain.debug = True
# 本地向量库
vector_store_dir = "../knowledge_base/vector_store"
# 本地向量模型地址
vector_model_name = "{your vector model dir}"

# 准备嵌入引擎
embeddings = HuggingFaceEmbeddings(model_name=vector_model_name)
# 向量化
vectordb = Chroma(embedding_function=embeddings, persist_directory=vector_store_dir)


def get_custom_prompt_template(history=[]):
    prompt_template = """Use the following pieces of context to answer the question at the end in Chinese answer. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    ----- Chat History start -----
    {chat_history}
    
    ----- Chat History end -----

    Question: {question}
    Helpful Answer:"""
    prompt_template = prompt_template.format(context="{context}", chat_history=history, question="{question}")
    return PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )


def chat_history(message, history) -> str:
    PROMPT = get_custom_prompt_template(history)
    chain_type_kwargs = {"prompt": PROMPT}

    llm = ChatGLM()
    # 创建您的检索引擎
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectordb.as_retriever(), chain_type_kwargs=chain_type_kwargs)

    return qa.run(query=message, history=history)


def chat(message) -> str:
    llm = ChatGLM()
    # 创建您的检索引擎
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectordb.as_retriever())

    return qa.run(query=message)


def main():
    output = chat("我叫什么名字")
    print(type(output))
    print(output)


if __name__ == '__main__':
    main()
