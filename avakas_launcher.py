import subprocess
import pickle
from os import chdir


def load_args():

    script_names = pickle.load(open("avakas_launcher_args.p", mode='rb'))
    return script_names


def save_job_names(job_names):

    pickle.dump(job_names, open("avakas_job_names.p", mode='wb'))


def main():

    chdir("../scripts")

    script_names = load_args()

    a = subprocess.check_output("pyenv local 2.7.12".split())
    print(a)

    job_names = []

    # print(script_names)

    for script_name in script_names:

        print("Launch script '{}'...".format(script_name))
        a = subprocess.check_output("qsub {}".format(script_name.split("../scripts/")[1]).split())

        print("System answers '{}'.".format(a))
        job_names.append(str(a).split(".")[0])  # Remove the \n at the end

    a = subprocess.check_output("pyenv local 3.5.2".split())
    print(a)

    save_job_names(job_names)

if __name__ == "__main__":

    main()