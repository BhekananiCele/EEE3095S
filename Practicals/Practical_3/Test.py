import datetime
import time
import decimal
currentDT = datetime.datetime.now()
time.sleep(2);
endDT = datetime.datetime.now()



print(decimal.Decimal((endDT-currentDT).seconds))