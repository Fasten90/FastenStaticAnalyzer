/* Workaround for pycparser */
#ifndef _Bool
typedef int _Bool;
#endif

#define _Atomic(_arg) _arg

#include <stdio.h>
//#include "testheader.h"

int main(void)
{
	int var = 5;
	
	/* In first test, pycparser will die on va_args at printf() */
	printf("Print variable value: %d\r\n", var);
	
	int var2 = 2;
	
	int var3 = var / var2;
	
	return var3;	
}
