# REFERENCES
# https://pymotw.com/3/threading/
# https://realpython.com/intro-to-python-threading/
# https://docs.python.org/3/library/concurrent.futures.html
# https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
# https://stackoverflow.com/questions/3221655/python-threading-string-arguments
# https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
# https://medium.com/school-of-code/classmethod-vs-staticmethod-in-python-8fe63efb1797

# Currently, we are using threading with nested threadpoolexecutor due to the instability of asyncio (still developing and changing APIs...)
# https://stackoverflow.com/questions/44989473/nesting-concurrent-futures-threadpoolexecutor


# IMPORTS
from enum import Enum
from tools import stdo, timeLog, timeList
import threading
from concurrent.futures import ThreadPoolExecutor
from inspect import currentframe, getframeinfo

# GLOBALS
globalMap = None
globalMapEngine = None
globalLock = threading.Lock()


# globalErrorInformation = None


# CLASSES
class Rotation(Enum):
    up = 0
    right = 1
    down = 2
    left = 3


class NodeWay(Enum):
    up = 0
    right = 1
    down = 2
    left = 3


class MapCorner(Enum):
    leftDown = 0
    leftUp = 1
    rightDown = 2
    rightUp = 3


class RobotStruct(object):
    def __init__(self, id = None, Rotation=Rotation.up):
        # Node ID
        self.id = id

        # Neighbor Nodes
        self.currentNode = None
        self.nodeHistory = []
        self.upNode = None
        self.downNode = None
        self.leftNode = None
        self.rightNode = None

    def moveOneNode(self, destinationNodeID):
        if self.upNode.id == destinationNodeID:
            self.currentNode = self.upNode
        elif self.downNode.id == destinationNodeID:
            self.currentNode = self.downNode
        elif self.rightNode.id == destinationNodeID:
            self.currentNode = self.rightNode
        elif self.leftNode.id == destinationNodeID:
            self.currentNode = self.leftNode


class objectStruct(object):
    def __init__(self, id = None, nodeID = None):
        self.id = None
        self.node = None
        self.currentNode = None


class nodeStruct(object):
    idCounter = 0

    def __init__(self, name = None, object = None):
        # Changed with __new__function
        # self.id = self.getID()

        self.name = name
        self.object = object
        self.weight = 0
        self.id = self.idCounter

        # Neighbor Nodes
        self.upNode = None
        self.downNode = None
        self.leftNode = None
        self.rightNode = None

        self.connectedNodeList = [None]

    # https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new
    def __new__(cls, name = None, object = None):
        # Node ID
        nodeStruct.idCounter += 1
        return super(nodeStruct, cls).__new__(cls)


class mapStruct(object):
    idCounter = 0

    def __init__(self, mapName = "Map", mapStartNodeCorner = MapCorner.leftDown):
        self.name = mapName
        self.id = self.idCounter
        self.headNode = nodeStruct(name = "base", object = None)  # To store head of map, also can be start point
        self.mapStartCorner = mapStartNodeCorner
        self.cachedNode = None  # To store a temporary node, usually last modified or checked
        self.nodeCounter = 0  # To store the number of nodes in map

        self._lock = threading.Lock()  # To ensure there will be no rise condition between threads at searching (DO NOT USE DIRECTLY)
        self.searchedNodeHistory = list()  # To store a history of last search (CRITICAL SECTION - DO NOT USE DIRECTLY)
        self.containsObjectNodes = list()  # To store a nodes which are contains objects (CRITICAL SECTION - DO NOT USE DIRECTLY)
        self.nodeList = list()  # To store nodes in map for fast reach

    # https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new
    def __new__(cls, name = None, object = None):
        # Node ID
        mapStruct.idCounter += 1
        return super(mapStruct, cls).__new__(cls)

    def addSearchHistory(self, node):
        """
            Adds given node to map's search history to remember checked nodes. Necessary to use because this function locks the access of critical section while working with multiple threads.

            Used class variables
                _lock   -> lock object for critical section (DO NOT USE DIRECTLY)
                searchedNodeHistory -> List of checked nodes to remember while using search function (CRITICAL SECTION - DO NOT USE DIRECTLY)
        """
        with self._lock:
            self.searchedNodeHistory.append(node)
        """
        self._lock.acquire()
        map.searchedNodeHistory.append(node)
        self._lock.release()
        """

    def clearSearchHistory(self):
        with self._lock:
            self.searchedNodeHistory.clear()

    def addObject2node(self, node):
        with self._lock:
            self.containsObjectNodes.append(node)

    def addNode2MapContainer(self, node):
        with self._lock:
            self.containsObjectNodes.append(node)


