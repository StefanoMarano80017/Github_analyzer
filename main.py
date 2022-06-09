from GUI import Window_manager
from Unit_elaborazione import Controller
import logging


def main():
    """
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
    matplotlib.use("TkAgg")
    gui = Window_manager.Window_Manager()
    gui.event_loop()
    """

    #w = Window_manager.Window_Manager()
    #w.event_loop()

    c = Controller.Controller('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 ', 'Util/db_prova.db')
    # c.get_git_data('created:2017-05-31 language:Python', 10)
    #c.print_repo()
    cloc_calc = c.repo_cloc()
    for cloc in cloc_calc:
        print(cloc)

    #for link in c.get_link(92966807):
     #   print(link)

    #logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    #logging.info('INFO')
    #logging.warning('WARNING')


if __name__ == '__main__':
    main()
