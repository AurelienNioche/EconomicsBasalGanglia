import subprocess
import pickle


def load_args():

    script_names = pickle.load(open("../data/scripts/avakas_launcher_args.p", mode='rb'))
    return script_names


def save_job_names(job_names):

    pickle.dump(job_names, open("../data/scripts/avakas_job_names.p", mode='wb'))


def main():

    job_names = []
    script_names = load_args()
    print(script_names)

    for script_name in script_names:
        a = subprocess.check_output("qsub {}".format(script_name).split())
        print(a)
        job_names.append(str(a).split(".")[0])  # Remove the \n at the end

    save_job_names(job_names)

if __name__ == "__main__":

    main()
