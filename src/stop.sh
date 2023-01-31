for KILLPID in `ps ax | grep 'ocean.py' | awk '{print $1;}'`; do
kill -9 $KILLPID;
done
