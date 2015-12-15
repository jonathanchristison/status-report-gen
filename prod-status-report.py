#!/usr/bin/env python
import argparse
import json
from jinja2 import Template, Environment, PackageLoader
from datetime import date, timedelta
import subprocess
import re
import pdb

env = Environment(loader=PackageLoader('prod-status-report', 'templates'))
template = env.get_template('prod-status-report.txt')

#Logging
import logging

def gen_subject():
    subject = "Prod status "
    d = date.today()
    td = timedelta(d.weekday())
    week_start = d - td
    subject += week_start.isoformat()
    return subject

#Maybe meta information from todo.sh/ip-config git commits
def work_areas():
    wa = dict()
    wa.update(name="Fuse")
    wa.update(description="")

    return [wa]

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

tasklist = subprocess.Popen(['todo.sh', 'projectview'], stdout=subprocess.PIPE).communicate()[0]
#ansi_escape = re.compile(r'\x1b[^m]*m')
#tasklist = ansi_escape.sub('',tasklist)
def from_todo(projname=None):


    #prj = re.compile('(---\s+)(?P<projtitle>.+\S)(\s+---)|(?P<taskid>^[0-9]+)\s((?P<priority>\([a-zA-Z]\)|)(?P<task>.+))')
    #prj = re.compile('---\s+(?P<projtitle>.+\S)\s+---|(?P<taskid>[0-9]+)\s((?P<priority>\([A-Z]\)|)(?P<task>.+))')
    prj = re.compile('---\s+(?P<projtitle>.+\S)\s+---')
    if projname is None:
        #tasklist = subprocess.Popen(['todo.sh', 'projectview'], stdout=subprocess.PIPE).communicate()[0]
        for m in prj.finditer(tasklist):
            yield m.group('projtitle')
    else:
        prj = re.compile('(?P<taskid>[0-9]+)\s((?P<priority>\([A-Z]\)|)(?P<task>.+))')
        projtasklist = subprocess.Popen(['todo.sh', 'projectview', projname ], stdout=subprocess.PIPE).communicate()[0]
        #Remove not in projects item
        projtasklist = re.sub(r'(Not in projects.*)', r'', projtasklist, re.MULTILINE, re.DOTALL)
        for m in prj.finditer(projtasklist):
            if m.group('taskid') is not None:
                yield m.group('taskid'), m.group('priority'), m.group('task')

    #regex for --- PROJECT NAME --- and create list with children


#Statistics about work done from meta information
#No of coffees drank, number of line changes, number of incorrect commands etc
#def statistics():


def main():
    print "Subject: {}".format(gen_subject())
    for proj in from_todo():
        if proj is not None:
            print '\'' + proj + '\''
            for taskid, pri, task in from_todo(proj):
                print taskid
                print pri
                print task

    print template.render(workareas=work_areas(),
            keyupdates=key_updates(),
            expectedevents=upcoming_events()
            )

if __name__ == "__main__":
    main()
