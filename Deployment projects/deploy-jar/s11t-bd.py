#!/home/ansible/.venv/bin/python
# - * - coding: utf-8 - * -
"""Spring-Project Build-Deploy CLI.

Usage:[]
    s11t-bd.py keeplatest [--branch=<kn>]
    s11t-bd.py inspect-file
    s11t-bd.py update-manifest
    s11t-bd.py maven [--profile=<kn>] [--pom_xml=<kn>]
    s11t-bd.py rsync
    s11t-bd.py packaging
    s11t-bd.py upload --project-server=<kn>
    s11t-bd.py offline-slb --ecs-id=<kn>
    s11t-bd.py stop-tomcat --project-server=<kn>
    s11t-bd.py backup --project-server=<kn>
    s11t-bd.py rollback-pkg --backup-file=<kn> --project-server=<kn>
    s11t-bd.py deploy --project-server=<kn>
    s11t-bd.py change-machine-id --project-server=<kn> --machine-id=<kn>
    s11t-bd.py change-db-65 --project-server=<kn>
    s11t-bd.py change-db-15 --project-server=<kn>
    s11t-bd.py start-tomcat --project-server=<kn>
    s11t-bd.py tomcat-health --project-url=<kn>
    s11t-bd.py online-slb --ecs-id=<kn>
    s11t-bd.py -h | --help
    s11t-bd.py --version

Options:
  -h, --help               display this help and exit.
  --version                output version information and exit.
  --branch=<kn>            repository branch name [default: default].
  --profile=<kn>           maven profile value [default: prod].
  --pom_xml=<kn>           pom-xml file [default: pom.xml].
  --project-server=<kn>    project run machine.
  --ecs-id=<kn>            aliyun ecs id.
  --machine-id=<kn>        spring project machine id.
  --backup-file=<kn>       spring project backup file name.
  --project-url=<kn>       spring project url.
"""

from docopt import docopt
from action import spring


def action_route(docoptArgs):
    spring.initFab()
    if docoptArgs.get("keeplatest"):
        spring.keepLatest(docoptArgs.get("--branch"))
    elif docoptArgs.get("inspect-file"):
        spring.inspectFile()
    elif docoptArgs.get("update-manifest"):
        spring.updateManifest()
    elif docoptArgs.get("maven"):
        spring.maven(docoptArgs.get("--profile"), docoptArgs.get("--pom_xml"))
    elif docoptArgs.get("rsync"):
        spring.rsync()
    elif docoptArgs.get("packaging"):
        spring.packaging()
    elif docoptArgs.get("upload"):
        spring.uploadPKG4SCP(docoptArgs.get("--project-server"))
    elif docoptArgs.get("offline-slb"):
        spring.offlineSLB(docoptArgs.get("--ecs-id"))
    elif docoptArgs.get("stop-tomcat"):
        spring.stopTomcat(docoptArgs.get("--project-server"))
    elif docoptArgs.get("backup"):
        spring.backup(docoptArgs.get("--project-server"))
    elif docoptArgs.get("rollback-pkg"):
        spring.rollbackPKG(
            docoptArgs.get("--backup-file"),
            docoptArgs.get("--project-server"))
    elif docoptArgs.get("deploy"):
        spring.deploy(docoptArgs.get("--project-server"))
    elif docoptArgs.get("change-machine-id"):
        spring.changeMachineID(
            docoptArgs.get("--project-server"), docoptArgs.get("--machine-id"))
    elif docoptArgs.get("change-db-65"):
        spring.changeDB65(docoptArgs.get("--project-server"))
    elif docoptArgs.get("change-db-15"):
        spring.changeDB15(docoptArgs.get("--project-server"))
    elif docoptArgs.get("start-tomcat"):
        spring.startTomcat(docoptArgs.get("--project-server"))
    elif docoptArgs.get("tomcat-health"):
        spring.tomcatHealth(docoptArgs.get("--project-url"))
    elif docoptArgs.get("online-slb"):
        spring.onlineSLB(docoptArgs.get("--ecs-id"))
    spring.closeConnection()


if __name__ == '__main__':
    args = docopt(__doc__, version='S11T-BD CLI 1.0')
    action_route(args)
