from pyspark import SparkContext

sc = SparkContext("local", "wordcount")
text_file = sc.textFile("Harry Potter 1 - Sorcerer's Stone.txt")
# 其他文件同理可得
# \表示换行连接。(word, 1)中只能为1，是2的话表示出现个数的2倍，3的话表示三倍。
wordcount = text_file.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b)

wordcount.foreach(print)  # 依次打印统计次数
