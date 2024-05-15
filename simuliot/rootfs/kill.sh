echo "Stopping Simulator..."
kill -9 $(cat ./simuliot_backend.pid)
kill -9 $(cat ./simuliot_frontend.pid)
rm ./simuliot_backend.pid
rm ./simuliot_frontend.pid