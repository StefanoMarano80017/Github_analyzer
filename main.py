from GUI import Window_manager

def main():
    """
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
    matplotlib.use("TkAgg")
    gui = Window_manager.Window_Manager()
    gui.event_loop()
    """

    w = Window_manager.Window_Manager()
    w.event_loop()

if __name__ == '__main__':
    main()
