import gradio as gr

from unsloth import FastLanguageModel

from llama_index.core.agent.react import ReActOutputParser
from llama_index.core.agent.react.types import ActionReasoningStep
from llama_index.llms.ollama import Ollama
 
import vecdb

repo = "SamNaing/work-right-uae"
summary_model_name = "gemma3:4b-it-q4_K_M"


model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=repo, 
    max_seq_length=8192, 
    dtype=None,
    load_in_4bit = True,
)

FastLanguageModel.for_inference(model)
summary_model = Ollama(model=summary_model_name, request_timeout=1000000)

tools = vecdb.tools(summary_model)

with open("./sys-prompt.md", "r") as f: 
    sys_prompt = f.read()

def tool_call(tools, tool_name, tool_args):
    tools_by_name = {tool.metadata.get_name(): tool for tool in tools} 
    
    try: 
        tool = tools_by_name.get(tool_name)
        if not tool: 
            return f"{tool_name} is not a valid tool name. Available tools: {', '.join(tools_by_name.keys())}"
        
        tool_response = tool(**tool_args)
        
        return tool_response 
    
    except Exception as e:
        return f"Error calling tool: {str(e)}"
    
    
def react_agent(
    model, 
    tokenizer,
    user_question, 
    tools, 
    sys_prompt, 
    max_steps = 30,
    eos_id = 106
):
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_question}
    ]
    response = None
    output_parser = ReActOutputParser()
    
    for step_num in range(max_steps): 
        try: 
            inputs = tokenizer.apply_chat_template(messages, tokenize = True, add_generation_prompt = True, return_tensors = "pt").to("cuda")
            response = model.generate(input_ids = inputs, max_new_tokens = 200, use_cache = True, eos_token_id=eos_id)
            response = tokenizer.decode(response[0])
            model_response_text = response.split("<start_of_turn>model")[-1]
            reasoning_step = output_parser.parse(model_response_text)

            print(reasoning_step)
            print('\n')
            if reasoning_step.is_done: 
                response = reasoning_step.response
                break 
            
            if isinstance(reasoning_step, ActionReasoningStep):
                observation = tool_call(tools, reasoning_step.action, reasoning_step.action_input)
                print(observation)
                messages.append({
                    "role": "assistant", 
                    "content": f"Thought: {reasoning_step.thought}\nAction: {reasoning_step.action}\nAction Input: {reasoning_step.action_input}"
                })
                messages.append(
                    {"role": "observation", "content": f"Observation: {observation}"}
                )
                print("==" * 100)
                continue
            
            
        except Exception as e:
            print(f"Error during step {step_num}: {e}")
            

    return response


def chat(question):
    result = react_agent(
        model, 
        tokenizer,
        question, 
        tools,  
        sys_prompt,  
    )
    
    return result

def chat_interface(message, history):
    """Wrapper for Gradio ChatInterface."""
    response = chat(message)
    return response

def main():
    gr.ChatInterface(
        fn=chat_interface,
        title="WorkRight UAE",
        type="messages",
    ).launch(share=True)  


if __name__ == "__main__":
    main()
