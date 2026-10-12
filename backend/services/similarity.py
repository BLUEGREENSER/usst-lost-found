import jieba
from flask import current_app

STOP_WORDS = {"的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没", "看", "好", "这", "那", "他", "她", "它", "们", "个", "中", "来", "对", "下", "里", "面", "吧", "被", "把", "给", "向", "从", "与", "或", "但", "而", "则"}


def tokenize(text):
    if not text:
        return set()
    words = jieba.lcut(text)
    return {w.strip() for w in words if w.strip() and w not in STOP_WORDS and len(w.strip()) > 0}


def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 0.0
    union = set_a | set_b
    if not union:
        return 0.0
    return len(set_a & set_b) / len(union)


class SimilarityCalculator:
    def compute(self, lost, found):
        w_cat = current_app.config["MATCH_WEIGHT_CATEGORY"]
        w_name = current_app.config["MATCH_WEIGHT_NAME"]
        w_desc = current_app.config["MATCH_WEIGHT_DESCRIPTION"]
        w_loc = current_app.config["MATCH_WEIGHT_LOCATION"]

        s_category = 1.0 if lost.category == found.category else 0.0

        lost_name_tokens = tokenize(lost.name)
        found_name_tokens = tokenize(found.name)
        s_name = jaccard(lost_name_tokens, found_name_tokens)

        lost_desc_tokens = tokenize(lost.description)
        found_desc_tokens = tokenize(found.description)
        s_description = jaccard(lost_desc_tokens, found_desc_tokens)

        lost_loc_tokens = tokenize(lost.location)
        found_loc_tokens = tokenize(found.location)
        s_location = jaccard(lost_loc_tokens, found_loc_tokens)

        total = w_cat * s_category + w_name * s_name + w_desc * s_description + w_loc * s_location

        hit_keywords = list((lost_name_tokens & found_name_tokens) | (lost_desc_tokens & found_desc_tokens))

        dimensions = {
            "category": round(s_category, 4),
            "name": round(s_name, 4),
            "description": round(s_description, 4),
            "location": round(s_location, 4),
            "hit_keywords": hit_keywords[:10],
        }

        return round(total, 4), dimensions


similarity_calculator = SimilarityCalculator()