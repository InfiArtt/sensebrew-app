import json
import urllib.request

with open('keys.json', 'r', encoding='utf-8') as f:
    keys = json.load(f)

api_key = 'AIzaSyAfhSwpVzfD4DPQBGn2CkouqMCgLNhg7sI'
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'

def translate(text):
    prompt = "Translate the following Indonesian coffee brewing instruction to English. Return ONLY the English translation:\n\n" + text
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print(e)
        return text

translated = {'desc': {}, 'extra': {}}
print("Translating desc...")
for k, v in keys['desc'].items():
    translated['desc'][k] = translate(v)
print("Translating extra...")
for k, v in keys['extra'].items():
    translated['extra'][k] = translate(v)

with open('translated.json', 'w', encoding='utf-8') as out:
    json.dump(translated, out, ensure_ascii=False)
print("Done")
