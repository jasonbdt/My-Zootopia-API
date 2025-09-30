# Zootopia with API

The Zootopia project is part of my learning journey to become
an expert AI Engineer. An earlier version of Zootopia
introduced the basics of file operation (reading/writing).

To further improve my Python skill set, the goal of this
repository was to implement an HTTP RESTAPI (APINinja) to
gather informations about animals instead of reading the
data from a `.json` file.

![API Playground](docs/api-illustration.jpg)

## Table of Contents

* [Technologies](#technologies)
* [Setup](#setup)
* [Sources](#sources)

## Technologies
Project is created with:
- Python: 3.13
- requests:  2.32
- python-dotenv: 1.1

## Setup
To run this project, install it locally by cloning the repository.
Make sure that you have an account at [APINinjas](https://api-ninjas.com/),
as you'll need your own private API Key.

1. Create an account at [APINinjas](https://api-ninjas.com/)
2. Rename `.env.example` to `.env`
3. Insert your API Key
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   python animals_web_generator.py
   ```

## Sources
This app has been developed by Jason Bladt and
is part of [Masterschool's AI Engineering Course](https://de.masterschool.com/domains/ai-engineering-14-months/)