import time
import os
import re
import base64
import datetime
import requests
import threading
from queue import Queue
from datetime import datetime


#  获取远程港澳台直播源文件
url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/iamfang2019/MyTV/main/TW_allsource"
r = requests.get(url)
open('DIYP-v4.txt', 'wb').write(r.content)

keywords = ['凤凰卫视', '凤凰资讯', 'TVB翡翠', 'TVB明珠', 'TVB星河', 'J2', '无线', '有线', '天映', 'VIU', 'RTHK', 'HOY',
            '香港卫视']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
with open('DIYP-v4.txt', 'r', encoding='utf-8') as file, open('HK.txt', 'w', encoding='utf-8') as HK:
    HK.write('\n港澳频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
            HK.write(line)  # 将该行写入输出文件

keywords = ['民视', '中视', '台视', '华视', '新闻台', '东森', '龙祥', '公视', '三立', '大爱', '年代', '人间卫视',
            '人間', '大立']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
with open('DIYP-v4.txt', 'r', encoding='utf-8') as file, open('TW.txt', 'w', encoding='utf-8') as TW:
    TW.write('\n台湾频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
            TW.write(line)  # 将该行写入输出文件

# 读取要合并的香港频道和台湾频道文件
file_contents = []
file_paths = ["HK.txt", "TW.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
# 生成合并后的文件
with open("GAT.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))



#  获取远程体育直播源文件
url = "https://raw.githubusercontent.com/Love4vn/love4vn/main/IPTVSport.m3u"
response = requests.get(url)
m3u_content = response.text

# 移除第一行
# m3u_content = m3u_content.split('\n', 1)[1]

# 初始化变量
group_name = ""
channel_name = ""
channel_link = ""
output_dict = {}

# 处理每两行为一组的情况
for line in m3u_content.split('\n'):
    if line.startswith("#EXTINF"):
        # 获取 group-title 的值
        group_name = line.split('group-title="')[1].split('"')[0]
        
        # 获取频道名
        channel_name = line.split(',')[-1]
    elif line.startswith("http"):
        # 获取频道链接
        channel_link = line
        # 合并频道名和频道链接
        combined_link = f"{channel_name},{channel_link}"

        # 将组名作为键，合并链接作为值存储在字典中
        if group_name not in output_dict:
            output_dict[group_name] = []
        output_dict[group_name].append(combined_link)

# 将结果写入 sport.txt 文件
with open("sport.txt", "w", encoding="utf-8") as output_file:
    # 遍历字典，写入结果文件
    for group_name, links in output_dict.items():
        output_file.write(f"{group_name},#genre#\n")
        for link in links:
            output_file.write(f"{link}\n")


# 扫源湖北电信IPTV

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

urls = ["wuhan", "yichang", "xiangyang", "jingzhou", "ezhou", "huangshi", "shiyan", "jingmen", "xiaogan", "huanggang", "xianning", "suizhou", "enshi"]
channelsx = [
    "湖北公共新闻,http://8.8.8.8:8/rtp/239.69.1.40:9880","湖北经视,http://8.8.8.8:8/rtp/239.69.1.41:9886","湖北综合,http://8.8.8.8:8/rtp/239.69.1.42:9892",
"湖北垄上,http://8.8.8.8:8/rtp/239.69.1.43:9898","湖北影视,http://8.8.8.8:8/rtp/239.69.1.204:10866","湖北生活,http://8.8.8.8:8/rtp/239.69.1.205:10872",
"湖北教育,http://8.8.8.8:8/rtp/239.69.1.206:10878","CCTV1,http://8.8.8.8:8/rtp/239.254.96.96:8550","CCTV2,http://8.8.8.8:8/rtp/239.69.1.102:10250",
"CCTV3,http://8.8.8.8:8/rtp/239.69.1.122:10370","CCTV4,http://8.8.8.8:8/rtp/239.69.1.138:10466","CCTV5,http://8.8.8.8:8/rtp/239.69.1.123:10376",
"CCTV5+,http://8.8.8.8:8/rtp/239.254.96.234:9484","CCTV6,http://8.8.8.8:8/rtp/239.69.1.124:10382","CCTV7,http://8.8.8.8:8/rtp/239.69.1.103:10256",
"CCTV8,http://8.8.8.8:8/rtp/239.69.1.125:10388","CCTV9,http://8.8.8.8:8/rtp/239.69.1.104:10262","CCTV10,http://8.8.8.8:8/rtp/239.69.1.105:10268",
"CCTV11,http://8.8.8.8:8/rtp/239.69.1.154:10560","CCTV12,http://8.8.8.8:8/rtp/239.69.1.106:10274","CCTV13,http://8.8.8.8:8/rtp/239.254.96.161:9040",
"CCTV14,http://8.8.8.8:8/rtp/239.69.1.107:10280","CCTV15,http://8.8.8.8:8/rtp/239.69.1.155:10566","CCTV16,http://8.8.8.8:8/rtp/239.69.1.247:11124",
"CCTV17,http://8.8.8.8:8/rtp/239.69.1.152:10548","CCTV第一剧场,http://8.8.8.8:8/rtp/239.69.1.74:10084","CCTV兵器科技,http://8.8.8.8:8/rtp/239.69.1.79:10114",
"CCTV风云足球,http://8.8.8.8:8/rtp/239.69.1.81:10126","CCTV高尔夫网球,http://8.8.8.8:8/rtp/239.69.1.83:10138","CCTV世界地理,http://8.8.8.8:8/rtp/239.69.1.91:10186",
"CCTV央视台球,http://8.8.8.8:8/rtp/239.69.1.98:10224","CCTV16奥林匹克-4K,http://8.8.8.8:8/rtp/239.69.1.249:11136","BestTV测试1-4K,http://8.8.8.8:8/rtp/239.69.1.26:9796",
"BestTV测试2-4K,http://8.8.8.8:8/rtp/239.69.1.27:9802","BestTV测试3-4K,http://8.8.8.8:8/rtp/239.69.1.25:9790","爱上4K,http://8.8.8.8:8/rtp/239.69.1.141:10482",
"湖北卫视,http://8.8.8.8:8/rtp/239.254.96.115:8664","河北卫视,http://8.8.8.8:8/rtp/239.254.96.113:9616","深圳卫视,http://8.8.8.8:8/rtp/239.254.96.137:8896",
"黑龙江卫视,http://8.8.8.8:8/rtp/239.254.96.138:8902","湖南卫视,http://8.8.8.8:8/rtp/239.254.96.139:8908","广东卫视,http://8.8.8.8:8/rtp/239.254.96.140:8914",
"北京卫视,http://8.8.8.8:8/rtp/239.254.96.141:8920","东方卫视,http://8.8.8.8:8/rtp/239.254.96.142:8926","浙江卫视,http://8.8.8.8:8/rtp/239.254.96.143:8932",
"江苏卫视,http://8.8.8.8:8/rtp/239.254.96.144:8938","天津卫视,http://8.8.8.8:8/rtp/239.69.1.68:10048","山东卫视,http://8.8.8.8:8/rtp/239.69.1.69:10054",
"安徽卫视,http://8.8.8.8:8/rtp/239.69.1.70:10060","辽宁卫视,http://8.8.8.8:8/rtp/239.69.1.71:10066","东南卫视,http://8.8.8.8:8/rtp/239.69.1.108:10286",
"江西卫视,http://8.8.8.8:8/rtp/239.69.1.126:10394","重庆卫视,http://8.8.8.8:8/rtp/239.69.1.149:10530","贵州卫视,http://8.8.8.8:8/rtp/239.69.1.150:10536",
"海南卫视,http://8.8.8.8:8/rtp/239.69.1.151:10542","河南卫视,http://8.8.8.8:8/rtp/239.69.1.168:10644","四川卫视,http://8.8.8.8:8/rtp/239.69.1.169:10650",
"广西卫视,http://8.8.8.8:8/rtp/239.69.1.191:10788","吉林卫视,http://8.8.8.8:8/rtp/239.69.1.212:10914","CHC-高清电影,http://8.8.8.8:8/rtp/239.69.1.241:11088",
"CHC-动作电影,http://8.8.8.8:8/rtp/239.69.1.242:11094","CHC-家庭影院,http://8.8.8.8:8/rtp/239.69.1.243:11100","武汉一台新闻综合,http://8.8.8.8:8/rtp/239.69.1.145:10506",
"武汉二台电视剧,http://8.8.8.8:8/rtp/239.69.1.146:10512","武汉三台科技生活,http://8.8.8.8:8/rtp/239.69.1.251:11148","武汉四台经济,http://8.8.8.8:8/rtp/239.69.1.35:9850",
"武汉五台文体,http://8.8.8.8:8/rtp/239.69.1.147:10518","武汉六台外语,http://8.8.8.8:8/rtp/239.69.1.36:9856","武汉教育,http://8.8.8.8:8/rtp/239.69.1.60:9994",
"蔡甸综合,http://8.8.8.8:8/rtp/239.69.1.245:11112","阳新综合,http://8.8.8.8:8/rtp/239.69.1.34:9844","房县综合,http://8.8.8.8:8/rtp/239.69.1.192:10794",
"卡酷少儿,http://8.8.8.8:8/rtp/239.69.1.193:10800","梨园频道,http://8.8.8.8:8/rtp/239.69.1.33:9838","武术世界,http://8.8.8.8:8/rtp/239.69.1.47:9922",
"快乐垂钓,http://8.8.8.8:8/rtp/239.69.1.142:10488","茶频道,http://8.8.8.8:8/rtp/239.69.1.144:10500","金鹰卡通,http://8.8.8.8:8/rtp/239.69.1.248:11130",
"金鹰纪实,http://8.8.8.8:8/rtp/239.69.1.109:10292","CETV1,http://8.8.8.8:8/rtp/239.69.1.110:10298","CCTV5+,http://8.8.8.8:8/rtp/239.69.1.12:9712",
"河北卫视,http://8.8.8.8:8/rtp/239.69.1.157:10578","东方卫视,http://8.8.8.8:8/rtp/239.69.1.173:10674","江苏卫视,http://8.8.8.8:8/rtp/239.69.1.174:10680",
"CCTV16-4K,http://8.8.8.8:8/rtp/239.69.1.13:9718",
]


results = []
channel = []
urls_all = []
resultsx = []
resultxs = []
error_channels = []

for url in urls:
    url_0 = str(base64.b64encode((f'"Server: udpxy" && city="{url}" && asn="4134"').encode("utf-8")), "utf-8")
    url_64 = f'https://fofa.info/result?qbase64={url_0}&page=1&page_size=20'
    print(url_64)
    try:
        response = requests.get(url_64, headers=headers, timeout=15)
        page_content = response.text
        print(f" {url}  访问成功")
        pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
        page_urls = re.findall(pattern, page_content)
        for urlx in page_urls:
            try:
                response = requests.get(url=urlx + '/status', timeout=1)
                response.raise_for_status()  # 返回状态码不是200异常
                page_content = response.text
                pattern = r'class="proctabl"'
                page_proctabl = re.findall(pattern, page_content)
                if page_proctabl:
                    urls_all.append(urlx)
                    print(f"{urlx} 可以访问")

            except requests.RequestException as e:
                pass
    except:
        print(f"{url_64} 访问失败")
        pass

urls_all = set(urls_all)  # 去重得到唯一的URL列表
for urlx in urls_all:
    channel = [f'{name},{url.replace("http://8.8.8.8:8", urlx)}' for name, url in
               [line.strip().split(',') for line in channelsx]]
    results.extend(channel)
            
results = sorted(results)
# with open("hb.txt", 'w', encoding='utf-8') as file:
#     for result in results:
#         file.write(result + "\n")
#         print(result)

# 定义工作线程函数
def worker():
    while True:
        result = task_queue.get()
        channel_name, channel_url = result.split(',', 1)
        try:
            response = requests.get(channel_url, stream=True, timeout=3)
            if response.status_code == 200:
                result = channel_name, channel_url
                resultsx.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
            else:
                error_channels.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channels.append(result)
            numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
            print(
                f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 20
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# 添加下载任务到队列
for result in results:
    task_queue.put(result)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字


for resulta in resultsx:
    channel_name, channel_url = resulta
    resultx = channel_name, channel_url
    resultxs.append(resultx)

# 对频道进行排序
resultxs.sort(key=lambda x: channel_key(x[0]))
# now_today = datetime.date.today()

result_counter = 20  # 每个频道需要的个数

with open("hb.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if 'CCTV' in channel_name or 'CGTN' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n卫视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n湖北频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '湖北' in channel_name or '武汉' in channel_name or '宜昌' in channel_name or '黄石' in channel_name or '十堰' in channel_name or '荆门' in channel_name or '荆州' in channel_name or '随州' in channel_name or '襄阳' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.write('\n其他频道,#genre#\n')
    for resultx in resultxs:
        channel_name, channel_url = resultx
        if 'CCTV' not in channel_name and 'CGTN' not in channel_name and '卫视' not in channel_name and '湖北' not in channel_name and '武汉' not in channel_name and '宜昌' not in channel_name and '黄石' not in channel_name and '十堰' \
              not in channel_name and '荆门' not in channel_name and '荆州' not in channel_name and '随州' not in channel_name and '襄阳' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

# 扫源河南联通IPTV

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

urls = ["zhengzhou", "kaifeng", "luoyang", "pingdingshan", "anyang", "hebi", "xinxiang", "jiaozuo", "puyang", "xuchang", "luohe", "sanmenxia", "nanyang", "shangqiu", "xinyang", "zhoukou", "zhumadian"]
channelsx = [
    "CCTV1,http://8.8.8.8:8/rtp/225.1.4.73:1102","CCTV2,http://8.8.8.8:8/rtp/225.1.4.74:1103","CCTV3,http://8.8.8.8:8/rtp/225.1.4.158:1194",
    "CCTV4,http://8.8.8.8:8/rtp/225.1.5.30:1333","CCTV5,http://8.8.8.8:8/rtp/225.1.4.159:1195","CCTV6,http://8.8.8.8:8/rtp/225.1.4.160:1196",
    "CCTV7,http://8.8.8.8:8/rtp/225.1.4.76:1105","CCTV8,http://8.8.8.8:8/rtp/225.1.4.161:1197","CCTV9,http://8.8.8.8:8/rtp/225.1.4.77:1106",
    "CCTV11,http://8.8.8.8:8/rtp/225.1.4.215:1268","CCTV12,http://8.8.8.8:8/rtp/225.1.4.79:1108","CCTV13,http://8.8.8.8:8/rtp/225.1.4.113:1293",
    "CCTV14,http://8.8.8.8:8/rtp/225.1.4.80:1109","CCTV15,http://8.8.8.8:8/rtp/225.1.4.216:1269","CCTV17,http://8.8.8.8:8/rtp/225.1.4.226:2506",
    "CCTV5+,http://8.8.8.8:8/rtp/225.1.4.75:1104","爱上4K,http://8.8.8.8:8/rtp/225.1.4.162:1204","河南卫视4K,http://8.8.8.8:8/rtp/225.1.4.254:1300",
    "河南都市,http://8.8.8.8:8/rtp/225.1.4.52:1081","河南民生,http://8.8.8.8:8/rtp/225.1.4.53:1082","河南法治,http://8.8.8.8:8/rtp/225.1.4.54:1083",
    "河南电视剧,http://8.8.8.8:8/rtp/225.1.4.55:1084","河南新闻,http://8.8.8.8:8/rtp/225.1.4.56:1085","河南公共,http://8.8.8.8:8/rtp/225.1.4.58:1087",
    "河南乡村,http://8.8.8.8:8/rtp/225.1.4.120:1149","河南国际,http://8.8.8.8:8/rtp/225.1.4.102:1131","河南戏曲,http://8.8.8.8:8/rtp/225.1.4.99:1128",
    "河南文博,http://8.8.8.8:8/rtp/225.1.4.100:1129","河南功夫,http://8.8.8.8:8/rtp/225.1.4.101:1130","睛彩中原,http://8.8.8.8:8/rtp/225.1.4.163:1203",
    "移动戏曲,http://8.8.8.8:8/rtp/225.1.4.206:1254","河南移动,http://8.8.8.8:8/rtp/225.1.5.40:1350","健康中原,http://8.8.8.8:8/rtp/225.1.5.48:1358",
    "河南导视,http://8.8.8.8:8/rtp/225.1.4.194:1244","郑州新闻,http://8.8.8.8:8/rtp/225.1.4.140:1176","郑州商都,http://8.8.8.8:8/rtp/225.1.4.141:1177",
    "郑州文旅,http://8.8.8.8:8/rtp/225.1.4.142:1178","郑州影视,http://8.8.8.8:8/rtp/225.1.4.146:1182","郑州妇女,http://8.8.8.8:8/rtp/225.1.4.147:1183",
    "郑州都市,http://8.8.8.8:8/rtp/225.1.4.149:1185","郑州教育,http://8.8.8.8:8/rtp/225.1.4.191:1241","新密新闻,http://8.8.8.8:8/rtp/225.1.4.239:1285",
    "新郑综合,http://8.8.8.8:8/rtp/225.1.4.243:1289","中牟综合,http://8.8.8.8:8/rtp/225.1.4.244:1290","巩义综合,http://8.8.8.8:8/rtp/225.1.5.50:1360",
    "北京卫视,http://8.8.8.8:8/rtp/225.1.4.81:1110","湖南卫视,http://8.8.8.8:8/rtp/225.1.4.82:1111","江苏卫视,http://8.8.8.8:8/rtp/225.1.4.83:1112",
    "浙江卫视,http://8.8.8.8:8/rtp/225.1.4.84:1113","东方卫视,http://8.8.8.8:8/rtp/225.1.4.85:1114","天津卫视,http://8.8.8.8:8/rtp/225.1.4.86:1115",
    "山东卫视,http://8.8.8.8:8/rtp/225.1.4.88:1117","安徽卫视,http://8.8.8.8:8/rtp/225.1.4.87:1116","湖北卫视,http://8.8.8.8:8/rtp/225.1.4.89:1118",
    "深圳卫视,http://8.8.8.8:8/rtp/225.1.4.90:1119","黑龙江卫视,http://8.8.8.8:8/rtp/225.1.4.91:1120","贵州卫视,http://8.8.8.8:8/rtp/225.1.4.122:1302",
    "河北卫视,http://8.8.8.8:8/rtp/225.1.4.123:1304","江西卫视,http://8.8.8.8:8/rtp/225.1.4.139:1305","四川卫视,http://8.8.8.8:8/rtp/225.1.4.151:1306",
    "云南卫视,http://8.8.8.8:8/rtp/225.1.4.152:1307","重庆卫视,http://8.8.8.8:8/rtp/225.1.4.157:1308","广东卫视,http://8.8.8.8:8/rtp/225.1.4.166:1207",
    "辽宁卫视,http://8.8.8.8:8/rtp/225.1.4.167:1208","吉林卫视,http://8.8.8.8:8/rtp/225.1.4.174:1309","海南卫视,http://8.8.8.8:8/rtp/225.1.4.195:1310",
    "东南卫视,http://8.8.8.8:8/rtp/225.1.4.228:1274","CHC高清电影,http://8.8.8.8:8/rtp/225.1.4.207:1260","CHC动作电影,http://8.8.8.8:8/rtp/225.1.4.208:1261",
    "CHC家庭影院,http://8.8.8.8:8/rtp/225.1.4.209:1262","CETV1,http://8.8.8.8:8/rtp/225.1.4.173:1712","纪实人文,http://8.8.8.8:8/rtp/225.1.4.170:1222",
    "金鹰纪实,http://8.8.8.8:8/rtp/225.1.4.172:1711","国学,http://8.8.8.8:8/rtp/225.1.4.196:1311","CCTV4,http://8.8.8.8:8/rtp/225.1.5.31:1342",
    "CCTV4美洲,http://8.8.8.8:8/rtp/225.1.5.32:1343","CGTN英语,http://8.8.8.8:8/rtp/225.1.5.34:1344","CGTN英文记录,http://8.8.8.8:8/rtp/225.1.5.35:1345",
    "CGTN西班牙语,http://8.8.8.8:8/rtp/225.1.5.36:1346","CGTN法语,http://8.8.8.8:8/rtp/225.1.5.37:1347","CGTN阿拉伯语,http://8.8.8.8:8/rtp/225.1.5.38:1348",
    "CGTN俄语,http://8.8.8.8:8/rtp/225.1.5.39:1349","爱体育,http://8.8.8.8:8/rtp/225.1.4.168:1220","河南卫视,http://8.8.8.8:8/rtp/225.1.5.45:1355","河南卫视,http://8.8.8.8:8/rtp/225.1.4.98:1127",
]


results = []
channel = []
urls_all = []
resultsx = []
resultxs = []
error_channels = []

for url in urls:
    url_0 = str(base64.b64encode((f'"Server: udpxy" && city="{url}" && asn="4837"').encode("utf-8")), "utf-8")
    url_64 = f'https://fofa.info/result?qbase64={url_0}&page=1&page_size=20'
    print(url_64)
    try:
        response = requests.get(url_64, headers=headers, timeout=15)
        page_content = response.text
        print(f" {url}  访问成功")
        pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
        page_urls = re.findall(pattern, page_content)
        for urlx in page_urls:
            try:
                response = requests.get(url=urlx + '/status', timeout=1)
                response.raise_for_status()  # 返回状态码不是200异常
                page_content = response.text
                pattern = r'class="proctabl"'
                page_proctabl = re.findall(pattern, page_content)
                if page_proctabl:
                    urls_all.append(urlx)
                    print(f"{urlx} 可以访问")

            except requests.RequestException as e:
                pass
    except:
        print(f"{url_64} 访问失败")
        pass

urls_all = set(urls_all)  # 去重得到唯一的URL列表
for urlx in urls_all:
    channel = [f'{name},{url.replace("http://8.8.8.8:8", urlx)}' for name, url in
               [line.strip().split(',') for line in channelsx]]
    results.extend(channel)
            
results = sorted(results)
# with open("he.txt", 'w', encoding='utf-8') as file:
#     for result in results:
#         file.write(result + "\n")
#         print(result)

# 定义工作线程函数
def worker():
    while True:
        result = task_queue.get()
        channel_name, channel_url = result.split(',', 1)
        try:
            response = requests.get(channel_url, stream=True, timeout=3)
            if response.status_code == 200:
                result = channel_name, channel_url
                resultsx.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
            else:
                error_channels.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channels.append(result)
            numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
            print(
                f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 20
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# 添加下载任务到队列
for result in results:
    task_queue.put(result)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字


for resulta in resultsx:
    channel_name, channel_url = resulta
    resultx = channel_name, channel_url
    resultxs.append(resultx)

# 对频道进行排序
resultxs.sort(key=lambda x: channel_key(x[0]))
# now_today = datetime.date.today()

result_counter = 20  # 每个频道需要的个数

with open("he.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if 'CCTV' in channel_name or 'CGTN' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n卫视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n河南频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '河南' in channel_name or '郑州' in channel_name or '中原' in channel_name or '新郑' in channel_name or '新密' \
                in channel_name or '中牟' in channel_name or '巩义' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.write('\n其他频道,#genre#\n')
    for resultx in resultxs:
        channel_name, channel_url = resultx
        if 'CCTV' not in channel_name and 'CGTN' not in channel_name and '卫视' not in channel_name and '河南' not in channel_name and '郑州' not in channel_name and '中原' not in channel_name and '新郑' not in channel_name and '新密' \
              not in channel_name and '中牟' not in channel_name and '巩义' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

# 扫源北京联通IPTV

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

urls = ["beijing"]
channelsx = [
    "CCTV1,http://8.8.8.8:8/rtp/239.3.1.129:8008","CCTV2,http://8.8.8.8:8/rtp/239.3.1.60:8084","CCTV3,http://8.8.8.8:8/rtp/239.3.1.172:8001",
    "CCTV4,http://8.8.8.8:8/rtp/239.3.1.105:8092","CCTV4（4K）,http://8.8.8.8:8/rtp/239.3.1.245:2000","CCTV4 欧洲,http://8.8.8.8:8/rtp/239.3.1.213:4220",
    "CCTV4 美洲,http://8.8.8.8:8/rtp/239.3.1.214:4220","CCTV5,http://8.8.8.8:8/rtp/239.3.1.173:8001","CCTV5+,http://8.8.8.8:8/rtp/239.3.1.130:8004",
    "CCTV6,http://8.8.8.8:8/rtp/239.3.1.174:8001","CCTV7,http://8.8.8.8:8/rtp/239.3.1.61:8104","CCTV8,http://8.8.8.8:8/rtp/239.3.1.175:8001",
    "CCTV9,http://8.8.8.8:8/rtp/239.3.1.62:8112","CCTV10,http://8.8.8.8:8/rtp/239.3.1.63:8116","CCTV11,http://8.8.8.8:8/rtp/239.3.1.152:8120",
    "CCTV12,http://8.8.8.8:8/rtp/239.3.1.64:8124","CCTV13,http://8.8.8.8:8/rtp/239.3.1.124:8128","CCTV14,http://8.8.8.8:8/rtp/239.3.1.65:8132",
    "CCTV15,http://8.8.8.8:8/rtp/239.3.1.153:8136","CCTV16,http://8.8.8.8:8/rtp/239.3.1.184:8001","CCTV17,http://8.8.8.8:8/rtp/239.3.1.151:8144",
    "CCTV16[4K]1,http://8.8.8.8:8/rtp/239.3.1.97:8001","CCTV16[4K]2,http://8.8.8.8:8/rtp/239.3.1.183:8001","北京卫视,http://8.8.8.8:8/rtp/239.3.1.241:8000",
    "北京文艺,http://8.8.8.8:8/rtp/239.3.1.242:8000","北京纪实科教,http://8.8.8.8:8/rtp/239.3.1.227:8000","北京影视,http://8.8.8.8:8/rtp/239.3.1.158:8000",
    "北京生活,http://8.8.8.8:8/rtp/239.3.1.231:8000","北京财经,http://8.8.8.8:8/rtp/239.3.1.229:8000","北京青年,http://8.8.8.8:8/rtp/239.3.1.232:8000",
    "北京新闻,http://8.8.8.8:8/rtp/239.3.1.159:8000","北京卡酷少儿,http://8.8.8.8:8/rtp/239.3.1.189:8000","北京体育休闲,http://8.8.8.8:8/rtp/239.3.1.243:8000",
    "北京国际频道,http://8.8.8.8:8/rtp/239.3.1.235:8000","湖南卫视,http://8.8.8.8:8/rtp/239.3.1.132:8012","浙江卫视,http://8.8.8.8:8/rtp/239.3.1.137:8036",
    "江苏卫视,http://8.8.8.8:8/rtp/239.3.1.135:8028","东方卫视,http://8.8.8.8:8/rtp/239.3.1.136:8032","山东卫视,http://8.8.8.8:8/rtp/239.3.1.209:8052",
    "安徽卫视,http://8.8.8.8:8/rtp/239.3.1.211:8064","湖北卫视,http://8.8.8.8:8/rtp/239.3.1.138:8044","东南卫视,http://8.8.8.8:8/rtp/239.3.1.156:8148",
    "广东卫视,http://8.8.8.8:8/rtp/239.3.1.142:8048","辽宁卫视,http://8.8.8.8:8/rtp/239.3.1.210:8056","黑龙江卫视,http://8.8.8.8:8/rtp/239.3.1.133:8016",
    "深圳卫视,http://8.8.8.8:8/rtp/239.3.1.134:8020","贵州卫视,http://8.8.8.8:8/rtp/239.3.1.149:8076","天津卫视,http://8.8.8.8:8/rtp/239.3.1.141:1234",
    "河北卫视,http://8.8.8.8:8/rtp/239.3.1.148:8072","重庆卫视,http://8.8.8.8:8/rtp/239.3.1.122:8160","江西卫视,http://8.8.8.8:8/rtp/239.3.1.123:8164",
    "吉林卫视,http://8.8.8.8:8/rtp/239.3.1.240:8172","南方卫视,http://8.8.8.8:8/rtp/239.3.1.161:8001","广西卫视,http://8.8.8.8:8/rtp/239.3.1.39:8300",
    "海南卫视,http://8.8.8.8:8/rtp/239.3.1.45:8304","厦门卫视,http://8.8.8.8:8/rtp/239.3.1.143:4120","云南卫视,http://8.8.8.8:8/rtp/239.3.1.26:8108",
    "西藏卫视,http://8.8.8.8:8/rtp/239.3.1.47:8164","四川卫视,http://8.8.8.8:8/rtp/239.3.1.29:8288","河南卫视,http://8.8.8.8:8/rtp/239.3.1.27:8128",
    "陕西卫视,http://8.8.8.8:8/rtp/239.3.1.41:8140","新疆卫视,http://8.8.8.8:8/rtp/239.3.1.48:8160","宁夏卫视,http://8.8.8.8:8/rtp/239.3.1.46:8124",
    "青海卫视,http://8.8.8.8:8/rtp/239.3.1.44:8184","甘肃卫视,http://8.8.8.8:8/rtp/239.3.1.49:8188","山西卫视,http://8.8.8.8:8/rtp/239.3.1.42:8172",
    "内蒙古卫视,http://8.8.8.8:8/rtp/239.3.1.43:8176","三沙卫视,http://8.8.8.8:8/rtp/239.3.1.155:4120","兵团卫视,http://8.8.8.8:8/rtp/239.3.1.144:4120",
    "山东教育,http://8.8.8.8:8/rtp/239.3.1.52:4120","中国教育1台,http://8.8.8.8:8/rtp/239.3.1.57:8152","中国教育2台,http://8.8.8.8:8/rtp/239.3.1.54:4120",
    "中国教育3台,http://8.8.8.8:8/rtp/239.3.1.55:4120","中国教育4台,http://8.8.8.8:8/rtp/239.3.1.56:4120","CGTN 新闻,http://8.8.8.8:8/rtp/239.3.1.215:4220",
    "CGTN 记录,http://8.8.8.8:8/rtp/239.3.1.216:4220","CGTN 西班牙语,http://8.8.8.8:8/rtp/239.3.1.217:4220","CGTN 法语,http://8.8.8.8:8/rtp/239.3.1.218:4220",
    "CGTN 阿拉伯语,http://8.8.8.8:8/rtp/239.3.1.219:4220","CGTN 俄语,http://8.8.8.8:8/rtp/239.3.1.220:4220",
]


results = []
channel = []
urls_all = []
resultsx = []
resultxs = []
error_channels = []

for url in urls:
    url_0 = str(base64.b64encode((f'"Server: udpxy" && city="{url}" && asn="4808"').encode("utf-8")), "utf-8")
    url_64 = f'https://fofa.info/result?qbase64={url_0}&page=1&page_size=20'
    print(url_64)
    try:
        response = requests.get(url_64, headers=headers, timeout=15)
        page_content = response.text
        print(f" {url}  访问成功")
        pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
        page_urls = re.findall(pattern, page_content)
        for urlx in page_urls:
            try:
                response = requests.get(url=urlx + '/status', timeout=1)
                response.raise_for_status()  # 返回状态码不是200异常
                page_content = response.text
                pattern = r'class="proctabl"'
                page_proctabl = re.findall(pattern, page_content)
                if page_proctabl:
                    urls_all.append(urlx)
                    print(f"{urlx} 可以访问")

            except requests.RequestException as e:
                pass
    except:
        print(f"{url_64} 访问失败")
        pass

urls_all = set(urls_all)  # 去重得到唯一的URL列表
for urlx in urls_all:
    channel = [f'{name},{url.replace("http://8.8.8.8:8", urlx)}' for name, url in
               [line.strip().split(',') for line in channelsx]]
    results.extend(channel)

results = sorted(results)
# with open("bj.txt", 'w', encoding='utf-8') as file:
#     for result in results:
#         file.write(result + "\n")
#         print(result)

# 定义工作线程函数
def worker():
    while True:
        result = task_queue.get()
        channel_name, channel_url = result.split(',', 1)
        try:
            response = requests.get(channel_url, stream=True, timeout=3)
            if response.status_code == 200:
                result = channel_name, channel_url
                resultsx.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
            else:
                error_channels.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channels.append(result)
            numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
            print(
                f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 20
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# 添加下载任务到队列
for result in results:
    task_queue.put(result)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字


for resulta in resultsx:
    channel_name, channel_url = resulta
    resultx = channel_name, channel_url
    resultxs.append(resultx)

# 对频道进行排序
resultxs.sort(key=lambda x: channel_key(x[0]))
# now_today = datetime.date.today()

result_counter = 20  # 每个频道需要的个数

with open("bj.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if 'CCTV' in channel_name or 'CGTN' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n卫视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n北京频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '北京' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.write('\n其他频道,#genre#\n')
    for resultx in resultxs:
        channel_name, channel_url = resultx
        if 'CCTV' not in channel_name and 'CGTN' not in channel_name and '卫视' not in channel_name and '北京' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1


# 扫源湖南电信IPTV
# 线程安全的队列，用于存储下载任务
task_queue = Queue()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

urls = ["changsha", "zhuzhou", "xiangtan", "hengyang", "shaoyang", "yueyang", "changde", "zhangjiajie", "yiyang",
        "chenzhou", "yongzhou", "huaihua", "loudi"]
channelsx = [
    "湖南卫视,http://8.8.8.8:8/udp/239.76.245.115:1234", "湖南经视,http://8.8.8.8:8/udp/239.76.245.116:1234",
    "湖南都市,http://8.8.8.8:8/udp/239.76.245.117:1234", "湖南电视剧,http://8.8.8.8:8/udp/239.76.245.118:1234",
    "湖南电影,http://8.8.8.8:8/udp/239.76.245.119:1234", "湖南娱乐,http://8.8.8.8:8/udp/239.76.245.121:1234",
    "湖南国际,http://8.8.8.8:8/udp/239.76.245.124:1234", "湖南公共,http://8.8.8.8:8/udp/239.76.245.123:1234",
    "CCTV1,http://8.8.8.8:8/udp/239.76.245.51:1234", "CCTV1,http://8.8.8.8:8/udp/239.76.246.151:1234",
    "CCTV2,http://8.8.8.8:8/udp/239.76.246.152:1234", "CCTV3,http://8.8.8.8:8/udp/239.76.246.153:1234",
    "CCTV4,http://8.8.8.8:8/udp/239.76.245.195:1234", "CCTV4,http://8.8.8.8:8/udp/239.76.246.154:1234",
    "CCTV5,http://8.8.8.8:8/udp/239.76.246.155:1234", "CCTV5+,http://8.8.8.8:8/udp/239.76.246.168:1234",
    "CCTV6,http://8.8.8.8:8/udp/239.76.246.156:1234", "CCTV7,http://8.8.8.8:8/udp/239.76.246.157:1234",
    "CCTV8,http://8.8.8.8:8/udp/239.76.246.158:1234", "CCTV9,http://8.8.8.8:8/udp/239.76.246.159:1234",
    "CCTV10,http://8.8.8.8:8/udp/239.76.246.160:1234", "CCTV11,http://8.8.8.8:8/udp/239.76.245.251:1234",
    "CCTV12,http://8.8.8.8:8/udp/239.76.246.162:1234", "CCTV13,http://8.8.8.8:8/udp/239.76.246.93:1234",
    "CCTV14,http://8.8.8.8:8/udp/239.76.246.164:1234", "CCTV15,http://8.8.8.8:8/udp/239.76.245.252:1234",
    "CCTV16,http://8.8.8.8:8/udp/239.76.246.98:1234", "CCTV17,http://8.8.8.8:8/udp/239.76.245.238:1234",
    "CCTV16 4K,http://8.8.8.8:8/udp/239.76.246.214:1234", "CCTV16 4k,http://8.8.8.8:8/udp/239.76.246.224:1234",
    "CCTV16 4k,http://8.8.8.8:8/udp/239.76.246.230:1234", "体育,http://8.8.8.8:8/udp/239.76.246.136:1234",
    "金鹰卡通,http://8.8.8.8:8/udp/239.76.245.120:1234", "金鹰纪实,http://8.8.8.8:8/udp/239.76.245.122:1234",
    "快乐垂钓,http://8.8.8.8:8/udp/239.76.245.127:1234", "湖南教育,http://8.8.8.8:8/udp/239.76.245.233:1234",
    "茶频道,http://8.8.8.8:8/udp/239.76.245.239:1234", "广东卫视,http://8.8.8.8:8/udp/239.76.245.189:1234",
    "东南卫视,http://8.8.8.8:8/udp/239.76.245.190:1234", "安徽卫视,http://8.8.8.8:8/udp/239.76.245.196:1234",
    "辽宁卫视,http://8.8.8.8:8/udp/239.76.245.197:1234", "江西卫视,http://8.8.8.8:8/udp/239.76.245.225:1234",
    "河北卫视,http://8.8.8.8:8/udp/239.76.245.199:1234", "贵州卫视,http://8.8.8.8:8/udp/239.76.245.198:1234",
    "江苏卫视,http://8.8.8.8:8/udp/239.76.246.181:1234", "东方卫视,http://8.8.8.8:8/udp/239.76.246.186:1234",
    "浙江卫视,http://8.8.8.8:8/udp/239.76.246.182:1234", "北京卫视,http://8.8.8.8:8/udp/239.76.246.184:1234",
    "天津卫视,http://8.8.8.8:8/udp/239.76.246.185:1234", "深圳卫视,http://8.8.8.8:8/udp/239.76.246.188:1234",
    "湖北卫视,http://8.8.8.8:8/udp/239.76.246.193:1234", "山东卫视,http://8.8.8.8:8/udp/239.76.246.195:1234",
    "黑龙江卫视,http://8.8.8.8:8/udp/239.76.246.200:1234", "吉林卫视,http://8.8.8.8:8/udp/239.76.246.201:1234",
    "河南卫视,http://8.8.8.8:8/udp/239.76.246.202:1234", "海南卫视,http://8.8.8.8:8/udp/239.76.246.203:1234",
    "四川卫视,http://8.8.8.8:8/udp/239.76.246.91:1234", "重庆卫视,http://8.8.8.8:8/udp/239.76.246.92:1234",
    "甘肃卫视,http://8.8.8.8:8/udp/239.76.246.94:1234", "中国教育,http://8.8.8.8:8/udp/239.76.245.192:1234",
    "长沙女姓,http://8.8.8.8:8/udp/239.76.245.23:1234", "长沙影视,http://8.8.8.8:8/udp/239.76.245.204:1234",
    "湘西综合,http://8.8.8.8:8/udp/239.76.245.208:1234", "湘西综合,http://8.8.8.8:8/udp/239.76.245.209:1234",
    "河南梨园,http://8.8.8.8:8/udp/239.76.245.179:1234", "武术世界,http://8.8.8.8:8/udp/239.76.245.181:1234",
    "张家界,http://8.8.8.8:8/udp/239.76.245.235:1234", "张家界综合,http://8.8.8.8:8/udp/239.76.245.234:1234",
    "CHC动作电影,http://8.8.8.8:8/udp/239.76.245.243:1234", "CHC高清电影,http://8.8.8.8:8/udp/239.76.245.242:1234",
    "CHC家庭影院,http://8.8.8.8:8/udp/239.76.245.241:1234", "快乐垂钓,http://8.8.8.8:8/udp/239.76.246.5:1234",
    "凤凰资讯,http://8.8.8.8:8/udp/239.76.246.8:1234", "凤凰中文,http://8.8.8.8:8/udp/239.76.246.7:1234",
    "湖南卫视,http://8.8.8.8:8/udp/239.76.246.101:1234", "湖南卫视,http://8.8.8.8:8/udp/239.76.246.100:1234",
    "湖南经视,http://8.8.8.8:8/udp/239.76.246.103:1234", "湖南国际,http://8.8.8.8:8/udp/239.76.246.102:1234",
    "湖南都市,http://8.8.8.8:8/udp/239.76.246.104:1234", "湖南娱乐,http://8.8.8.8:8/udp/239.76.246.105:1234",
    "湖南电影,http://8.8.8.8:8/udp/239.76.246.106:1234", "湖南公共,http://8.8.8.8:8/udp/239.76.246.109:1234",
    "湖南电视剧,http://8.8.8.8:8/udp/239.76.246.108:1234", "金鹰卡通,http://8.8.8.8:8/udp/239.76.246.107:1234",
    "金鹰纪实,http://8.8.8.8:8/udp/239.76.246.110:1234", "长沙政法,http://8.8.8.8:8/udp/239.76.246.122:1234",
    "长沙新闻,http://8.8.8.8:8/udp/239.76.246.121:1234", "健康电视,http://8.8.8.8:8/udp/239.76.246.127:1234",
    "欢笑剧场4K,http://8.8.8.8:8/udp/239.76.246.130:1234", "都市剧场,http://8.8.8.8:8/udp/239.76.246.215:1234",
    "极速汽车,http://8.8.8.8:8/udp/239.76.246.133:1234", "动漫秀场,http://8.8.8.8:8/udp/239.76.246.131:1234",
    "游戏风云,http://8.8.8.8:8/udp/239.76.246.132:1234", "凤凰中文,http://8.8.8.8:8/udp/239.76.246.134:1234",
    "凤凰中文,http://8.8.8.8:8/udp/239.76.253.135:9000", "凤凰资讯,http://8.8.8.8:8/udp/239.76.253.134:9000",
    "凤凰资讯,http://8.8.8.8:8/udp/239.76.246.135:1234", "体育,http://8.8.8.8:8/udp/239.76.253.136:9000",
    "全纪实,http://8.8.8.8:8/udp/239.76.246.137:1234", "法治天地,http://8.8.8.8:8/udp/239.76.246.138:1234",
    "生活时尚,http://8.8.8.8:8/udp/239.76.246.223:1234", "浏阳新闻,http://8.8.8.8:8/udp/239.76.248.6:1234",
    "常德综合,http://8.8.8.8:8/udp/239.76.248.10:1234", "常德公共,http://8.8.8.8:8/udp/239.76.248.11:1234",
    "衡阳综合,http://8.8.8.8:8/udp/239.76.248.13:1234", "衡阳公共,http://8.8.8.8:8/udp/239.76.248.14:1234",
    "娄底综合,http://8.8.8.8:8/udp/239.76.248.18:1234", "娄底公共,http://8.8.8.8:8/udp/239.76.248.19:1234",
    "张家界综合,http://8.8.8.8:8/udp/239.76.252.234:9000", "张家界,http://8.8.8.8:8/udp/239.76.252.235:9000",
    "邵阳新闻,http://8.8.8.8:8/udp/239.76.248.23:1234", "永州新闻,http://8.8.8.8:8/udp/239.76.248.57:1234",
    "怀化综合,http://8.8.8.8:8/udp/239.76.255.12:9000", "金色夕阳,http://8.8.8.8:8/udp/239.76.254.43:9000",
    "CCTV第一剧场,http://8.8.8.8:8/udp/239.76.254.49:9000", "CCTV风云足球,http://8.8.8.8:8/udp/239.76.254.52:9000",
    "CCTV风云音乐,http://8.8.8.8:8/udp/239.76.254.51:9000", "CCTV风云剧场,http://8.8.8.8:8/udp/239.76.254.50:9000",
    "CCTV女姓时尚,http://8.8.8.8:8/udp/239.76.254.55:9000", "CCTV央视文化精品,http://8.8.8.8:8/udp/239.76.254.56:9000",
    "CCTV世界地理,http://8.8.8.8:8/udp/239.76.254.57:9000", "CCTV兵器科技,http://8.8.8.8:8/udp/239.76.254.59:9000",
    "CCTV央视台球,http://8.8.8.8:8/udp/239.76.254.58:9000", "CCTV怀旧剧场,http://8.8.8.8:8/udp/239.76.254.53:9000",
    "CCTV电视指南,http://8.8.8.8:8/udp/239.76.254.61:9000", "CCTV央视高尔夫,http://8.8.8.8:8/udp/239.76.254.62:9000",
    "北京少儿,http://8.8.8.8:8/udp/239.76.254.81:9000", "快乐垂钓,http://8.8.8.8:8/udp/239.76.253.5:9000",
    "湖南卫视,http://8.8.8.8:8/udp/239.76.253.101:9000", "湖南国际,http://8.8.8.8:8/udp/239.76.253.102:9000",
    "湖南卫视,http://8.8.8.8:8/udp/239.76.253.100:9000", "湖南经视,http://8.8.8.8:8/udp/239.76.253.103:9000",
    "湖南都市,http://8.8.8.8:8/udp/239.76.253.104:9000", "湖南娱乐,http://8.8.8.8:8/udp/239.76.253.105:9000",
    "湖南电影,http://8.8.8.8:8/udp/239.76.253.106:9000", "湖南电视剧,http://8.8.8.8:8/udp/239.76.253.108:9000",
    "金鹰卡通,http://8.8.8.8:8/udp/239.76.253.107:9000", "湖南公共,http://8.8.8.8:8/udp/239.76.253.109:9000",
    "金鹰纪实,http://8.8.8.8:8/udp/239.76.253.110:9000", "长沙新闻,http://8.8.8.8:8/udp/239.76.253.121:9000",
    "长沙政法,http://8.8.8.8:8/udp/239.76.253.122:9000", "欢笑剧场4K,http://8.8.8.8:8/udp/239.76.253.130:9000", 
    "极速汽车,http://8.8.8.8:8/udp/239.76.253.133:9000", "动漫秀场,http://8.8.8.8:8/udp/239.76.253.131:9000",
    "凤凰资讯,http://8.8.8.8:8/udp/239.76.253.135:9000", "凤凰中文,http://8.8.8.8:8/udp/239.76.253.134:9000",
    "体育,http://8.8.8.8:8/udp/239.76.253.136:9000", "全纪实,http://8.8.8.8:8/udp/239.76.253.137:9000",
    "金色学堂,http://8.8.8.8:8/udp/239.76.253.139:9000", "法治天地,http://8.8.8.8:8/udp/239.76.253.138:9000",
    "CCTV1,http://8.8.8.8:8/udp/239.76.253.151:9000", "CCTV2,http://8.8.8.8:8/udp/239.76.253.152:9000",
    "CCTV3,http://8.8.8.8:8/udp/239.76.253.153:9000", "CCTV4,http://8.8.8.8:8/udp/239.76.253.154:9000",
    "CCTV5,http://8.8.8.8:8/udp/239.76.253.155:9000", "CCTV5+,http://8.8.8.8:8/udp/239.76.253.168:9000",
    "CCTV6,http://8.8.8.8:8/udp/239.76.253.156:9000", "CCTV7,http://8.8.8.8:8/udp/239.76.253.157:9000",
    "CCTV8,http://8.8.8.8:8/udp/239.76.253.158:9000", "CCTV9,http://8.8.8.8:8/udp/239.76.253.159:9000",
    "CCTV10,http://8.8.8.8:8/udp/239.76.253.160:9000", "CCTV12,http://8.8.8.8:8/udp/239.76.253.162:9000",
    "CCTV13,http://8.8.8.8:8/udp/239.76.253.93:9000", "CCTV14,http://8.8.8.8:8/udp/239.76.253.164:9000",
    "CCTV16,http://8.8.8.8:8/udp/239.76.253.98:9000", "CCTV16 4K,http://8.8.8.8:8/udp/239.76.253.214:9000",
    "CCTV16 4K,http://8.8.8.8:8/udp/239.76.254.200:9000", "CCTV16 4K,http://8.8.8.8:8/udp/239.76.253.224:9000",
    "CCTV16 4K,http://8.8.8.8:8/udp/239.76.253.230:9000", "江苏卫视,http://8.8.8.8:8/udp/239.76.253.181:9000",
    "浙江卫视,http://8.8.8.8:8/udp/239.76.253.182:9000", "北京卫视,http://8.8.8.8:8/udp/239.76.253.184:9000",
    "天津卫视,http://8.8.8.8:8/udp/239.76.253.185:9000", "东方卫视,http://8.8.8.8:8/udp/239.76.253.186:9000",
    "深圳卫视,http://8.8.8.8:8/udp/239.76.253.188:9000", "湖北卫视,http://8.8.8.8:8/udp/239.76.253.193:9000",
    "山东卫视,http://8.8.8.8:8/udp/239.76.253.195:9000", "黑龙江卫视,http://8.8.8.8:8/udp/239.76.253.200:9000",
    "吉林卫视,http://8.8.8.8:8/udp/239.76.253.201:9000", "河南卫视,http://8.8.8.8:8/udp/239.76.253.202:9000",
    "海南卫视,http://8.8.8.8:8/udp/239.76.253.203:9000", "四川卫视,http://8.8.8.8:8/udp/239.76.253.91:9000",
    "重庆卫视,http://8.8.8.8:8/udp/239.76.253.92:9000", "广西卫视,http://8.8.8.8:8/udp/239.76.254.54:9000",
    "陕西卫视,http://8.8.8.8:8/udp/239.76.254.76:9000", "云南卫视,http://8.8.8.8:8/udp/239.76.254.60:9000",
    "青海卫视,http://8.8.8.8:8/udp/239.76.254.132:9000", "甘肃卫视,http://8.8.8.8:8/udp/239.76.253.94:9000",
    "都市剧场,http://8.8.8.8:8/udp/239.76.253.215:9000", "生活时尚,http://8.8.8.8:8/udp/239.76.253.223:9000",
    "长沙女姓,http://8.8.8.8:8/udp/239.76.252.23:9000", "湖南卫视,http://8.8.8.8:8/udp/239.76.252.115:9000",
    "湖南经视,http://8.8.8.8:8/udp/239.76.252.116:9000", "湖南电视剧,http://8.8.8.8:8/udp/239.76.252.118:9000",
    "湖南电影,http://8.8.8.8:8/udp/239.76.252.119:9000", "金鹰卡通,http://8.8.8.8:8/udp/239.76.252.120:9000",
    "湖南公共,http://8.8.8.8:8/udp/239.76.252.123:9000", "湖南娱乐,http://8.8.8.8:8/udp/239.76.252.121:9000",
    "金鹰纪实,http://8.8.8.8:8/udp/239.76.252.122:9000", "湖南国际,http://8.8.8.8:8/udp/239.76.252.124:9000",
    "湖南都市,http://8.8.8.8:8/udp/239.76.252.117:9000", "快乐垂钓,http://8.8.8.8:8/udp/239.76.252.127:9000",
    "河南梨园,http://8.8.8.8:8/udp/239.76.252.179:9000", "文物宝库,http://8.8.8.8:8/udp/239.76.252.180:9000",
    "武术世界,http://8.8.8.8:8/udp/239.76.252.181:9000", "广东卫视,http://8.8.8.8:8/udp/239.76.252.189:9000",
    "东南卫视,http://8.8.8.8:8/udp/239.76.252.190:9000", "中国教育,http://8.8.8.8:8/udp/239.76.252.192:9000",
    "安徽卫视,http://8.8.8.8:8/udp/239.76.252.196:9000", "辽宁卫视,http://8.8.8.8:8/udp/239.76.252.197:9000",
    "河北卫视,http://8.8.8.8:8/udp/239.76.252.199:9000", "贵州卫视,http://8.8.8.8:8/udp/239.76.252.198:9000",
    "长沙影视,http://8.8.8.8:8/udp/239.76.252.204:9000", "湘西综合,http://8.8.8.8:8/udp/239.76.252.208:9000",
    "湘西公共,http://8.8.8.8:8/udp/239.76.252.209:9000", "湘西公共,http://8.8.8.8:8/udp/239.76.252.210:9000",
    "湖南教育,http://8.8.8.8:8/udp/239.76.252.233:9000","浏阳新闻,http://8.8.8.8:8/udp/239.76.255.6:9000",
    "湘西公共,http://8.8.8.8:8/udp/239.76.252.209:9000", "湘西公共,http://8.8.8.8:8/udp/239.76.252.210:9000",
    "湘西综合,http://8.8.8.8:8/udp/239.76.252.208:9000", "湘西综合,http://8.8.8.8:8/udp/239.76.245.208:1234",
    "衡阳公共,http://8.8.8.8:8/udp/239.76.255.14:9000", "衡阳综合,http://8.8.8.8:8/udp/239.76.255.13:9000",
    "衡阳县电视台,http://8.8.8.8:8/udp/239.76.255.26:9000", "邵阳公共,http://8.8.8.8:8/udp/239.76.255.22:9000",
    "邵阳综合,http://8.8.8.8:8/udp/239.76.255.21:9000", "娄底教育,http://8.8.8.8:8/udp/239.76.255.20:9000",
    "娄底综合,http://8.8.8.8:8/udp/239.76.255.18:9000", "娄底公共,http://8.8.8.8:8/udp/239.76.255.19:9000",
    "郴州综合,http://8.8.8.8:8/udp/239.76.253.75:9000", "张家界综合,http://8.8.8.8:8/udp/239.76.252.234:9000",
    "张家界公共,http://8.8.8.8:8/udp/239.76.252.235:9000", "怀化综合,http://8.8.8.8:8/udp/239.76.255.12:9000",
    "常德综合,http://8.8.8.8:8/udp/239.76.255.10:9000", "常德公共,http://8.8.8.8:8/udp/239.76.255.11:9000",
    "永州综合,http://8.8.8.8:8/udp/239.76.255.23:9000", "溆浦综合,http://8.8.8.8:8/udp/239.76.255.25:9000",
    "武冈综合,http://8.8.8.8:8/udp/239.76.255.29:9000", "新化,http://8.8.8.8:8/udp/239.76.255.31:9000",
    "津市,http://8.8.8.8:8/udp/239.76.255.30:9000", "桂东融媒,http://8.8.8.8:8/udp/239.76.253.231:9000",
    "道县综合,http://8.8.8.8:8/udp/239.76.255.28:9000", "永州公共,http://8.8.8.8:8/udp/239.76.255.24:9000",
    "株洲公共,http://8.8.8.8:8/udp/239.76.252.236:9000", "株洲综合,http://8.8.8.8:8/udp/239.76.255.1:9000",
    "湘潭公共,http://8.8.8.8:8/udp/239.76.255.5:9000", "湘潭综合,http://8.8.8.8:8/udp/239.76.255.4:9000",
    "益阳公共,http://8.8.8.8:8/udp/239.76.255.16:9000", "益阳综合,http://8.8.8.8:8/udp/239.76.255.15:9000",
    "岳阳综合,http://8.8.8.8:8/udp/239.76.255.7:9000", "岳阳科教,http://8.8.8.8:8/udp/239.76.255.9:9000",
    "岳阳公共,http://8.8.8.8:8/udp/239.76.255.8:9000",
]


results = []
channel = []
urls_all = []
resultsx = []
resultxs = []
error_channels = []

for url in urls:
    url_0 = str(base64.b64encode((f'"Server: udpxy" && city="{url}" && asn="4134"').encode("utf-8")), "utf-8")
    url_64 = f'https://fofa.info/result?qbase64={url_0}&page=1&page_size=20'
    print(url_64)
    try:
        response = requests.get(url_64, headers=headers, timeout=15)
        page_content = response.text
        print(f" {url}  访问成功")
        pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
        page_urls = re.findall(pattern, page_content)
        for urlx in page_urls:
            try:
                response = requests.get(url=urlx + '/status', timeout=1)
                response.raise_for_status()  # 返回状态码不是200异常
                page_content = response.text
                pattern = r'class="proctabl"'
                page_proctabl = re.findall(pattern, page_content)
                if page_proctabl:
                    urls_all.append(urlx)
                    print(f"{urlx} 可以访问")

            except requests.RequestException as e:
                pass
    except:
        print(f"{url_64} 访问失败")
        pass

urls_all = set(urls_all)  # 去重得到唯一的URL列表
for urlx in urls_all:
    channel = [f'{name},{url.replace("http://8.8.8.8:8", urlx)}' for name, url in
               [line.strip().split(',') for line in channelsx]]
    results.extend(channel)
            
results = sorted(results)
# with open("hn.txt", 'w', encoding='utf-8') as file:
#     for result in results:
#         file.write(result + "\n")
#         print(result)

# 定义工作线程函数
def worker():
    while True:
        result = task_queue.get()
        channel_name, channel_url = result.split(',', 1)
        try:
            response = requests.get(channel_url, stream=True, timeout=3)
            if response.status_code == 200:
                result = channel_name, channel_url
                resultsx.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
            else:
                error_channels.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channels.append(result)
            numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
            print(
                f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 20
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# 添加下载任务到队列
for result in results:
    task_queue.put(result)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字


for resulta in resultsx:
    channel_name, channel_url = resulta
    resultx = channel_name, channel_url
    resultxs.append(resultx)

# 对频道进行排序
resultxs.sort(key=lambda x: channel_key(x[0]))
# now_today = datetime.date.today()

result_counter = 20  # 每个频道需要的个数

with open("hn.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n卫视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n港澳频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '凤凰' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1            
    channel_counters = {}
    file.write('\n湖南频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '湖南' in channel_name or '长沙' in channel_name or '金鹰' in channel_name or '娄底' in channel_name or '常德' \
                in channel_name or '张家界' in channel_name or '怀化' in channel_name or '浏阳' in channel_name or '湘西' \
                in channel_name or '衡阳' in channel_name or '邵阳' in channel_name or '郴州' in channel_name  or '岳阳' in channel_name or '溆浦' \
                in channel_name or '武冈' in channel_name or '新化' in channel_name or '津市' in channel_name or '桂东' in channel_name \
                 or '道县' in channel_name or '永州' in channel_name or '株洲' in channel_name or '湘潭' in channel_name or '益阳' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

# 扫源凤凰卫视

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

urls = ["chengdu", "mianyang", "guangyuan", "deyang", "nanchong", "guangan", "suining", "neijiang", "leshan", "zigong", "luzhou", "yibin", "panzhihua", "bazhong", "dazhou", "ziyang", "meishan", "yaan",
    "lanzhou", "jiayuguan", "jinchang", "baiyin", "tianshui", "wuwei", "zhangye", "pingliang", "jiuquan", "qingyang", "dingxi", "longnan",
    "hangzhou", "ningbo", "wenzhou", "jiaxing", "huzhou", "shaoxing", "jinhua", "quzhou", "zhoushan", "taizhou", "lishui",
    "fuzhou", "xiamen", "zhangzhou", "quanzhou", "sanming", "putian", "nanping", "longyan", "ningde"]
channelsx = [
        "凤凰中文,http://8.8.8.8:8/rtp/239.93.1.9:2192","凤凰资讯,http://8.8.8.8:8/rtp/239.93.1.4:2191","凤凰香港,http://8.8.8.8:8/udp/239.255.30.123:8231",
            "凤凰中文,http://8.8.8.8:8/udp/239.255.30.50:8231","凤凰资讯,http://8.8.8.8:8/udp/239.255.30.70:8231","凤凰中文,http://8.8.8.8:8/udp/233.50.200.42:5140",
            "凤凰中文,http://8.8.8.8:8/udp/233.50.200.191:5140","凤凰资讯,http://8.8.8.8:8/udp/233.50.200.192:5140","凤凰资讯,http://8.8.8.8:8/udp/239.76.246.8:1234",
            "凤凰中文,http://8.8.8.8:8/udp/239.76.246.7:1234","凤凰资讯,http://8.8.8.8:8/rtp/239.61.2.183:9086","凤凰中文,http://8.8.8.8:8/rtp/239.61.2.184:9092",
]


results = []
channel = []
urls_all = []
resultsx = []
resultxs = []
error_channels = []

for url in urls:
    url_0 = str(base64.b64encode((f'"Server: udpxy" && city="{url}" && asn="4134"').encode("utf-8")), "utf-8")
    url_64 = f'https://fofa.info/result?qbase64={url_0}&page=1&page_size=20'
    print(url_64)
    try:
        response = requests.get(url_64, headers=headers, timeout=15)
        page_content = response.text
        print(f" {url}  访问成功")
        pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
        page_urls = re.findall(pattern, page_content)
        for urlx in page_urls:
            try:
                response = requests.get(url=urlx + '/status', timeout=1)
                response.raise_for_status()  # 返回状态码不是200异常
                page_content = response.text
                pattern = r'class="proctabl"'
                page_proctabl = re.findall(pattern, page_content)
                if page_proctabl:
                    urls_all.append(urlx)
                    print(f"{urlx} 可以访问")

            except requests.RequestException as e:
                pass
    except:
        print(f"{url_64} 访问失败")
        pass

urls_all = set(urls_all)  # 去重得到唯一的URL列表
for urlx in urls_all:
    channel = [f'{name},{url.replace("http://8.8.8.8:8", urlx)}' for name, url in
               [line.strip().split(',') for line in channelsx]]
    results.extend(channel)
            
results = sorted(results)
# with open("ph.txt", 'w', encoding='utf-8') as file:
#     for result in results:
#         file.write(result + "\n")
#         print(result)

# 定义工作线程函数
def worker():
    while True:
        result = task_queue.get()
        channel_name, channel_url = result.split(',', 1)
        try:
            response = requests.get(channel_url, stream=True, timeout=3)
            if response.status_code == 200:
                result = channel_name, channel_url
                resultsx.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
            else:
                error_channels.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channels.append(result)
            numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
            print(
                f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 20
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# 添加下载任务到队列
for result in results:
    task_queue.put(result)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字


for resulta in resultsx:
    channel_name, channel_url = resulta
    resultx = channel_name, channel_url
    resultxs.append(resultx)

# 对频道进行排序
resultxs.sort(key=lambda x: channel_key(x[0]))
# now_today = datetime.date.today()

result_counter = 20  # 每个频道需要的个数

with open("ph.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('港澳频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '凤凰' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

# 定义合并频道函数
def merge_channels(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    channels = {}
    current_channel = None

    for line in lines:
        line = line.strip()
        if line.endswith('#genre#'):
            current_channel = line
            if current_channel not in channels:
                channels[current_channel] = []
        else:
            channels[current_channel].append(line)

    with open(file_name, 'w', encoding="utf-8") as f:
        for channel, urls in channels.items():
            f.write(channel + '\n')
            for url in urls:
                f.write(url + '\n')

# 合并自定义频道文件内容
file_contents = []
file_paths = ["hb.txt","he.txt","bj.txt","hn.txt","ph.txt","GAT.txt","gat2.txt","sport.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("iptv_list.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

# 在合并后的文件中进一步合并相同的频道
merge_channels('iptv_list.txt')

# 写入更新日期时间
with open("iptv_list.txt", "a", encoding="utf-8") as output:  # 使用 "a" 模式以追加方式打开文件
    now = datetime.now()  # 这一行的缩进应与上一行的 with 语句对齐
    output.write(f"更新时间,#genre#\n")
    output.write(f"{now.strftime('%Y-%m-%d')},url\n")
    output.write(f"{now.strftime('%H:%M:%S')},url\n")

os.remove("hb.txt")
os.remove("he.txt")
os.remove("bj.txt")
os.remove("hn.txt")
os.remove("ph.txt")
os.remove("DIYP-v4.txt")
os.remove("GAT.txt")
os.remove("HK.txt")
os.remove("TW.txt")
os.remove("sport.txt")

def txt_to_m3u(input_file, output_file):
    # 读取txt文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 打开m3u文件并写入内容
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')

        # 初始化genre变量
        genre = ''

        # 遍历txt文件内容
        for line in lines:
            line = line.strip()
            if "," in line:  # 防止文件里面缺失“,”号报错
                # if line:
                # 检查是否是genre行
                channel_name, channel_url = line.split(',', 1)
                if channel_url == '#genre#':
                    genre = channel_name
                    print(genre)
                else:
                    # 将频道信息写入m3u文件
                    f.write(f'#EXTINF:-1 group-title="{genre}",{channel_name}\n')
                    f.write(f'{channel_url}\n')


# 将txt文件转换为m3u文件
txt_to_m3u('iptv_list.txt', 'iptv_list.m3u')

print("任务运行完毕，分类频道列表可查看文件夹内iptv_list.txt和iptv_list.m3u文件！")
