
import gradio as gr
import gpt
examples = [["What are latest news about basketball?"],["What is the current situation in Russia and Ukraine?"],["特朗普近期面临什么指控?"]]
def predict(function, input, temperature):
    # 根据用户选择的函数调用相应的函数
    if function=='GPT-3.5':
        output = gpt.get_completion(input, temperature)
    else:
        output=gpt.custom_get_response(input)
    return output
# 定义选择组件
function_choice = gr.Dropdown(choices=["GPT-3.5", "ChatGLM-6B"],
                                     label="Choose a model")

# 定义输入组件
input_text = gr.inputs.Textbox(lines=4, label="Please input your news question here...")

# 定义温度选择组件
temperature_slider = gr.inputs.Slider(
    label="Select a temperature value from 0 to 1",
    minimum=0,
    maximum=1,
)

# 定义输出组件
output_text = gr.Textbox(label="Answer:", lines=10, placeholder="Show answer based on relevant news here.")

# 定义接口
interface = gr.Interface(
    fn=predict,
    inputs=[input_text, function_choice],
    outputs=output_text,
    title="Low-End New Bing\n"
          "Created by Gao Lang.",
    description="你可以用英文提问比较简短宽泛的时政问题，我们的语言模型可以查找相关新闻并基于此做出回答。\n"
                "参数说明：文本框直接输入英文问句，不要过于详细，一句话即可。\n",
    examples=examples
)



# 运行接口
interface.launch(debug=True, enable_queue=True, share=False)