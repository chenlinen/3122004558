import os
import jieba
import gensim
import re

import coverage
def get_file_contents(path):
    """
        功能：定义读取文件内容的函数
        参数：路径
        返回值：str类型的文件内容
    """
    string = ''
    fo = open(path, 'r', encoding='UTF-8')  # 打开文件
    line = fo.readline()
    while line:
        string = string + line
        line = fo.readline()
    fo.close()
    return string


if __name__ == '__main__':
    # 初始化coverage对象，设置覆盖率度量方式为语句覆盖率
    cov = coverage.Coverage(omit=['*.test.py'])

    # 开始统计覆盖率
    cov.start()
    path1 = input("输入原文件的绝对路径：")
    path2 = input("输入抄袭文件的绝对路径：")
    if not os.path.exists(path1):
        print("原文件不存在！")
        exit()
    if not os.path.exists(path2):
        print("抄袭文件不存在！")
        exit()

    # 读取文件内容
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    # 消除内容中的逗号，句号等符号，只提取文字，字母
    pattern = r"[^a-zA-Z0-9\u4e00-\u9fa5]"
    str_new1 = re.sub(pattern, '', str1)
    str_new2 = re.sub(pattern, '', str2)
    # 对文件内容进行分词
    result1 = jieba.lcut(str_new1)
    result2 = jieba.lcut(str_new2)
    print('原文件分词结果', result1)
    print('抄袭文件分词结果', result2)
    # 传入过滤之后的数据，通过调用gensim.similarities.Similarity计算余弦相似度
    texts = [result1, result2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(result1)
    result = similarity[test_corpus_1][1]
    print("文章相似度： %.6f" % result)
    cov.stop()
    # 将相似度结果写入指定文件
    f = open(r'.\\test\save_result.txt', 'w',
             encoding="utf-8")
    f.write("文章相似度： %.2f" % result)
    f.close()
    # 停止统计覆盖率

    # 生成自定义覆盖率报告
    cov.report(omit=['*.test.py'])
