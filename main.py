from GithubCommitsScraper import *

repo = 'alpaylan/sars'
api_key = '<your-api-key>'
df = build_commit_file_pair_matrix_from_repository(repo, api_key)
write_matrix_to_csv_file(df, 'commit_file_pair_matrix.csv')
df = read_matrix_from_csv_file('commit_file_pair_matrix.csv')
print(df)