The profiler and and dynamic partitioner for offloading

Steps for installing line Profiler:

1. Install mercurial (Skip this step if using Official line_profiler from rkern)

sudo apt-get install mercurial



Note: rkern’s Official line_profiler has recently added Python3 support in 1.0 release


2. Clone the line_profiler repository


Update:  git clone https://github.com/rkern/line_profiler.git

Note: The old repo was moved from BitBucket link to GitHub link


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


a) line_profiler for python

python setup.py install


b) line_profiler for python3


python3 setup.py install

6. Go to the folder where your .py file is located and run the following command:


kernprof.py -l example.py; python3 -m line_profiler example.py
