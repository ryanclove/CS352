my name netID

1. The main error in my code is it iterates several times through, not just once.
Like in the test case we were given, it runs 4 times and outputs the result 4 times.
I imagine the reason why is the for loop causes it to run for as many lines in the test
case and prints the data each time.
Also, I have a BrokenPipeError {Errno 32] and I'm not sure how to fix it - it occurs
on the line csockid.sendall(data.encode('utf-8')). 

2. Some of the problems I faced was just getting used to the Python library, 
as well as formatting the code in the way that would produce the output I wanted.
I also spent time changing my method of how to get the output, varying with for loops
and if statements before I decided to go with my current design that utilizes lists.
I spent shy of 2 days working on this project (non-consecutive) which was less than ideal, 
but I had other CS projects due within the days leading to this due date.
