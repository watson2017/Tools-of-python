# - * - coding: utf-8 - * -

import conf
import yaml
import sys
import os
import requests
import time
from fabric.api import run, env, task, execute, local, settings, sudo, hide, put, cd, lcd
from fabric.state import output
from fabric.network import disconnect_all
from datetime import datetime


def closeConnection():
    # 关闭会话链接
    disconnect_all()


def parseYaml():
    ymlRead = dict()
    try:
        with open("conf/hosts.yml") as f:
            ymlRead = yaml.load(f)
    except Exception as e:
        conf.log.error(e)
        sys.exit(1)
    conf.log.info("parse yaml file success.")
    return ymlRead


def initFab():
    ymlRead = parseYaml()
    # 解析yaml文件内容到env全局变量中
    for key, value in ymlRead.iteritems():
        env[key] = value
    # 全局配置，关闭running模式输出
    output.running = False
    # 关闭disconnect_all方法信息输出
    output.status = False
    # 全局配置，关闭输出前缀
    env.output_prefix = False


@task
def startRiskControlTask():
    rootFolder = "/data/web"
    projectFolder = "%s/%s" % (rootFolder, env.project_name)
    javaHome = "/usr/local/jdk1.8.0_25"
    logName = "risk_control.log"
    arg = "--spring.config.location=/web/share/riskcontrol/application.properties"
    shellFile = os.path.join(os.getcwd(), "shell", env.shell_name)
    startCmd = '''/bin/bash %s/%s %s %s %s %s %s && sleep 3s''' % (
        env.upload_folder, env.shell_name, projectFolder, javaHome,
        env.package_name, arg, logName)
    from fabric.api import show
    with show("everything"):
        with settings(warn_only=True):
            with cd(projectFolder):
                # 删除旧脚本文件
                result = sudo("rm %s/%s -f" %
                              (env.upload_folder, env.shell_name))
                if result.failed:
                    conf.log.error(
                        "delete old shell on project server failed.")
                    sys.exit(1)
                else:
                    conf.log.info(
                        "delete old shell on project server success.")

                # 上传脚本到项目服务器
                result = put(shellFile, env.upload_folder)
                if result.failed:
                    conf.log.error("upload shell to project server failed.")
                    sys.exit(1)
                else:
                    conf.log.info("upload shell to project server success.")

                result = sudo(startCmd)
                if result.failed:
                    conf.log.error("start riskcontrol failed.")
                else:
                    conf.log.info("start riskcontrol success.")


@task
def backupTask():
    # 防止yaml文件配置目录错误，导致删除系统文件，采用固化项目目录，如项目特殊
    # 可以自定义修改
    rootFolder = "/data/web"
    projectFolder = "%s/%s" % (rootFolder, env.project_name)
    nowTime = datetime.now().strftime("%Y-%m-%d_%H_%M")
    with hide("everything"):
        with settings(warn_only=True):
            # 获取项目服务器主机名
            result = sudo("hostname")
            hostname = result.stdout
            if hostname in [""]:
                conf.log.error("get project server hostname failed.")
                sys.exit(1)

            backup_folder = os.path.join(env.backup_folder, hostname)
            createFolderCmd = "mkdir %s" % (backup_folder)
            # 备份文件名称
            backupPkgName = "%s-%s.%s.jar" % (nowTime, env.project_name,
                                              hostname)
            # 复制文件
            cpCmd = "cp -rpf %s %s" % (env.package_name, os.path.join(
                backup_folder, backupPkgName))

            # 创建备份目录
            result = sudo(createFolderCmd)
            if result.failed:
                conf.log.warn("folder %s existed." % (backup_folder))
            else:
                conf.log.info("create %s success." % (backup_folder))

            with cd(projectFolder):
                # 重命名项目名称
                result = sudo(cpCmd)
                if result.failed:
                    conf.log.error("backup jar failed.")
                    sys.exit(1)
                else:
                    conf.log.info("backup jar success.")


