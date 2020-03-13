#!/usr/bin/env python3
# coding: utf-8

from collections import defaultdict
import re
import matplotlib.pyplot as plt
import os
import json


def time_to_int(time_str):
    # mu_sec
    try:
        return int(time_str)
    except:
        t = time_str.split(':')
        if len(t) == 2:
            h = 0
            m = int(t[0])
            s = float(t[1])
        elif len(t) == 3:
            h = int(t[0])
            m = int(t[1])
            s = float(t[2])
        else:
            raise Exception("Time format error: %s" % time_str)
        return (3600_000 * h + 60_000 * m + int(s*1000 + 0.1)) * 1000

'''
01:56.382	ID:1	[INFO: App       ] Sending request 0 to 6G-005
01:56.467	ID:5	[INFO: App       ] Received request 0 from 6G-001
01:56.467	ID:5	[INFO: App       ] Sending response 0 to 6G-001
01:56.637	ID:1	[INFO: App       ] Received response 0 from 6G-005
'''

def parseApp(log):
    res = re.compile(r'(\S+)\s+?ID:(\d+)\s+?\[.*?\] Sending (.+?) (\d+) to 6G-([\dabcdef]+)\s?').match(log)
    if res:
        _time = time_to_int(res.group(1))
        _src = int(res.group(2))
        _type = res.group(3)
        _id = int(res.group(4))
        _dest = int(res.group(5), 16)
        return {'event': 'send', 'type': _type, 'id': _id, 'src': _src, 'dest': _dest, 'time': _time}
    res = re.compile(r'(\S+)\s+?ID:(\d+)\s+?\[.*?\] Received (.+?) (\d+) from 6G-([\dabcdef]+)\s?').match(log)
    if res:
        _time = time_to_int(res.group(1))
        _dest = int(res.group(2))
        _type = res.group(3)
        _id = int(res.group(4))
        _src = int(res.group(5), 16)
        return {'event': 'recv', 'type': _type, 'id': _id, 'src': _src, 'dest': _dest, 'time': _time}
    return None


def parse_file(file):
    send_items = {}
    recv_items = {}
    all_json = []
    err_line = ""

    with open(file, 'r') as fr:
        for line in fr.readlines():
            if "[INFO: App" not in line:
                continue
            res = parseApp(line)
            if not res:
                err_line += line
                continue
            all_json.append(res)
            if res['event'] == 'send':
                send_items[(res['src'], res['dest'], res['id'], res['type'])] = res['time']
            else:
                recv_items[(res['src'], res['dest'], res['id'], res['type'])] = res['time']

    return send_items, recv_items, all_json, err_line


time_unit = 1_000_000 # unit in micro sec, 1 s = 1,000,000 ms
SMALL_NUM = 1e-20

def analyse_data(file, base_dir='./', file_prefix='', time_interval_secs=[0.5, 1, 1.5, 2, 5, 10], draw_fig=True, save_json=True):
    # file = 'log-20200227-201756/COOJA.testlog'
    if file_prefix:
        file_prefix = file_prefix.rstrip("_") + "_"

    parse_res = parse_file(os.path.join(base_dir, file))
    sends = parse_res[0]
    recvs = parse_res[1]

    with open(os.path.join(base_dir, '%slog_err_app_lines.txt' % file_prefix), 'w') as fw:
        fw.write(parse_res[3])

    latency_count = []
    deliver_count = []
    for msg in sends:
        if msg in recvs:
            deliver_count.append(1)
            latency_count.append(recvs[msg] - sends[msg])
        else:
            deliver_count.append(0)

    avg_latency = sum(latency_count) / (len(latency_count) + SMALL_NUM)
    avg_deliver_rate = sum(deliver_count) / (len(deliver_count) + SMALL_NUM)

    parse_info = ""
    parse_info += "packet sent count:      %d\n" % len(sends)
    parse_info += "packet received count:  %d\n" % len(recvs)
    parse_info += "average latency:        %.6f\n" % avg_latency
    parse_info += "average delivery ratio: %.6f\n" % avg_deliver_rate

    with open(os.path.join(base_dir, '%sparse_info.txt' % file_prefix), 'w') as fw:
        fw.write(parse_info)

    if save_json:
        with open(os.path.join(base_dir, '%slog_data.json' % file_prefix), 'w') as fw:
            json.dump(parse_res[2], fw, indent=2)

    for time_interval_sec in time_interval_secs:
        group_analysis(sends, recvs, time_interval_sec, base_dir, file_prefix, draw_fig, save_json)

