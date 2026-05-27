# ========== 第1步：导入工具包 ==========
import requests      # 【大白话：负责"上网发请求"的工具，就像浏览器一样】
import json          # 【大白话：负责处理JSON格式，一种网络通用的"快递单格式"】
import os            # 【大白话：负责读取电脑环境变量，用来安全存放密码】
from datetime import datetime  # 【大白话：获取当前时间，用来给聊天记录打时间戳】


# ========== 第2步：配置信息 ==========
# 【大白话：API-KEY就是"门卡"，没有它阿里云不让你用AI。不要直接写在代码里，容易被偷】
API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

# 【大白话：URL就是"收件地址"，告诉程序把问题发到阿里云哪个房间】
URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# 【大白话：聊天记录要存进哪个文件】
HISTORY_FILE = "history.txt"


# ========== 第3步：对话历史（这是实现"多轮对话"的关键） ==========
# 【大白话：messages是一个"记忆盒子"，里面按顺序放着System设定、用户说的话、AI说的话】
# 【大白话：System是"给AI的入职培训"，告诉它扮演什么角色，回答什么风格】
messages = [
    {"role": "system", "content": "你是一位知识渊博的助手，回答简洁准确，控制在200字以内。"}
]
# 【大白话：role（角色）有三种：system（系统设定）、user（用户）、assistant（AI）】


# ========== 第4步：联网问AI的函数 ==========
def call_ai(user_input):
    """
    【大白话：这个函数就像"打电话"]】
    输入：用户刚说的话
    输出：AI的回复文字
    """
    
    # 【大白话：先把用户说的话，按"快递单格式"装进记忆盒子】
    messages.append({"role": "user", "content": user_input})
    
    # 【大白话：准备"快递单"的表头，证明你有门卡】
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # 【大白话：Bearer后面跟门卡号，证明身份】
        "Content-Type": "application/json"      # 【大白话：告诉对方"我发的是JSON格式的信"】
    }
    
    # 【大白话：准备"快递包裹"】
    data = {
        "model": "qwen-turbo",  # 【大白话：model就是"你找哪个AI员工回答"，qwen-turbo是通义千问基础版，便宜够用】
        "input": {
            "messages": messages  # 【大白话：把"记忆盒子"整个发过去，AI才能看到之前的对话，实现上下文】
        }
    }
    
    # 【大白话：try...except就是"试一试，万一网断了不崩溃"】
    try:
        # 【大白话：requests.post就是"把信扔进邮筒"，等30秒，超时就认为网络断了】
        response = requests.post(URL, headers=headers, json=data, timeout=30)
        
        # 【大白话：response.json()就是把对方回信从"快递单格式"翻译成Python能看懂的字典】
        result = response.json()
        
        # 【大白话：从回信里提取AI真正说的话。如果这里报错，说明AI没正常回复】
        ai_reply = result["output"]["text"]
        
        # 【大白话：把AI的回复也装进记忆盒子，下次用户追问时，AI能看到自己之前说过什么】
        messages.append({"role": "assistant", "content": ai_reply})
        
        return ai_reply  # 【大白话：把AI的回答"交还给"主程序】
        
    except Exception as e:
        # 【大白话：如果网络断了、门卡错了、AI服务器炸了，就返回错误提示，程序不崩溃】
        return f"【网络或API出错】{e}"


# ========== 第5步：保存聊天记录到文件 ==========
def save_to_file(user_input, ai_reply):
    """
    【大白话：这个函数就像"记日记"，把刚才聊了什么写进硬盘】
    """
    # 【大白话：获取现在的时间，格式：2026-05-28 14:30:00】
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 【大白话：with open就是"打开文件"，a表示追加（append），不覆盖旧记录】
    # 【大白话：encoding="utf-8"保证中文不乱码】
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{now} | 用户：{user_input}\n")   # 【大白话：写入"时间 | 用户：xxx"】
        f.write(f"{now} | AI：{ai_reply}\n")       # 【大白话：写入"时间 | AI：xxx"】
        f.write("-" * 50 + "\n")                   # 【大白话：画一条分割线，美观】


# ========== 第6步：主程序——程序的"大门" ==========
def main():
    # 【大白话：打印欢迎界面】
    print("=" * 40)
    print("命令行AI助手")
    print("输入你的问题，输入'退出'或'quit'结束对话")
    print("=" * 40)
    
    # 【大白话：while True就是"无限循环"，一直等用户说话，直到遇到break才停】
    while True:
        # 【大白话：input就是"在屏幕上显示'你：'，然后光标闪烁等你打字，按回车后把文字存进user_input"】
        user_input = input("\n你：").strip()
        
        # ========== 退出判断 ==========
        # 【大白话：lower()就是把"退出""退出""QUIT"都变成小写"quit"，统一判断】
        if user_input.lower() in ["退出", "再见", "quit", "exit", "bye", "q"]:
            print("AI：再见！聊天记录已保存到 history.txt")
            break  # 【大白话：break就是"砸碎循环"，程序结束】
        
        # 【大白话：如果用户只按了回车，没打字，就跳过这次，重新问】
        if not user_input:
            continue  # 【大白话：continue就是"跳过下面所有代码，从头再来"】
        
        # ========== 调用AI ==========
        print("AI：", end="", flush=True)  # 【大白话：先打印"AI："，不换行，等回复出来再显示】
        reply = call_ai(user_input)        # 【大白话：给"打电话函数"传用户的话，拿回AI回复】
        print(reply)                       # 【大白话：把AI回复显示在屏幕上】
        
        # ========== 保存记录 ==========
        save_to_file(user_input, reply)    # 【大白话：把刚才聊的写进日记本】


# ========== 第7步：程序启动点 ==========
# 【大白话：这行代码的意思是"如果直接运行这个文件，就执行main()；如果被别的文件导入，就不自动执行"】
if __name__ == "__main__":
    main()