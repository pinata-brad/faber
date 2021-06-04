import os
import logging
logger = logging.getLogger(__name__)

class dataIO:
    """
    To enable a functions use with this class you must create the function in the local io,
    the function must be added to the catalog as 'read/write_func'
    the function must be added with the set io method which reads a dictionary that converts the
    strings in catalog to their respective functions
    """
    def __init__(self, catalog: dict):
        self.catalog = catalog
        return

    def set_io(self, io_def=None):
        """
        set the io reference dictionary
        :param io_def:
        :return:
        """
        if not io_def:
            io_def = unpack_io()
        self.reading_dict = io_def['read'].copy()
        self.writing_dict = io_def['write'].copy()
        return

    def write(self, writer: dict):
        """
        handle writing data to disk
        :param writer: a dictionary of the table name and object to write
        :return:
        """
        for k in list(writer):
            write_dict = self.catalog.copy().get(k)
            if not write_dict:
                continue
            func = self.writing_dict.get(write_dict.get('write_func'))
            if not func:
                try:
                    logger.critical(f'function {write_dict["write_func"]} not added to set_io parameter')
                    continue
                except:
                    logger.critical(f'writer not defined for {k} in catalog')
                    continue
            else:
                func(obj=writer[k], **write_dict)
        return

    def read(self, inputs):
        """
        Reads generic data from function. handles multiple data io and functions
        :param inputs: the inputs from a node
        :return: dictionary to update state in faber
        """
        updater = {}
        for k in inputs:
            read_dict = self.catalog.copy().get(k)
            if not read_dict:
                continue
            func = self.reading_dict.get(read_dict.get('read_func'))
            if not func:
                try:
                    raise NotImplementedError(f'function {read_dict["read_func"]} not added to set_io parameter')
                except:
                    raise NotImplementedError(f'reader not defined for {k} in catalog')

            updater.update({k: func(**read_dict)})
        return updater
