from random import randint
import time
import math
from numpy.random import choice

start = time.time()

# Constants
NUM_OF_TYPES = 5

MAX_NUM_OF_JOBS = 1000
MIN_NUM_OF_JOBS = 1

NUM_OF_GEN = 10
NUM_OF_CHROMOZOMS = 10


debug_file = open("debugout.txt", "w")
out_file = open("out.txt", "w")


# returns the total number of machines that will be in use , and a raw jobs data
def handleInput():
    if input("Would you like to generate a new input file? Y/N\n") == "Y":
        num_of_machines = int(input("Please enter the number of machines: \n"))
        min_processing_time = int(input("Please enter the minimum processing time for a single job: \n"))
        max_processing_time = int(input("Please enter the maximum processing time for a single job: \n"))
        num_of_jobs = int(input("Please enter the number of jobs: \n"))

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

        # # Generate random number of jobs
        # num_of_jobs = randint(MIN_NUM_OF_JOBS,MAX_NUM_OF_JOBS)
        print("number of jobs generated: ", num_of_jobs)
        jobs = []
        for index in range(0, num_of_jobs):
            j = []
            j.append(index)
            job_size = randint(min_processing_time, int(max_processing_time))
            j.append(job_size)
            type = randint(1, NUM_OF_TYPES)
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
            if index == 0:
                num_of_machines = int(line)
                print("The number of machines loaded : ", line, "\n")
            else:
                jobs.append(line.split())

        inpt.close()

    return num_of_machines, jobs


class Job(object):
    def __init__(self, ind, length, kind):
        self.number = ind
        self.length = length
        self.type = kind
        self.in_machine = -1

    def __iter__(self):
        return iter(self)

    # def __str__(self):
    #     return "#: %s Length :%s Type: %s" % (self.number, self.length, self.type)

    def __str__(self):
        return "[%s, %s, %s]" % (self.number, self.length, self.type)

    # def __repr__(self):
    #     return "#: %s Length :%s Type: %s" % (self.number, self.length, self.type)

    def __repr__(self):
        return "[%s, %s, %s]" % (self.number, self.length, self.type)

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
        self.number = num  # Machine serial #
        self.span = 0  # Initial makespan
        self.types = [0] * NUM_OF_TYPES  # Histogram of size 5 - to count each type assigned to the machine
        self.types_sums = [0] * NUM_OF_TYPES

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
        job_type = job.getType() - 1
        self.assigned_jobs[job.getNumber()] = job
        self.span += job.getLength()
        self.types[job_type] = self.types[job_type] + 1
        self.types_sums[job_type] = self.types_sums[job_type] + job.length
        job.in_machine = self.number

    def retrieveJob(self, job_number):
        return self.assigned_jobs[job_number]

    # TODO: make another version of this, for job objects and not numbers
    # removing job from the machine by job number
    def removeJob(self, job_number):
        job = self.retrieveJob(job_number)
        job_type = job.getType() - 1
        del (self.assigned_jobs[job_number])
        self.span -= job.getLength()
        self.types[job_type] = self.types[job_type] - 1
        self.types_sums[job_type] = self.types_sums[job_type] - job.length
        job.in_machine = -1

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
            if t > 0:
                count = count + 1
        return count

    # returns a list of the types numbers assigned
    def getTypes(self):
        re_list = []
        for index, t in enumerate(self.types):
            if t > 0:
                re_list.append(index + 1)
        return re_list


num_of_machines, raw_jobs = handleInput()
num_of_jobs = len(raw_jobs)

# Creates and returns a machines list
def createMachines():
    machines = []
    for i in range(0, num_of_machines):
        cur_machine = Machine(i)
        machines.append(cur_machine)
    return machines


# Create and returns a list of jobs objects
def createJobs():
    jobs_list = []
    for job in raw_jobs:
        cur_job = Job(int(job[0]), int(job[1]), int(job[2]))
        print("Created job: index:", cur_job.number, "Length:", cur_job.length, "Type", cur_job.type, file=debug_file)
        jobs_list.append(cur_job)
    print("-----------------FINISHED CREATING JOB OBJECTS----------------------\n\n", file=debug_file)
    return jobs_list

# Creating objects
machines_list = createMachines()
jobs_list = createJobs()

