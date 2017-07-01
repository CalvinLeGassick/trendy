# Increasing orders of magnitude:
# movie
# book
# cats
# mouse
# hen
# pickle

def get_topic_ids(pytrend, keywords, debug=False):
    keyword_to_topic_id = {}
    for k in keywords:
        suggestions = pytrend.suggestions(k)
        for s in suggestions:
            if "field" in s["type"].lower() and k.lower() == s["title"].lower():
                if debug: print("%s: %s" % (k, s["mid"]))
                keyword_to_topic_id[k] = s["mid"]
                continue
            if "topic" in s["type"].lower() and k.lower() == s["title"].lower():
                if debug: print("%s: %s" % (k, s["mid"]))
                keyword_to_topic_id[k] = s["mid"]
                continue
            keyword_to_topic_id[k] = k
    return keyword_to_topic_id