def group_analysis(sends, recvs, time_interval_sec, base_dir, file_prefix, draw_fig, save_json):
    time_interval = int(time_interval_sec * time_unit)

    all_times = list(sends.values()) + list(recvs.values())
    all_times.sort()
    times = list(range(0, all_times[-1]+1, time_interval))

    deliver_count_time = defaultdict(list)
    latency_count_time = defaultdict(list)

    for msg, send_time in sends.items():
        index = send_time // time_interval
        if msg in recvs:
            recv_time = recvs[msg]
            deliver_count_time[index].append(1)
            latency_count_time[index].append(recv_time - send_time)
        else:
            deliver_count_time[index].append(0)

    deliver_time = [sum(deliver_count_time[i]) / (len(deliver_count_time[i]) + SMALL_NUM) for i in range(len(times))]
    latency_time = [sum(latency_count_time[i]) / (len(latency_count_time[i]) + SMALL_NUM) / time_unit for i in range(len(times))]

    throughput_count_time = defaultdict(int)
    for msg, send_time in sends.items():
        if msg in recvs:
            index = send_time // time_interval
            throughput_count_time[index] += 1
    throughput_time = [throughput_count_time[i] / (time_interval / time_unit) for i in range(len(times))]

    if save_json:
        deliverrate_t = dict(zip([i * time_interval / time_unit for i in range(len(times))], deliver_time))
        with open (os.path.join(base_dir, '%sdeliverrate_ti=%ss.json' % (file_prefix, time_interval_sec)), 'w') as fw:
            json.dump(deliverrate_t, fw, indent=2)

        latency_t = dict(zip([i * time_interval / time_unit for i in range(len(times))], latency_time))
        with open (os.path.join(base_dir, '%slatency_ti=%ss.json' % (file_prefix, time_interval_sec)), 'w') as fw:
            json.dump(latency_t, fw, indent=2)

        throughput_t = dict(zip([i * time_interval / time_unit for i in range(len(times))], throughput_time))
        with open (os.path.join(base_dir, '%sthroughput_ti=%ss.json' % (file_prefix, time_interval_sec)), 'w') as fw:
            json.dump(throughput_t, fw, indent=2)

    if draw_fig:
        plt.figure(figsize=(15, 10))
        plt.plot([i * time_interval / time_unit for i in range(len(times))], deliver_time, 'black', label='deliver rate')
        plt.xlabel('time (s)', family='Times New Roman', fontsize=40)
        plt.ylabel('packet delivery ratio', family='Times New Roman', fontsize=40)
        plt.xticks(family='Times New Roman', fontsize=40)
        plt.yticks(family='Times New Roman', fontsize=40)
        plt.savefig(os.path.join(base_dir, '%sdeliverrate_ti=%ss.png' % (file_prefix, time_interval_sec)))
        plt.close()

        plt.figure(figsize=(15, 10))
        plt.plot([i * time_interval / time_unit for i in range(len(times))], latency_time, 'black', label='latency')
        plt.xlabel('time (s)', family='Times New Roman', fontsize=40)
        plt.ylabel('latency (s)', family='Times New Roman', fontsize=40)
        plt.xticks(family='Times New Roman', fontsize=40)
        plt.yticks(family='Times New Roman', fontsize=40)
        plt.savefig(os.path.join(base_dir, '%slatency_ti=%ss.png' % (file_prefix, time_interval_sec)))
        plt.close()

        plt.figure(figsize=(15, 10))
        plt.plot([i * time_interval / time_unit for i in range(len(times))], throughput_time, 'black', label='throughput')
        plt.xlabel('time (s)', family='Times New Roman', fontsize=40)
        plt.ylabel('throughput (packets/s)', family='Times New Roman', fontsize=40)
        plt.xticks(family='Times New Roman', fontsize=40)
        plt.yticks(family='Times New Roman', fontsize=40)
        plt.savefig(os.path.join(base_dir, '%sthroughput_ti=%ss.png' % (file_prefix, time_interval_sec)))
        plt.close()

if __name__ == '__main__':
    analyse_data('COOJA.testlog')
