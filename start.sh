while true
do
	echo "START.SH BEGIN"
	cd "/home/python/web/public"
	screen -S web python3 web.py
	echo "START.SH BROKE"
	sleep 3
	pip install -r requirements.txt
	echo "START.SH END"
done