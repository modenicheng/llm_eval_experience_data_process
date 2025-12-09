import csv
import json
import re
from tokenize import Comment
from rich import print
from typing import Optional, TypedDict

with open("llms_subjective_scores.csv", 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    score_data = list(reader)
    # print(score_data)

with open("eval_session_1764350780851_1765191680240.csv",
          'r',
          encoding="utf-8") as f:
    reader = csv.reader(f)
    eval_data = list(reader)
    # print(eval_data)


class ModelAnwser(TypedDict):
    quest_id: str
    platform: str
    model: str
    content: str | None
    reasoning: str | None
    score: float | None
    comment: str | None


class Data(TypedDict):
    quest_id: str
    aspect: Optional[str]
    judgement: Optional[str]
    prompt: str
    data: list[ModelAnwser]


data: list[Data] = []
# process & organize data

float_patter = r'^\d+(\.\d+)?$'

model_list = []
for item in eval_data:
    delta = (item[3], item[4])
    model_list.append(delta) if delta not in model_list else None

# print(model_list)

for i in range(2, len(score_data) - 1):
    quest_id = score_data[i][0]
    quest_index = int(quest_id.split(".")[0])

    anwser_list = [
        ModelAnwser(
            quest_id=quest_id,
            platform="deepseek",
            model="deepseek-chat",
            content=eval_data[quest_index * 2][6],
            reasoning=eval_data[quest_index * 2][7],
            score=float(score_data[i][3])
            if re.match(float_patter, score_data[i][3]) else None,
            comment=score_data[i][4],
        ),
        ModelAnwser(
            quest_id=quest_id,
            platform="deepseek",
            model="deepseek-reasoner",
            content=eval_data[quest_index * 2 + 22 * 4][6],
            reasoning=eval_data[quest_index * 2 + 22 * 4][7],
            score=float(score_data[i][5])
            if re.match(float_patter, score_data[i][5]) else None,
            comment=score_data[i][6],
        ),
        ModelAnwser(
            quest_id=quest_id,
            platform="deepseek-special",
            model="deepseek-reasoner",
            content=eval_data[quest_index * 2 + 22 * 8][6],
            reasoning=eval_data[quest_index * 2 + (22 * 8)][7],
            score=float(score_data[i][7])
            if re.match(float_patter, score_data[i][7]) else None,
            comment=score_data[i][8],
        ),
        ModelAnwser(
            quest_id=quest_id,
            platform="tongyi",
            model="qwen3-max",
            content=eval_data[quest_index * 2 + 22 * 6][6],
            reasoning=eval_data[quest_index * 2 + 22 * 6][7],
            score=float(score_data[i][9])
            if re.match(float_patter, score_data[i][9]) else None,
            comment=score_data[i][10],
        ),
        ModelAnwser(
            quest_id=quest_id,
            platform="tongyi",
            model="qwen-plus",
            content=eval_data[quest_index * 2 + 22 * 7][6],
            reasoning=eval_data[quest_index * 2 + 22 * 7][7],
            score=float(score_data[i][11])
            if re.match(float_patter, score_data[i][11]) else None,
            comment=score_data[i][12],
        ),
        ModelAnwser(
            quest_id=quest_id,
            platform="moonshot",
            model="kimi-k2-turbo-preview",
            content=eval_data[quest_index * 2 + 22 * 1][6],
            reasoning=eval_data[quest_index * 2 + 22 * 1][7],
            score=float(score_data[i][13])
            if re.match(float_patter, score_data[i][13]) else None,
            comment=score_data[i][14],
        ),
        ModelAnwser(
            quest_id=quest_id,
            platform="moonshot",
            model="kimi-k2-thinking-turbo",
            content=eval_data[quest_index * 2 + 22 * 5][6],
            reasoning=eval_data[quest_index * 2 + 22 * 5][7],
            score=float(score_data[i][15])
            if re.match(float_patter, score_data[i][15]) else None,
            comment=score_data[i][16],
        ),
        ModelAnwser(
            quest_id=quest_id,
            platform="volcengine",
            model="doubao-seed-1-6-251015",
            content=eval_data[quest_index * 2 + 22 * 2][6],
            reasoning=eval_data[quest_index * 2 + 22 * 2][7],
            score=float(score_data[i][17])
            if re.match(float_patter, score_data[i][17]) else None,
            comment=score_data[i][18],
        ),
        ModelAnwser(
            quest_id=quest_id,
            platform="google-aistudio",
            model="gemini-3-pro-preview",
            content=eval_data[quest_index * 2 + 22 * 3][6],
            reasoning=eval_data[quest_index * 2 + 22 * 3][7],
            score=float(score_data[i][19])
            if re.match(float_patter, score_data[i][19]) else None,
            comment=score_data[i][20],
        ),
    ]

    entry = Data(quest_id=quest_id,
                 aspect=score_data[i][1],
                 judgement=score_data[i][2],
                 prompt=eval_data[quest_index * 2 - 1][6],
                 data=anwser_list)

    data.append(entry)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
