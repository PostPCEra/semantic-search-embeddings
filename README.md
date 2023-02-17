![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)

<h1>
<p align="center">
<img align="center" src="https://lohxt1.github.io/_assets/pyAsyncFlow.svg" alt="pyAsyncFlow" width="150" height="150" />semantic-search-embeds
</h1>
  <p align="center">
    A Flask app for performing semantic search using tweet embeddings.
    <br />
    </p>
</p>

#### About The Project

An app for performing semantic search using tweet embeddings. When paired with UI, users will be able to enter search queries, and the application will return relevant tweets based on their semantic similarity to the query.

#### Running the code `locally`

To run the code locally, open _Terminal_ in your `projects` folder and take the steps:

```bash
# STEP 1: Get sources from GitHub
$ git clone https://github.com/lohxt1/semantic-search-embeddings.git
$ cd semantic-search-embeddings

# STEP 2: Install the requirements
$ pip3 install -r requirements.txt

# STEP 3: Running the app
$ python3 main.py
```

#### Deploying the app

I personally prefer [Railway](http://railway.app).

STEPS:

After importing the project into the Railway dashboard.

1. Update the `Start` command field. More details [here](https://docs.railway.app/deploy/deployments#start-command)

   Navigate to _Settings_ tab → _Deploy_ subsection → _Start Command_, to make the changes.

   ```bash
   python3 main.py
   ```
