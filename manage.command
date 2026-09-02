#!/bin/bash
# Меню управления проектом "Сайт".
# Двойной клик по этому файлу в Finder откроет Терминал с этим меню.

cd "$(dirname "$0")"

PORT=8080
PIDFILE=".server.pid"
LOGFILE="server.log"

start_server() {
  if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "Сервер уже запущен (PID $(cat "$PIDFILE")) — http://localhost:$PORT"
  else
    nohup python3 -m http.server "$PORT" > "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    sleep 1
    echo "Сервер запущен: http://localhost:$PORT"
  fi
}

stop_server() {
  if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    kill "$(cat "$PIDFILE")"
    rm -f "$PIDFILE"
    echo "Сервер остановлен."
  else
    echo "Сервер и так не запущен."
    rm -f "$PIDFILE"
  fi
}

restart_server() {
  stop_server
  sleep 1
  start_server
}

push_github() {
  git add -A
  if git diff --cached --quiet; then
    echo "Нет изменений для отправки."
    return
  fi
  read -r -p "Сообщение коммита (что изменилось): " msg
  if [ -z "$msg" ]; then
    msg="Обновление сайта"
  fi
  git commit -m "$msg"
  git push
}

pull_github() {
  git pull
}

while true; do
  echo ""
  echo "===== Управление проектом «Сайт» ====="
  echo "1) Запустить проект локально"
  echo "2) Перезапустить проект локально"
  echo "3) Завершить проект локально"
  echo "4) Запушить в GitHub"
  echo "5) Стянуть последнюю версию из GitHub"
  echo "0) Выход"
  echo "========================================"
  read -r -p "Выбери пункт (0-5): " choice
  case "$choice" in
    1) start_server ;;
    2) restart_server ;;
    3) stop_server ;;
    4) push_github ;;
    5) pull_github ;;
    0) echo "Пока!"; exit 0 ;;
    *) echo "Такого пункта нет, попробуй ещё раз." ;;
  esac
done
