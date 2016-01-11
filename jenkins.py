import jenkinsapi
import pprint
from datetime import timedelta
import datetime
from dateutil import parser
import Queue
from collections import Counter


class jenkins_builds(object):
    build_id = job = timestamp = status = ''

    def __init__(self, job, build_id, timestamp, status):
        self.build_id = build_id
        self.job = job
        self.timestamp = timestamp
        self.status = status


def initiate_connection():
    server = jenkinsapi.jenkins.Jenkins('http://172.20.78.88/')
    return server


def get_builds(job):
    builds = []
    jenkins = initiate_connection()
    job = jenkins.get_job(job)
    for build_id in job.get_build_ids():
        build = job.get_build(build_id)
        j = jenkins_builds(job, build_id,
                           build.get_timestamp(), build.get_status())
        builds.append(j)
        print build_id, build.get_timestamp(), build.get_status()

    return builds


def get_week_range(today):
    dates = [today + datetime.timedelta(days=i)
             for i in range(0 - today.weekday(), 7 - today.weekday())]
    return dates


def get_this_week_builds(week_dates, job_name):
    builds_within_range = []
    for build in get_builds(job_name):
        for date in week_dates:
            if date.isocalendar() == build.timestamp.isocalendar():
                builds_within_range.append(build)
    return builds_within_range


def filter_successful_builds(builds):
    successeful_builds = []
    for build in builds:
        if build.status == "SUCCESS":
            # print build.status, build.build_id
            successeful_builds.append(build)
            # print build.timestamp.strftime('%u')
        else:
            print build.status, build.build_id

    return successeful_builds


def map_reduce(successeful_builds):
    builds_counter = []
    mapped_reduced = []

    for build in successeful_builds:
        builds_counter.append(build.timestamp.strftime(
            '%u') + '\t' + build.timestamp.strftime('%H'))
    builds_dict = Counter(builds_counter)
    for record in builds_dict:
        mapped_reduced.append(str(record + '\t' + str(builds_dict[record])))

    return mapped_reduced


def fill_the_gaps(mapped_reduced_data):
    optimal_sequence = generate_optimal_sequence()
    clean_data = []
    for optimal in optimal_sequence:
        for mapped in mapped_reduced_data:
            if (mapped.split('\t')[0] == optimal.split('\t')[0]) and (mapped.split('\t')[1] == optimal.split('\t')[1]):
                clean_data.append(mapped)
        clean_data.append(optimal)
    return clean_data


def generate_optimal_sequence():
    optimal_sequence = []
    for day in range(1, 8):
        for hour in range(1, 25):
            optimal_sequence.append(str(day) + '\t' + "%02d" % hour + '\t0')
    return optimal_sequence


def write_data(clean_data, env):
    data_header = 'day\thour\tvalue\n'
    data_file = open('static/prod', 'w')
    data_file.writelines(data_header)
    for i in clean_data:
        data_file.writelines(i + '\n')
    data_file.close()

if __name__ == '__main__':
    dt = parser.parse("Jan 8 2016 12:00AM")
    week_dates = get_week_range(dt)
    print week_dates
    builds = get_this_week_builds(week_dates, 'promote-dev')
    successeful_builds = filter_successful_builds(builds)
    mapped_reduced_data = map_reduce(successeful_builds)
    clean_data = fill_the_gaps(mapped_reduced_data)
    write_data(clean_data, 'prod')

# Number of projects in the pipeline
# Most Active Project:
# Succsessful / Failed Promotions:
# Most Aactive Day:
# Most Active hour:
# Promotions Today:
# Last Promoted Project:
