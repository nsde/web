while true
do
	echo "START.SH BEGIN"
	source web/bin/activate
	cd "/home/python/web/public/"
	date +"%s" > logs/last_start.txt
	/stuff/./pypy3.9-v7.3.9-linux64/bin/pypy web.py > logs/web.txt
	echo "START.SH BROKE"
	sleep 3
	/stuff/./pypy3.9-v7.3.9-linux64/bin/pypy -m pip install -r ./requirements.txt > logs/pip.txt
	echo "START.SH END"
done
