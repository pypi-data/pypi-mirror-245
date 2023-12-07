import re
from dataclasses import dataclass
from datetime import datetime

import gitlab
from decouple import config
from loguru import logger


@dataclass
class ChangelogEntry:
    title: str
    url: str = None
    author: str = None
    issue_iid: int = None
    issue_labels: list[str] = None

    def get_title(self) -> str:
        if self.issue_iid:
            return f"#{self.issue_iid} {self.title}"
        else:
            return self.title


@dataclass
class Deployment:
    deployed_at: datetime
    deployed_by: str
    environment: str
    changelog: list[ChangelogEntry]


class GitlabConnector:
    def __init__(self, personal_api_token: str, project_id: str):
        """
        Create Gitlab instance with token and project
        :param personal_api_token:
        :param project_id:
        """
        assert personal_api_token
        assert project_id
        self.project_id = project_id
        self.__gitlab = gitlab.Gitlab(private_token=personal_api_token)

    @staticmethod
    def factory() -> "GitlabConnector":
        personal_api_token = config('PAT')
        project_id = config('PROJECT_ID', default=False)
        if not project_id:
            # if project is not defined, assume current project
            project_id = config('CI_PROJECT_ID')
        return GitlabConnector(personal_api_token, project_id)

    @property
    def project(self):
        return self.__gitlab.projects.get(self.project_id)

    def get_changelog(self, environment: str = "staging/the_exb", deployments_count: int = 1) -> list[Deployment]:
        kwargs = {
            'order_by': "finished_at", 'sort': "desc", 'iterator': True,
            "environment": environment, "status": "success"
        }
        deployments_iter = self.project.deployments.list(**kwargs)
        deployment_list: list[Deployment] = []

        while deployments_count > 0:
            deployments_count -= 1
            deployment = next(deployments_iter)
            logger.info(f"Deployment to {environment} created at: {deployment.created_at} "
                        f"deployed_by: {deployment.user['username']}")

            log_entries = []
            mr_iter = deployment.mergerequests.list(iterator=True)
            issues_merged = []
            for mr in mr_iter:
                if mr.description is None or "Closes" not in mr.description:
                    logger.debug(f"MR without issue: {mr.title}")
                    log_entries.append(
                        ChangelogEntry(
                            title=mr.title,
                            author=mr.author['name'],
                            url=mr.web_url
                        )
                    )
                    continue

                issue_ids = re.findall(r'#(\d+)', mr.description)
                if not issue_ids:
                    logger.warning("MR with description and 'Closes' but with no issues ids")
                    logger.debug(mr)
                    continue
                logger.debug(issue_ids)
                for id in issue_ids:
                    try:
                        issues_merged.append(self.project.issues.get(id))
                    except gitlab.exceptions.GitlabGetError as error:
                        if error.response_code != 404:
                            raise
            for issue in issues_merged:
                logger.debug(f"Issue: {issue.title}")
                logger.debug(issue)
                log_entries.append(
                    ChangelogEntry(
                        title=issue.title,
                        author=issue.author['username'],
                        url=issue.web_url,
                        issue_iid=issue.iid,
                        issue_labels=issue.labels
                    )
                )
            deployment_list.append(
                Deployment(
                    deployed_at=deployment.created_at,
                    deployed_by=deployment.user['username'],
                    environment=environment,
                    changelog=log_entries)
            )
        return deployment_list
