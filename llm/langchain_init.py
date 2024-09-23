from config.llm_config import LLMConfig
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from llm.promptemplate import prompt_template
from langchain.chat_models import init_chat_model
import torch
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.llms.vllm import VLLMOpenAI
from langchain_community.llms.ollama import Ollama
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline, 
)

prompt = ChatPromptTemplate.from_template(template=prompt_template)

config = LLMConfig()

def get_device():
    return "cuda" if torch.cuda.is_available() and int(config.IS_CUDA) != -1 else "cpu"

def init_huggingface_pipeline(model_id, task, device):
    model = AutoModelForCausalLM.from_pretrained(
        model_id=model_id,
        device_map="auto" if device == "cuda" else None
    )
    return pipeline(
        task=task,
        model=model,
        tokenizer=AutoTokenizer.from_pretrained(model_id),
        max_new_tokens=100,
        trust_remote_code=True,
        device=config.IS_CUDA
    )

model_provider = config.MODEL_PROVIDER

if model_provider == 'huggingface-local':
    huggingface_model = config.HuggingFACE_CACHE
    huggingface_task = config.HuggingFACE_TASK

    device = get_device()
    hf_pipeline = init_huggingface_pipeline(huggingface_model, huggingface_task, device)

    llm = HuggingFacePipeline(
        pipeline=hf_pipeline,
    )

elif model_provider == 'huggingface-endpoint':
    llm = HuggingFaceEndpoint(
        repo_id=config.REPO_MODEL,
        huggingfacehub_api_token=config.HUGGINGFACE_API_KEY
    )

elif model_provider == 'openai':
    llm = init_chat_model(
        model=config.MODEL, 
        base_url=config.OPENAI_BASE_URL,
        api_key=config.OPENAI_API_KEY,
        model_provider=config.MODEL_PROVIDER,
        temperature=0.5,
        max_tokens=config.LLM_MAX_TOKENS,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )

elif model_provider == 'ollama':
    llm = Ollama(
        model=config.OLLAMA_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )

elif model_provider == 'vllm':
    llm = VLLMOpenAI(
        openai_api_key=config.VLLM_API_KEY,
        openai_api_base=config.VLLM_BASE_URL,
        model_name=config.VLLM_MODEL,
    )

# 创建 ConversationSummaryBufferMemory
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=1024)

# 创建一个支持流式输出的对话链
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True
)

# 创建一个新的流式预测函数
async def stream_predict(input_text):
    try:
        response = await conversation.apredict_and_parse(input=input_text)
        for chunk in response:
            yield chunk
    except Exception as e:
        yield f"Error: {str(e)}"

# 导出 stream_predict 函数
__all__ = ['conversation', 'stream_predict']

if __name__ == "__main__":
    conversation.predict(input="你好，今天天气怎么样？")

