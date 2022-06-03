from Unit_elaborazione import Analisi_sorgente
import prova_API

def main():

    links = ['https://raw.githubusercontent.com/SOM-Research/Gitana/master/gitana/gitana.py', 'https://raw.githubusercontent.com/rrwick/LinesOfCodeCounter/master/lines_of_code_counter.py']
    suffixs = ['.py', '.py']
    analizer = Analisi_sorgente.analyzer('prova', links, suffixs)

    analizer.cloc_files()


if __name__ == '__main__':
    main()