class mapEngine(object):
    def __init__(self):
        self.mapList = list()

    def createMap(self, mapName, mapStartNodeCorner = MapCorner.leftDown):
        self.mapList.append(mapStruct(mapName, mapStartNodeCorner))
        return self.mapList[-1]

    @staticmethod
    def getMapBase(map):
        return map.headNode

    @staticmethod
    def getMapInfo(map, silent = True):
        if not silent:
            stdo(1, string = """
                Map ID\t\t\t: {}
                Map Name\t\t\t: {}
                Number of Node\t: {}
                """)
        return map.id, map.name, map.nodeCounter

    def getAllMapsInfo(self, silent = True):
        cache = list()
        for map in self.mapList:
            cache.append(self.getMapInfo(map, silent))
        return cache

    @staticmethod
    def addNode2MapContainer(map, node):
        # Parameter 'node' variable can be a list or tuple which means contains
        # more than 1 node
        if isinstance(node, list) or isinstance(node, tuple):
            for n in node:
                map.nodeList.append(n)
            return len(node)

        # Parameter 'node' variable can be a node which means it is 1 node
        elif isinstance(node, nodeStruct):
            map.nodeList.append(node)
            return 1

        # Parameter 'node' variable can be anything else which means nothing to
        # this function
        else:
            return -1

    @staticmethod
    def autoInitofMapNodeContainer(map):
        # Development state
        stdo(3, "This API still at development state", getframeinfo( currentframe()) )

    @staticmethod
    def removeNodeFromMapContainer(map, node):
        if node in map.nodeList:
            map.nodeList.remove(node)
        else:
            stdo(2, "Map '{}' has no node named '{}'".format(map.name, node.name))

    @staticmethod
    def connect2node(firstNode, firstNodeWay, secondNode):
        if firstNodeWay is NodeWay.up:
            firstNode.upNode = secondNode
            firstNode.connectedNodeList.insert(0, firstNode.upNode)
            secondNode.downNode = firstNode
            secondNode.connectedNodeList.insert(0, secondNode.downNode)

        elif firstNodeWay is NodeWay.right:
            firstNode.rightNode = secondNode
            firstNode.connectedNodeList.insert(0, firstNode.rightNode)
            secondNode.leftNode = firstNode
            secondNode.connectedNodeList.insert(0, secondNode.leftNode)

        elif firstNodeWay is NodeWay.down:
            firstNode.downNode = secondNode
            firstNode.connectedNodeList.insert(0, firstNode.downNode)
            secondNode.upNode = firstNode
            secondNode.connectedNodeList.insert(0, secondNode.upNode)

        elif firstNodeWay is NodeWay.left:
            firstNode.leftNode = secondNode
            firstNode.connectedNodeList.insert(0, firstNode.leftNode)
            secondNode.rightNode = firstNode
            secondNode.connectedNodeList.insert(0, secondNode.rightNode)

    def searchNode(self, map, startNode, destinationNodeName):
        # If given start node is not we are looking for, check connected sub nodes with threading
        if startNode.name != destinationNodeName:
            map.clearSearchHistory()
            map.addSearchHistory(startNode)
            threadList = list()
            returnedPaths = list()

            with ThreadPoolExecutor(max_workers = None) as executor:
                for node in startNode.connectedNodeList:
                    if node not in map.searchedNodeHistory:
                        map.addSearchHistory(node)
                        threadList.append(
                            executor.submit(
                                self.__searchThread,
                                map,
                                node,
                                destinationNodeName
                            )
                        )

                for thread in threadList:
                    # Here, we will wait for threads one by one, and store their
                    # return elements which will be Path to object if found
                    if thread.result() is not None:
                        for path in thread.result():
                            returnedPaths.append(path)

                    """     # OLD Return Control
                    path = thread.result()
                    if path is not None:
                        returnedPaths.append(path)
                    """     # OLD Return Control
                    # else:
                    #    stdo(2, "{} Thread Return Value Eliminated: {}".format(threading.currentThread()._ident, path))

                # Here, we will sort paths upon their lengths which depends number of elements
                if len(returnedPaths) > 1:
                    # Here, we won't sort paths upon their lengths which
                    # depends number of elements because it will be a waste
                    # of time and power in CPU usage.
                    # returnedPaths.sort(key = len, reverse = False)

                    # We will return all paths because even if we eliminate
                    # some of them now, this may not be shortest path at search
                    # moment. However and only we can sort and select best
                    # path, after all search process done (finished jobs of all
                    # search threads).
                    # Footnote: At this section, we don't have None returned
                    # paths, which means didn't find the destination node. So
                    # all paths will be useful for us.
                    for path in returnedPaths:
                        path.append(startNode)
                    return startNode, returnedPaths

                elif len(returnedPaths) == 1:
                    # Here, we have only 1 returned path, so there is no need to sort
                    returnedPaths[0].append(startNode)
                    return startNode, returnedPaths

                else:
                    # This section include 3 different scenarios;
                    # 1.) There is no such node named in variable
                    # destinationNodeName (Cause User Actions)
                    # 2.) Search threads may block the neighbor nodes which
                    # cause no search activity at center of searched nodes
                    # (This makes like a wall because search threads remembers
                    # searched nodes and avoids to search again)
                    # (Cause Developer Actions)
                    # 3.) There are some improper node connections
                    # (Cause User Actions)
                    stdo(3, """There is no returned path from thread.
                        1.) There is no such node named in variable destinationNodeName (Cause User Actions)
                        2.) Search threads may block the neighbor nodes which cause no search activity at center of searched nodes (This makes like a wall because search threads remembers saerched nodes and avoids to search again) (Cause Developer Actions)
                        3.) There are some improper node connections (Cause User Actions)

                    Please inform the developer in detail if you sure it is 2. scenario. Otherwise, check your node or/and map structure connections.
                        Developer e-mail: msaidbilgehan@gmail.com""", getframeinfo(currentframe()) )
                    return startNode, None

        else:
            return startNode, [[startNode]]

    def __searchThread(self, map, currentNode, destinationNodeName):

        if currentNode is not None:
            # If given start node is not we are looking for, check connected sub nodes with threading
            if currentNode.name != destinationNodeName:
                localThreadList = list()
                returnedPaths = list()

                try:
                    with ThreadPoolExecutor(max_workers = None) as executor:
                        for node in currentNode.connectedNodeList:
                            if node not in map.searchedNodeHistory:
                                map.addSearchHistory(node)
                                localThreadList.append(
                                    executor.submit(
                                        self.__searchThread,
                                        map,
                                        node,
                                        destinationNodeName
                                    )
                                )

                        for thread in localThreadList:
                            # Results always will be nested lists
                            if thread.result() is not None:
                                for path in thread.result():
                                    returnedPaths.append(path)

                            """     # FOR DEBUG
                            else:
                                stdo(2, "Returned Value to {} Thread Eliminated: {}".format(threading.currentThread()._ident, path))
                            """     # FOR DEBUG

                except Exception as error:  # FOR DEBUG

                    neighborNodes = ""

                    if currentNode.upNode is not None:
                        neighborNodes += """\t\t\t\t\t\t\t\t\t\t\t|> upNode: {}""".format(
                            currentNode.rightNode.name)

                    if currentNode.rightNode is not None:
                        neighborNodes += """\n\t\t\t\t\t\t\t\t\t\t\t|> rightNode: {}""".format(
                            currentNode.rightNode.name)

                    if currentNode.downNode is not None:
                        neighborNodes += """\n\t\t\t\t\t\t\t\t\t\t\t|> downNode: {}""".format(
                            currentNode.downNode.name)

                    if currentNode.leftNode is not None:
                        neighborNodes += """\n\t\t\t\t\t\t\t\t\t\t\t|> leftNode: {}""".format(
                            currentNode.leftNode.name)

                    stdo(3, """An error ocurred while searching the map in '__searchThread' function
                                Error:  {}
                                Variables
                                    |- currentNode.name:    {}
{}
                                    |- localThreadList:     {}
                                    '- destinitionNodeName: {}""".format(
                                        error.__str__(),
                                        currentNode.name,
                                        neighborNodes,
                                        localThreadList,
                                        destinationNodeName),
                            getframeinfo(currentframe()))
                    """ # FOR DEBUG
                    output = "Thread '{}' at '{}' information's".format(threading.currentThread()_ident, threading.currentThread().getName())
                    counter = len(thread.__dict__)
                    for k, v in thread.__dict__.items():
                        counter -= 1
                        if counter == 0:
                            output += "\n\t\t\t\t\t'- {:20} : {}".format(k, v)
                        else:
                            output += "\n\t\t\t\t\t|- {:20} : {}".format(k, v)
                    stdo( 3, output )
                    """  # FOR DEBUG

                # for path in returnedPaths:
                if len(returnedPaths) > 1:
                    # Here, we won't sort paths upon their lengths which
                    # depends number of elements because it will be a waste
                    # of time and power in CPU usage.
                    # returnedPaths.sort(key = len, reverse = False)

                    # We will return all paths because even if we eliminate
                    # some of them now, this may not be shortest path at search
                    # moment. However and only we can sort and select best
                    # path, after all search process done (finished jobs of all
                    # search threads).
                    # Footnote 1: At this section, we don't have None returned
                    # paths, which means didn't find the destination node. So
                    # all paths will be useful for us.
                    # Footnote 2: Actually, we can reduce code in this
                    # statement (len(returnedPaths) > 1) and next statement
                    # (len(returnedPaths) == 1). But it makes the code slower.
                    # Thats why we have 2 different action;
                    #   1) a for loop for more than 1 returned path
                    #   2) a basic append action to list of returned path for
                    #      1 returned path
                    for path in returnedPaths:
                        path.append(currentNode)
                    return returnedPaths

                elif len(returnedPaths) == 1:
                    # Here, we have only 1 returned path, so there is no need to sort
                    returnedPaths[0].append(currentNode)
                    return returnedPaths

                else:
                    # Here, we have no returned path (None can be returned from threads but None types will be eliminated)
                    # stdo(2, "There is no returned path from thread '{}'.".format(threading.currentThread()._ident))
                    return None

            else:
                return [[currentNode]]

        else:  # If currentNode is none, we archived end of the path, didn't find the destinition
            return None

    def createNode(self, nodeName = None, nodeObject = None):
        return nodeStruct(name = nodeName, object = nodeObject)

    def createAndConnectNode(self, destinitionNodeName = None, newNodeNeighbor = NodeWay.up, newNode = None):
        stdo(3, "Still at development state", getframeinfo(currentframe()) )
        exit(-1)


