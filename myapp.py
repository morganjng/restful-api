#!/usr/bin/env python3

from flask import Flask, jsonify
import requests

app = Flask(__name__)

myheaders = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSNkIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk1NDQ0LCJpYXQiOjE2NjA3NTk0NDR9.bILcGIrPRXPWRrWBZDKRLsZdtTKKqPUpZ4NZZ-U3k5g"
}
myheaders = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRNVIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIxOTk2LCJpYXQiOjE2NjA3ODU5OTZ9.Rw2SpXEMA3YVx1-O1W0ZamKq2BwRnUpOw_fQCMRn0z8"
}
myheaders = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRUEYiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIyMTc4LCJpYXQiOjE2NjA3ODYxNzh9.t4-tjP-pBKe-wdbYLTL9t-h7wAOWsAlu-cGurSkfJiU"
}
url_prefix = "https://api.fitbit.com"


@app.route("/heartrate/last", methods=["GET"])
def last_heartrate():
    json_request = requests.get(
        url_prefix + "/1/user/-/activities/heart/date/today/1d/1min.json",
        headers=myheaders,
    ).json()["activities-heart-intraday"]["dataset"]
    for i in range(len(json_request)):
        if json_request[0 - i - 1]["value"] != 0:
            ret = {"heart-rate": json_request[0 - i - 1]["value"], "time offset": i}
    return jsonify(ret)


@app.route("/steps/last", methods=["GET"])
def last_steps():
    # steps = requests.get(
    #     url_prefix + "/1/user/-/activities/steps/date/today/1d/1min.json",
    #     headers=myheaders,
    # ).json()["activities-steps-intraday"]["dataset"]
    # distance = requests.get(
    #     url_prefix + "/1/user/-/activities/distance/date/today/1d/1min.json",
    #     headers=myheaders,
    # ).json()["activities-distance-intraday"]["dataset"]

    # for i in range(len(steps)):
    #     if steps[0 - i - 1]["value"] != 0:
    #         ret = {
    #             "steps": steps[0 - i - 1]["value"],
    #             "distance": distance[0 - i - 1]["value"],
    #             "time offset": i,
    #         }
    summary = requests.get(
        url_prefix + "/1/user/-/activities/date/today.json", headers=myheaders
    ).json()["summary"]
    distance = 0
    for dict in summary["distances"]:
        if dict["activity"] == "total":
            distance = dict["distance"]
    ret = {
        "steps": summary["steps"],
        "distance": distance,
        "offset": 0,
    }
    return jsonify(ret)


@app.route("/sleep/<date>", methods=["GET"])
def sleep_date(date):
    json_request = requests.get(
        url_prefix + "/1.2/user/-/sleep/date/" + date + ".json", headers=myheaders
    ).json()
    # print(json_request)
    if json_request["sleep"] == []:
        return jsonify({"deep": 0, "light": 0, "rem": 0, "wake": 0})
    ret = {
        "deep": json_request["summary"]["stages"]["deep"],
        "light": json_request["summary"]["stages"]["light"],
        "rem": json_request["summary"]["stages"]["rem"],
        "wake": json_request["summary"]["stages"]["wake"],
    }
    return jsonify(ret)


@app.route("/activity/<date>", methods=["GET"])
def activity_date(date):
    json_request = requests.get(
        url_prefix + "/1/user/-/activities/date/" + date + ".json", headers=myheaders
    ).json()["summary"]
    ret = {
        "very-active": json_request["veryActiveMinutes"],
        "lightly-active": json_request["lightlyActiveMinutes"],
        "sedentary": json_request["sedentaryMinutes"],
    }
    return jsonify(ret)


if __name__ == "__main__":
    app.run(debug=True)
