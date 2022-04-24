import re
import string


def cleanSentence(sentence):
    sentence = sentence.split(' ')
    sentence = [word.strip(string.punctuation + string.whitespace) for word in sentence]
    sentence = [word for word in sentence if len(word) > 1 or (word.lower() == 'a' or word.lower() == 'i')]
    return sentence


def cleanInput(content):
    content = re.sub('\n|[[\d+\]]', ' ', content)
    # 过滤仅留下ASCII编码
    content = bytes(content, "utf-8")
    content = content.decode("ascii", "ignore")
    sentences = content.split('.')
    return [cleanSentence(sentence) for sentence in sentences]


def getNgramFromSentence(content, n):
    output = []
    for i in range(len(content) - n + 1):
        output.append(content[i:i + n])
    return output


def getNgrams(content, n):
    content = cleanInput(content)
    ngrams = []
    for sentence in content:
        ngrams.append(getNgramFromSentence(sentence), n)
    return ngrams


if __name__ == '__main__':
    print(string.punctuation + string.whitespace)
