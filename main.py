# Python native libs
import os
import random
import sys
import time

# Open source libs
import matplotlib.pyplot as plt
import pandas as pd
from pytrends.request import TrendReq

# Local files
from keywords import get_topic_ids

# Log in & keyword setup
DEFAULT_KEYWORD_FILE = "keyword.txt"
cred = "credentials.txt"
google_username, google_password = [line.strip() for line in open(cred, "r").readlines()]
logged_in = [False]
pytrend = None

def compare_two_keywords(keyword1, keyword2=None, pytrend=pytrend):
    # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
    if keyword2 is None:
        pytrend.build_payload(kw_list=[keyword1], timeframe='all')
        interest_df = pytrend.interest_over_time()
    else:
        pytrend.build_payload(kw_list=[keyword1, keyword2], timeframe='all')
        # Interest Over Time
        interest_df = pytrend.interest_over_time()
        if 100 not in interest_df[keyword1].values:
            interest_df = interest_df.reindex(columns=[keyword2, keyword1])
    return interest_df

def keywords_over_time(max_keyword, max_mid, other_keywords, keyword_file, overwrite=False):
    if os.path.isfile(keyword_file + ".csv") and not overwrite:
        pd.read_csv(keyword_file + ".csv")

    # Get "Normalizer" Trend
    normalizer = compare_two_keywords(max_mid, pytrend=pytrend)
    final = pd.DataFrame(columns = [max_keyword], index=normalizer.index)
    final[max_keyword] = normalizer[max_mid]

    # Compare other trends to normalizer
    for other_key, other_mid in other_keywords.items():
        df = compare_two_keywords(max_mid, other_mid, pytrend=pytrend)
        if df[other_mid].sum() > 0:
            final[other_key] = df[other_mid].copy()
            print("Finished %s" % other_key)
            print("%s, %s\n" % (str(df[other_mid].min()), str(df[other_mid].max())))
        else:
            print("%s had all zero values" % other_key)

    final.to_csv(keyword_file + ".csv")
    return final

def get_trends(max_keyword, keyword_map, keyword_file):
    max_mid = keyword_map[max_keyword]
    del(keyword_map[max_keyword])
    df = keywords_over_time(max_keyword, max_mid, keyword_map, keyword_file)

    # Plot Trends
    fig = plt.figure()
    df.plot()
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.savefig("GoogleTrends-" + keyword_file + ".png", bbox_inches="tight")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        keyword_file = DEFAULT_KEYWORD_FILE
    else:
        keyword_file = sys.argv[1]
    keywords = [f.strip() for f in open(keyword_file, "r").readlines()]
    pytrend = TrendReq(google_username, google_password, custom_useragent='trendy')
    keyword_map = get_topic_ids(pytrend, keywords)
    get_trends(keywords[0], keyword_map, keyword_file.split(".")[0])
