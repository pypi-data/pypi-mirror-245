#!/usr/bin/env python3
"""
We create a unit, that will be the test_ unit by ln -s simoultaneously. Runs with 'pytest'
"""
import datetime as dt
import time
import os
import tiktoken
from console import fg,bg,fx
from fire import Fire

import openai
from cmd_ai import config
from cmd_ai import texts
from cmd_ai.version import __version__

# print("v... unit 'unitname' loaded, version:",__version__)



def num_tokens_from_messages(model="gpt-3.5-turbo-0613"):
    """
    Return the number of tokens used by a list of messages.
    Use by force this model 3.5, gpt4 didnt work
    """

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(config.messages, model="gpt-3.5-turbo-0613")

    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return num_tokens_from_messages(config.messages, model="gpt-4")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in config.messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


# ===============================================================================================
def get_price(model, tokens_in = 1, tokens_out = 1):
    if model == "gpt-4-1106-preview":
        return 0.01/1000 * tokens_in + 0.03/1000 * tokens_out
    if model == "gpt-4":
        return 0.03/1000 * tokens_in + 0.06/1000 * tokens_out
    if model == "gpt-4-32k":
        return 0.06/1000 * tokens_in + 0.12/1000 * tokens_out
    if model == "gpt-3.5-turbo-1106":
        return 0.001/1000 * tokens_in + 0.002/1000 * tokens_out
    return -1

# ===============================================================================================
def log_price(model, tokens_in = 1, tokens_out = 1):
    price = round(100000*get_price( model, tokens_in, tokens_out ))/100000
    with open( os.path.expanduser( config.CONFIG['pricelog']), "a" )  as f:
        now = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        f.write(f"{now} {tokens_in} {tokens_out} {price}")
        f.write("\n")

def g_ask_chat(prompt, temp, model, limit_tokens=300, total_model_tokens=4096 * 2 - 50):
    """
    CORE ChatGPT function
    """
    # global task_assis, limit_tokens

    # ---- if no system present, add it
    if len(config.messages) == 0:
        config.messages.append({"role": "system", "content": texts.role_assistant})
    # add the message~
    config.messages.append({"role": "user", "content": prompt})

    max_tokens = total_model_tokens - num_tokens_from_messages()
    limit_tokens = config.CONFIG['limit_tokens']
    if limit_tokens < max_tokens:
        max_tokens = limit_tokens
    now = dt.datetime.now().replace(microsecond=0)

    print(
        f"i...  max_tokens= {max_tokens}, model = {model};  task: {(now-config.started_task).total_seconds()}; total:{(now-config.started_total).total_seconds()}"
    )

    # THIS CAN OBTAIN ERROR: enai.error.RateLimitError: Rate limit reached for 10KTPM-200RPM in organization org-YaucYGaAecppFiTrhbnquVvB on tokens per min. Limit: 10000 / min. Please try again in 6ms.
    # token size block it

    waittime = [
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
    ]
    DONE = len(waittime) - 1
    responded = False
    while DONE > 0:  # I forgot to decrease
        DONE -= 1
        time.sleep(1 * waittime[0])
        try:
            # print(messages)
            print(bg.white," --> ", bg.default, end="", flush=True)

            response = config.client.chat.completions.create(
                # model="gpt-3.5-turbo",
                model=model,
                messages=config.messages,
                temperature=temp,
                max_tokens=max_tokens,
            )
            print("...",bg.green," >>OK", bg.default)
            DONE = 0
            responded = True
            # print(response)
        # except Exception as e:
        #     print(f"An error occurred:  {type(e)}.. <{str(e)}>")
        #     print(e.keys())#error.message)
        #     print(
        #         f"i... re-trying {DONE+1}x more time ... after {waittime[0]} seconds ..."
        #     )
        #     time.sleep(1 * waittime[0])
        #     waittime.pop(0)
        #     DONE -= 1


        except openai.RateLimitError as e:
            retry_time = e.retry_after if hasattr(e, 'retry_after') else 1 * waittime[0]
            #if hasattr(e,"message"): print(e.message)
            if hasattr(e,"code"): print(e.code)
            if hasattr(e,"type"): print(e.type)
            print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
            time.sleep(retry_time)
            waittime.pop(0)
            DONE -= 1

        except openai.APIError as e:
            retry_time = e.retry_after if hasattr(e, 'retry_after') else 1 * waittime[0]
            if hasattr(e,"code"): print(e.code)
            if hasattr(e,"type"): print(e.type)
            print(f"API error occurred. Retrying in {retry_time} seconds...")
            time.sleep( retry_time)
            waittime.pop(0)
            DONE -= 1

        except openai.ServiceUnavailableError as e:
            retry_time = 10  # Adjust the retry time as needed
            if hasattr(e,"code"): print(e.code)
            if hasattr(e,"type"): print(e.type)
            print(f"Service is unavailable. Retrying in {retry_time} seconds...")
            time.sleep(1 * waittime[0])
            waittime.pop(0)
            DONE -= 1

        except openai.Timeout as e:
            retry_time = 10  # Adjust the retry time as needed
            if hasattr(e,"code"): print(e.code)
            if hasattr(e,"type"): print(e.type)
            print(f"Request timed out: {e}. Retrying in {retry_time} seconds...")
            time.sleep(1 * waittime[0])
            waittime.pop(0)
            DONE -= 1

        except OSError as e:
            if isinstance(e, tuple) and len(e) == 2 and isinstance(e[1], OSError):
                retry_time = 10  # Adjust the retry time as needed
                if hasattr(e,"code"): print(e.code)
                if hasattr(e,"type"): print(e.type)
                print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")
                time.sleep(1 * waittime[0])
                waittime.pop(0)
                DONE -= 1


            else:
                retry_time = 10  # Adjust the retry time as needed
                print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")
                time.sleep(retry_time)
                raise e







    # print("i... OK SENT")
    if not responded:
        print("i... NOT RESPONDED  ====================================")
        return None

    #print(type(response))
    #print(str(response))

    resdi = response.choices[0].message.content
    finish = response.choices[0].finish_reason
    tokens_out = response.usage.completion_tokens
    tokens_in = response.usage.prompt_tokens
    tokens = response.usage.total_tokens
    price = get_price( model, tokens_in, tokens_out)
    print(f"i... tokens: {tokens_in} in + {tokens_out} out == {tokens}  for {round(price*10000)/10000}$")
    log_price( model, tokens_in, tokens_out )
    if finish != "stop": print(f"!... {fg.red} stopped because : {finish} {fg.default}")
    # resdi = json.loads( str(response)  )
    return resdi
    # print(resdi)

    # ========================================================================


def g_askme(
    prompt,
    temp=0.0,
    model="gpt-4-1106-preview",
    limit_tokens=300,
    total_model_tokens=4096 * 2 - 50, # guess
):

    estimate_tokens = num_tokens_from_messages() + len(prompt) + 600
    estimate_tokens = 300
    resdi = g_ask_chat(
        prompt, temp, model, estimate_tokens
    )

    if resdi is None:
        return None
    return resdi


if __name__ == "__main__":
    print("i... in the __main__ of unitname of cmd_ai")
    Fire()
