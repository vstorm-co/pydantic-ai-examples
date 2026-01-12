from pprint import pprint

from dotenv import load_dotenv
from loguru import logger as log
from pydantic_ai import Agent, ModelMessage, ModelRequest, ModelResponse

load_dotenv()

### Basic PydanticAI Agent telling a joke
agent = Agent(
    model="openai:gpt-4o",
    system_prompt="Be a helpful assistant"
)
q = "Tell me a funny joke. Respond in plain text."
result = agent.run_sync(q)
log.info(f"\nPrompt: {q} \nAnswer: {result.output}")
# log.info(f"All messages from this inference: {result.all_messages()}")


### Now agent tells a joke and explains it in the second answer
# To do so, he needs to get the historic context 
q1 = "Provide a really, really funny joke. Respond in plain text."
result_1 = agent.run_sync(q1)
log.info(f"\nPrompt: {q1} \nAnswer: {result_1.output}")


# Historic context is being provided via `message_history` arg in the agent call
# It can be for example a whole history up to this point - thus `new_messages()` 
# is being called on the `result_1` object which is the output of first inference
q2 = "I didn't get it. Care to explain?"
result_2 = agent.run_sync(q2, message_history=result_1.new_messages())
log.info(f"\nPrompt: {q2} \nAnswer: {result_2.output}")

log.info("Whole history after the 2nd inference")
for idx, item in enumerate(result_2.all_messages()):
    log.info(f"History item no {idx+1}")
    pprint(item)
    
    
### Working with the history itself
# For example, it can be summarized by the LLM
q3 = "Please summarize the conversations that were held earlier"
result_3 = agent.run_sync(q3, message_history=result_2.all_messages())
log.info(result_3.output)

### Editing the history
# History object can also be edited of filtered
# Let's try to perform the same summary as above but only on user messages
def filter_only_user_messages(messages: list[ModelMessage]) -> list[ModelMessage]:
    """Remove all ModelResponse Messages, keep only ones from user (ModelRequest)"""
    return [msg for msg in messages if isinstance(msg, ModelRequest)]

agent_user = Agent('openai:gpt-4o', history_processors=[filter_only_user_messages])
result_4a = agent_user.run_sync(q3, message_history=result_2.all_messages())
log.info(f"Summary of only user messages: {result_4a.output}")


# Now the same, but let's retain only model messages from the history
# 
def filter_only_model_messages(messages: list[ModelMessage]) -> list[ModelMessage]:
    """Remove all ModelRequest Messages, keep only ones from model (ModelResponse)"""
    return [msg for msg in messages if isinstance(msg, ModelResponse)]

try:
    agent_model = Agent('openai:gpt-4o', history_processors=[filter_only_model_messages])
    result_4b = agent_model.run_sync(q3, message_history=result_2.all_messages())
    log.info(result_4b.output)
    log.info(f"Summary of only model messages: {result_4a.output}")
except Exception as e:
    log.error(e)
    log.info("This will error out since the history object needs to end with a ModelRequest which we've filtered out")

