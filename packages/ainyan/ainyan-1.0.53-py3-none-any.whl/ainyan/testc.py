import configparser

config = configparser.ConfigParser()
config.read("jgate.ini")

# post_queries = config.options('queries')
post_queries = [key for key, value in config.items('queries')]
print(post_queries)

post_queries = config.options('queries')
for query in post_queries:
    print(query)
