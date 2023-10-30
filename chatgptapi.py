import openai

openai.organization = ""
openai.api_key = ''

def gptpredict(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
        messages=[{"role": "user", "content": f'determine if this review satisfied or not: "{text}"answear with 1 or 0,ONLY and ONLY a single digit nothing else'}])
    reply=completion.choices[0].message.content
    print(reply)
    if (reply=='0' or reply=='1'):
        return int(reply)
    else:
        return 0

def replygen(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
        messages=[{"role": "user", "content": f'this client is unsatisfied with the product that they purchesed :"{text}" write an response to this client based on their problem as you are the seller.start the msg with dear client and end it with best regards Sales Team'}])
    
    return completion.choices[0].message.content

def replygen(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
        messages=[{"role": "user", "content": f'this client is unsatisfied with the product that they purchesed :"{text}" write an response to this client based on their problem as you are the seller.start the msg with dear client and end it with best regards Sales Team'}])
    return completion.choices[0].message.content

def replygen2(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
        messages=[{"role": "user", "content": f'this client is satisfied with the product that they purchesed :"{text}" write an response to thank them for their postive feedback as you are the seller.start the msg with dear client and end it with best regards Sales Team'}])
    return completion.choices[0].message.content