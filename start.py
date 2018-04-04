from random import randint


# Constants
NUM_OF_TYPES = 5

MAX_NUM_OF_JOBS = 1000
MIN_NUM_OF_JOBS = 1

# returns the total number of machines that will be in use , and a raw jobs data
def handleInput():
    if input("Would you like to generate a new input file? Y/N\n") == "Y":
        num_of_machines = input("Please enter the number of machines: \n")
        max_processing_time = input("Please enter the maximum processing time for a single job: \n")
        print("max process time is :", max_processing_time)


        # Generate the soon-to-be input file
        # input file format will be :
        #
        # NUMBER_OF_MACHINES
        # JOB_INDEX JOB_SIZE JOB_TYPE
        #
        # notice that the total number of jobs will be indicated in the [n-1,0] cell

        inpt = open("input.txt", 'w')

        inpt.write(num_of_machines)
        inpt.write("\n")

        # Generate random number of jobs
        jobs = randint(MIN_NUM_OF_JOBS,MAX_NUM_OF_JOBS)
        print("number of jobs generated: ", jobs)

        for index in range(0,jobs):
            job_size = randint(1,int(max_processing_time))
            type = randint(1,NUM_OF_TYPES)
            inpt.write(str(index))
            inpt.write(" ")
            inpt.write(str(job_size))
            inpt.write(" ")
            inpt.write(str(type))
            inpt.write("\n")

        inpt.close()


    else:
        inpt = open("input.txt", 'r')
        jobs = []
        for index, line in enumerate(inpt):
            if index == 0 :
                num_of_machines = int(line)
                print("The number of machines loaded are : ", line, "\n")
            else:
                jobs.append(line.split())


        inpt.close()

    return num_of_machines,jobs


class Job(object):
    def __init__(self, ind, length, kind):
        self.number = ind
        self.length = length
        self.type = kind


    def __str__(self):
        return "#: %s Length :%s Type: %s" % (self.number, self.length, self.type)

    def __repr__(self):
        return "#: %s Length :%s Type: %s" % (self.number, self.length, self.type)


    def __len__(self):
        return self.length

    def __eq__(self, other):
        if self.number != other.number:
            return False
        else:
            return True

    def getNumber(self):
        return self.number

class Machine(object):
    def __init__(self, num):
        self.assigned_jobs = []
        self.number = num


    def __str__(self):
        ret = ""
        for a in self.assigned_jobs:
           ret.join(a.getNumber()).join(", ")
        return "Jobs numbers : %s" % (ret)

    def __repr__(self):
        ret = ""
        for a in self.assigned_jobs:
           ret.join(a.getNumber()).join(", ")
        return "Jobs numbers : %s" % (ret)

    def __iter__(self):
        return iter(self.d)

    def __getitem__(self, index):
        return self.d[index]

    def __setitem__(self, index, value):
        self.d[index] = value



    def addJob(self, job):
        self.assigned_jobs.append(job)






num_of_machines, raw_jobs = handleInput()


# Creates and returns a machines list
def createMachines():
    machines = []
    for i in range(0,num_of_machines):
        cur_machine = Machine(i)
        machines.append(cur_machine)
    return machines




# Create and returns a list of jobs objects
def createJobs():
    jobs_list = []
    for job in raw_jobs:
        cur_job = Job(job[0], job[1], job[2])
        print("Created: ",job[0], " ", job[1], " ", job[2])
        jobs_list.append(cur_job)
    return jobs_list


machines_list = createMachines()
jobs_list = createJobs()


for j in jobs_list:
    ran_machine = randint(0, num_of_machines-1)
    machines_list[ran_machine].assigned_jobs.append(j)

print()