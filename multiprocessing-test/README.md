# Raspberry Multiprocessing test
Simple test to explore python multiprocessing mechanism.  
The test is structured as follows: the main process instantiates 2 sub-process using the `spawn` method.  
According to python3 documentation, using `spawn` implies that:

> The parent process starts a fresh python interpreter process.
> The child process will only inherit those resources necessary to run the process objects run() method.
> In particular, unnecessary file descriptors and handles from the parent process will not be inherited.
> Starting a process using this method is rather slow compared to using fork or forkserver.

The two processes share a `Queue`: the process `time_checker` puts a `datetime.today()` object on the queue every two seconds, while process `printer` just fetches anything that comes from the Queue and prints it.
