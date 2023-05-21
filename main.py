from website import create_app
import asyncio

import sys, asyncio

# to solve ValueError: set_wakeup_fd only works in main thread
# from https://stackoverflow.com/questions/60359157/valueerror-set-wakeup-fd-only-works-in-main-thread-on-windows-on-python-3-8-wit
if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = create_app()

@app.before_first_request
def start_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.call_soon_threadsafe(loop.stop)
    loop.run_forever()

if __name__ == '__main__':  #only if when we run(not input) this file will execute line 7
    app.run(debug=True)     #turn on to avoid manually rerun###
