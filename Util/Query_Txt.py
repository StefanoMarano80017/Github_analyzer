import configparser

file_name: str = 'Util/specs.ini'


# Questa funzione ha lo scopo di rendere leggibili al db
# le operazioni di insert e di select scritte nel file specs.ini
def read_query(query_id, section_name) -> str:
    """

    :rtype: object
    """
    config = None
    try:
        config = configparser.ConfigParser()
        config.read(file_name)
    except Exception as e:
        print(e)
    finally:
        return str(config[section_name][query_id])
