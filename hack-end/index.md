---
layout: page
title: H4CK-3ND
permalink: /hack-end/
---

An interactive back-end workshop created for [SwampHacks 2019](https://2019.swamphacks.com).

Google Slides Presentation: [link](https://docs.google.com/presentation/d/1ULkphbBF57rHCoGMabkZhV81xK_VMx9fTCVAD-4ktBc/edit)

## ABOUT

The purpose of this workshop is to help participants learn how to use Flask and Python in an interactive manner. Less slides, more code.

Since this is a back-end workshop, all front-end material (HTML, CSS) can be left untouched.

## DO IT YOURSELF

1. Make sure you have a working Python environment with `pip` installed.
1. Download and unzip [flask-workshop.zip](/back-end/flask-workshop.zip).
1. `cd` into the `flask-workshop` directory containing `hack-end.py`.
1. `pip install flask` and `pip install pandas` (in a virtualenv if you wish).
1. Set appropriate environment variables (`FLASK-APP=hack-end.py`, `FLASK_DEBUG=1`)
1. `flask run` (set the `-p` flag if the default port `5000` is already used).
1. Take a look at the running app on `localhost:` in your browser. Make sure you see "Hello world!".
1. Download [0-start.py](/hack-end/0-start.py) and copy/replace the contents into `hack-end.py`.
1. Take a look at the running app again. You'll see some broken links. Fix them.
1. Download the next file once you've completed each segment. Have fun!

## SOLUTIONS/NEXT STEPS

I was hoping to do this in the style of a [CTF](https://ctftime.org/ctf-wtf/). Then I realized it would be very difficult to serve the answer tokens individually since the participants have full access to the back-end files. I ended up giving these links out iteratively to the entire group.

1. [0-start.py](/hack-end/0-start.py)
2. [1-www.py](/hack-end/1-www.py)
3. [2-anaconda.py](/hack-end/2-anaconda.py)
4. [3-matlab.py](/hack-end/3-matlab.py)
5. [4-python.py](/hack-end/4-python.py)
6. [5-hacked.py](/hack-end/5-hacked.py) (all)

## ACKNOWLEDGEMENTS

- Data source: [Kaggle: S&P 500 stock data](https://www.kaggle.com/camnugent/sandp500/version/4#individual_stocks_5yr.zip)
- Hack4Impact's Flask Workshop: [GitHub](https://github.com/hack4impact/flask-workshop)
- SwampHacks 2019 sponsors and organizers!
