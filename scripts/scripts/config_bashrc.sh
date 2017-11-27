#!/bin/sh

cd /etc
sudo printf "alias mars='java -jar /opt/Mars4_5.jar &'" >> bash.bashrc
printf '\nexport PATH=/usr/local/cuda-6.5/bin:$PATH\n
export LD_LIBRARY_PATH=/usr/local/cuda-6.5/lib64:$LD_LIBRARYPATH\n' >> bash.bashrc 
