
import gpt
print("input your question:")
question=input()
response = gpt.get_completion(question,temperature=0,model='gpt-3.5-turbo-0613')
print(response)