# creating a chromosome - returning a list of size num_of_jobs , each index is job number, value is the assigned machine
def createChrom():
    ch = [0]*num_of_jobs
    for i in range(num_of_jobs):
        legal = False
        while not legal:
            machine_rand = randint(0,num_of_machines-1)
            ch[i] = machine_rand
            machines_list[machine_rand].addJob(jobs_list[i])
            if machines_list[machine_rand].isLegal():
                legal = True
            else:
                machines_list[machine_rand].removeJob(i)


    return ch

# creating a population - returning a list (of lists) of NUM_OF_CHROMOZOMS chromosomes
def createPop():
    pop = []
    for i in range(NUM_OF_CHROMOZOMS):
        curr = []
        legal = False
        while not legal:
            chrom = createChrom()
            eval = evaluateOne(chrom)

            if eval > 0:
                legal = True
        curr.append(chrom)
        curr.append(eval)
        pop.append(curr)
    return pop


def makeSpan():
    max_span = 0
    for machine in machines_list:
        if machine.span > max_span:
            max_span = machine.span
    return max_span





def printMachineStatConsole(chrom):
    print("---------------MACHINES STATS--------------------------\n")
    print("current chromosome:",chrom)
    for machine in machines_list:
        cur_job_list = machine.retrieveJobsList()
        print("machine number ", machine.number, "assigned jobs [number,length,type]:")
        l = []
        for job_number, job in cur_job_list.items():
            l.append(job)
        print("".join(str(l)))

        print("Assigned types: ", machine.getTypes())
        print("Types histogram: ", machine.types, "Sum of each type: ", machine.types_sums, "Makespan : ", machine.span)
        print("\n")

    print("Max makespan is : ", makeSpan())
    # print("------------------------------------------------\n", file=out_file)


def removeAllJobs():
    for machine in machines_list:
        cur_jobs = dict(machine.assigned_jobs)
        for key, job in cur_jobs.items():
            if key != job.number:
                print("SOMETHING WENT WRONG")
            num = job.number
            machine.removeJob(num)
            # print("REMOVED  -- machine#: ", machine.number, "assigned jobs: ", job)


# TODO: better evaluiation
# evalutation at the moment is just the makespan of a single chromosome
def evaluateOne(chromosome: list):
    # simulate adding the jobs
    # TODO: If slow run, consider removing thos for. Might be redundant anyway
    for i in range(len(chromosome)):
        machines_list[chromosome[i]].addJob(jobs_list[i])
        if not machines_list[chromosome[i]].isLegal():
            removeAllJobs()
            return -1
    # printMachineStatConsole(chromosome)

    span = makeSpan()

    # revert to neutral state
    removeAllJobs()

    # for i in range(len(chromosome)):
    #     machines_list[chromosome[i]].removeJob(i)

    return span

def distributionRank(worst,population):
    dist = []
    sum  = 0
    # for p in population:


# current fitness function = the difference between chromosome's makespan and the worst chromosome's makespan
def updateFitness(chormosome,worst):
    fitness = (worst-chormosome[1])+1   # TODO: fix smoothing
    chormosome.append(fitness)
    return fitness

def updateProb(chromosome, sum):
    prob = chromosome[2]/(sum)
    chromosome.append(prob)
    return prob

# go over popluation and calculate each one's fitness
def evaluateAll(population: list):
    worst = 0
    sum = 0
    # prob_sum = 0
    probabilites = []
    for i in range(len(population)):
        eval = population[i][1]
        # population[i].append(eval)
        if eval > worst:
            worst = eval
        # print(population[i],population[i][1])
        print(population[i][0])
        print(eval)
    for j in range(len(population)):
        fitness = updateFitness(population[j], worst)
        sum += fitness
    for k in range(len(population)):
        prob = updateProb(population[k], sum)
        probabilites.append(prob)
        # prob_sum += prob




    print("worst chromosome makespan:", worst)

    return probabilites




def printPop(population: list):
    for p in population:
        print(p)



def selection(probs):
    # pick 2 parents out of this distribution
    t = [i for i in range(len(probs))]
    draw = choice(t, 2, p=probs, replace=False)


pop = createPop()
printPop(pop)

print("evaluate:")
probs = evaluateAll(pop)


print("####################")

for p in pop:
    print(p)



#debug
probs_sum = 0
for i in range(len(probs)):
    probs_sum += probs[i]
print(probs_sum)


debug_file.close()
out_file.close()
