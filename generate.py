from transformers import AutoTokenizer, AutoModel
question=input()
tokenizer = AutoTokenizer.from_pretrained("E:\作业\科研项目\WLUNLP\OLDBING\THUDM\chatglm-6b",  trust_remote_code=True,local_files_only=True)
model = AutoModel.from_pretrained("E:\作业\科研项目\WLUNLP\OLDBING\THUDM\chatglm-6b",  trust_remote_code=True,local_files_only=True).half().cuda()
response, history = model.chat(tokenizer,question)
print(response)