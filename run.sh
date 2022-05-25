while true
do
	echo "START.SH BEGIN"
	cd "/home/python/web/public/"
	python3 web.py
	echo "START.SH BROKE"
	sleep 3
	pip3 install -r requirements.txt
	echo "START.SH END"
done
