#!/home/ansible/.venv/bin/python
# - * - coding: utf-8 - * -
"""RK-Project Build-Deploy CLI.

Usage:[]
    rk-bd.py keeplatest [--branch=<kn>]
    rk-bd.py maven [--profile=<kn>] [--pom_xml=<kn>]
    rk-bd.py rsync
    rk-bd.py upload --project-server=<kn>
    rk-bd.py stop-rk --project-server=<kn>
    rk-bd.py backup --project-server=<kn>
    rk-bd.py rollback-pkg --backup-file=<kn> --project-server=<kn>
    rk-bd.py deploy --project-server=<kn>
    rk-bd.py start-rk --project-server=<kn>
    rk-bd.py tomcat-health --project-url=<kn>
    rk-bd.py -h | --help
    rk-bd.py --version

Options:
  -h, --help               display this help and exit.
  --version                output version information and exit.
  --branch=<kn>            repository branch name [default: default].
  --profile=<kn>           maven profile value [default: prod].
  --pom_xml=<kn>           pom-xml file [default: pom.xml].
  --project-server=<kn>    project run machine.
  --backup-file=<kn>       riskcontrol project backup file name.
  --project-url=<kn>       riskcontrol project url.
"""

from docopt import docopt
from action import rk


def action_route(docoptArgs):
    rk.initFab()
    if docoptArgs.get("keeplatest"):
        rk.keepLatest(docoptArgs.get("--branch"))
    elif docoptArgs.get("maven"):
        rk.maven(docoptArgs.get("--profile"), docoptArgs.get("--pom_xml"))
    elif docoptArgs.get("rsync"):
        rk.rsync()
    elif docoptArgs.get("upload"):
        rk.uploadPKG4SCP(docoptArgs.get("--project-server"))
    elif docoptArgs.get("stop-rk"):
        rk.stopRiskControl(docoptArgs.get("--project-server"))
    elif docoptArgs.get("backup"):
        rk.backup(docoptArgs.get("--project-server"))
    elif docoptArgs.get("rollback-pkg"):
        rk.rollbackPKG(
            docoptArgs.get("--backup-file"),
            docoptArgs.get("--project-server"))
    elif docoptArgs.get("deploy"):
        rk.deploy(docoptArgs.get("--project-server"))
    elif docoptArgs.get("start-rk"):
        rk.startRiskControl(docoptArgs.get("--project-server"))
    elif docoptArgs.get("tomcat-health"):
        rk.tomcatHealth(docoptArgs.get("--project-url"))
    rk.closeConnection()


if __name__ == '__main__':
    args = docopt(__doc__, version='RK-BD CLI 1.0')
    action_route(args)
