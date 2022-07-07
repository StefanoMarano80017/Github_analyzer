from GUI import Window_manager
from Unit_elaborazione import Controller
from Unit_elaborazione.source_analyze import Analisi_sorgente


def main():
    Elab_cloc = Analisi_sorgente.source_analyzer()
    Elab_dens = Analisi_sorgente.density_analyzer()

    controller = Controller.Controller()
    controller.AttachElab(Elab_cloc)
    controller.AttachElab(Elab_dens)

    e = Window_manager.Event_Processor(controller)
    e.event_loop()


if __name__ == '__main__':
    main()
