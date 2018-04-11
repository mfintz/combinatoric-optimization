from random import randint


# Constants
NUM_OF_TYPES = 5

MAX_NUM_OF_JOBS = 50
MIN_NUM_OF_JOBS = 1

debug_file = open("debugout.txt","w")


# returns the total number of machines that will be in use , and a raw jobs data
def handleInput():
    if input("Would you like to generate a new input file? Y/N\n") == "Y":
        num_of_machines = int(input("Please enter the number of machines: \n"))
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

        inpt.write(str(num_of_machines))
        inpt.write("\n")

        # Generate random number of jobs
        num_of_jobs = randint(MIN_NUM_OF_JOBS,MAX_NUM_OF_JOBS)
        print("number of jobs generated: ", num_of_jobs)
        jobs = []
        for index in range(0,num_of_jobs):
            j = []
            j.append(index)
            job_size = randint(1,int(max_processing_time))
            j.append(job_size)
            type = randint(1,NUM_OF_TYPES)
            j.append(type)
            inpt.write(str(index))
            inpt.write(" ")
            inpt.write(str(job_size))
            inpt.write(" ")
            inpt.write(str(type))
            inpt.write("\n")
            jobs.append(j)

        inpt.close()


    else:
        inpt = open("input.txt", 'r')
        jobs = []
        for index, line in enumerate(inpt):
            if index == 0 :
                num_of_machines = int(line)
                print("The number of machines loaded : ", line, "\n")
            else:
                jobs.append(line.split())


        inpt.close()

    return num_of_machines,jobs


class Job(object):
    def __init__(self, ind, length, kind):
        self.number = ind
        self.length = length
        self.type = kind
        self.in_machine = -1

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

    def getType(self):
        return self.type



class Machine(object):
    def __init__(self, num):
        # self.assigned_jobs = [] #TODO: maybe switch to dictionary
        self.assigned_jobs = {}
        self.number = num # Machine serial #
        self.span = 0   # Initial makespan
        self.types = [0]*5    # Histogram of size 5 - to count each type assigned to the machine



    def __str__(self):
        ret = ""
        for key, val in self.assigned_jobs.items():
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
        self.types[job.getType()-1] = self.types[job.getType()-1] + 1
        job.in_machine = self.number


    def retrieveJob(self, job_number):
        return self.assigned_jobs[job_number]



    # removing job from the machine by job number
    def removeJob(self, job_number):
        job = self.retrieveJob(job_number)
        del (self.assigned_jobs[job_number])
        self.span -= job.getLength()
        self.types[job.getType()-1] = self.types[job.getType()-1] - 1
        job.in_machine = -1

    # def makeSpan(self):
    #     span = 0
    #     for job in self.assigned_jobs:
    #         span += job.getLength()
    #     return span
    #

    # Check if the machine has jobs of at most three types
    def isLegal(self):
        counter = 0
        for t in self.types:
            if t > 0:
                counter = counter + 1
        if counter < 4:
            return True
        else:
            return False

    # Check how many different types do I have
    def checkDiffTypes(self):
        count = 0
        for t in self.types:
            if t > 0 :
                count = count + 1
        return count

    # returns a list of the types numbers assigned
    def getTypes(self):
        re_list = []
        for index, t in enumerate(self.types):
            if t > 0:
                re_list.append(index)
        return re_list







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
        print("Created job: index:",cur_job.number, "Length:", cur_job.length, "Type", cur_job.type, file=debug_file)
        jobs_list.append(cur_job)
    print("-----------------FINISHED CREATING JOB OBJECTS----------------------\n\n",file=debug_file)
    return jobs_list


machines_list = createMachines()
jobs_list = createJobs()




# Assign jobs to machines randomly , mainly for debug
# def randAssign():
#     for j in jobs_list:
#         ran_machine = randint(0, num_of_machines-1)
#         machines_list[ran_machine].addJob(j)


# Initial assignment of jobs to machines as follows : Machine 1 - types 1,2,3   Machine 2 - types 4,5
def initialAssign():
    for j in jobs_list:
        if j.type == 1 or j.type == 2 or j.type == 3:
            machines_list[0].addJob(j)
        else:
            machines_list[1].addJob(j)



def finalMakeSpan():
    max_span = 0
    for machine in machines_list:
        if machine.span > max_span:
            max_span = machine.span
    return max_span


