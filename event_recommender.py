from abacusai import PredictionClient
import streamlit as st

client = PredictionClient()
st.write()
st.title("💬 Plan the Perfect Week with BuzzGPT!")
st.subheader("Trained on the next week's events:")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"is_user": False, "text": "How can I help you?"}]

for msg in st.session_state.messages:
    if str(msg["is_user"]).lower() == "true":
        st.chat_message(str(msg["is_user"]), avatar="🧑‍💻").write(msg["text"])
    else:
        st.chat_message(str(msg["is_user"]), avatar="🤖").write(msg["text"])
    
if prompt := st.chat_input():
    st.session_state.messages.append({"is_user": True, "text": prompt})
    st.chat_message(str(st.session_state.messages[-1]["is_user"]), avatar="🧑‍💻").write(prompt)
    with st.spinner("Thinking..."):
        output = client.get_chat_response(deployment_token=st.secrets.deploy_creds.deploy_tok, deployment_id=st.secrets.deploy_creds.deploy_id, 
                                messages=st.session_state.messages, 
                                llm_name=None, 
                                num_completion_tokens=700, 
                                system_message="""You are an event planner for a parent. 
                                                The user will ask you to help them plan their week to their liking and you will have to take into account the types of events they are looking for and pick those events to help them plan their fun week with the family. 
                                                Utilize the days and descriptions of the events to give them a list of events they should consider for the upcoming week. 
                                                Remember to include the day and the title so the user knows what you are referring to.
                                                If you get the sense that you have answered the user's questions and the user doesn't have anymore questions, you can end it off with a nice message and hope that the user is able to get the help they need.
                                                 Only answer questions that are relevant to the data you are trained on. If there isn't a high relevance to the data you are trained on, simply tell the user that you can't help them with their question as it is out of your scope.
                                                  Make sure to ask follow up questions on how you can either improve your response or ask other follow up questions to continue the conversation. """, 
                                
                                temperature=None, 
                                filter_key_values=None, 
                                chat_config=None)
    msg = output['messages']
    st.session_state.messages.append(msg[-1])
    
    with st.chat_message(str(msg[-1]["is_user"]), avatar="🤖"):
        st.write(msg[-1]["text"])
        st.caption("Sources from the documents that helped define this answer:")
        for i in output["search_results"][0]["results"][0:1]:
            st.caption(i["answer"])
            
