![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)

<h1>
<p align="center">
<img align="center" src="https://lohxt1.github.io/_assets/pyAsyncFlow.svg" alt="pyAsyncFlow" width="150" height="150" />pyAsyncFlow
</h1>
  <p align="center">
    [Flask - Celery - Redis - sqlite] starter template for performing async tasks
    <br />
    </p>
</p>

#### About The Project
pyAsyncFlow is a Python Flask app that enables users to perform async tasks seamlessly. The app allows users to execute time-consuming tasks in the background without affecting the performance of the main application. It's designed to handle tasks that run concurrently, making it possible to perform multiple tasks at once without slowing down the system.

#### Running the code `locally`

> 💡 Before proceeding make sure you have [Redis](https://redis.io/docs/getting-started/) installed in your system

To run the code locally, open _Terminal_ in your `projects` folder and take the steps:

```bash
# STEP 1: Get sources from GitHub
$ git clone https://github.com/aregtech/areg-sdk.git
$ cd pyAsyncFlow

# STEP 2: Install the requirements
$ pip3 install -r requirements.txt

# STEP 3: Running the app

# You'l need to exceute 3 different commands in sequence, (preferably in 3 seperate terminal tabs)
# 1.
$ redis-server # Make sure you have redis installed on your system before this step.

# 2.
$ python3 -m celery -A tasks.celery worker --concurrency=3 --loglevel=info --without-mingle

# 3.
$ python3 main.py
```

#### Deploying the app

I personally prefer [Railway](http://railway.app).

STEPS:

After importing the project into the Railway dashboard.

1. Update the `Start` command field. More details [here](https://docs.railway.app/deploy/deployments#start-command)

   Navigate to _Settings_ tab → _Deploy_ subsection → _Start Command_, to make the changes.

   ```bash
   redis-server & celery -A tasks.celery worker --concurrency=3 --loglevel=info --without-mingle & python3 main.py
   ```

2. Add the `NIXPACKS_PKGS` environment variable.

   Navigate to _Variables_ tab → _New Variable_ button → Add the variable name and value.

   ```bash
   NIXPACKS_PKGS : python39Packages.celery, ffmpeg, python39Packages.redis, redis
   ```
