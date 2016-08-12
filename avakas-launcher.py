import subprocess
import json
from os import listdir
from os.path import isfile, join


class AvakasLauncher(object):

    def __init__(self):

        self.folder = {
            "script": "../avakas_scripts",
            "job_names": ".."
        }

    def load_scripts(self):

        mypath = self.folder["script"]
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        script_names = [f for f in onlyfiles if f[:3] == ".sh"]

        return script_names

    def save_job_names(self, job_names):

        with open('{}/job_names.json'.format(self.folder["job_names"]), 'w') as f:

            json.dump(job_names, f, indent=4)

    def launch_jobs(self, script_names):

        job_names = []

        for script_name in script_names:

            print("Launch script '{}'...".format(script_name))

            # output = subprocess.check_output("qsub {}/{}".format(self.folder["script"], script_name).split())
            output = subprocess.check_output("qsub {}".format(script_name.split("../scripts/")[1]).split())

            print("System answers '{}'.".format(output))
            job_names.append(str(output).split(".")[0])  # Remove the \n at the end

        print("Come back to python 3.5.2")
        output = subprocess.check_output("pyenv local 3.5.2".split())
        print(output)

        return job_names

    def run(self):

        script_names = self.load_scripts()
        job_names = self.launch_jobs(script_names)
        self.save_job_names(job_names)


def main():

    avakas_launcher = AvakasLauncher()
    avakas_launcher.run()

if __name__ == "__main__":

    main()