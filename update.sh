set -eux

git pull
killall uwsgi
tmux new -d uwsgi --ini /etc/uwsgi/apps-available/jdrpoly
