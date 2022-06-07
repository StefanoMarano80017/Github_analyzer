from GUI import Window_manager

from Broker import Broker
from datetime import date
from Unit_elaborazione import Controller

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def main():
    """
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
    matplotlib.use("TkAgg")
    gui = Window_manager.Window_Manager()
    gui.event_loop()
    """

    b = Broker.Broker('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', 'Util/prova.db')
    date_b = date(2014, 3, 4)
    #b.do_search(date=date_b, lang = 'python', size_max=10)

    #b.print_table_repo()
    #b.print_table_link()

    c = Controller.Controller('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', 'Util/prova.db')
    c.get_git_data(date_b, 'py', 3)
    result = c.repo_cloc()
    for res in result:
        print(res)

if __name__ == '__main__':
    main()
