# Coaster
Search engine for edx.org built on Python 2.7, Redis and Postgres.

Crawler combining [Scrapy's distributed architecture](http://doc.scrapy.org/en/1.0/topics/architecture.html) with [Selenium's](http://www.seleniumhq.org/) ability to traverse Javascript-based web applications (Selenium is configured on a headless Ubuntu server via Docker).

All courses' publicly accessible data (sections, subsections, units as well as videos' links and transcripts) are categorized and stored on a complex relational database built with Postgres.

Calculations (TF-IDF) and cache-like structures required for the search engine are stored using Redis.

Simple web interface made with Flask and jQuery.
