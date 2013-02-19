#!/usr/bin/env python

from django.core.management import setup_environ
from kgreg.conf import settings
setup_environ(settings)

from django_pbs.servers.models import Server
from pygooglechart import *
import datetime

DEBUG = False

def gen_graph(width=420, height=130, bar_width=30, title=True, legend=True):


    chart = StackedHorizontalBarChart(width, height)
    chart.set_bar_width(bar_width)
    chart.set_colours(['00FF00','FF0000'])
    if title:
        chart.set_title("VPAC CPUs - generated %s" % datetime.datetime.now().strftime('%d/%m/%y %I:%M%p'))
    if legend:
        chart.set_legend(['Free', 'Used'])

    return chart


def gen_data(server_list):
    used = []
    total = []
    labels = []
    max_total = 0
    for server in server_list:
        try:
            s = Server(server)
            u, t = s.cpu_stats()
            used.append(u)
            total.append(t)
            if t > max_total:
                max_total = t
            labels.append(server.split('.')[0].split('-')[0])
        except:
            pass

        #print "%s - %s - %s" % (server, u, t)
    ratio = 4096.00 / max_total
#    for i in range(len(used)):
#        used[i] = used[i] * ratio

#    for i in range(len(total)):
#        total[i] = (total[i] * ratio)
    for i in range(len(used)):
        total[i] = total[i] - used[i]

    return used, total, max_total, labels

if __name__ == "__main__":

    SERVERS = ['tango-m.vpac.org', 
#               'edda-m.vpac.org',
               ]

    if DEBUG:
        used = [784, 3736, 1232, 288]
        total = [416, 72, 224, 64]
        max_total = 476
        labels = ['brecca', 'tango', 'edda', 'wexstan']
    else:
        used, total, max_total, labels = gen_data(SERVERS)

    chart = gen_graph()
    small_chart = gen_graph(height=70, width=250, bar_width=15, title=False, legend=False)
    chart.add_data(total)
    chart.add_data(used)
    small_chart.add_data(total)
    small_chart.add_data(used)

    labels.reverse()
    chart.set_axis_labels('y', labels)
    small_chart.set_axis_labels('y', labels)
    chart.set_axis_range('x', 0, max_total)
    small_chart.set_axis_range('x', 0, max_total)

    chart.download('%s/img/cpu_stats.png' % settings.MEDIA_ROOT)
    small_chart.download('%s/img/cpu_stats-small.png' % settings.MEDIA_ROOT)
