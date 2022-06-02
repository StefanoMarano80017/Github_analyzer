from Broker import Query_Txt

def main():

    data = datetime.date(2017, 5, 31)
    #g = Github('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')
    #repo = g.get_repo("SOM-Research/Gitana")
    #contents = repo.get_contents("/importers/db/dbschema.py")

    #link = 'https://raw.githubusercontent.com/SOM-Research/Gitana/master/gitana/gitana.py'
    #f = requests.get(link)
    #print(f.text)
    #print(contents.decoded_content)

    #broker = Broker.Broker(token = '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', db_file='prova.db')

    #print(broker.extract_file_repo(repo))

    #prova_API.prova_loc()

    txt = Query_Txt.read_query('insert_repo', 'DB')
    print(txt)

if __name__ == '__main__':
    main()
