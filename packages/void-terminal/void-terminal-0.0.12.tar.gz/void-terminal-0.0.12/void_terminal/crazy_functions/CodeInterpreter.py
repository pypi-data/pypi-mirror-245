from collections.abc import Callable, Iterable, Mapping
from typing import Any
from void_terminal.toolbox import CatchException, update_ui, gen_time_str, trimmed_format_exc
from void_terminal.toolbox import promote_file_to_downloadzone, get_log_folder
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.crazy_functions.crazy_utils import input_clipping, try_install_deps
from multiprocessing import Process, Pipe
import os
import time

templete = """
```python
import ...  # Put dependencies here, e.g. import numpy as np

class TerminalFunction(object): # Do not change the name of the class, The name of the class must be `TerminalFunction`

    def run(self, path):    # The name of the function must be `run`, it takes only a positional argument.
        # rewrite the function you have just written here 
        ...
        return generated_file_path
```
"""

def inspect_dependency(chatbot, history):
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    return True

def get_code_block(reply):
    import re
    pattern = r"```([\s\S]*?)```" # regex pattern to match code blocks
    matches = re.findall(pattern, reply) # find all code blocks in text
    if len(matches) == 1: 
        return matches[0].strip('python') #  code block
    for match in matches:
        if 'class TerminalFunction' in match:
            return match.strip('python') #  code block
    raise RuntimeError("GPT is not generating proper code.")

def gpt_interact_multi_step(txt, file_type, llm_kwargs, chatbot, history):
    # Input
    prompt_compose = [
        f'Your job:\n'
        f'1. write a single Python function, which takes a path of a `{file_type}` file as the only argument and returns a `string` containing the result of analysis or the path of generated files. \n',
        f"2. You should write this function to perform following task: " + txt + "\n",
        f"3. Wrap the output python function with markdown codeblock."
    ]
    i_say = "".join(prompt_compose)
    demo = []

    # Step one
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say, inputs_show_user=i_say, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=demo, 
        sys_prompt= r"You are a programmer."
    )
    history.extend([i_say, gpt_say])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update

    # Step two
    prompt_compose = [
        "If previous stage is successful, rewrite the function you have just written to satisfy following templete: \n",
        templete
    ]
    i_say = "".join(prompt_compose); inputs_show_user = "If previous stage is successful, rewrite the function you have just written to satisfy executable templete. "
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say, inputs_show_user=inputs_show_user, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
        sys_prompt= r"You are a programmer."
    )
    code_to_return = gpt_say
    history.extend([i_say, gpt_say])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update
    
    # # Step three
    # i_say = "Please list to packages to install to run the code above. Then show me how to use `try_install_deps` function to install them."
    # i_say += 'For instance. `try_install_deps(["opencv-python", "scipy", "numpy"])`'
    # installation_advance = yield from request_gpt_model_in_new_thread_with_ui_alive(
    #     inputs=i_say, inputs_show_user=inputs_show_user, 
    #     llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
    #     sys_prompt= r"You are a programmer."
    # )
    # # # Step three  
    # i_say = "Show me how to use `pip` to install packages to run the code above. "
    # i_say += 'For instance. `pip install -r opencv-python scipy numpy`'
    # installation_advance = yield from request_gpt_model_in_new_thread_with_ui_alive(
    #     inputs=i_say, inputs_show_user=i_say, 
    #     llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
    #     sys_prompt= r"You are a programmer."
    # )
    installation_advance = ""
    
    return code_to_return, installation_advance, txt, file_type, llm_kwargs, chatbot, history

def make_module(code):
    module_file = 'gpt_fn_' + gen_time_str().replace('-','_')
    with open(f'{get_log_folder()}/{module_file}.py', 'w', encoding='utf8') as f:
        f.write(code)

    def get_class_name(class_string):
        import re
        # Use regex to extract the class name
        class_name = re.search(r'class (\w+)\(', class_string).group(1)
        return class_name

    class_name = get_class_name(code)
    return f"{get_log_folder().replace('/', '.')}.{module_file}->{class_name}"

def init_module_instance(module):
    import importlib
    module_, class_ = module.split('->')
    init_f = getattr(importlib.import_module(module_), class_)
    return init_f()

