#!/bin/bash

main() {
    project_folder="$1"
    java_home="$2"
    package_name="$3"
    arg_name="$4"
    log_name="$5"
    cd ${project_folder}
    /usr/bin/nohup ${java_home}/bin/java -jar ${package_name} ${arg_name} > ./${log_name} 2>&1 &
}

main $@
