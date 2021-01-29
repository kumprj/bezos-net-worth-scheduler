import boto3
import json
import datetime
import holidays
import pytz

client = boto3.client("lambda")
weird_holidays = ['Labor Day', 'Christmas Day'] # We close at 1pm when these holidays fall tues-fri
# Lambda 1
# If its a closed holiday, do not run
# at 1, check if its a 1 holiday. If it is, trigger lambda 2
# run again at 4. if its not a 1 day nor a holiday, execute lambda 2
def check_weird_holiday(today, us_holidays):
    curr_year = datetime.datetime.now().year
    check_christmas_labor = today + datetime.timedelta(days=1) 

    for day in holidays.US(years = curr_year).items(): # [0] date 1/1/year [1] text name of holiday
        if check_christmas_labor == day[0] and day[1] in weird_holidays:
            # If we're a Tuesday to Friday and tomorrow is a weird_holiday, we close at 1 today
            if check_christmas_labor.weekday() <= 4 and check_christmas_labor.weekday() >= 1:
                return True
    return False

def main():
    output = ""
    today = datetime.date.today() # - datetime.timedelta(days=25)
    us_holidays = holidays.US()
    # print(today in us_holidays and 'New Yearr\'s Day' in us_holidays[1]) # works for td 25
    eastern = pytz.timezone('US/Eastern')
    fmt = '%H'
    curr_time = datetime.datetime.now(eastern).strftime(fmt)
    # Need to handle when holidays are observed for markets vs when they actually are
    # for ptr in holidays.US(years = 2021).items():
    #     print(ptr)
    
    if today in us_holidays:
        output = f'Today is holiday.'
    else: 
        # 18 and 21 are daylight savings numbers, how to handle this?
        closes_at_one = check_weird_holiday(today, us_holidays)

        if closes_at_one == True and curr_time == '18':
            # run lambda at 1
            output = invoke_lambda(today, closes_at_one)
        elif closes_at_one == False and curr_time == '21':
            # run lambda at 4
            output = invoke_lambda(today, closes_at_one)
        else:
            output = 'Error running tweet.'

    print(output)

def invoke_lambda(today, closes_at_one):
    inputParams = {
        "Today" : today,
        "closes_at_one" : closes_at_one
    }
    invoke_function = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:875660052076:function:bezos-net-worth',
        InvocationType = 'Event',
        Payload = json.dumps(inputParams)
    )
    return invoke_function

# Handler
# def lambda_handler(event, context):
#     main()

# For Local dev
if __name__ == "__main__":
    main()
