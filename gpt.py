import os
import json
import getnews_en
import openai
from transformers import AutoTokenizer, AutoModel
openai.api_key='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'
import re

def is_chinese_sentence(s):
    """
    判断字符串是否为中文句子
    """
    pattern = re.compile(u'[\u4e00-\u9fa5]+[，。！？；]?')
    return bool(pattern.match(s))


def get_completion(question,temperature=0.5,model='gpt-3.5-turbo-0613'):
  prompt=""
  if is_chinese_sentence(question) == False:
    info = getnews_en.make_info(question)#这里仅仅包含了判断问题为英文的部分，后面还要补中文的处理。
  else:
    info= getnews_en.make_info_chi(question)#中文关键词抽取后翻译英文，并且获取新闻
    prompt+= "你的最终输出应该是中文。"
  prompt+=getnews_en.make_prompt(question=question,info=info)
  # print(prompt)
  messages=[{"role":"user","content":prompt}]
  response=openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=temperature
  )
  return response.choices[0].message["content"]

def custom_get_response(question):
  prompt = ""
  if is_chinese_sentence(question) == False:
    info = getnews_en.make_info(question)  # 这里仅仅包含了判断问题为英文的部分，后面还要补中文的处理。
  else:
    info = getnews_en.make_info_chi(question)  # 中文关键词抽取后翻译英文，并且获取新闻
    prompt += "你的最终输出应该是中文。"
  prompt += getnews_en.make_prompt(question=question, info=info)
  # print(prompt)
  tokenizer = AutoTokenizer.from_pretrained("E:\作业\科研项目\WLUNLP\OLDBING\THUDM\chatglm-6b",
                                            trust_remote_code=True,
                                            local_files_only=True)
  model = AutoModel.from_pretrained("E:\作业\科研项目\WLUNLP\OLDBING\THUDM\chatglm-6b",
                                    trust_remote_code=True,
                                    local_files_only=True).half().cuda()
  response, history = model.chat(tokenizer, prompt)
  return response