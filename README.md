# Python Multiprocessing

# Why Use Multiprocessing

# Python's `multiprocessing` module

- supports a variety of coding techniques
  - object-oriented or function based
  - data passing
  - managing execution across hardware processors/cores
- data types include native `ctype` or (pickleable) Python object 
- selecting the most appropriate pattern for a particular program can be a little daunting

This talk will mainly discuss `multiprocessing.Process` using OOP and `multiprocessing.Pool` with a function based pattern.

## Using `multiprocessing.Process`

- supports an object-oriented pattern
  - Similar to the `multithreading.Thread` API
  - pass parameters in via `.__init__` (optional) 
  - `.start()` is called to start the process
  - `.run()` is the method that actually runs in the separate process
- can also be run procedurally via `Process(target=<function>)` (not a focus in these examples)
- must return values via communication capabilities provided in the `multiprocessing` module
  - e.g. `Queue`, `Value`, etc.

## Using `multiprocessing.Pool`

- manages mapping execution to the underlying hardware
- works well with a more functional programming style, including `map`
- manages return data

# Logging

The created process ends up with a "new" logging instance (not inherited). It must be configured.

# Common Pitfalls

- Trying to access data "directly" across processes without using multiprocessing communication "channels".
  - Mechanisms exist to facilitate communication, but you should choose wisely.
  - Make sure you communicate using pickle-able data.
- Using "HyperThread" (AKA Simultaneous Multi-Threading or SMT) processors as "real" cores.

# Design Decisions

- one (or more) disparate processes or mapping a single function across many data instances
- how to pass data
- how to address process-specific aspects such as logging
- consider first prototyping a design pattern appropriate for your application
