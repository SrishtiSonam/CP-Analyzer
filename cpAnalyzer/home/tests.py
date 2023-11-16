from django.test import TestCase
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Create your tests here.
def codeforces_problems_solved(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
    data = response.json()
    if data["status"] != "OK" or not data["result"]:
        raise Exception(f"Data not found for {handle}")
    current_date = datetime.now()
    one_month_ago = current_date - timedelta(days=30)
    problems_solved = 0
    for submission in data["result"]:
        submission_time = datetime.fromtimestamp(submission["creationTimeSeconds"])
        if one_month_ago <= submission_time <= current_date:
            if submission["verdict"] == "OK": 
                problems_solved += 1
    return problems_solved

def codeforces_rating(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
    data = response.json()
    if data["status"] != "OK" or not data["result"]:
        raise Exception(f"Contest rating not found for {handle}")
    rating = data["result"][0].get("rating", "Not rated")
    return rating


def codechef_rating(username):
    req = requests.get(f"https://www.codechef.com/users/{username}")
    soup = BeautifulSoup(req.content, "html.parser")
    rating_element = soup.find("div", class_="rating-number")
    if rating_element:
        rating = rating_element.text.strip()
        return rating

def codechef_problems_solved(username):
    req = requests.get(f"https://www.codechef.com/users/{username}")
    soup = BeautifulSoup(req.content, "html.parser")
    total_problem_solved = soup.find("h5")
    if total_problem_solved:
        total_problem = total_problem_solved.text.strip()
        if (total_problem[-4]=='('):
            total = total_problem[-3:-1]
        elif (total_problem[-5]=='('):
            total = total_problem[-4:-1]
        else:
            total = total_problem[-5:-1]
        return total


def leetcode_ranking(userid):
    req = requests.get(f"https://leetcode.com/{userid}")
    soup = BeautifulSoup(req.content, "html.parser")
    ranking_element = soup.find("span", class_="ttext-label-1")
    if ranking_element:
        ranking = ranking_element.text.strip()
        return ranking

def leetcode_total_problems_solved(userid):
    req = requests.get(f"https://leetcode.com/{userid}")
    soup = BeautifulSoup(req.content, "html.parser")
    solved_element = soup.find("div", class_="text-[24px] font-medium text-label-1 dark:text-dark-label-1")
    if solved_element:
        problems_solved = solved_element.text.strip()
        return problems_solved


def total_problems_solved(handle,username,userid):
    try:
        codeforces=codeforces_problems_solved(handle)
        codechef=codechef_problems_solved(username)
        leetcode=leetcode_total_problems_solved(userid)
        total= int(codeforces)+int(codechef)+int(leetcode)
        return total
    except:
        return 0

