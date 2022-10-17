def load_dataset():
    dataset = [['egg', 'milk', 'bread', 'beer'],
               ['egg', 'milk', 'bread'],
               ['cola', 'beer'],
               ['cola', 'egg', 'bread']]
    return dataset


def createInitSet(dataSet):
    """产生初始数据集合"""
    retDict = {}
    for trans in dataSet:
        f_set = frozenset(trans)
        retDict.setdefault(f_set, 0)
        retDict[f_set] += 1
    return retDict


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print('   ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)


def createTree(dataSet, minSup=0):
    headerTable = {}
    # 此一次遍历数据集， 记录每个数据项的支持度
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + 1

    # 根据最小支持度过滤
    lessThanMinsup = list(filter(lambda k: headerTable[k] < minSup, headerTable.keys()))
    for k in lessThanMinsup:
        del (headerTable[k])

    freqItemSet = set(headerTable.keys())
    # 如果所有数据都不满足最小支持度，返回None, None
    if len(freqItemSet) == 0:
        return None, None

    for k in headerTable:
        headerTable[k] = [headerTable[k], None]

    retTree = treeNode('φ', 1, None)
    # 第二次遍历数据集，构建fp-tree
    for tranSet, count in dataSet.items():
        # 根据最小支持度处理一条训练样本，key:样本中的一个样例，value:该样例的的全局支持度
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]

        if len(localD) > 0:
            # 根据全局频繁项对每个事务中的数据进行排序,等价于 order by p[1] desc, p[0] desc
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: (p[1], p[0]), reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # 检查该元素是否已经存在fp树中
        inTree.children[items[0]].inc(count)  # 计数+1
    else:  # 不存在则添加到fp树中
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] is None:  # 更新头表
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

    if len(items) > 1:  # 截取已排序list的剩余部分，并以当前节点作为父节点
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink is not None:  # 找到尾节点
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def ascendTree(leafNode, prefixPath):
    """获取当前节点的所有祖先"""
    if leafNode.parent is not None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, headTable):
    """获取当前频繁项的所有前缀路径（条件模式基）"""
    condPats = {}
    treeNode = headTable[basePat][1]
    while treeNode is not None:
        # 获取当前频繁项的所有前缀路径（条件模式基）
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count  # 该条件模式基获得该节点所具有的置信度
        treeNode = treeNode.nodeLink
    return condPats


def mineTree(inTree, headerTable, minSup=1, preFix=set([]), freqItemList=[]):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: (p[1][0], p[0]))]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        # 通过条件模式基找到的频繁项集
        condPattBases = findPrefixPath(basePat, headerTable)
        # 创建条件fp树
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead is not None:
            print('condPattBases: ', basePat, condPattBases)
            myCondTree.disp()
            print('*' * 30)

            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


def main():
    simpDat = load_dataset()
    dictDat = createInitSet(simpDat)
    myFPTree, myheader = createTree(dictDat, 3)
    myFPTree.disp()
    print('*' * 30)
    # 获取条件模式基
    for key in [v[0] for v in sorted(myheader.items(), key=lambda p: (p[1][0], p[0]), reverse=True)]:
        condPats = findPrefixPath(key, myheader)
        print(key, condPats)
    print('*' * 30)
    # 创建条件fp树
    mineTree(myFPTree, myheader, 2)


if __name__ == '__main__':
    main()
