from functions.logger_sec import logger_project
import requests
import os


logger=logger_project('pryecto_seguridad')

link=''
def downloader(link):

    os.makedirs('data/',exist_ok=True)

    try:
        # requesting file and saving

        req = requests.get(link)
        open('data/datos_seguridad.csv','wb').write(req.content)
        logger.info('CSV file created')

    except:
        logger.debug('Warning, the request action could not be performed')
        pass

    return