@task
def rollbackPKGTask(backup_file):
    with hide("everything"):
        with settings(warn_only=True):
            # 获取项目服务器主机名
            result = sudo("hostname")
            hostname = result.stdout
            if hostname in [""]:
                conf.log.error("get project server hostname failed.")
                sys.exit(1)

            backup_folder = os.path.join(env.backup_folder, hostname)
            lastestPKGName = backup_file
            lastestPKGAbs = os.path.join(backup_folder, lastestPKGName)
            uploadPKGAbs = os.path.join(
                env.local_storage.rstrip("/"), env.package_name)
            rollbackPKGCmd = "sudo cp -rpf %s %s" % (lastestPKGAbs,
                                                     uploadPKGAbs)
            with lcd(env.local_storage):
                # 压缩成包
                local("sudo rm %s -f" % (env.package_name))
                result = local(rollbackPKGCmd)
                if result.failed:
                    conf.log.error("%s failed." % (rollbackPKGCmd))
                    sys.exit(1)
                else:
                    conf.log.info("%s success." % (rollbackPKGCmd))


@task
def deployTask():
    pkgAbs = os.path.join(env.upload_folder, env.package_name)
    # 防止yaml文件配置目录错误，导致删除系统文件，采用固化项目目录，如项目特殊
    # 可以自定义修改
    rootFolder = "/data/web"
    projectFolder = "%s/%s" % (rootFolder, env.project_name)
    delProjectCmd = "rm %s/%s -rf" % (projectFolder, env.package_name)
    updateProjectCmd = "cp -rpf %s %s" % (pkgAbs, projectFolder)
    with hide("everything"):
        with settings(warn_only=True):
            # 删除项目目录
            result = sudo(delProjectCmd)
            if result.failed:
                conf.log.error("delete project folder failed.")
                sys.exit(1)
            else:
                conf.log.info("delete project folder success.")

            # 更新项目
            result = sudo(updateProjectCmd)
            if result.failed:
                conf.log.error("update project failed.")
                sys.exit(1)
            else:
                conf.log.info("update project success.")


@task
def stopRiskControlTask():
    preCheckCmd = """netstat -anp | grep ":%s" | grep "LISTEN" | awk '{print $7}' | awk -F'/' '{print $1}'""" % (
        env.project_port)
    stopCmd = """%s | xargs kill -9""" % (preCheckCmd)
    with hide("everything"):
        with settings(warn_only=True):
            result = sudo(preCheckCmd)
            if result.stdout in [""]:
                conf.log.warn("riskcontrol is not alived.")
            else:
                result = sudo(stopCmd)
                if result.failed:
                    conf.log.error("stop riskcontrol failed.")
                    sys.exit(1)
                else:
                    conf.log.info("stop riskcontrol success.")


@task
def uploadPKG4SCPTask():
    local_pkg = os.path.join(env.local_storage.rstrip("/"), env.package_name)
    remote_old_pkg = os.path.join(env.upload_folder, env.package_name)
    with hide("everything"):
        with settings(warn_only=True):
            # 删除项目服务器老版本包
            result = run("rm %s -f" % remote_old_pkg)
            if result.failed:
                conf.log.error("delete old package on project server failed.")
                sys.exit(1)
            else:
                conf.log.info("delete old package on project server success.")
            # 上传包到项目服务器
            result = put(local_pkg, env.upload_folder)
            if result.failed:
                conf.log.error("upload package to project server failed.")
                sys.exit(1)
            else:
                conf.log.info("upload package to project server success.")


@task
def rsyncTask():
    passwdAbs = os.path.join(os.getcwd(), "conf", env.passwd_file)
    passFile = "--password-file=%s" % (passwdAbs)
    authInfo = "%s@%s::%s" % (env.rsync_user, env.rsync_host,
                              env.rsync_section)
    rsyncCmd = """sudo rsync -qzrtopg --include="%s" --exclude="/*" --port=%s --delete %s %s %s""" % (
        env.package_name, env.rsync_port, passFile, authInfo,
        env.local_storage)
    with hide("everything"):
        with settings(warn_only=True):
            # 下载远程仓库最新代码
            result = local(rsyncCmd)
            if result.failed:
                conf.log.error("%s failed." % (rsyncCmd))
                sys.exit(1)
            else:
                conf.log.info("rsync success.")


