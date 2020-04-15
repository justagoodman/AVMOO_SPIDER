from scrapy.cmdline import execute

if __name__ == "__main__":
    # execute(['scrapy', 'crawl', 'avmoo'])
    execute(['scrapy', 'crawl', 'avmoo', '-s', 'LOG_LEVEL=INFO'])
    # execute(['scrapy', 'crawl', 'avmoo', '-s', 'JOBDIR = JOB'])
    # jobbole - s
    # JOBDIR = job_info / 001
