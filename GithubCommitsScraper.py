
# get all commits of a github repository


import requests
def getCommits(repository, api_key):
    url = 'https://api.github.com/repos/' + repository + '/commits'
    commits = []
    while True:
        response = requests.get(url, headers={'Authorization': 'token ' + api_key})
        if response.status_code == 200:
            commits.extend(response.json())
            if 'link' in response.headers:
                links = response.headers['link'].split(',')
                url = None
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(';')[0].strip()[1:-1]
                        break
                if url is None:
                    break
            else:
                break
        else:
            break
    return commits

# get the list of changed files for each commit
def getChangedFiles(repository, commit, api_key):
    url = 'https://api.github.com/repos/' + repository + '/commits/' + commit
    response = requests.get(url, headers={'Authorization': 'token ' + api_key})
    if response.status_code == 200:
        return response.json()['files']
    else:
        return []


def get_commits_with_files(repository, api_key):
    commits = getCommits(repository, api_key)
    for commit in commits:

        commit['files'] = getChangedFiles(repository, commit['sha'], api_key)
    return commits

def count_file_pairs_commited_together(commits):
    file_pairs = {}
    for commit in commits:
        for file in commit['files']:
            for file2 in commit['files']:
                if file['filename'] != file2['filename']:
                    f1, f2 = sorted([file['filename'], file2['filename']])
                    file_pair = (f1, f2)
                    if file_pair in file_pairs:
                        file_pairs[file_pair] += 1
                    else:
                        file_pairs[file_pair] = 1
    return file_pairs

def get_two_dimensional_matrix_from_file_pair_counts(file_pairs):
    files = set()
    for file_pair in file_pairs:
        files.add(file_pair[0])
        files.add(file_pair[1])
    files = sorted(list(files))
    matrix = [[0 for x in range(len(files))] for y in range(len(files))]
    for file_pair in file_pairs:
        i = files.index(file_pair[0])
        j = files.index(file_pair[1])
        matrix[i][j] = file_pairs[file_pair]
        matrix[j][i] = file_pairs[file_pair]
    return files, matrix

def build_pandas_dataframe_from_matrix(files, matrix):
    import pandas as pd
    df = pd.DataFrame(matrix, index=files, columns=files)
    return df


def build_commit_file_pair_matrix_from_repository(repository, api_key):
    commits = get_commits_with_files(repository, api_key)
    file_pairs = count_file_pairs_commited_together(commits)
    files, matrix = get_two_dimensional_matrix_from_file_pair_counts(file_pairs)
    df = build_pandas_dataframe_from_matrix(files, matrix)
    return df

def write_matrix_to_csv_file(df, filename):
    df.to_csv(filename)

def read_matrix_from_csv_file(filename):
    import pandas as pd
    return pd.read_csv(filename, index_col=0)