@task
def mavenTask(profile, pom_xml):
    mavenCmd = "mvn -U -f %s clean package -P %s -Dmaven.test.skip=true" % (
        pom_xml, profile)
    with hide("everything"):
        with settings(warn_only=True):
            with cd(env.build_folder):
                # 下载远程仓库最新代码
                result = sudo(mavenCmd)
                if result.failed:
                    conf.log.error("%s failed." % (mavenCmd))
                    sys.exit(1)
                else:
                    conf.log.info("%s success." % (mavenCmd))


@task
def keepLatestTask(branchName):
    hgPullCmd = "hg pull --rev %s" % (branchName)
    hgUpdateCmd = "hg update --clean --rev %s" % (branchName)
    hgSwitchBranchCmd = "hg update %s" % (branchName)
    hgPurgeCmd = "hg purge"
    with hide("everything"):
        with settings(warn_only=True):
            with cd(env.build_folder):
                # 下载远程仓库最新代码
                result = sudo(hgPullCmd)
                if result.failed:
                    conf.log.error("%s failed." % (hgPullCmd))
                    sys.exit(1)
                else:
                    conf.log.info("%s success." % (hgPullCmd))

                # 清除未提交的代码，更新代码到当前目录
                result = sudo(hgUpdateCmd)
                if result.failed:
                    conf.log.error("%s failed." % (hgUpdateCmd))
                    sys.exit(1)
                else:
                    conf.log.info("%s success." % (hgUpdateCmd))

                # 切换分支
                result = sudo(hgSwitchBranchCmd)
                if result.failed:
                    conf.log.error("%s failed." % (hgSwitchBranchCmd))
                    sys.exit(1)
                else:
                    conf.log.info("%s success." % (hgSwitchBranchCmd))

                # 清除当前目录无关文件,purge扩展命令，需要安装配置，默认hg没有集成
                result = sudo(hgPurgeCmd)
                if result.failed:
                    conf.log.error("%s failed." % (hgPurgeCmd))
                    sys.exit(1)
                else:
                    conf.log.info("%s success." % (hgPurgeCmd))


def keepLatest(branchName):
    # fab集成到项目时，调用方式
    # 6.22-jenkins服务器上更新仓库代码
    execute(keepLatestTask, branchName, hosts=[env.build_server])


def maven(profile, pom_xml):
    # fab集成到项目时，调用方式
    # 6.22-jenkins服务器上编译代码
    execute(mavenTask, profile, pom_xml, hosts=[env.build_server])


def rsync():
    # fab集成到项目时，调用方式
    # 从6.22-jenkins服务器同步编译后代码
    execute(rsyncTask)


def uploadPKG4SCP(project_server):
    # fab集成到项目时，调用方式
    # SCP方式上传包到项目服务器
    execute(uploadPKG4SCPTask, hosts=[project_server])


def stopRiskControl(project_server):
    # fab集成到项目时，调用方式
    # 停止riskcontrol服务
    execute(stopRiskControlTask, hosts=[project_server])


def backup(project_server):
    # fab集成到项目时，调用方式
    # 全量备份项目
    execute(backupTask, hosts=[project_server])


def rollbackPKG(backup_file, project_server):
    # fab集成到项目时，调用方式
    # 部署项目
    execute(rollbackPKGTask, backup_file, hosts=[project_server])


def deploy(project_server):
    # fab集成到项目时，调用方式
    # 部署项目
    execute(deployTask, hosts=[project_server])


def startRiskControl(project_server):
    # fab集成到项目时，调用方式
    # 启动tomcat服务
    execute(startRiskControlTask, hosts=[project_server])


def tomcatHealth(project_url):
    # fab集成到项目时，调用方式
    # 检查tomcat服务健康状况
    for i in xrange(3):
        try:
            req = requests.head(project_url)
            req.raise_for_status()
        except requests.RequestException as e:
            conf.log.error("tomcat status is unknow in retry %d.msg: %s" %
                           (i, e.message))
            if i in [2]:
                sys.exit(1)
            time.sleep(2)
        else:
            conf.log.info("tomcat status is normal.")
            break
