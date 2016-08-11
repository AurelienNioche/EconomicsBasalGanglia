from subprocess import check_output
import argparse


def kill_job():
    parser = argparse.ArgumentParser()

    parser.add_argument('begin', type=int,
                        help='The number of the first job of the list to kill is required')

    parser.add_argument('end', type=int,
                        help='The number of the second job of the list to kill is required')

    args = parser.parse_args()

    begin_job = args.begin
    end_job = args.end

    for i in range(begin_job, end_job+1):

        print(check_output("qdel {}".format(i).split(" ")))

if __name__ == "__main__":

    kill_job()
