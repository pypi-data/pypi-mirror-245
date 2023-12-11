#ifndef _GLOBALS_H_
#define _GLOBALS_H_

typedef void (*ProgressCallback)(int value, int maximum, const char * text);
extern ProgressCallback g_progressCallback;

#endif