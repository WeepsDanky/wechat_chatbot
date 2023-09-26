import openai
import tiktoken 
import os

def gpt_request(role, prompt, model="gpt-3.5-turbo-0613"):
    response = openai.ChatCompletion.create(
        model=model, 
        messages = [
            {"role": "system", "content" : "I need you to be my personal secretary. I will give you previous chat records, and then you need to respond based on these chat messages. For example, if the other person sends you a message, 你今天晚上要来吃饭吗? You need to reply: 好的，我知道了我会转告给我的主人，问他今天要不要吃饭呢。"}, 
            {"role": role, "content": prompt}
            ], 
        user = "mark"
    )
    return response['choices'][0]['message']['content']
        

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""") 

'''
def main(): 
    gpt_request("user", "你好")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os._exit(1)
'''