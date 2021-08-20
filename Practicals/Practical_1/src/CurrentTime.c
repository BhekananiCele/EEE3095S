#include "CurrentTime.h"
#include <time.h>

int HH,MM,SS;

void getCurrentTime(void){
  time_t rawtime;
  struct tm * timeinfo;
  time ( &rawtime );
  timeinfo = localtime ( &rawtime );

  HH = timeinfo ->tm_hour;
  MM = timeinfo ->tm_min;
  SS = timeinfo ->tm_sec;
}

int getHours(void){
    getCurrentTime();
    return HH;
}

int getMins(void){
    return MM;
}

int getSecs(void){
    return SS;
}

int addHours(int hours){
	time_t rawtime;
	struct tm * timeinfo;
	time ( &rawtime );
	timeinfo = localtime ( &rawtime );
	
	printf("Hr: Before > %d",timeinfo ->tm_min);
	timeinfo ->tm_hour +=hours; 
	printf("Hr: After > %d",timeinfo ->tm_min);
}

int addMinutes(int minutes){
	time_t rawtime;
	struct tm * timeinfo;
	time ( &rawtime );
	timeinfo = localtime ( &rawtime );
	
	printf("Min: Before > %d",timeinfo ->tm_min);
	timeinfo ->tm_min +=minutes; 
	printf("Min: After > %d",timeinfo ->tm_min);
}