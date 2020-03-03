#!/bin/bash

#set -o errexit
#set -o nounset
#set -o pipefail

# a(app)e(env)v(version)z(zip)p(pkg)
# o(port)c(act)i(inc_tot)u(url)
# -a ZEP-BACKEND-JAVA -e test -v 2020-02-25-002806TO -z javademo-1.0.tar.gz   \
# -p javademo-1.0.jar -o 8080 -c stop -i TOT -u http://192.168.12.103


while getopts "a:e:v:z:p:o:c:i:u:" opt
do 
  case $opt in
    a) APP=$OPTARG ;;
    e) ENV=$OPTARG ;;
    v) VER=$OPTARG ;;
    z) ZIP=$OPTARG ;;
    p) PKG=$OPTARG ;;
    o) PORT=$OPTARG ;;
    c) ACT=$OPTARG ;;
    i) INC_TOT=$OPTARG ;;
    u) URL=$OPTARG ;;
    ?) echo "error" 
       exit 11;;
  esac
done

#echo $APP $ENV $VER $ZIP $PKG $PORT $ACT $INC_TOT $URL


APP_ROOT_HOME="/app"
LOCAL_ROOT_STORE="/var/ops"

APP_HOME=$APP_ROOT_HOME/$APP
LOCAL_STORE=$LOCAL_ROOT_STORE/$APP/$VER
LOCAL_BACKUP=$LOCAL_ROOT_STORE/$APP/BACKUP
LOG="$APP_HOME/$APP.log"

psid=0

pid_of_app(){
  psid=$(pgrep -f "java.*${PKG}" | tr -d " ") 
  #psid=$psid/$$
  if [ -z $psid ]; then
    psid=0
  fi
  echo $psid"@@@@@@@@@@"
}

rm_tmp_file(){
  rm -rf $LOCAL_STORE/$ZIP
  rm -rf $LOCAL_STORE/tmp/*
}

rollback(){
  rm -rf $APP_HOME/*
  cp -arp $LOCAL_BACKUP/* $APP_HOME
  echo "$APP rollback success."
}

backup(){
  if [ ! -d $LOCAL_BACKUP ];then
    mkdir -p $LOCAL_BACKUP
  fi
  rm -rf $LOCAL_BACKUP/*
  cp -arp $APP_HOME/* $LOCAL_BACKUP
  echo "$APP backup success."
}

prepare(){
  if [ ! -d $APP_HOME ];then
    mkdir -p $APP_HOME
  fi
  if [ ! -d $LOCAL_STORE ];then
    mkdir -p $LOCAL_STORE
  fi
  if [ -f $LOCAL_STORE/$ZIP ];then
    echo "$LOCAL_STORE/$ZIP found."
  else
    wget -P $LOCAL_STORE $URL/$APP/$VER/$ZIP
    if [ ! -d $LOCAL_STORE/tmp ];then
      mkdir -p $LOCAL_STORE/tmp
    fi
    tar xzf $LOCAL_STORE/$ZIP -C $LOCAL_STORE/tmp/
  fi
  echo "$APP prepare success."
}

deployall(){
  if [ $INC_TOT == "TOT" ];then
    rm -rf $APP_HOME/*
    cp -rf $LOCAL_STORE/tmp/* $APP_HOME
    rm_tmp_file
    echo "$APP deployall tot success"
  else
    cp -rf $LOCAL_STORE/tmp/* $APP_HOME
    rm_tmp_file
    echo "$APP deployall inc success"
  fi
}

deploypkg(){
  if [ $INC_TOT == "TOT" ];then
    rm -rf $APP_HOME/$PKG
    cp -rf $LOCAL_STORE/tmp/$PKG $APP_HOME
    rm_tmp_file
    echo "$APP deploypkg tot success"
  else
    cp -rf $LOCAL_STORE/tmp/$PKG $APP_HOME
    rm_tmp_file
    echo "$APP deploypkg inc success"
  fi
}

deploycfg(){
  if [ $INC_TOT == "TOT" ];then
    rm -rf $APP_HOME/config*
    cp -rf $LOCAL_STORE/tmp/config* $APP_HOME
    rm_tmp_file
    echo "$APP deploycfg tot success"
  else
    cp -rf $LOCAL_STORE/tmp/config* $APP_HOME
    rm_tmp_file
    echo "$APP deploycfg inc success"
  fi
}

startserver(){
  pid_of_app
  if [ $psid -ne 0 ];then
    echo "$APP already started, error."
    exit 2
  fi
  # 这里必须要切换到$APP_HOME下，再进行服务启动，否则无法找到config目录
  cd $APP_HOME
  nohup java -jar $APP_HOME/$PKG --server.port=$PORT --spring.profiles.active=$ENV >> $LOG 2>&1 &
  #echo "nohup java -jar $APP_HOME/$PKG --server.port=$PORT --spring.profiles.active=$ENV >> $LOG 2>&1 &"
  sleep 3
  pid_of_app
  if [ $psid -ne 0 ];then
    echo "$APP start success."
  else
    echo "$APP start fail."
    exit 3
  fi
}


stopserver(){
  pid_of_app
  if [ $psid -ne 0 ];then
    kill -9 $psid
    if [ $? -eq 0 ];then
      echo "$APP stop success."
    else
      echo "$APP stop fail."
      exit 4
    fi
  else
    echo "$APP has stoped."
  fi
}

check(){
  echo "$APP check success"
}

case "$ACT" in
	backup) backup;;
	prepare) prepare;;
	deployall) deployall;;
	deploypkg) deploypkg;;
	deploycfg) deploycfg;;
	rollback) rollback;;
        start) startserver;;
        stop) stopserver;;
	check) check;;
    *)
        echo "Usage: $0 {only 9 kinds of action can be choose: "
        echo "backup, prepare, deploy[all|pkg|cfg], rollback, start, stop, check}"
        exit 1;;
esac
  
