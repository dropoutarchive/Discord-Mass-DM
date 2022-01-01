import json, time, os
start = time.time()
with open ("data/tokens.json") as f:
    tokens = json.load(f)
with open('data/tokens.txt') as f:
    all_infos = [i.strip() for i in f]
f.close()



total_tokens = 0

for i in all_infos:
    token = i.split(":")
    for i in token:
        if len(i) > 50:
            if "@" not in i:
                if "!" not in i:
                    if "?" not in i:
                        if i not in tokens:
                            total_tokens += 1
                            tokens.append(i)

with open("data/tokens.json", "w") as file:
    json.dump(tokens, file)
end = time.time()
print(f"Formatted {total_tokens} tokens in {end - start}s")
