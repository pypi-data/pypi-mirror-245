#include <assert.h>
#include <errno.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "log.h"


int logging_level = 0;


int log_setup()
{
    return 0;
}

void log_real_(pid_t tid, int lvl, const char *format, ...)
{
    va_list args;
    char datestr[13]; /* HH:MM:SS.mmm */
    static char *buffer = NULL;
    static size_t bufsize = 4096;
    size_t length;

    if(lvl < logging_level)
        return;

    if(buffer == NULL)
        buffer = malloc(bufsize);
    {
        struct timeval tv;
        gettimeofday(&tv, NULL);
        strftime(datestr, 13, "%H:%M:%S", localtime(&tv.tv_sec));
        sprintf(datestr+8, ".%03u", (unsigned int)(tv.tv_usec / 1000));
    }
    va_start(args, format);
    length = (size_t)vsnprintf(buffer, bufsize, format, args);
    va_end(args);
    if(length + 1 >= bufsize)
    {
        while(length + 1 >= bufsize)
            bufsize *= 2;
        free(buffer);
        buffer = malloc(bufsize);
        va_start(args, format);
        length = vsnprintf(buffer, bufsize, format, args);
        va_end(args);
    }

    if(tid > 0)
        fprintf(stderr, "[%d] %s", tid, buffer);
    else
        fprintf(stderr, "%s", buffer);
}
