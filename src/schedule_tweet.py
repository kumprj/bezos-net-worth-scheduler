import boto3
import json
import datetime
import holidays

client = boto3.client("lambda")
weird_holidays = ['Labor Day', 'Christmas Day'] # We close at 1pm when these holidays fall tues-fri
# Lambda 1
# If its a closed holiday, do not run
# at 1:30, check if its a 1:30 holiday. If it is, trigger lambda 2
# run again at 4. if its not a 1:30 day nor a holiday, execute lambda 2
def check_weird_holiday(today, us_holidays):

    check_christmas_labor = today + datetime.timedelta(days=1) 
    for day in holidays.US(years = 2021).items(): # [0] date [1] text name of holiday
        if check_christmas_labor == day[0] and day[1] in weird_holidays:
            if check_christmas_labor.weekday() <= 4 and check_christmas_labor.weekday() >= 1:
                return True 
    return False

def main():
    today = datetime.date.today() # - datetime.timedelta(days=25)
    us_holidays = holidays.US()
    curr_year = datetime.datetime.now().year
    # print(today in us_holidays and 'New Yearr\'s Day' in us_holidays[1]) # works for td 25

    # closes_at_one = check_weird_holiday(today, us_holidays) # Revisit this
    
    # Need to handle when holidays are observed for markets vs when they actually are
    for ptr in holidays.US(years = 2021).items():
        print(ptr)
    
    if today in us_holidays:
        # return
        pass
    else: 
        # run lambda
        pass

    inputParams = {
        "ProductName"   : "iPhone SE",
        "Quantity"      : 2,
        "UnitPrice"     : 499
    }
    # invoke_function = client.invoke(
    #     FunctionName = 'arn:aws:lambda:us-east-1:875660052076:function:bezos-net-worth',
    #     InvocationType = 'Event',
    #     Payload = json.dumps(inputParams)
    # )
    pass


# Handler
# def lambda_handler(event, context):
#     main()

# For Local dev
if __name__ == "__main__":
    main()
