
from newsapi import NewsApiClient
import spacy
import jieba.analyse
from deep_translator import GoogleTranslator

# Init
newsapi = NewsApiClient(api_key='8aa1825732aa43bba611163e5a814f8d')

def getresources():
    resources=newsapi.get_sources()
# print(resources)
    with open ("newsresources.txt","w")as f:
        for resource in resources["sources"]:
            # print(resource['id'])
            f.write(resource["id"]+"\n")

def keywords_extract(question):
    # 加载预训练的模型
    nlp = spacy.load("en_core_web_sm")
    # 定义一个疑问句
    question = question
    # 使用spaCy进行关键词提取
    doc = nlp(question)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
    # 输出提取得到的关键词
    # print(keywords)
    return keywords
def make_info(question):
  keywords=keywords_extract(question)
  query=""
  for keyword in keywords:
      query+="".join(keyword)
      query+=" "
  # print(query)
  all_articles = newsapi.get_everything(q=query,
                                        sort_by="relevancy",
                                        #采用BBC-NEWS因为它的新闻描述没有截断
                                        language='en')
  # print(all_articles)
  articles=all_articles["articles"]
  print(articles)
  info=""
  cnt=0
  for article in articles:
      info+=(str(cnt)+'.')
      info+="".join(article["title"])
      info+=' '
      info+="".join(article["description"])
      info+="\n"
      cnt+=1
      if cnt>40:
          break
  return info



def get_keywords_chi(sentence):
    ans=""
    keywords = jieba.analyse.extract_tags(sentence, topK=4)
    for keyword in keywords:
        result = GoogleTranslator(source='auto', target='en').translate(keyword)
        ans+="".join(result)
        ans+=" "
    return ans

def make_info_chi(question):
  query=get_keywords_chi(question)
  print(query)
  all_articles = newsapi.get_everything(q=query,
                                        sort_by="relevancy",
                                        #采用BBC-NEWS因为它的新闻描述没有截断
                                        language='en')
  # print(all_articles)
  articles=all_articles["articles"]
  info=""
  cnt=0
  for article in articles:
      info+=(str(cnt)+'.')
      info+="".join(article["title"])
      info+=' '
      info+="".join(article["description"])
      info+="\n"
      cnt+=1
      if cnt>40:
          break
  return info
def make_prompt(question,info):
    prompt="In this Q&A round, I will give a question and a paragraph of material in the following format:\n"\
        "Question: \'\'\'(question body)\'\'\'\n"\
        "Information: \'\'\' (material body)\'\'\'\n"\
        "Suppose you are an information analyst and your task is to extract and summarize information from the messy news data provided and to answer news questions based on the information you obtain. "\
            "All the information I am giving you now is the latest news, and my questions can certainly be answered from this information. You need to do everything you can to find the answer to the question. "\
            "In order to accomplish this task more accurately, you can try: explain and replace the proper noun." \
           "For example: \"basketball\" in the question, then replace it like this: [NBA-- \"basketball association\", [game-- \"basketball game\"]. " \
           "If the question contains a gender, it is also necessary to make an appropriate gender prediction for the name, such as: Brittney Griner's --&gt; A female. Or: John Smith -- a man. If relevant material can be found, it should also be analyzed whether the person is a public figure, such as John Smith----- a male actor."\
           "If my question is about the international situation, you may also need to analyze public figures and place names. For example, the White House ---- the presidential palace of the United States ---- America; Or, Barack Obama ---- former president of the United States; Or, Moscow ---- Russia. I'll give you some information beyond 2021: Current U.S. presidents: Joe Biden; Former U.S. presidents: Donald Trump; Ukrainian Prime Minister: Volodymyr Zelensky."\
           "Note that not all of the information will support your answer, but make sure that there is enough information for you to answer. If you think you can't find the right information, you can first extract the keywords of the question, and then do a keyword search of the entire information to find relevant information."\
           "I do not allow you to say that I did not find appropriate information from the material, so if a similar situation occurs, please give your answer based on information that may be relevant.If there are more than one answer, you need to state it in sections.\""\
          "In addition, if you can't get valid information, you can modify the question accordingly.   For example, relax the scope of the question (What's happening on Someone  ----What's happening that's related to Someone) ,(financial and tax situation ---- Economic situation), etc.   If you want to modify, the requirement is that the problem before and after the modification is strongly related, but the latter is broader.  "\
          "Your answer should not have any prefixes such as \"information:\", \"answer:\", \"situation:\" or anything else."\
          "Finally, your answer does not show your reasoning process or that I have provided you with any information. Your answer should contain only your conclusions."\
           +"\nQuestion:"+ "\'\'\'"+question+"\'\'\'"+"\nInformation:"+"\'\'\'"+info+"\'\'\'"
    print(prompt)
    return prompt
# print("input your question:")
# question=input()
# info=make_info(question)
# print(info)
# print(prompt)
# with open("news.json", "w")as f:
    # for response in articles:
#         f.write(response["url"]+",")
# with open("news.txt","w")as f:
# #     for response in articles:
# #         json.dump(resp, f)
#         f.write(info)
# prompt=make_prompt(question=question,info=info)
# print(prompt)
# print(prompt)
# with open("newsurls.csv", "w")as f:
#     for response in articles:
#         f.write(response["url"]+",")
# with open("news.json","w")as f:
#     for response in articles:
#         json.dump(response, f)
#         f.write(",\n")
