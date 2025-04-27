# import gradio as gr
# from client import send_query_to_bot

# title = 'Asha: Your Partner in Every Career Dream.'

# # Gradio UI
# with gr.Blocks() as demo:
#     gr.Markdown("# Job Search Assistant 🌟")
#     gr.Markdown("I'm here to help you find the perfect job! Just enter your query and preferences below.")

#     query_input = gr.Textbox(label="Enter your job query", placeholder="e.g., Software Developer, Data Scientist")
#     location_input = gr.Textbox(label="Location (optional)", placeholder="e.g., Bangalore")
#     category_input = gr.Textbox(label="Category (optional)", placeholder="e.g., IT, HR")
#     experience_input = gr.Textbox(label="Experience (optional)", placeholder="e.g., 3-5 years")

#     submit_button = gr.Button("Search Jobs")

#     output = gr.Textbox(label="Search Results", interactive=False)

#     submit_button.click(send_query_to_bot, 
#                         inputs=[query_input, location_input, category_input, experience_input], 
#                         outputs=output)

# demo.launch(server_port=5000, server_name="0.0.0.0", debug=True)




import gradio as gr
from client import send_query_to_bot

title = "Asha: Your Partner in Every Career Dream"

# Maintain chat history
chat_history = []

def chatbot(user_message, history):
    global chat_history
    response = send_query_to_bot(user_message, history)
    chat_history.append((user_message, response))
    return "", chat_history

with gr.Blocks() as demo:
    gr.Markdown("# 👩‍💼 Asha: Your Partner in Every Career Dream")
    gr.Markdown("Ask me anything job-related — I’ll guide you step-by-step ✨")

    chatbot_output = gr.Chatbot()
    message_input = gr.Textbox(placeholder="Ask me about jobs, e.g. 'I want a remote job in Hyderabad'", show_label=False)
    send_button = gr.Button("Send")

    send_button.click(fn=chatbot, inputs=[message_input, chatbot_output], outputs=[message_input, chatbot_output])
    message_input.submit(fn=chatbot, inputs=[message_input, chatbot_output], outputs=[message_input, chatbot_output])

demo.launch(server_port=5000, server_name="0.0.0.0", debug=True)
