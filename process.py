import json
import openai
import os
import time


# Set up OpenAI API key
openai.api_key = "<put your openAI API key here>"

# Define function to call OpenAI API and fill in bankInfo section
def fill_in_bank_info(description):
    prompt = f"Fill in the bankInfo section based on the description: {description}, \
    and return me in the same format a strict json structure, except with fields in bankinfo filled in. \
    The returned string must use double quotation for all properties such as keys and values.\
    Mske sure to put curly brackets both before and after the string to it is a valid json object. \
     Do not add any other word except the json content."
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    message = completions.choices[0].text.strip()
    print("****************************")
    print(message)
    print("****************************")
    return json.loads(message)

# Read in metadata.json file
with open("metadata.json", "r") as f:
    metadata = json.load(f)

# Loop through each credit card and fill in the bankInfo section using OpenAI API
start = time.time()
success = 0
fail = 0

for cc_num, cc_info in metadata.items():
    description = cc_info
    bank_info = cc_info["bankInfo"]
    if not all(value == "" for value in bank_info.values()):
        continue  # Bank info already filled in, skip to next card
    try:
        filled_in_info = fill_in_bank_info(description)
        success += 1
    except Exception as e:
        filled_in_info = description
        fail += 1
        print(e)
    bank_info.update(filled_in_info.get("bankInfo", {}))

# Write updated metadata to a new json file
with open("updated_metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

end = time.time()
time_elapsed_in_sec = end - start

print("============================")
print("success:       " + str(success))
print("fail:          " + str(fail))
print("time elapsed:  " + str(time_elapsed_in_sec))
print("============================")


