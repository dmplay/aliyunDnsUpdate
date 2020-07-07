

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import yaml
import sys
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
import urllib.request
from json import load
from datetime import datetime
import logging

def AliAccessKey(id,Secret,region):
    try:
        client = AcsClient(id, Secret, region)
        return client
    except Exception as e:
        print("验证aliyun key失败")
        print(e)
        sys.exit(-1)

def read_yaml(filename):
    try:
        yaml_file = open(filename,"rb")
        yaml_data = yaml.safe_load(yaml_file)
        yaml_file.close()
        return yaml_data
    except Exception as e:
        print("读取配置文件错误")
        print(e)
        sys.exit(-1)

def GetDNSRecord(yaml_data,client,DomainName):
    try:
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))
        for Record in json_data['DomainRecords']['Record']:
            if yaml_data['DnsData']['RR'] == Record['RR']:
                return Record

    except Exception as e:
        print("获取RecordId失败")
        print(e)
        sys.exit(-1)

def UpdateDomainRecord(client,yaml_data,RecordId,ip):
    try:
        dnsData = yaml_data['DnsData']
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        DomainValue = ip
        request.set_Value(DomainValue)
        request.set_Type(dnsData['DomainType'])
        request.set_RR(dnsData['RR'])
        request.set_RecordId(RecordId)
        response = client.do_action_with_exception(request)
        print("更新域名解析成功")
        print("域名:" + dnsData['DomainName'] + " 主机:" + dnsData['RR'] + " 记录类型:" +  dnsData['DomainType'] + " 记录值:" +  DomainValue)
    except Exception as e:
        print("更新域名解析失败")
        print(e)


def getIp():
    my_ip = load(urllib.request.urlopen('https://jsonip.com'))['ip']
    return my_ip


def checkDomain():

    yaml_data = read_yaml('conf/conf.yaml')
    dnsData=yaml_data['DnsData']
    domanName=dnsData['RR']+"."+dnsData['DomainName']

    print('校验域名[', domanName, ']: ', datetime.now())

    client = AliAccessKey(yaml_data['AliyunData']['AccessKey_ID'], yaml_data['AliyunData']['Access_Key_Secret'],
                          yaml_data['AliyunData']['region_id'])
    Record = GetDNSRecord(yaml_data, client, dnsData['DomainName'])
    macIp = getIp()
    if(macIp != Record['Value']):
        print('校验域名[', ']: IP修改 ', Record['Value'], '-> ', macIp)
        UpdateDomainRecord(client, yaml_data, Record['RecordId'], macIp)
    else:
        print('校验域名[', domanName, ']: 无需修改')
    print('-----------')


if __name__ == "__main__" :
    checkDomain()