# FUNCTIONS
def init():
    global globalMap
    globalMap = mapEngine.createMap(mapName = "Example Map")

    return 0


def mapExample():
    """
        An example of manuel mapping. Inspired from ITURO 2020 Challenge real map. Referenced in github.
    """
    mapObject = None
    mEngine = None

    def init():
        nonlocal mapObject, mEngine
        # INITIALIZING NODES
        mEngine = mapEngine()
        mapObject = mEngine.createMap(mapName = "Example Map", mapStartNodeCorner = MapCorner.leftDown)

        base = mEngine.getMapBase(mapObject)

        e5 = mEngine.createNode(nodeName = "e5")
        e4 = mEngine.createNode(nodeName = "e4")
        e3 = mEngine.createNode(nodeName = "e3")
        e2 = mEngine.createNode(nodeName = "e2")
        e1 = mEngine.createNode(nodeName = "e1")

        d4 = mEngine.createNode(nodeName = "d4")
        d3 = mEngine.createNode(nodeName = "d3")
        d2 = mEngine.createNode(nodeName = "d2")
        d1 = mEngine.createNode(nodeName = "d1")

        c4 = mEngine.createNode(nodeName = "c4")
        c3 = mEngine.createNode(nodeName = "c3")
        c2 = mEngine.createNode(nodeName = "c2")
        c1 = mEngine.createNode(nodeName = "c1")

        b4 = mEngine.createNode(nodeName = "b4")
        b3 = mEngine.createNode(nodeName = "b3")
        b2 = mEngine.createNode(nodeName = "b2")
        b1 = mEngine.createNode(nodeName = "b1")

        a4 = mEngine.createNode(nodeName = "a4")
        a3 = mEngine.createNode(nodeName = "a3")
        a2 = mEngine.createNode(nodeName = "a2")
        a1 = mEngine.createNode(nodeName = "a1")

        # CONNECTING NODES
        # mEngine.connect2node(firstNode, firstNodeWay (NodeWay.up), secondNode)

        # Base and E Connections
        mEngine.connect2node(base, NodeWay.up, e5)
        mEngine.connect2node(e5, NodeWay.right, e4)

        # E Row Connections
        mEngine.connect2node(e4, NodeWay.right, e3)
        mEngine.connect2node(e3, NodeWay.right, e2)
        mEngine.connect2node(e2, NodeWay.right, e1)

        # E Column Connections
        mEngine.connect2node(e4, NodeWay.up, d4)
        mEngine.connect2node(e3, NodeWay.up, d3)
        mEngine.connect2node(e2, NodeWay.up, d2)
        mEngine.connect2node(e1, NodeWay.up, d1)

        # D Row Connections
        mEngine.connect2node(d4, NodeWay.right, d3)
        mEngine.connect2node(d3, NodeWay.right, d2)
        mEngine.connect2node(d2, NodeWay.right, d1)

        # D Column Connections
        mEngine.connect2node(d4, NodeWay.up, c4)
        mEngine.connect2node(d3, NodeWay.up, c3)
        mEngine.connect2node(d2, NodeWay.up, c2)
        mEngine.connect2node(d1, NodeWay.up, c1)

        # C Row Connections
        mEngine.connect2node(c4, NodeWay.right, c3)
        mEngine.connect2node(c3, NodeWay.right, c2)
        mEngine.connect2node(c2, NodeWay.right, c1)

        # C Column Connections
        mEngine.connect2node(c4, NodeWay.up, b4)
        mEngine.connect2node(c3, NodeWay.up, b3)
        mEngine.connect2node(c2, NodeWay.up, b2)
        mEngine.connect2node(c1, NodeWay.up, b1)

        # B Row Connections
        mEngine.connect2node(b4, NodeWay.right, b3)
        mEngine.connect2node(b3, NodeWay.right, b2)
        mEngine.connect2node(b2, NodeWay.right, b1)

        # B Column Connections
        mEngine.connect2node(b4, NodeWay.up, a4)  # Left Up Corner A4
        mEngine.connect2node(b3, NodeWay.up, a3)
        mEngine.connect2node(b2, NodeWay.up, a2)
        mEngine.connect2node(b1, NodeWay.up, a1)

        # A Row Connections - UP WALL
        mEngine.connect2node(a4, NodeWay.right, a3)
        mEngine.connect2node(a3, NodeWay.right, a2)
        mEngine.connect2node(a2, NodeWay.right, a1)  # Right Up Corner A1

    # Function's Body
    init()
    return mapObject, mEngine


