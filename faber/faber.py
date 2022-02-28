"""
core logic for faber
"""
import logging
from typing import Union
from faber.dataio import dataIO
from faber.utils import show_node

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def node(func, inputs, outputs, name=None, tags=None):
    """
    defines the node from a function adn list of inputs
    """
    assert isinstance(outputs, list)
    assert isinstance(inputs, list)
    return {
            'function':func,
            'inputs':inputs,
            'outputs':outputs,
            'name':name,
            'tags':tags
            }

class Faber:
    """
    faber class
    """
    def __init__(self, catalog):
        """
        initialise the class
        """
        self.state={}
        self.pipelines={}
        self.data_io = dataIO(catalog)

    def set_io(self, io_def):
        """
        define connectors to use when loading data
        """
        self.data_io.set_io(io_def)

    def set_state(self, state: dict):
        """
        set the state loaded by build_catalog into the faber class
        """
        self.state = state.copy()

    def update_state(self, update: dict):
        """
        updates the project with latest loaded data from function execution
        """
        return self.state.update(update)

    def check_state(self, node):
        """
        checks whether the inputs are defined or loads them from the catalog
        """
        if self.state:
            check_state = [i for i in node['inputs'] if i not in list(self.state)]
            if check_state:
                self.update_state(self.data_io.read(check_state))
            else:
                logger.warning('inputs not in state: %s', check_state)
            check_state = [i for i in node['inputs'] if i not in list(self.state)]
            assert not check_state, f'inputs not in state: {check_state}'
        else:
            self.update_state(self.data_io.read(node['inputs']))
            check_state = [i for i in node['inputs'] if i not in list(self.state)]
            assert not check_state, f'inputs not in state or catalog: {check_state}'

    @staticmethod
    def check_node(node):
        """
        checks the node contains all the relelvent info
        """
        expected = ['function', 'inputs', 'outputs', 'name', 'tags']
        have = list(node)
        assert set(expected+have) == set(expected)
        return 0

    def evaluate_node(self, node):
        """
        executes the function contained within the node using the defined inputs and outputs
        :param self:
        :param node:
        :return:
        """
        logger.info('''running node: \n %s''', show_node(node))
        self.check_node(node)
        self.check_state(node)

        out=node['function'](*[self.state[i] for i in node['inputs']])
        if isinstance(out, tuple):
            updater = {key: value for key, value in zip(node['outputs'], out)}
        else:
            updater = {node['outputs'][0]: out}

        self.update_state(updater)
        self.data_io.write(updater)
        return 0

    def create_pipeline(self, nodes, pipe_name):
        """
        create hte pipeline in the faber class
        """
        self.pipelines[pipe_name] = nodes
        logger.info('Pipeline %s created', pipe_name)

    def extend_pipeline(self, nodes, pipe_name):
        """
        extend the pipeline by multiple node in the faber class
        """
        self.pipelines[pipe_name].extend(nodes)

    def append_pipeline(self, node, pipe_name):
        """
        extend the pipeline by 1 node in the faber class
        """
        self.pipelines[pipe_name].append(node)

    def run_pipeline(self, pipe_name, tags: Union[list, None] = None):
        """
        execute the given pipeline
        """
        for node in self.pipelines[pipe_name]:
            if self.check_tags(node, tags):
                self.evaluate_node(node)
            else:
                pass

    def run(self, tags: Union[list, None]=None):
        """
        run all pipelines loaded
        """
        for pipe_line in self.pipelines:
            self.run_pipeline(pipe_line, tags)

    @staticmethod
    def check_tags(node,tags):
        """
        def test():
        #     case1: no tags and no nodes
        node = {'func':'f','inputs':['i1'],'outputs':['o2'], 'tags':None}
        tags=None
        assert check_tags(node,tags) == True

        #     case2: no tags and node tags
        node = {'func':'f','inputs':['i1'],'outputs':['o2'], 'tags':['tag1']}
        tags=None
        assert check_tags(node,tags) == True

        #     case3: tags and no node
        node = {'func':'f','inputs':['i1'],'outputs':['o2'], 'tags':None}
        tags=['tag1']
        assert check_tags(node,tags) == False

        #     case4: tags and matching node tag
        node = {'func':'f','inputs':['i1'],'outputs':['o2'], 'tags':['tag1','tag2']}
        tags=['tag1']
        assert check_tags(node,tags) == True

        #     case5: tags and non-matching node tag
        node = {'func':'f','inputs':['i1'],'outputs':['o2'], 'tags':['tag3','tag2']}
        tags=['tag1']
        assert check_tags(node,tags) == False

        #     case6: bad tags and  node tag
        node = {'func':'f','inputs':['i1'],'outputs':['o2'], 'tags':['tag3','tag2']}
        tags='tag1'
        assert check_tags(node,tags) == False
        """
        if isinstance(tags,list):
            if isinstance(node['tags'], list):
                set(node['tags'])
                return len(set(tags) & set(node['tags']))>0
            else:
                return False
        elif isinstance(tags, str):
            return False
        else:
            return True
