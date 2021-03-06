from .bitbucket_client import BitbucketClient
from .github_client import GitHubClient


class Bitbucket2GitHub:
    def __init__(
        self,
        gh_token, gh_organization, gh_team,
        bb_username, bb_password, bb_organization=None,
        repos_to_migrate=None
    ):
        self._setup_github(gh_token, gh_organization, gh_team)
        self._setup_bitbucket(bb_username, bb_password, bb_organization)
        self.repos_to_migrate = repos_to_migrate

    def _setup_bitbucket(self, username, password, organization):
        self.bitbucket_username = username
        self.bitbucket_password = password
        self.bitbucket = BitbucketClient(
            username=username,
            password=password,
            organization=organization
        )

    def _setup_github(self, token, organization, team):
        self.github = GitHubClient(
            token=token,
            organization=organization,
            team=team
        )

    def migrate(self):
        repos = self.bitbucket.get_repositories()
        repos_to_migrate = self.repos_to_migrate
        for repo in repos:
            repo_data = {
                'name': repo['name'],
                'slug': repo['slug'],
                'is_private': repo['is_private'],
                'url': repo['links']['clone'][0]['href']
            }
            if (not repos_to_migrate or repo_data['name'] in repos_to_migrate):
                self.github.import_repo(
                    repo_data,
                    self.bitbucket_username,
                    self.bitbucket_password
                )
