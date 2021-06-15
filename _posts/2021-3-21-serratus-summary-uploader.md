---
layout: post-no-cover
title: Efficiently uploading Serratus files to AWS databases using Lambda
date: 2021-3-21
description: 
ext_img: http://s19386.pcdn.co/wp-content/uploads/2017/01/amazon_aurora.png
tags: [software]
---

I recently implemented an update across the stack for [serratus.io](https://serratus.io). Here, I'll share some experiences from the process.

1. The data
2. The goals
3. Our approach, including experimentation of various AWS offerings.

## Data

- `summary2/<sra_id>.summary`: Serratus analysis results stored as S3 files in [Serratus summary format](https://github.com/ababaian/serratus/wiki/.summary-Reports).
    - For the [Nucleotide search](https://serratus.io/explorer), there was 3,837,755 files.
    - For the [RdRP search](https://serratus.io/explorer-rdrp), there was 5,686,715 files.
- `index.txt`: index file containing one `sra_id` per line.

## Goals

1. Quickly upload all summary data.
2. Expose the data as publicly searchable. Consumption options:
	1. Direct databse connection
	2. R [[tantalus](https://github.com/serratus-bio/tantalus)]
	3. Graphical interface [[serratus.io](https://serratus.io)]
	4. REST API [[serratus-summary-api](https://github.com/serratus-bio/serratus-summary-api)]

## Upload

Source code: [serratus-summary-uploader](https://github.com/serratus-bio/serratus-summary-uploader)

This didn't take much trial/error - it was clear that **AWS Lambda** would be perfect for this. A [manager-worker parallelism](http://etutorials.org/Linux+systems/cluster+computing+with+linux/Part+II+Parallel+Programming/Chapter+8+Parallel+Programming+with+MPI/8.2+Manager+Worker+Example/) approach was used. This means 2 Lambda functions:

1. Manager lambda
	- Iterate through the index file
	- Invoke the worker lambda for every batch of lines to be processed (used `n=1000`)
	- Self-invoke prior to function timeout to continue index file iteration
2. Worker lambda
	- Download summary files from S3 (with exponential backoff for throttling)
	- Parse summary files into `pandas` dataframes
	- Upload data to destination. The destination choice was an experiment itself which is discussed in the next section.

Each worker lambda takes ~5 minutes to complete. Adding in the sequential nature of the manager lambda + time for lambda function invocation, an index file with 3,837,755 lines finished in < 20 minutes.

## Data storage

The choice of upload destination was tricky and much time was spent experimenting with various AWS offerings. Below is a section for each offering we tried.

### Athena

Pros:

- Easily view files in S3
- `awswrangler` made it easy to upload data with optimizations

Cons:

- Not publicly query-able (requires access to Athena on host AWS account)
- S3 upload is slow with frequent throttling during parallelized upload (`SlowDown`)
- Simple queries are extremely slow, e.g.
    ```sql
    select * from nfamily
    where sra_id = 'ERR2756788'
    limit 10
    ```
	- Initially, this was the problem for any column used in `where`. After adding partition projection for `score` and `percent_identity` (since those are the filter options on [serratus.io](https://serratus.io)), queries on those columns were manageable. However, partitioning on a high-cardinality column e.g. `sra_id` isn't the right optimization. Bucketing could be an option, but it didn't seem possible with our parallelized upload approach, and would result in many small parquet files (undesireble for Athena queries)

### DynamoDB

I didn't spend much time evaluating this one.

Pros:

- Fast upload

Cons:

- NoSQL (our data is relational)
- PartiQL isn't SQL, and no ability to have a direct public database connection

### Aurora Serverless (PostgreSQL) (v1)

Pros:

- Low cost
- Auto/manual scaling of "capacity units"
- Fast upload when instance count manually scaled up

Cons:

- [Direct connection must be from within the VPC](https://stackoverflow.com/questions/56977625/aws-rds-aurora-how-to-connect-using-pgadmin).
- Data API is publicly accessible but has *drastic* limitations
	- 1MB / 1000-row query result limit
	- Requires Secrets Manager entry retrieval (not publicly accessible via password auth)
- Waking from "0 capacity units" state takes up to a minute, even for simple queries. This would result in painful experiences for the end user on serratus.io.

### Aurora Provisioned

Pros:

- Publicly accessible
- Always-on

Cons:

- No way to scale up/down for batch uploads to save cost.

### Final setup

The final setup is a mixture of provisioned and serverless Aurora:

- Serverless Aurora for data upload
- Restore from snapshot to `db.t3.medium` provisioned Aurora instance for every update.
	- Provide read-only access to database with public credentials.

We can do this because our data is served as read-only with infrequent updates. All updates go to the Serverless cluster first, then a snapshot is created and restored (takes ~30min) and references to the current endpoint are updated. This way we can also stage changes in a separate endpoint and make a PR downstream ([example](https://github.com/serratus-bio/serratus-summary-api/pull/21/files)).

See [this wiki page](https://github.com/ababaian/serratus/wiki/Serratus-SQL-Database-Management) for more info on Serratus database management.
