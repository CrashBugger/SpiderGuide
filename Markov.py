import random

import requests
from requests import request


def bulidWordDict(text: str):
    # 剔除换行符和引号
    text = text.replace('\n', ' ')
    text = text.replace('"', '')
    # 保证每个标点符号都被当成一个单词
    # 这样就不会剔除，而是保存在马尔科夫链中
    punctuation = [',', ':', '.', ':']
    for symbol in punctuation:
        text.replace(symbol, ' {} '.format(symbol))
    words = text.split(" ")
    # 过滤空单词
    words = [word for word in words if word != '']
    wordDict = {}
    # 构建概率字典,----->前一个单词预测下一个单词
    for i in range(1, len(words)):
        if words[i - 1] not in wordDict:
            wordDict[words[i - 1]] = {}
        if words[i] not in wordDict[words[i - 1]]:
            wordDict[words[i - 1]][words[i]] = 0
        # 总是会执行到
        wordDict[words[i - 1]][words[i]] += 1
    return wordDict


def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum


def retrieveRandomWord(wordList):
    randIndex = random.randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        # 用占的块大小和随机大小randIndex表示概率
        if randIndex <= 0:
            return word


if __name__ == '__main__':
    resp = requests.get("https://pythonscraping.com/files/inaugurationSpeech.txt")
    text = resp.text
    wordDict = bulidWordDict(text)
    # 生成链长为100的马尔科夫链
    length = 100
    chain = ['I']
    for i in range(0, length):
        newWord = retrieveRandomWord(wordDict[chain[-1]])
        chain.append(newWord)
    print(" ".join(chain))
