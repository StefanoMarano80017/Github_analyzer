import QueryGit
import DAO
import datetime

def do_git_query(token, date:datetime.date, lang):
    git = QueryGit.QueryRepo(token)

    # fork > 0 & star > 0
    # created:2017-05-31 stars:>0 forks:>0 language:Java
    query_txt = "created:" + str(date) + " stars:>0 forks:>0 language:" + lang
    print(query_txt)
    return git.do_query_txt(query_txt)


def repos_to_db(db_file, token, date:datetime.date, lang):
    repos = do_git_query(token, date, lang)
    dao_repo = DAO.DAO_Repo(db_file)

    for repo in repos:
        args = (None, repo.name)
        dao_repo.set_data(repo, args)
