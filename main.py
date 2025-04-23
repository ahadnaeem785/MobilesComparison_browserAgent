from __future__ import annotations
import asyncio
import os
import chainlit as cl
from pydantic import BaseModel, Field
from pydantic.types import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,TResponseInputItem,function_tool,RunContextWrapper,set_default_openai_client
from agents.run import RunConfig
from browser_use import Agent as BrowserAgent, Browser 

# from maxim import Maxim,Config
# from maxim.logger.openai.agents import MaximOpenAIAgentsTracingProcessor

load_dotenv()

# logger = Maxim(Config()).logger()
# add_trace_processor(MaximOpenAIAgentsTracingProcessor(logger))

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


## CONTEXT

class MobileComparisonContext(BaseModel):
    phoneModel1: str = Field(default="", description="The first phone model provided by the user")
    phoneModel2: str = Field(default="", description="The second phone model provided by the user")
    phoneModel1FeatureData: str = Field(default="", description="Raw data about the first phone model")
    phoneModel2FeatureData: str = Field(default="", description="Raw data about the second phone model")
    comparisonMarkdown: str = Field(default="", description="A structured markdown table comparing both phone models")


## TOOLS

@function_tool(
    name_override="online_search",
    description_override="Searches online for phone model features and specifications."
)
async def online_search(
    context: RunContextWrapper[MobileComparisonContext], 
    query: str) -> str:
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(gemini_api_key))
    agent = BrowserAgent(
        task=f"Find detailed specifications and features of {query} and return structured data.",
        llm=llm,
        browser=Browser()
    )
    history = await agent.run()
    
    ## update the context with the extracted content
    if context.context.phoneModel1FeatureData == "":
        context.context.phoneModel1FeatureData = history.extracted_content()
    else:
        context.context.phoneModel2FeatureData = history.extracted_content()
    print("updated context - ", context.context)
    return history.extracted_content()




## AGENTS

# 1. Online Search Agent
online_search_agent = Agent[MobileComparisonContext](
    name="Online Search Agent",
    handoff_description="An agent that searches for phone specifications online.",
    instructions="""
    You are an Online Search Agent. Your goal is to fetch detailed specifications for a phone model.
    # Routine:
    1. Use the `online_search` tool to get specifications for the given phone model.
    2. Save the retrieved information in the context.
    """,
    tools=[online_search],
    model=model
)

# 2. Triage Agent
triage_agent = Agent[MobileComparisonContext](
    name="Triage Agent",
    handoff_description="An agent that delegates tasks to the correct sub-agents.",
    instructions="""
    You are a Triage Agent. Your goal is to coordinate the process of phone model comparison. You have to 
    delegate tasks to the Online Search Agent. 
    # Sequence:
    1. Receive two phone model names from the user.
    2. Handoff the first phone model to the `Online Search Agent`.
    3. Handoff the second phone model to the `Online Search Agent`.
    4. Return the proper comparison in table form in markdown format string.
    
    
    """,
    handoffs=[online_search_agent],
    model=model
)



# Chainlit entrypoint
@cl.on_message
async def on_message(message: cl.Message):
    if " vs " not in message.content:
        await cl.Message(content="❗ Please enter phone models in the format: `iPhone 13 vs Samsung S21`").send()
        return

    phone1, phone2 = map(str.strip, message.content.split("vs"))

    context = MobileComparisonContext(phoneModel1=phone1, phoneModel2=phone2)
    input_items: list[TResponseInputItem] = [{"content": message.content, "role": "user"}]

    # Initial placeholder message
    msg = cl.Message(content=f"Fetching specifications for **{phone1}** and **{phone2}**...")
    await msg.send()

    # Run your multi-agent system
    result = await Runner.run(triage_agent, input_items, context=context)

    # Final markdown output
    markdown = result.final_output.strip()

    # Clear previous content and stream line-by-line
    msg.content = ""
    lines = markdown.splitlines()

    for line in lines:
        await msg.stream_token(line + "\n")
        await asyncio.sleep(0.1)  # Adjust speed as needed

    await msg.update()

    # # Optionally save result
    # with open("comparison.md", "w", encoding="utf-8") as f:
    #     f.write(markdown)






# ## RUNNER
# async def main():
#     # Hardcoded phone models
#     context = MobileComparisonContext(
#         phoneModel1="iPhone 13",
#         phoneModel2="Samsung Galaxy S21"
#     )
#     input_items: list[TResponseInputItem] = [
#         {"content": f"{context.phoneModel1} vs {context.phoneModel2}", "role": "user"}
#     ]
#     result = await Runner.run(triage_agent, input_items, context=context)
    
#     print("Final Comparison Markdown:")
#     print(result)
    
#     # Save the final result to a file
#     with open("comparison.md", "w") as f:
#         f.write(result.final_output)
#     print("Comparison saved to comparison.md file")
    
    
# if __name__ == "__main__":
#     asyncio.run(main())




























# async def main():
#     context = MobileComparisonContext()
#     phone1 = input("Enter the first phone model 1: ")
#     phone2 = input("Enter the second phone model 2: ")
#     context.phoneModel1 = phone1
#     context.phoneModel2 = phone2
#     input_items: list[TResponseInputItem] = [{"content": f"{phone1} vs {phone2}", "role": "user"}]
#     result = await Runner.run(triage_agent, input_items, context=context)
    
#     print("Final Comparison Markdown:")
#     print(result)
    
#     # save the final result to a file in same folder
    
#     with open("comparison.md", "w") as f:
#         f.write(result.final_output)
#     print("Comparison saved to comparison.md file")