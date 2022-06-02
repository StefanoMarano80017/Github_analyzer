from Unit_elaborazione import Analisi_sorgente

def main():

    links = ['https://raw.githubusercontent.com/SOM-Research/Gitana/master/gitana/gitana.py']
    suffixs = ['py']
    analizer = Analisi_sorgente.analyzer('prova', links, suffixs)

    analizer.analyser_files()

if __name__ == '__main__':
    main()
