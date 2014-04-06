#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<zhiyuan>--
  Purpose: 
  Created: 2014/3/28
"""
import time
import datetime
from sphinxapi import *

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


class Sphinx_search():
    
    #----------------------------------------------------------------------
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
    #----------------------------------------------------------------------
    def query(self, q):
        count = 3
        while count:
            try:
                res = self.cl.Query (q, 'delta main' )
            except:
                pass
            if 'res' in dir():
                self.cl._reqs = []
                break
            count = count-1
            self.cl._reqs = []
            time.sleep(0.5)
        if 'res' not in dir():
            return [None, None]
        results = []
        info = {}
        if res.has_key('matches') and res.has_key('total_found') and res.has_key('words'):
            for match in res['matches']:
                match['attrs']['name'] = match['attrs'].pop('name_new')
                if match['attrs']['creation_date']:
                    match['attrs']['creation_date'] = self.timestamp_datetime(match['attrs']['creation_date'])
                else:
                    match['attrs']['creation_date']  = None
                results.append(match['attrs'])
            for k in ['time','total_found','words']:
                info[k] = res[k]
            #info = {k:res.get(k) for k in ['time','total_found','words']}
                #sql = "select * from magnet where id = %s"
                #result = self.db.query(sql,match['id'])
                #results.append(result[0])
        return [info, results]    
    #----------------------------------------------------------------------
    def timestamp_datetime(self, value):
        '''Unix timestamp'''
        format = '%Y-%m-%d'
        value = time.localtime(value)
        dt = time.strftime(format, value)
        return dt
        
    
    #def query_bits(self, q=sphinx_conf['q']):
        #res = self.cl.Query ( q, 'bitsnoop' )
        #results = []
        #if res.has_key('matches'):
            #for match in res['matches']:
                #sql = "select * from bitsnoop where id = %s"
                #result = self.db.query(sql,match['id'])
                #results.append(result[0])
        #return results    