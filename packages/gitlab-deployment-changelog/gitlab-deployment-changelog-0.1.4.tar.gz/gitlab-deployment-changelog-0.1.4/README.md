# Gitlab Deployment Changelog

Home of this code is now https://github.com/ExB-Group/gitlab-deployment-changelog 

This package grabs the last `n` deployments for a project from gitlab and creates a summary of the merge requests
and their issues. Decoration is done based on scoped labels `type::`. As of now we cover `bug`. Everything else is
considered as a feature. Merge requests without issues, were indicated as well.


## Mandatory setup 

- set gitlab access token `PAT` (https://gitlab.com/-/profile/personal_access_tokens)  
- `WEBHOOK_URL` for slack 
  - go to https://api.slack.com/apps 
  - create or select your app
  - Features/Incoming Webhooks
  - Add new webhook to workspace, select the channel where you would like to see the notifications 

## How to use at all

```bash
> pip install gitlab-deployment-changelog

> gdc -h
usage: Gitlab Deployment Changelog [-h] [-c COUNT] [-n] [-d] env

positional arguments:
  env                   Name of the environment

options:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        How many last deployments to consider
  -n, --no_slack        Dont send to slack
  -d, --debug           Show debug output

> gdc environment_to_run_again  # find merges and issues which were deployed
```



## How to use locally or manually

- checkout
- `pdm install`
- Make sure you have `PROJECT_ID` properly set
- `pdm run changelog <environment>`, the environment is mandatory and could be something like `production/the_exb` 

## Pipeline usage

- call it with the environment name as argument, e.g., `pdm run changelog staging/the_exb`


