import boto3
import json
import datetime
import holidays
import pytz
import os
# setuptools==51.1.0
# Global Variables for our Lambda
client = boto3.client("lambda")
# arn_name = os.environ['arn'] 
weird_holidays = ['Labor Day', 'Christmas Day'] 
# We close at 1pm when these holidays fall tues-fri

# TODO: Pull ARN from environment variable since it seems it should be secured?

# Lambda 1
# If its a closed holiday, do not run
# at 1, check if its a 1 holiday. If it is, trigger lambda 2
# run again at 4. if its not a 1 day nor a holiday, execute lambda 2
def check_weird_holiday(today, us_holidays):
    curr_year = datetime.datetime.now().year
    check_christmas_labor = today + datetime.timedelta(days=1) 

    for day in holidays.US(years = curr_year).items(): # [0] date 1/1/year [1] text name of holiday
        if check_christmas_labor == day[0] and day[1] in weird_holidays:
            # If we're a Tuesday to Friday and tomorrow is a 'weird_holiday', we close at 1 today
            if check_christmas_labor.weekday() <= 4 and check_christmas_labor.weekday() >= 1:
                return True
    return False

def invoke_sendtweet_lambda(today, closes_at_one, time_ran):
    inputParams = {
        "Today" : today.strftime("%m/%d/%Y"),
        "closes_at_one" : closes_at_one,
        "Time Ran" : time_ran
    }
    invoke_function = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:875660052076:function:bezos-net-worth', # convert this to env var?
        InvocationType = 'Event',
        Payload = json.dumps(inputParams)
    )
    return invoke_function
    
def main():
    output = ""
    today = datetime.date.today() # - datetime.timedelta(days=25)
    us_holidays = holidays.US()
    # print(today in us_holidays and 'New Yearr\'s Day' in us_holidays[1]) # works for td 25
    # Need to handle when holidays are observed for markets vs when they actually are
    # for ptr in holidays.US(years = 2021).items():
    #     print(ptr)

    # Handles EST vs EDT for us by using US/Eastern.  We only care about the hour.
    eastern = pytz.timezone('US/Eastern')
    fmt = '%H'
    curr_time = datetime.datetime.now(eastern).strftime(fmt)
    print (curr_time)
    if today in us_holidays:
        output = 'Today is a holiday. Market is closed.'
        # If market is closed, we just want to print an output and not
        # invoke our other lambda.
    else: 
        # 18 and 21 are daylight savings numbers, how to handle this?
        closes_at_one = check_weird_holiday(today, us_holidays)

        if closes_at_one == True and curr_time == '13': # or curr_time == '17' ?
            # run lambda at 1
            print('Running at 1pm')
            time_ran = 'Running at 1pm.'
            output = invoke_sendtweet_lambda(today, closes_at_one, time_ran)
        # elif closes_at_one == False and (curr_time == '21' or curr_time == '20'):
        elif closes_at_one == False and curr_time == '16':
        # elif closes_at_one == False:
            # run lambda at 4
            print('Running at 4pm')
            time_ran = 'Running at 4pm.'
            output = invoke_sendtweet_lambda(today, closes_at_one, time_ran)
        else:
            output = f'Error running tweet. {curr_time}'

    print(output)

# Handler
def lambda_handler(event, context):
    main()

# For Local dev
# if __name__ == "__main__":
#     main()
