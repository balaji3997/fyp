OS  REQUIRED FOR EDGE DEVICE: UBUNTU

OS USED  FOR LOCAL DEVICE : KALI LINUX 2018.1 VERSION 

LANGUAGE USED: PYTHON 

CLOUD SERVER USED :DIGITAL OCEAN 



INSTALL PYTHON VERSION 3 :sudo apt-get install python3(in both edge device and local device) 




install psutil module for python3 using : pip3 install psutil(for the profiler collecting cpu information,network bandwidth) 

 
install sklearn module for python3 using: pip3 install sklearn (for the random forest classifier)


install netifaces module for python3 using: pip3 install netifaces (for getting network information such as ip address, subnet ip ,broadcast address)


############################################################################################################################################


TO BE INSTALLED IN LOCAL MACHINE  IN THE DIRECTORY (mecc/fyp/)
 
For installing line profiler in the local machine (application profiler)


Steps for installing line Profiler in the local machine:


1. Install mercurial (Skip this step if using Official line_profiler from rkern)

sudo apt-get install mercurial



Note: rkern’s Official line_profiler has recently added Python3 support in 1.0 release


2. Clone the line_profiler repository


Update:  git clone https://github.com/rkern/line_profiler.git
note:if the above doesn't work try the below 

(Note: The old repo was moved from BitBucket link to GitHub link)


You can directly jump to Step 3 now, as Python3 support is provided by rkern’s line_profiler 🙂


Note: If this doesn’t work for you properly (Seems that they have kept support for 3.x on hold for now). You can clone this repository which is a fork of the above with 3.x compatibility.



hg clone https://bitbucket.org/kmike/line_profiler

or you can clone this one too:


hg clone https://bitbucket.org/thefalcon/line_profiler


3. Navigate into the line_profiler clone folder


cd line_profiler


4. Now you need to Install Cython (for python) / Cython3 (for python 3.x)


sudo apt-get install cython
sudo apt-get install cython3



5. Install line_profiler by running:



line_profiler for python3


python3 setup.py install


6. Go to the folder where your .py file is located and run the following command:


kernprof.py -l example.py; python3 -m line_profiler example.py (example.py should be replaced by sudokusolver.py or nqueenalgo.py)

( The above gives the execution time of each methods in the algorithm(nqueenalgo.py or sudokusolver.py) ,hit ratio of each line in every module etc.)


##########################################################################################################################################

HELP NOTES:


copy all the codes in all the machines (code in the directory mecc/fyp ) 

consider  atleast one device as local device

consider  atleast one device as edge device (actually sserver.py code is enough in edge device) 

In edge device run "python3 sserver.py"

In local device run "python3 profiler.py filename" ( filename can be replaced with nqueenalgo.py or sudokusolver.py)

For cloud use "ssh -p 443 root@142.93.222.110" and run "python3 server.py"






