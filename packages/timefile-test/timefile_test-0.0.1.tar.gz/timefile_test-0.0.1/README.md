# ⏱️ timefile
Probably the simplest time profiling in python 
# TODO: 
- [ ] Fix project structure
- [ ] Implement custom logging level to avoid other modules logs
- [ ] Add total time per function bar graph
- [ ] allow args and kwargs using <code>func.__code__.co_varnames </code>
- [ ] Parse out constant multi kwargs
- [ ] Add some way to plot with multi variable func
- [ ] Add dt tolerance to avoid too many logs
    > ~10^5 func calls Starts to get slow => 15 sec :/