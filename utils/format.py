from argument.argument_dict import (
        emo_dict,
        emoji_dict,
        event_dict,
        lang_dict,
)
from argument.argument_set import (
        emo_set,
        event_set,
)

def format_str(s):
    """
    格式化字符串,将特殊标记替换为对应的表情符号
    
    参数:
        s (str): 要格式化的字符串
    
    返回:
        str: 格式化后的字符串
    """
    for sptk in emoji_dict:
        s = s.replace(sptk, emoji_dict[sptk])
    return s


def format_str_v2(s):
    """
    格式化字符串,处理表情、事件和语言标记
    
    参数:
        s (str): 要格式化的字符串
    
    返回:
        str: 格式化后的字符串
    """
    sptk_dict = {}
    for sptk in emoji_dict:
        sptk_dict[sptk] = s.count(sptk)
        s = s.replace(sptk, "")
    emo = "<|NEUTRAL|>"
    for e in emo_dict:
        if sptk_dict[e] > sptk_dict[emo]:
            emo = e
    for e in event_dict:
        if sptk_dict[e] > 0:
            s = event_dict[e] + s
    s = s + emo_dict[emo]

    for emoji in emo_set.union(event_set):
        s = s.replace(" " + emoji, emoji)
        s = s.replace(emoji + " ", emoji)
    return s.strip()

def format_str_v3(s):
    """
    格式化字符串,处理表情、事件和语言标记(版本3)
    
    参数:
        s (str): 要格式化的字符串
    
    返回:
        str: 格式化后的字符串
    """
    # 获取字符串中的情感标记
    def get_emo(s):
        return s[-1] if s[-1] in emo_set else None
    
    # 获取字符串中的事件标记
    def get_event(s):
        return s[0] if s[0] in event_set else None

    # 替换特定的标记为问号
    s = s.replace("<|nospeech|><|Event_UNK|>", "❓")
    
    # 替换语言标记
    for lang in lang_dict:
        s = s.replace(lang, "<|lang|>")
    
    # 分割字符串并格式化每个部分
    s_list = [format_str_v2(s_i).strip(" ") for s_i in s.split("<|lang|>")]
    
    # 初始化新字符串
    new_s = " " + s_list[0]
    cur_ent_event = get_event(new_s)
    
    # 处理剩余的字符串部分
    for i in range(1, len(s_list)):
        if len(s_list[i]) == 0:
            continue
        # 如果当前部分的事件标记与前一个相同且不为None，则移除事件标记
        if get_event(s_list[i]) == cur_ent_event and get_event(s_list[i]) != None:
            s_list[i] = s_list[i][1:]
        cur_ent_event = get_event(s_list[i])
        # 如果当前部分的情感标记与新字符串的情感标记相同，则移除新字符串的情感标记
        if get_emo(s_list[i]) != None and get_emo(s_list[i]) == get_emo(new_s):
            new_s = new_s[:-1]
        # 添加当前部分到新字符串
        new_s += s_list[i].strip().lstrip()
    
    # 移除特定的字符串
    new_s = new_s.replace("The.", " ")
    
    # 返回处理后的字符串
    return new_s.strip()