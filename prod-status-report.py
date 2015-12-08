#!/usr/bin/env python
import argparse
import json
from jinja2 import Template, Environment, PackageLoader
from datetime import date, timedelta

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
    wa.update(description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus varius dictum metus vel ornare. Aliquam ac rutrum turpis. Aenean hendrerit et nisi ac cursus. Sed a finibus nibh, tempus venenatis massa. Aliquam iaculis et urna vitae sodales. Phasellus cursus aliquam velit. Suspendisse sit amet lectus imperdiet, dapibus erat aliquam, eleifend enim. Sed convallis laoreet erat at vehicula. Curabitur euismod lacus lacinia rhoncus lobortis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc nec tortor vitae urna hendrerit tempor." +

     "Sed elementum purus risus, eget bibendum nisi ultrices at. In hac habitasse platea dictumst. Fusce condimentum vulputate nibh, aliquet sodales magna sollicitudin a. Fusce id rutrum magna, quis sollicitudin augue. Praesent cursus accumsan purus in condimentum. Nullam ac mollis ipsum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec interdum ex sed nulla tincidunt cursus. Phasellus cursus quam at venenatis vehicula. Mauris hendrerit elementum mi, aliquet vestibulum mauris porta ut. Mauris elementum ante id luctus gravida. Quisque blandit vel velit interdum hendrerit. Integer ac nisl nibh")

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

#Statistics about work done from meta information
#No of coffees drank, number of line changes, number of incorrect commands etc
#def statistics():

def main():
    print "Subject: {}".format(gen_subject())
    print template.render(workareas=work_areas(),
            keyupdates=key_updates(),
            expectedevents=upcoming_events()
            )

if __name__ == "__main__":
    main()
