#!/usr/bin/env python
import argparse
import json
from jinja2 import Template, Environment, PackageLoader
from datetime import datetime, date, timedelta
import re

#TODO functionality
import subprocess
import os
import cStringIO
#Logging
import logging


#from collections import defaultdict

#debug
import pdb
import pprint
pp = pprint.PrettyPrinter(indent=4)

#Template stuff
env = Environment(loader=PackageLoader('prod-status-report', 'templates'))
template = env.get_template('prod-status-report.txt')

def tree():
    return defaultdict(tree)

class TodoList(object):
    def __init__(self):
        self.full_task_list = subprocess.Popen(['todo.sh', 'projectview'],
                stdout=subprocess.PIPE).communicate()[0]
        self.dic = self.as_dict()
        self.history_text = cStringIO.StringIO
        self.history_text = open(os.path.join(os.environ["TODO_DIR"],'done.txt'), 'rb').read()
        self.history = [[d,t] for d, t in self._history()]

    def _history(self, td=timedelta(days=7)):
        task_regex = re.compile('x\s(?P<date>[-0-9]{10})\s(?P<task>.*)')
        for m in task_regex.finditer(self.history_text):
            dt = datetime.strptime(str(m.group('date')), "%Y-%m-%d")
            days_diff = abs(((dt.date()) - date.today()))
            if days_diff.days < td.days:
                yield dt.date(), m.group('task')

    def _projects(self):
        prj = re.compile('---\s+(?P<projtitle>.+\S)\s+---')
        for m in prj.finditer(self.full_task_list):
            yield m.group('projtitle')

    def _tasks(self, project):
        prj = re.compile('(?P<taskid>[0-9]+)\s((?P<priority>\([A-Z]\)|)(?P<task>.+))')
        projtasklist = subprocess.Popen(['todo.sh', 'projectview', project ], stdout=subprocess.PIPE).communicate()[0]
        #Remove not in projects items
        projtasklist = re.sub(r'(Not in projects.*)', r'', projtasklist, re.MULTILINE, re.DOTALL)
        for m in prj.finditer(projtasklist):
            if m.group('taskid') is not None:
                yield m.group('taskid'), m.group('priority'), m.group('task')

    def _contexts(self, task):
        context = re.compile('@(?P<context>[-\w]+)')
        for m in context.finditer(task):
            yield m.group('context')

    def _minutes_spent(self, task):
        m = re.search(r'(min:([0-9]+))', task)
        if m is not None:
            return timedelta(minutes=int(m.group(2)))

    def _strip(self, task):
        return re.sub(r'\x1b[^m]*m|@[-\w]+|(min:([0-9]+))', '', task).strip()


    def __iter__(self):
        for p in self._projects():
            for tid, pri, task in self._tasks(p):
                yield tid, p, pri, self._strip(task), [c for c in self._contexts(task)], self._minutes_spent(task)

    def as_dict(self):
        ret = {}
        for p in self._projects():
            for tid, pri, task in self._tasks(p):
                td = {}
                self._minutes_spent(task)
                td.update({'project':p})
                td.update({'priority':pri})
                td.update({'task':self._strip(task)})
                td.update({'contexts':[c for c in self._contexts(task)]})
                td.update({'timespent':self._minutes_spent(task)})
                ret.update({tid:td})
        return ret

def gen_subject():
    subject = "Prod status "
    d = date.today()
    td = timedelta(d.weekday())
    week_start = d - td
    subject += week_start.isoformat()
    return subject

#Maybe meta information from todo.sh/ip-config git commits
def work_areas(tdl):
    wa = {}

    for tid, p, pri, task, contexts, timespend in tdl:
        if wa.has_key(p):
            e = wa[p].get('events')
            e.append(task)
        else:
            wa.update({p:{'events':[task]}})
    return wa

#Maybe a database/flatfile of events
def significant_events():
    se = "Significant Events:\n\t"
    return se

#Tie in with work_areas
def key_updates():
    ku = dict()
    return ku

#Grab from todo.sh
def upcoming_events():
    ue = dict()
    return ue


#Statistics about work done from meta information
#No of coffees drank, number of line changes, number of incorrect commands etc
#def statistics():


def main():
    tdl = TodoList()
    print "Subject: {}".format(gen_subject())
    print template.render(workareas=work_areas(tdl),
            keyupdates=key_updates(),
            expectedevents=upcoming_events()
            )

if __name__ == "__main__":
    main()
