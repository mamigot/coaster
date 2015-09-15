# Coaster
Search engine for edx.org built on Python 2.7, Redis and Postgres.

Distributed crawler combining [Scrapy's](http://doc.scrapy.org/en/1.0/index.html) architecture with [Selenium's](http://www.seleniumhq.org/) ability to traverse Javascript-based web applications (Selenium is configured on a headless Ubuntu server via Docker).

All courses' publicly accessible data (sections, subsections, units as well as videos' links and transcripts) is categorized and stored on a complex relational database built with Postgres.

Calculations and cache-like structures required for the search engine are stored using Redis.
