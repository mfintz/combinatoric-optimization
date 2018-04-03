from random import randint


# Constants
NUM_OF_TYPES = 5

MAX_NUM_OF_JOBS = 1000
MIN_NUM_OF_JOBS = 1





if input("Would you like to generate a new input file? Y/N\n") == "Y":
    num_of_machines = input("Please enter the number of machines: \n")
    max_processing_time = input("Please enter the maximum processing time for a single job: \n")
    print("max process time is :",max_processing_time)


    # Generate the soon-to-be input file
    # input file format will be :
    #
    # NUMBER_OF_MACHINES
    # JOB_INDEX JOB_SIZE JOB_TYPE

    inpt = open("input.txt", 'w')

    inpt.write(num_of_machines)
    inpt.write("\n")

    # Generate random number of jobs
    jobs = randint(MIN_NUM_OF_JOBS,MAX_NUM_OF_JOBS)
    print("number of jobs generated: ", jobs)

    for index in range(0,jobs):
        job_size = randint(0,int(max_processing_time))
        type = randint(1,5)
        inpt.write(str(index))
        inpt.write(" ")
        inpt.write(str(job_size))
        inpt.write(" ")
        inpt.write(str(type))
        inpt.write("\n")



    inpt.close()


else:
    inpt = open("input.txt", 'r')

    inpt.close()