# Print machines' stats
def printMachineStat():
    print("---------------MACHINES STATS--------------------------\n",file=debug_file)
    for machine in machines_list:
        cur_job_list = machine.retrieveJobsList()
        print("machine # ", machine.number, "assigned jobs #:",file=debug_file)
        l = []
        for job in cur_job_list:
            l.append(job)
        print("".join(str(l)),file=debug_file)

        print("Types: ", machine.types, "Makespan : ", machine.span,file=debug_file)
    print("Total makespan is : ",finalMakeSpan(),file=debug_file)
    print("------------------------------------------------\n",file=debug_file)

def printMachineStatConsole():
    print("---------------MACHINES STATS--------------------------\n")
    for machine in machines_list:
        cur_job_list = machine.retrieveJobsList()
        print("machine # ", machine.number, "assigned jobs #:")
        l = []
        for job in cur_job_list:
            l.append(job)
        print("".join(str(l)))

        print("Types: ", machine.types, "Makespan : ", machine.span)
    print("Total makespan is : ",finalMakeSpan())
    print("------------------------------------------------\n")






initialAssign()
printMachineStat()


def removeAllJobs():
    for machine in machines_list:
        cur_jobs = dict(machine.assigned_jobs)
        for key, job in cur_jobs.items():
            if key != job.number:
                print("SOMETHING WENT WRONG")
            num = job.number
            machine.removeJob(num)
            print("REMOVED  -- machine#: ", machine.number,"assigned jobs: ", job)

    print("---------------MACHINES' REMAINING JOB LISTS-----------------------\n")

    for machine in machines_list:
        cur_jobs = dict(machine.assigned_jobs)
        for key, job in cur_jobs.items():
            if key != job.number:
                print("SOMETHING WENT WRONG")
            num = job.number
            print("LEFT  -- machine#: ",machine.number, "assigned jobs: ", job)


print(machines_list[0].isLegal())



# A method for moving a job
# parameters: origin machine , a single job to move , a target machine
# returns : True if successful , else False
# TODO: needs to decide if I want the jobs to move parma to be numbers or objects
# TODO: return what ? should I return a number telling how many jobs moved successfully ? or maybe return list of unsuccessfull ?
# TODO: EXTEND TO MOVE MORE THAN ONE JOB AT A TIME
def moveJob(origin_machine: Machine, target_machine: Machine , job_to_move):
    if target_machine.checkDiffTypes() < 3:
        cur_job = origin_machine.retrieveJob(job_to_move)
        origin_machine.removeJob(job_to_move)
        target_machine.addJob(cur_job)
        # print("moved job #",job_to_move,"from ",origin_machine,"to ",target_machine,file=debug_file)
        return True
    else:
        return False


# Check if a move is at least as good as current state .
def checkMoveSpan(origin_machine: Machine, target_machine: Machine , job_to_move):
    cur_span = finalMakeSpan()
    origin_span = origin_machine.span
    target_span = target_machine.span
    job_span = jobs_list[job_to_move].length
    if cur_span == target_span:
        return False # assuming job length is at least 1 , it won't be good to move to that machine, which is already at max span
    elif cur_span > target_span + job_span:
        return True
    else:
        return False


def isLegalMove(target_machine: Machine, job:Job):
    if target_machine.checkDiffTypes() < 3:
        return True    # we surely have free space so no further checking is needed
    else:    # check if the kinds we do have is of the same as new job
        if job.type in target_machine.getTypes():
            return True
        else:
            return False


# if all done return True, else return False
def isDone(d_list):
    return all(item is False for item in d_list)


# TODO: writh a target function
def localSearch():
    done = False
    while not done:
        done_list = [False] * num_of_machines  # for checking if at least one job has moved in the last machine iteration

        for index, machine in enumerate(machines_list):
            for job_number,job in machine.assigned_jobs.copy().items():
                moved = False
                for i in range(1, num_of_machines):
                    if isLegalMove(machines_list[(machine.number+i) % num_of_machines], job):
                        move_or_not_to_move = checkMoveSpan(machine,
                                                            machines_list[(machine.number+i) % num_of_machines],
                                                            job_number)
                        if move_or_not_to_move is True:
                            moved = moveJob(machine, machines_list[(machine.number+i) % num_of_machines], job_number)
                            if moved is True:
                                if done_list[machine.number] is False:
                                    done_list[machine.number] = True
                            break
                # if moved == True:
                #     break
            printMachineStat()
            # printMachineStatConsole()
            if isDone(done_list):
                done = True
                break
            # if index == 4 and moved is False:
            #     done = True
            # else:
            #     break
    print("im out of the while!")







localSearch()



debug_file.close()
