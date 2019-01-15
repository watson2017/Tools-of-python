#!/home/ansible/.venv/bin/python
# - * - coding: utf-8 - * -
"""RDS CLI.

Usage:[]
    rds_utils.py describe_backups_request
    rds_utils.py describe_backups_intranet_request
    rds_utils.py describe_dbinstanceperformance_request
    rds_utils.py -h | --help
    rds_utils.py --version

Options:
  -h, --help    display this help and exit.
  --version     output version information and exit.
"""

import json
import sys
import datetime
from docopt import docopt
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeBackupsRequest, \
    DescribeDBInstancePerformanceRequest
access_key_id = ""
access_key_secret = ""
access_region = "cn-shenzhen"
accept_fomat = "json"
db_instanceid = ""


def get_time_range():
    u"""获取查询备份数据库文件的开始和结束时间."""
    now_time = datetime.datetime.now()
    end_at = datetime.datetime.strftime(now_time, '%Y-%m-%dT%H:%MZ')
    yesterday = now_time + datetime.timedelta(days=-2)
    start_at = datetime.datetime.strftime(yesterday, '%Y-%m-%dT16:00Z')
    return (start_at, end_at,)


def get_session_time_range():
    u"""获取查询数据库session会话链接数时间范围."""
    now_time = datetime.datetime.now()
    end_at = datetime.datetime.strftime(now_time, '%Y-%m-%dT%H:%MZ')
    yesterday = now_time + datetime.timedelta(days=-2)
    start_at = datetime.datetime.strftime(yesterday, '%Y-%m-%dT16:00Z')
    return (start_at, end_at,)


def describe_dbinstanceperformance_request():
    u"""获取指定RDS会话链接数."""
    (start_at, end_at) = get_time_range()
    clt = client.AcsClient(access_key_id, access_key_secret, access_region)
    request = DescribeDBInstancePerformanceRequest.\
        DescribeDBInstancePerformanceRequest()
    request.set_accept_format(accept_fomat)
    request.set_action_name('DescribeDBInstancePerformance')
    request.set_DBInstanceId(db_instanceid)
    request.set_StartTime(start_at)
    request.set_EndTime(end_at)
    result = clt.do_action(request)
    result = json.loads(result)
    backup_list = result.get('Items', {}).get('Backup', None)
    print backup_list


def describe_backups_request():
    u"""获取指定RDS中互联网备份下载地址."""
    (start_at, end_at) = get_time_range()
    clt = client.AcsClient(access_key_id, access_key_secret, access_region)
    request = DescribeBackupsRequest.DescribeBackupsRequest()
    request.set_accept_format(accept_fomat)
    request.set_action_name('DescribeBackups')
    request.set_DBInstanceId(db_instanceid)
    request.set_StartTime(start_at)
    request.set_EndTime(end_at)
    result = clt.do_action(request)
    result = json.loads(result)
    backup_list = result.get('Items', {}).get('Backup', None)

    if backup_list is None:
        print "Retrive [elc_db] database backup file failed."
        sys.exit(1)
    elif not backup_list:
        print "Retrive [elc_db] database backup file failed."
        sys.exit(1)
    else:
        last_backup = backup_list[0]
        if last_backup.get('BackupType', None) in ['FullBackup']:
            # 线上新增数据库后，此处需要同步修改
            if last_backup.get('BackupDBNames', None) in ['elc_db,premium']:
                if last_backup.get('BackupMethod') in ['Physical']:
                    if last_backup.get('BackupStatus') in ['Success']:
                        print last_backup.get('BackupDownloadURL')
                        sys.exit(0)
                    else:
                        print "Invalid BackupStatus [{0}].".format(
                            last_backup.get('BackupStatus', None))
                        sys.exit(1)
                else:
                    print "Invalid BackupMethod [{0}].".format(
                        last_backup.get('BackupMethod', None))
                    sys.exit(1)
            else:
                print "Invalid BackupDBNames [{0}].".format(
                    last_backup.get('BackupDBNames', None))
                sys.exit(1)
        else:
            print "Invalid BackupType [{0}].".format(
                last_backup.get('BackupType', None))
            sys.exit(1)


def describe_backups_intranet_request():
    u"""获取指定RDS中阿里云内网备份下载地址."""
    (start_at, end_at) = get_time_range()
    clt = client.AcsClient(access_key_id, access_key_secret, access_region)
    request = DescribeBackupsRequest.DescribeBackupsRequest()
    request.set_accept_format(accept_fomat)
    request.set_action_name('DescribeBackups')
    request.set_DBInstanceId(db_instanceid)
    request.set_StartTime(start_at)
    request.set_EndTime(end_at)
    result = clt.do_action(request)
    result = json.loads(result)
    backup_list = result.get('Items', {}).get('Backup', None)

    if backup_list is None:
        print "Retrive [elc_db] database backup file failed."
        sys.exit(1)
    elif not backup_list:
        print "Retrive [elc_db] database backup file failed."
        sys.exit(1)
    else:
        last_backup = backup_list[0]
        if last_backup.get('BackupType', None) in ['FullBackup']:
            # 线上新增数据库后，此处需要同步修改
            if last_backup.get('BackupDBNames', None) in ['elc_db,premium']:
                if last_backup.get('BackupMethod') in ['Physical']:
                    if last_backup.get('BackupStatus') in ['Success']:
                        print last_backup.get('BackupIntranetDownloadURL')
                        sys.exit(0)
                    else:
                        print "Invalid BackupStatus [{0}].".format(
                            last_backup.get('BackupStatus', None))
                        sys.exit(1)
                else:
                    print "Invalid BackupMethod [{0}].".format(
                        last_backup.get('BackupMethod', None))
                    sys.exit(1)
            else:
                print "Invalid BackupDBNames [{0}].".format(
                    last_backup.get('BackupDBNames', None))
                sys.exit(1)
        else:
            print "Invalid BackupType [{0}].".format(
                last_backup.get('BackupType', None))
            sys.exit(1)


def action_route(args):
    u"""命令行参数解析后路由."""
    if args.get('describe_backups_request'):
        describe_backups_request()
    elif args.get('describe_backups_intranet_request'):
        describe_backups_intranet_request()
    elif args.get('describe_dbinstanceperformance_request'):
        describe_dbinstanceperformance_request()


if __name__ == '__main__':
    args = docopt(__doc__, version='RDS CLI 1.0')
    action_route(args)
