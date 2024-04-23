from langchain_community.chat_models import ChatOllama 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

def get_response(user_query, chat_history):

    llm = ChatOllama(model="tinyllama") #mistral, tinyllama

    template = """
        You are a helpful assistant. 
        Answer the following questions considering the history of the conversation:
        Chat history: {chat_history}
        User question: {user_question}
        """
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()

    # Collect all responses from the generator object
    responses = [response for response in chain.stream({
        "chat_history": chat_history,
        "user_question": user_query
    })]

    return ''.join(responses)

st.set_page_config(page_title="Streamlit Chatbot", page_icon="🤖")
st.title("ChatGPT-like clone")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hi, I'm a bot. How can I help you?")]

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

user_query = st.chat_input("Type your message here...")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        response = get_response(user_query, st.session_state.chat_history)
        st.write(response)

    st.session_state.chat_history.append(AIMessage(content=response))
