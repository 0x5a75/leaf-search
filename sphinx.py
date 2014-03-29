
sphinx_conf = {'q' : '',
               'mode' : SPH_MATCH_ALL,
               'host' : 'localhost',
               'port' : 9312,
               'index' : '*',
               'filtercol' : 'group_id',
               'filtervals' : [],
               'sortby' : '',
               'groupby' : '',
               'groupsort' : '@group desc',
               'limit' : 200
               }

db = torndb.Connection("127.0.0.1", "dht", "root", "admin")

class Sphinx_search():
    def __init__(self):
        self.cl = SphinxClient()
        self.cl.SetServer ( sphinx_conf['host'], sphinx_conf['port'] )
        self.cl.SetMatchMode ( sphinx_conf['mode'] )
        if sphinx_conf['filtervals']:
            self.cl.SetFilter ( sphinx_conf['filtercol'], sphinx_conf['filtervals'] )
        if sphinx_conf['groupby']:
            self.cl.SetGroupBy ( sphinx_conf['groupby'], SPH_GROUPBY_ATTR, groupsort )
        if sphinx_conf['sortby']:
            self.cl.SetSortMode ( SPH_SORT_EXTENDED, sphinx_conf['sortby'] )
        if sphinx_conf['limit']:
            self.cl.SetLimits ( 0, sphinx_conf['limit'], max(sphinx_conf['limit'],200) )
        
    def query(self, q=sphinx_conf['q']):
        res = self.cl.Query ( q, sphinx_conf['index'] )
        results = []
        if res.has_key('matches'):
            for match in res['matches']:
                sql = "select * from magnet where id = %s"
                result = db.query(sql,match['id'])
                results.append(result[0])
        return results