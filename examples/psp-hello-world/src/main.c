/**
* @file   main.c
* @author Luis Piñuel
* @date   23.07.2020
* @brief  main C file of hello-world example using WD Processor Support Package (PSP)
*/

/**
* include files
*/
#if defined(D_NEXYS_A7)
   #include "bsp_printf.h"
   #include "bsp_mem_map.h"
   #include "bsp_version.h"
#else
   PRE_COMPILED_MSG("no platform was defined")
#endif
#include "psp_api.h"

/**
* definitions
*/

/**
* macros
*/

/**
* types
*/

/**
* local prototypes
*/

/**
* external prototypes
*/

/**
* global variables
*/


//////////////////////////////////////////////////////////////////////
int main(void)
{
   /* Initialize Uart */
   uartInit();

   /* Print "hello world" message on the serial output (be carrefoul not all the printf formats are supported) */
   printfNexys("hello world");

   /* For OSless demos getting here means the demo has completed successfully */
   for( ;; );
}
