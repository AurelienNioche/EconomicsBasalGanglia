import pickle
from os import chdir


def get_job_names():

    chdir("../data/scripts")

    try:
        job_names = pickle.load(open("avakas_job_names.p", mode='wb'))
        return job_names
    except:
        return 'Not current jobs found'


if __name__ == "__main__":

    print(get_job_names())
