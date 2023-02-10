from flask import Flask, jsonify, request, send_from_directory, abort
import os
from waitress import serve
from flask_cors import CORS
from openai.embeddings_utils import get_embedding, cosine_similarity

import openai
import os
import emoji
import pandas as pd
import io
import json

from tqdm import tqdm

import numpy as np

from dotenv import load_dotenv
load_dotenv()

openaiOrg = os.getenv('openaiOrg', default=None)
openaiKey = os.getenv('openaiKey', default=None)
authKey = os.getenv('authKey', default=None)

openai.organization = openaiOrg
openai.api_key = openaiKey

app = Flask(__name__)
CORS(app)

MODEL = "text-embedding-ada-002"

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'X-CF-AUTH-KEY': authKey
}

print("downloading csvs")

embed_files = ['https://pulltweets.lohxt.workers.dev/embeds__0_2500__elonmusk__Yyjp4tU_1b.csv','https://pulltweets.lohxt.workers.dev/embeds__2500_5000__elonmusk__Yyjp4tU_1b.csv','https://pulltweets.lohxt.workers.dev/embeds__5000_7500__elonmusk__Yyjp4tU_1b.csv','https://pulltweets.lohxt.workers.dev/embeds__7500_10000__elonmusk__Yyjp4tU_1b.csv','https://pulltweets.lohxt.workers.dev/embeds__10000_12500__elonmusk__Yyjp4tU_1b.csv','https://pulltweets.lohxt.workers.dev/embeds__12500_15000__elonmusk__Yyjp4tU_1b.csv','https://pulltweets.lohxt.workers.dev/embeds__15000_17500__elonmusk__Yyjp4tU_1b.csv','https://pulltweets.lohxt.workers.dev/embeds__17500_20000__elonmusk__Yyjp4tU_1b.csv']
df = pd.concat((pd.read_csv(f, storage_options=hdr) for f in embed_files), ignore_index=True)

print("downloaded csvs")
print(df.shape)

# fix the embeds column
df.embeds = df.embeds.apply(eval).apply(np.array)
# fix the reply_to column
df['reply_to'] = df['reply_to'].apply(lambda x: eval(x))

df = df[['tweet', 'nlikes', 'nreplies', 'nretweets', 'reply_to', 'link', 'embeds', 'retweet']]

print("df formatted")

def search_text(__df, query, n=2000):
    embedding = get_embedding(
        query,
        engine=MODEL
    )
    __df["similarities"] = __df.embeds.apply(lambda x: cosine_similarity(x, embedding))

    ___df = __df.sort_values("similarities", ascending=False)
    res = ___df[___df['similarities'].apply(lambda x: x > 0.8)]
    res['tweet'] = res['tweet'].apply(lambda x: emoji.emojize(x))

    return res.head(n)

@app.route('/')
def index():
    return jsonify({"status":"alive" }), 202

@app.route("/search/<query>", methods=["GET"])
def searchFunc(query):
    res = search_text(df, query)
    result = json.loads(res.to_json(orient = "records"))
    return jsonify(result), 202

@app.route("/search", methods=["POST"])
def searchPostFunc():
    data = request.json
    query = data.get('query')
    tweetLengthLimit = data.get('tweetLengthLimit') or 0
    excludeReplies = data.get('excludeReplies') or False
    if query:
        res = search_text(df, query)

        if tweetLengthLimit > 0:
            # filter out tweets greater than string length 10
            res = res[ res['tweet'].apply(lambda x: len(x) > tweetLengthLimit) ]

        if excludeReplies:
            # filter out replies
            res = res[ res['reply_to'].apply(lambda x: len(list(x)) <= 0) ]

        result = json.loads(res.to_json(orient = "records"))
        return jsonify(result), 202

    return jsonify({"error":"invalid query"}), 202

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=os.getenv("PORT", default=5000))