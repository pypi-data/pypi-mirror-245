def create(openai_key, llm_model, workspace):
    agent = f'''Creating new ArcGPT AI Agent:
        OpenAI Key: {openai_key}
        ChatGPT Model: {llm_model}
        Workspace: {workspace}''' 

    return agent
