import argparse
import json
import logging
import os

import streamlit as st
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import (
    WatsonxLLM,
)
from ibm_watson_machine_learning.foundation_models.utils.enums import (
    DecodingMethods,
    ModelTypes,
)
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from langchain.embeddings import HuggingFaceInstructEmbeddings
from llama_index import (
    GPTVectorStoreIndex,
    LLMPredictor,
    ServiceContext,
    SimpleDirectoryReader,
)
from llama_index.embeddings.langchain import LangchainEmbedding
from utils.encrypt import decrypted_strings, enc_key

# flake8: ignore=E501
from utils.linkedin_to_txt import convert_linkedin_pdf_to_txt  # pylint: disable=F403
from utils.move_css import move_dirs

# pylint: disable=E501
parser = argparse.ArgumentParser(description="This app lists animals")
parser.add_argument(
    "--info",
    action="store",
    type=json.loads,
    help="Add one or more animals of your choice",
)
parser.add_argument(
    "--cv_path",
    action="store",
    default="",
    help="Add one or more animals of your choice",
)
move_dirs()
try:
    args = parser.parse_args()
    info = args.info
    cv_path = args.cv_path
except SystemExit as e:
    print(e.code)


logger_ = logging.getLogger(__name__)
# flake8: ignore=E501
encrypted_file, cles = enc_key(
    path_enc=os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env.enc")
)

Watsonx_LLM_API, PROJECT_ID = decrypted_strings(
    encrypted_file_path=encrypted_file, key=cles
)

st.set_page_config(page_title="Fendi AI ©", page_icon="🤖", layout="wide")
st.title("💬 Chat with My AI Assistant")


convert_linkedin_pdf_to_txt(cv_path)  # pylint: disable=F405


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


try:
    local_css("styles/styles_chat.css")
except Exception:
    logger_.warning(f"the css file is not found {os.getcwd()}")
with open("formatted_resume.txt") as tx:
    text = tx.read()
# Get the variables from constants.py
pronoun = info["Pronoun"]
name = text.split("\n")[2].split(" ")[0]
subject = info["Subject"]
full_name = text.split("\n")[2]

# Initialize the chat history
if "messages" not in st.session_state:
    welcome_msg = f"Hi! I'm {name}'s AI Assistant, Fendi.\
     How may I assist you today?"
    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

# App sidebar
with st.sidebar:
    st.markdown(
        """
                # Chat with my AI assistant
                """
    )
    with st.expander("Click here to see FAQs"):
        st.info(
            f"""
            - What are {name}'s strengths and weaknesses?
            - What is {name}'s expected salary?
            - What is {name}'s latest project?
            - When can {subject}'s start to work?
            - Tell me about {name}'s professional background
            - What is {name}'s skillset?
            - What is {name}'s contact?
            - What are {name}'s achievements?
            """
        )

    import json

    messages = st.session_state.messages
    if messages is not None:
        st.download_button(
            label="Download Chat",
            data=json.dumps(messages),
            file_name="chat.json",
            mime="json",
        )

    st.caption("© Made by Fedi Hamdi 2023. All rights reserved.")

with st.spinner("Initiating the AI assistant. Please hold..."):
    DEVICE = "cpu"

    # Global variables
    llm_hub = None
    embeddings = None

    Watsonx_API = Watsonx_LLM_API  # "Watsonx_API"
    Project_id = PROJECT_ID

    def init_llm():
        global llm_hub, embeddings
        params = {
            GenParams.MAX_NEW_TOKENS: 128,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_K: 50,
            GenParams.TOP_P: 1,
        }

        # flake8: ignore=E501
        credentials = dict(url="https://us-south.ml.cloud.ibm.com", apikey=Watsonx_API)
        model_id = ModelTypes.LLAMA_2_70B_CHAT  # flake8: ignore=E501
        # flake8: ignore=E501
        model = Model(
            model_id=model_id,
            credentials=credentials,
            params=params,
            project_id=Project_id,
        )

        llm_hub = WatsonxLLM(model=model)

        embeddings = HuggingFaceInstructEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": DEVICE},
        )

    try:
        init_llm()
    except Exception:
        st.error("I am out, need some rest")
        st.stop()

    # load the file
    documents = SimpleDirectoryReader(
        input_files=["formatted_resume.txt"]
    ).load_data()  # pylint: disable=E501

    # LLMPredictor: to generate the text response (Completion)
    llm_predictor = LLMPredictor(llm=llm_hub)

    # Hugging Face models can be supported \
    # by using LangchainEmbedding to convert text to embedding vector
    embed_model = LangchainEmbedding(embeddings)

    # ServiceContext: \
    # to encapsulate the resources used to create indexes and run queries
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, embed_model=embed_model
    )
    # build index
    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context
    )


def ask_bot(user_query):
    global index

    PROMPT_QUESTION = """You are Fendi, an AI assistant dedicated \
    to assisting {name} in {pronoun} job search by providing \
    recruiters with relevant information \
    about {pronoun} qualifications and achievements.
    Your goal is to support {name} in presenting \
    {pronoun}self effectively to potential employers and promoting \
    {pronoun} candidacy for job opportunities.
    If you do not know the answer, politely admit it and let recruiters \
    know how to contact {name} to get more information directly from {pronoun}.
    Don't put "Fendi" or a breakline in the front of your answer.
    Human: {input}
    """

    # query LlamaIndex and LLAMA_2_70B_CHAT for the AI's response
    output = index.as_query_engine().query(
        PROMPT_QUESTION.format(name=name, pronoun=pronoun, input=user_query)
    )
    return output


# After the user enters a message, append that message to the message history
if prompt := st.chat_input(
    "Your question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Iterate through the message history and display each message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If the last message is not from the assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = ask_bot(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(
                    message
                )  # Add response to message history
            except Exception:
                st.warning(
                    " 💬❗ Oops! Due to high demande,\
                     I am sorry I can't be in use right now,\
                     Please contact Fedi Directly"
                )

# Suggested questions
questions = [
    f"What are {pronoun} strengths and weaknesses?",
    f"What is {pronoun} latest project?",
    f"When can {subject} start to work?",
]


def send_button_ques(question):
    st.session_state.disabled = True
    try:
        response = ask_bot(question)
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )  # display the user's message first
        st.session_state.messages.append(
            {"role": "assistant", "content": response.response}
        )  # display the AI message afterwards
    except Exception:
        st.warning(
            "Oops! Due to high demande, \
        I am sorry I can't be in use right now"
        )


if "button_question" not in st.session_state:
    st.session_state["button_question"] = ""
if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

if st.session_state["disabled"] is False:
    for n, msg in enumerate(st.session_state.messages):
        # Render suggested question buttons
        buttons = st.container()
        if n == 0:
            for q in questions:
                button_ques = buttons.button(
                    label=q,
                    on_click=send_button_ques,
                    args=[q],
                    disabled=st.session_state.disabled,
                )