def for_immediate_show_off_when_possible(file_type, fp, chatbot):
    if file_type in ['png', 'jpg']:
        image_path = os.path.abspath(fp)
        chatbot.append(['This is an image, Display as follows:',  
            f'Local file address: <br/>`{image_path}`<br/>'+
            f'Local file preview: <br/><div align="center"><img src="file={image_path}"></div>'
        ])
    return chatbot

def subprocess_worker(instance, file_path, return_dict):
    return_dict['result'] = instance.run(file_path)

def have_any_recent_upload_files(chatbot):
    _5min = 5 * 60
    if not chatbot: return False    # chatbot is None
    most_recent_uploaded = chatbot._cookies.get("most_recent_uploaded", None)
    if not most_recent_uploaded: return False   # most_recent_uploaded is None
    if time.time() - most_recent_uploaded["time"] < _5min: return True # most_recent_uploaded is new
    else: return False  # most_recent_uploaded is too old

def get_recent_file_prompt_support(chatbot):
    most_recent_uploaded = chatbot._cookies.get("most_recent_uploaded", None)
    path = most_recent_uploaded['path']
    return path

@CatchException
def VoidTerminalCodeInterpreter(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field, For example, a paragraph that needs to be translated, For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters, Such as temperature and top_p, Generally pass it on as is
    plugin_kwargs   Plugin model parameters, No use for the time being
    chatbot         Chat display box handle, Displayed to the user
    history         Chat history, Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """
    raise NotImplementedError

    # Clear history, To avoid input overflow
    history = []; clear_file_downloadzone(chatbot)

    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "CodeInterpreter open source version, This plugin is in the development stage, It is recommended not to use it temporarily, Plugin initializing ..."
    ])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    if have_any_recent_upload_files(chatbot):
        file_path = get_recent_file_prompt_support(chatbot)
    else:
        chatbot.append(["File retrieval", "No recent uploaded files found. "])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Read the file
    if ("recently_uploaded_files" in plugin_kwargs) and (plugin_kwargs["recently_uploaded_files"] == ""): plugin_kwargs.pop("recently_uploaded_files")
    recently_uploaded_files = plugin_kwargs.get("recently_uploaded_files", None)
    file_path = recently_uploaded_files[-1]
    file_type = file_path.split('.')[-1]

    # Careful check
    if is_the_upload_folder(txt):
        chatbot.append([
            "...",
            f"Please fill in the requirements in the input box, Then click the plugin again（File path {file_path} Already memorized）"
        ])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    
    # Start doing real work
    for j in range(5):  # Retry up to 5 times
        try:
            code, installation_advance, txt, file_type, llm_kwargs, chatbot, history = \
                yield from gpt_interact_multi_step(txt, file_type, llm_kwargs, chatbot, history)
            code = get_code_block(code)
            res = make_module(code)
            instance = init_module_instance(res)
            break
        except Exception as e:
            chatbot.append([f"The{j}Attempt to generate code, Failed", f"Error tracking\n```\n{trimmed_format_exc()}\n```\n"])
            yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Code generation ends, Start executing
    try:
        import multiprocessing
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=subprocess_worker, args=(instance, file_path, return_dict))
        # only has 10 seconds to run
        p.start(); p.join(timeout=10)
        if p.is_alive(): p.terminate(); p.join()
        p.close()
        res = return_dict['result']
        # res = instance.run(file_path)
    except Exception as e:
        chatbot.append(["Execution failed", f"Error tracking\n```\n{trimmed_format_exc()}\n```\n"])
        # chatbot.append(["If it is缺乏依赖, 请参考以下Suggestion", installation_advance])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Completed smoothly, Wrap up
    res = str(res)
    if os.path.exists(res):
        chatbot.append(["Execution succeeded, The result is a valid file", "Result：" + res])
        new_file_path = promote_file_to_downloadzone(res, chatbot=chatbot)
        chatbot = for_immediate_show_off_when_possible(file_type, new_file_path, chatbot)
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update
    else:
        chatbot.append(["Execution succeeded, The result is a string", "Result：" + res])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update   

"""
Test：
    Crop image, Keep the lower half
    Swap blue channel and red channel of the image
    Convert the image to grayscale
    Convert CSV file to Excel table
"""