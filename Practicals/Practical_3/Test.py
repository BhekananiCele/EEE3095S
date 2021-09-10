import datetime
import time
import decimal
currentDT = datetime.datetime.now()
time.sleep(1.5);
endDT = datetime.datetime.now()



print(decimal.Decimal((endDT-currentDT).seconds))