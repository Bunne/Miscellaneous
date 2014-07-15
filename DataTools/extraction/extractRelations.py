import sys
import MySQLdb as msql
from config import Config

CONFIG = Config("config")

class extractRelationsNode(object):
    """Nodes of the extractRelations"""
    def __init__(self, id,name,parent_id):
        super(extractRelationsNode, self).__init__()
        self.id = id
        self.name = name.strip('\"')
        self.parent_id = parent_id
        self.parent_name = ""


class extractRelations(object):
    """Convert csv to tree"""
    def __init__(self,table, colID, colName, colRel):
        super(extractRelations, self).__init__()
        self.table = table
        self.colID = colID
        self.colName = colName
        self.colRel = colRel
        self.dbData = ()
        self.tree = []
        self.__extract()
        self.__create()
        self.__convert()

    def __str__(self):
        tree_rep = "Object, Parent"
        for node in self.tree:
            if node.parent_name:
                tree_rep += "\n{}, {}".format(node.name,node.parent_name)
        return tree_rep

    def __extract(self):
        try:
            cxn = msql.connect(host=CONFIG.get_config("host"),
                                db=CONFIG.get_config("database"),
                                user=CONFIG.get_config("user"),
                                passwd=CONFIG.get_config("password"))
            cur = cxn.cursor()
            cur.execute("SELECT {},{},{} FROM {}".format(self.colID,
                                                         self.colName,
                                                         self.colRel,
                                                         self.table))
            self.dbData = cur.fetchall()
        except Exception, e:
            raise e

    def __create(self):
        for x in self.dbData:
            self.tree.append(extractRelationsNode(int(x[0]),x[1],int(x[2])))

    def __convert(self):
        for node in self.tree:
            if node.parent_id and (node.parent_id not in (0,-1)):
                node.parent_name = [i.name for i in self.tree if i.id == node.parent_id][0]

    def writeOut(self,csvName):
        with open(csvName,'w') as csvOut:
            csvOut.write(tt.__str__())


if __name__ == '__main__':
    tt = extractRelations(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    tt.writeOut(sys.argv[5])