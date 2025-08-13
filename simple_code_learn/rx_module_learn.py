'''
import rx
import time

observable = rx.interval(1.0)

disposable = observable.subscribe(lambda x: print(f"Tick: {x}"))

#wait for 5 seconds, then dispose
time.sleep(5)
disposable.dispose()
'''

# https://medium.com/@michamarszaek/reactive-programming-in-python-2af1495c7922
# https://en.wikipedia.org/wiki/Observer_pattern#Python
# https://www.tutorialspoint.com/concurrency_in_python/concurrency_in_python_reactive_programming.htm
# https://keitheis.github.io/reactive-programming-in-python

import rx
import rx.operators as ops

# source = rx.from_iterable([1, 2, 3, 4])

# disposable = source.pipe(
#     ops.map(lambda i: i -1),
#     ops.filter(lambda i: i % 2 == 0),
# ).subscribe(
#     on_next = lambda i: print(f" on_next: {i}"),
#     on_completed = lambda: print("on_completed"),
#     on_error = lambda e:print(f"on_error: {e}")
# )

# disposable.dispose()
# print("Done !")

def my_observable(observer, scheduler):
    observer.on_next("Hello")
    observer.on_next("RxPy")
    observer.on_completed()

source = rx.create(my_observable)

source.subscribe(
    on_next = lambda value: print("Received:", value),
    on_error = lambda e: print("error:",e),
    on_completed = lambda: print("Done!")
)
