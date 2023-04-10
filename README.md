<p align="center">
  <img src="website/static/styles/logo.png" width="200" height="200">
</p>

<p align="center">
  <a href="https://img.shields.io/github/license/Isu21842/unique-turker-2?color=yellow">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-<COLOR>.svg">
  </a>
  <a href="https://pypi.org/project/Flask/">
    <img alt="PyPI - Flask" src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
  </a>
</p>

# Unique Turker 2: Python Application for Researchers to Manage Worker Access to HITs on Amazon Mechanical Turk

Full-stack Flask app with a built-in database that can be used by Mechanical Turk requesters to prevent duplicate HIT access from Mechanical Turk workers.

## 🔍Purpose

Unique Turker was a service created by Myle Ott that was designed for researchers and developers who use Amazon's Mechanical Turk (MTurk) platform. In short, it allowed requesters to avoid the 40% MTurk fee that comes when recruiting more than 9 workers in a single batch. Although one could deploy a HIT with multiple batches of <9 workers, there is always the possibility that a worker could access the same HIT from multiple batches. To combat this, requesters could go on the Unique Turker site and obtain a snippet of code that they could include in their HIT HTML source code. This snippet of code communicated with the Unique Turker database to ensure that each worker could complete a particular HIT only once, thus preventing duplicate submissions. For academic researchers, obtaining unique, non-repeated responses is an especially desirable quality when collecting data as multiple data submissions from the same participant is almost always of no use. Therefore, Unique Turker was valuable for allowing researchers to not get duplicated responses while also saving money from avoiding the 40% fee.\* Unfortunately, however, Unique Turker went down in 2022 and seems to no longer be maintained.

`Unique Turker 2` is a software that I created which does exactly what Unique Turker did. Instead of offering and maintaining a database for others to use, I've provided the source code for anyone to set up their own living and breathing server that can interact with their MTurk HITs to record worker data and, importantly, prevent multiple workers from accessing the same HIT. It's packaged as a `Flask` application that users can readily download and host somewhere online (e.g., Heroku, Docker). Once deployed, users can access their web app whenever they'd like to deploy a new HIT, generate a unique id, and receive the custom HIT HTML code that communicates with their web app. As workers enter your HIT, worker IDs are stored in a SQLite database which the app uses to manage access to your HIT.

\*Note that there was a way for some workers to bypass Unique Turker in the past and so I'm similarly not expecting for perfect prevention of duplicate workers. Indeed, I've run a few HITs to see how effective the app is and, as expected, very, very few workers had repeated responses (e.g., 2 out of 500 workers in my first run).

## ⬆️Deploying The App

Steps for setting up and deploying the app:

1. Download this repository.

2. Upload the repository source code on any platform that can host web applications (e.g., Heroku, PythonAnywhere, Docker).

3. Make sure to change `https://LINK-TO-YOUR-DATABASE.COM` in output.html to be the URL to your actual web app.

4. Deploy the web app online.

## 👨 💻How To Use

There are two pages in this web app: the home page and the HTML output page.

### _Home Page_

Once your app is running online, you will see two fields: a field where you can enter a unique identifier and another for you to upload the survey link that your workers will access (e.g., the Qualtrics survey that workers will take).

The app automatically creates a randomly-generated string of letters and numbers that you can use for the unique ID. This unique ID is essentially the "key" for your particular HIT. This unique ID can be anything though it must be at least 12 characters long.

Once you enter the unique ID and survey link, click "Get Script" to enter the HTML output page.

### _HTML Output Page_

The HTML output page contains the HIT HTML source code that you can upload to your MTurk HIT. The HIT code that is provided is always the same but there are two things that change everytime you submit the home page: the unique ID as well as the qualtrics survey link.

The default HIT code provided is a slight extension of the basic HIT HTML source code that MTurk provides. The only thing you need to do is replace `https://LINK-TO-YOUR-DATABASE.COM` with the actual URL to your site. You also need to make sure that your site uses a secure HTTPS port (i.e., starts with "https"). As a bonus for Qualtrics users, I've already set up the provided source code to append the important embedded data variables when recruiting participants from MTurk (i.e., the MID and AID variables).

Of course, you are free to alter the HIT HTML source code any way you'd like but make sure that it contains the snippet of code that grabs the MTurk worker's worker ID and checks that against your own database.

### _Final but most important step_

Lastly, once you copy the HIT HTML source code, upload it to your MTurk HIT. If using the template provided, you will likely see that it says "URL not shown because there is an error with Javascript on your computer. To perform this HIT, you must have Javascript and cookies enabled on your browser." somewhere when previewing the HIT, which is completely fine and just means that MTurk recognizes the JavaScript code in the HIT HTML source code.

## 📊Accessing the Database

Once you deploy your app and submit your first unique ID to be monitored by the web app, you will now see that the `database.db` file in the `instance` folder will be updated. To access your database, you can use any program that can read in SQL databases (e.g., SQLite packages in R or Python). Everytime you submit a unique id to the app, this automatically gets updated to the database. Moreover, everytime a worker accesses your HIT, their worker ID gets uploaded to the database.

Regarding the exact structure of the database, there are two tables: Uniqueid and Worker. These tables are related to each other through a one-to-many relationship.

The Uniqueid table stores unique identifiers that correspond to your HITs on Mechanical Turk. Each entry in this table has a primary key, `id`, and a unique identifier, `identifier`.

The Worker table stores worker IDs associated with each unique identifier. Each entry in the Worker table has a primary key, `id`, a worker ID, `workerid`, and a foreign key, `unique_id`. The foreign key, `unique_id`, refers to the id column in the Uniqueid table, establishing the relationship between the two tables.

In this structure, one unique identifier in the Uniqueid table can be associated with multiple worker IDs in the Worker table, creating a one-to-many relationship. This design allows the app to efficiently track and prevent duplicate HIT access for each unique identifier by checking the existence of a worker ID within the associated worker IDs.

## ✨Demo✨

<img src="demo.gif" width="700" height="400" alt="Demo GIF">
