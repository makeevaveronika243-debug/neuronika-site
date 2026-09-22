#!/bin/bash
# Меню управления проектом "Сайт".
# Двойной клик по этому файлу в Finder откроет Терминал с этим меню.

cd "$(dirname "$0")"

PORT=8080
PIDFILE=".server.pid"
LOGFILE="server.log"

port_pids() {
  lsof -ti :"$PORT" 2>/dev/null || true
}

free_port() {
  local pids
  pids=$(port_pids)
  if [ -n "$pids" ]; then
    echo "Останавливаю процесс(ы) на порту $PORT: $pids"
    kill $pids 2>/dev/null || true
    sleep 1
  fi
  rm -f "$PIDFILE"
}

server_running() {
  [ -n "$(port_pids)" ]
}

start_server() {
  if server_running; then
    local pid
    pid=$(port_pids | head -1)
    echo "$pid" > "$PIDFILE"
    echo "Сервер уже работает — http://localhost:$PORT (PID $pid)"
    echo "Открывайте сайт только по этой ссылке (не через файл index.html)."
    return
  fi

  free_port
  nohup python3 server.py >> "$LOGFILE" 2>&1 &
  echo $! > "$PIDFILE"
  sleep 1

  if server_running; then
    echo "Сервер запущен: http://localhost:$PORT"
    echo "Открывайте сайт только по этой ссылке (не через файл index.html)."
  else
    echo "Не удалось запустить сервер. Последние строки $LOGFILE:"
    tail -8 "$LOGFILE" 2>/dev/null || true
    rm -f "$PIDFILE"
  fi
}

stop_server() {
  if server_running; then
    free_port
    echo "Сервер остановлен."
  else
    rm -f "$PIDFILE"
    echo "На порту $PORT ничего не запущено."
  fi
}

restart_server() {
  echo "Перезапуск…"
  free_port
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
