from random import randint


# Constants
NUM_OF_TYPES = 5

MAX_NUM_OF_JOBS = 1000
MIN_NUM_OF_JOBS = 1

# returns the total number of machines that will be in use , and a raw jobs data
def handleInput():
    if input("Would you like to generate a new input file? Y/N\n") == "Y":
        num_of_machines = input("Please enter the number of machines: \n")
        max_processing_time = int(input("Please enter the maximum processing time for a single job: \n"))
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


    def __iter__(self):
        return iter(self)

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

    def getLength(self):
        return self.length




class Machine(object):
    def __init__(self, num):
        # self.assigned_jobs = [] #TODO: maybe switch to dictionary
        self.assigned_jobs = {}
        self.number = num # Machine serial #
        self.span = 0   # Initial makespan


    # def __str__(self):
    #     ret = ""
    #     for a in self.assigned_jobs:
    #        ret.join(a.getNumber()).join(", ")
    #     return "Jobs numbers : %s" % (ret)

    def __str__(self):
        ret = ""
        for key, val in self.assigned_jobs:
           ret.join(val.getNumber()).join(", ")
        return "Jobs numbers : %s" % (ret)

    def __repr__(self):
        ret = ""
        for a in self.assigned_jobs:
           ret.join(a.getNumber()).join(", ")
        return "Jobs numbers : %s" % (ret)

    def __iter__(self):
        return iter(self)

    # def __getitem__(self, index):
    #     return self.d[index]
    #
    # def __setitem__(self, index, value):
    #     self.d[index] = value

    def retrieveJobsList(self):
        return self.assigned_jobs

    def addJob(self, job):
        self.assigned_jobs[job.getNumber()] = job
        self.span += job.getLength()

    # def retrieveJob(self, job_number):
    #     for j in self.assigned_jobs:
    #         if j.getNumber() == job_number:
    #             return j
    #     else:
    #         return None

    def retrieveJob(self, job_number):
        return self.assigned_jobs[job_number]


    # def removeJob(self, job_number):
    #     job = self.retrieveJob(job_number)
    #     self.assigned_jobs.remove(job)
    #     self.span -= job.getLength()



    def removeJob(self, job_number):
        job = self.retrieveJob(job_number)
        del (self.assigned_jobs[job_number])
        self.span -= job.getLength()

    # def makeSpan(self):
    #     span = 0
    #     for job in self.assigned_jobs:
    #         span += job.getLength()
    #     return span
    #




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
        cur_job = Job(int(job[0]), int(job[1]), int(job[2]))
        print("Created: ",job[0], " ", job[1], " ", job[2])
        jobs_list.append(cur_job)
    return jobs_list


machines_list = createMachines()
jobs_list = createJobs()


for j in jobs_list:
    ran_machine = randint(0, num_of_machines-1)
    machines_list[ran_machine].addJob(j)

print("------------------------------------------------\n")

for j in jobs_list:
    print(j)

print("------------------------------------------------\n")

for machine in machines_list:
    cur_job_list = machine.retrieveJobsList()
    for job in cur_job_list:
        print("machine#: ",machine.number ,"assigned jobs #: ", job)
print("------------------------------------------------\n")

#
# for m in machines_list:
#     m_j = m.assigned_jobs
#     for job in m_j:
#         num = job.number
#         m.removeJob(num)
#     print()


for machine in machines_list:
    cur_jobs = dict(machine.assigned_jobs)
    for key, job in cur_jobs.items():
        if key != job.number:
            print("SOMETHING WENT WRONG")
        num = job.number
        machine.removeJob(num)
        print("REMOVED  -- machine#: ",machine.number ,"assigned jobs: ", job)

print("---------------MACHINES' JOB LISTS-----------------------\n")

for machine in machines_list:
    cur_jobs = dict(machine.assigned_jobs)
    for key, job in cur_jobs.items():
        if key != job.number:
            print("SOMETHING WENT WRONG")
        num = job.number
        print("REMOVED  -- machine#: ",machine.number ,"assigned jobs: ", job)


print()