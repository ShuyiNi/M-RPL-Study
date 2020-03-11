#!/usr/bin/env python3
# coding: utf-8

from collections import defaultdict
import re
import matplotlib.pyplot as plt


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

    with open('log_err_app_lines.txt', 'w') as fw:
        fw.write(err_line)

    return send_items, recv_items, all_json
            
            
def draw_fig(file):
    SMALL_NUM = 1e-20
    # file = 'log-20200227-201756/COOJA.testlog'

    parse_res = parse_file(file)

    time_unit = 1_000_000 # unit in micro sec, 1 s = 1,000,000 ms
    time_interval = 5 * time_unit

    sends = parse_res[0]
    recvs = parse_res[1]

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

    with open('parse_info.txt', 'w') as fw:
        fw.write(parse_info)

    all_times = list(sends.values()) + list(recvs.values())
    all_times.sort()
    times = list(range(0, all_times[-1]+1, time_interval))

    deliver_count_time = defaultdict(list)
    latency_count_time = defaultdict(list)

    for msg, send_time in sends.items():
        if msg in recvs:
            recv_time = recvs[msg]
            index = send_time // time_interval
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

    plt.figure(figsize=(15, 10))
    plt.plot([i * time_interval / time_unit for i in range(len(times))], deliver_time, 'black', label='deliver rate')
    plt.xlabel('time (s)', family='Times New Roman', fontsize=40)
    plt.ylabel('packet delivery ratio', family='Times New Roman', fontsize=40)
    plt.xticks(family='Times New Roman', fontsize=40)
    plt.yticks(family='Times New Roman', fontsize=40)
    plt.savefig('deliverrate_t.png')
    plt.show()

    plt.figure(figsize=(15, 10))
    plt.plot([i * time_interval / time_unit for i in range(len(times))], latency_time, 'black', label='latency')
    plt.xlabel('time (s)', family='Times New Roman', fontsize=40)
    plt.ylabel('latency (s)', family='Times New Roman', fontsize=40)
    plt.xticks(family='Times New Roman', fontsize=40)
    plt.yticks(family='Times New Roman', fontsize=40)
    plt.savefig('latency_t.png')
    plt.show()

    plt.figure(figsize=(15, 10))
    plt.plot([i * time_interval / time_unit for i in range(len(times))], throughput_time, 'black', label='throughput')
    plt.xlabel('time (s)', family='Times New Roman', fontsize=40)
    plt.ylabel('throughput (packets/s)', family='Times New Roman', fontsize=40)
    plt.xticks(family='Times New Roman', fontsize=40)
    plt.yticks(family='Times New Roman', fontsize=40)
    plt.savefig('throughput_t.png')
    plt.show()

    '''
    l1=plt.plot(x1,y1,'r--',label='type1')
    l2=plt.plot(x2,y2,'g--',label='type2')
    l3=plt.plot(x3,y3,'b--',label='type3')
    plt.plot(x1,y1,'ro-',x2,y2,'g+-',x3,y3,'b^-')
    plt.title('The Lasers in Three Conditions')
    plt.xlabel('row')
    plt.ylabel('column')
    plt.legend()
    plt.show()
    '''

if __name__ == '__main__':
    draw_fig('COOJA.testlog')
