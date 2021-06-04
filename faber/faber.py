from faber.dataio import dataIO
from faber.utils import *
import os
import yaml
import logging 
logger = logging.getLogger('faber')
import re

def node(func, inputs, outputs, name=None, tags=None):
    """
    """
    assert type(outputs) == list
    assert type(inputs) == list
    return {
            'function':func,
            'inputs':inputs,
            'outputs':outputs,
            'name':name,
            'tags':tags
            }

class faber:
    def __init__(self, catalog):
        self.state={}
        self.pipelines={}
        self.data_io = dataIO(catalog)

        return

    def set_state(self, state: dict):
        """
        """
        self.state = state.copy()

    def update_state(self, update: dict):

        return self.state.update(update)

    def check_state(self, node):

        if self.state:
            check_state = [i for i in node['inputs'] if i not in list(self.state)]
            logger.warning(f'inputs not in state: {check_state}')
            if check_state:
                self.update_state(self.data_io.read(node['inputs']))
            check_state = [i for i in node['inputs'] if i not in list(self.state)]
            assert not check_state, f'inputs not in state: {check_state}'
        else:
            self.update_state(self.data_io.read(node['inputs']))
            check_state = [i for i in node['inputs'] if i not in list(self.state)]
            assert not check_state, f'inputs not in state or catalog: {check_state}'

    def check_node(self, node):
        expected = ['function', 'inputs', 'outputs', 'name', 'tags']
        have = list(node)
        assert set(expected+have) == set(expected)
        return 0

    def evaluate_node(self, node):
        """

        :param self:
        :param node:
        :return:
        """
        logger.info(f'''running node: \n{show_node(node)}''')
        self.check_node(node)
        self.check_state(node)

        out=node['function'](*[self.state[i] for i in node['inputs']])
        if type(out) == tuple:
            updater = {key: value for key, value in zip(node['outputs'], out)}
        else:
            updater = {node['outputs'][0]: out}

        self.update_state(updater)
        self.data_io.write(updater)
        return 0

    def create_pipeline(self, nodes, pipe_name):
        self.pipelines[pipe_name] = nodes
        logger.info(f'Pipeline {pipe_name} created')

    def extend_pipeline(self, nodes, pipe_name):
        self.pipelines[pipe_name].extend(nodes)

    def append_pipeline(self, node, pipe_name):
        self.pipelines[pipe_name].append(node)

    def run_pipeline(self, pipe_name):
        """
        """
        for node in self.pipelines[pipe_name]:
            self.evaluate_node(node)

    def set_io(self, io_def):
        self.data_io.set_io(io_def)



















