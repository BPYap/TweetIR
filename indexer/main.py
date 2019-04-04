from indexing import create_index, query


create_index()
results = []
search_after_id = None
while True:
    response = query(match_word="trump", search_after=search_after_id)
    temp = response['results']
    if len(temp) == 0:
        break
    results.extend(temp)
    search_after_id = response['search_after']

print(len(results))