def specialScenario(destinations = None, startNode = None):
    global globalMap, globalMapEngine

    if destinations is None:
        destinations = ["b2", "b3", "a4", "c2", "c1"]
    if destinations is None:
        startNode = ["b3", "b3", "a4", "c2", "c1"]

    globalMap, globalMapEngine = mapExample()
    bestPaths = list()
    passedTime = 0

    for dest in destinations:
        timeLog("start", id = "nodeSearch-{}".format(dest), isShared = False)
        startNode, tempBestPath = globalMapEngine.searchNode(globalMap, globalMapEngine.getMapBase(globalMap), dest)
        bestPaths.append(tempBestPath[0])
        timeLog("end", id = "nodeSearch-{}".format(dest), isShared = False)
        stdo(1, "{:7.3f} ms time passed for '{}' node search".format(timeList["nodeSearch-{}".format(dest)]["passed"], dest) )
        passedTime += timeList["nodeSearch-{}".format(dest)]["passed"]

    for path in bestPaths:
        pathOutput = ""
        for node in path:
            pathOutput += "{} <- ".format(node.name)
        pathOutput = pathOutput[:-4]
        stdo(1, """Start Node:
                    |- Name: {}
                    '- Best Path: {}\n""".format(startNode.name, pathOutput))

    stdo( 1, "Sum of Passed Time: {:.3f} ms - Average of One Search: {:.3f} ms".format(passedTime, passedTime/len(destinations)) )

    return 0


# MAIN
def main():
    # init()
    specialScenario()
    return 0


if __name__ == '__main__':
    main()
