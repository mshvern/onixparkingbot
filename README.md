# onixparkingbot

**If you know the IP**

* Edit const_empty.py, fill in all the needed values and rename it to const.py
* Create a docker image and run it

**If you don't know the IP**
* Edit const_empty.py, fill in all the needed values and rename it to const.py
* Create a docker image and run it
* Run`docker ps -a`
* Get your container id
* Get your container IP by running `docker inspect <container_id> | grep "IPAddress"`
* Enter const.py and replace bot url with your container IP
* Run `python config.py`

**If you don't know the IP and want to run it through ngrok**
* Edit const_empty.py, fill in all the needed values and rename it to const.py
* Create a docker image and run it
* Run`docker ps -a`
* Get your container id
* Get your container IP by running `docker inspect <container_id> | grep "IPAddress"`
* Forward the IP with ngrok `./ngrok http <container_ip>:8000`
* Enter const.py and replace bot url with your ngrok IP
* Run `python config.py`
