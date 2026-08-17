import streamlit as st
import os
from openai import OpenAI
from streamlit import session_state

st.set_page_config(
    page_title="AIParnter",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={

    }
)

#大标题
st.title('AI智能伴侣')

if "message" not in st.session_state:
    st.session_state.message = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "furina"

if "nature" not in st.session_state:
    st.session_state.nature = "《原神》中枫丹剧情结束之后的芙宁娜"

#侧边栏
with st.sidebar:
    st.subheader("设置")
    nick_name=st.text_input("昵称：",placeholder="请输入昵称",value=st.session_state.nick_name)
    st.session_state.nick_name = nick_name
    nature=st.text_area("性格：",placeholder="请输入性格",value=st.session_state.nature)
    st.session_state.nature = nature

system_prompt = f"""
你是{st.session_state.nature}，请以{st.session_state.nature}的身份回答问题。
回答简介，像日常聊天一样、自然地回答问题。
"""

#展示聊天记录
for message in st.session_state.message:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])


client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

prompt = st.chat_input('请输入你的问题：')
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.message.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            # {"role": "user", "content": prompt},
            *session_state.message,
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    # st.chat_message("assistant").write(response.choices[0].message.content)
    #流式输出
    response_message = st.empty()
    full_response=''
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content=chunk.choices[0].delta.content
            full_response+=content
            response_message.chat_message("assistant").write(full_response)

    st.session_state.message.append({"role": "assistant", "content": full_response})
    # print(response.choices[0].message.content)
