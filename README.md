# MillionSongDataset
Analysis of the million song dataset released by Labrosa (https://labrosa.ee.columbia.edu/millionsong/) to predict the year of the song and the song genre

## Setup
We used AWS EMR clusters to run the entire code. In order to use some of the existing code, we needed to do a bit of configuration as follows:

From the console, install the following packages:
1. sudo yum-config-manager --enable epel to enable package additions
2. sudo yum -y install hdf5-devel for libhdf5-serial libs
3. sudo chmod +777 -R /usr/lib64/python2.7/dist-packages/

Mount the EBS volume as per directions mentioned at https://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset

Install the following python packages:
1. ! pip install h5py
2. ! pip install --user --install-option="--install-purelib=/usr/lib64/python2.7/dist-packages/" 'numpy==1.7.1'
3. ! pip install --user --install-option="--install-purelib=/usr/lib64/python2.7/dist-packages" 'tables==2.4'

Please not that the getters for the h5 files need particular versions of the packages mentioned above which is why it's needed to force install them.
