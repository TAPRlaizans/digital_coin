#!/usr/bin/python
import os
import sys
import time
import _thread
from fundamentals.blockbeats import get_rss_reponse_info 
 
try:
   # _thread.start_new_thread( print_time, ("Thread-1", 2, ))
   _thread.start_new_thread(get_rss_reponse_info.main())
except Exception as e:
   error_type = type(e).__name__
   print("Error: unable to start thread")
   print("捕获到错误：", error_type)
 
while 1:
   pass