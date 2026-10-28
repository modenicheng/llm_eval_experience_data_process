# llm_eval_experience_data_process

主观评测的数据处理脚本。输入两份 CSV——[llms_eval](https://github.com/modenicheng/llms_eval) 导出的会话记录和人工逐条打分表——合并成结构化的 `data.json`。

```python
class ModelAnwser(TypedDict):
    quest_id: str
    platform: str
    model: str
    content: str | None      # 模型回答
    reasoning: str | None    # 思维链
    score: float | None      # 人工评分
    comment: str | None      # 评语


class Data(TypedDict):
    quest_id: str
    aspect: Optional[str]     # 考察维度
    judgement: Optional[str]  # 评分标准
    prompt: str
    data: list[ModelAnwser]
```

背景：11 道手搓的防污染主观题 × 9 个模型，题目设计、评分标准和逐题分析见[博文](https://modenc.top/blog/wtn59ea4/)。

```bash
uv run main.py  # 两份 CSV 需在当前目录
```
