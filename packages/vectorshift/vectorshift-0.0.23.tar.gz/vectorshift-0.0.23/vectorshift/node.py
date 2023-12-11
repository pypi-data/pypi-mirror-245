# functionality defining the shape and properties of computation nodes, and how
# they connect to each other in pipelines
from abc import ABC, abstractclassmethod
import json
import re
import requests

import vectorshift
from vectorshift.consts import *
from vectorshift.pipeline_data_types import *

# A parent class for all nodes. Shouldn't be initialized by the user directly.
# Each node subclasses NodeTemplate and takes in class-specific parameters 
# depending on what the node does. Node classes below are organized by their
# order and structure of appearance in the no-code editor.
class NodeTemplate(ABC):
    # TODO: think about where we might want to use @property.
    def __init__(self):
        # Each node has a certain type, also called an "ID" in Mongo. The _id
        # of the node is formed by appending a counter to the node type.
        self.node_type:str = None
        self._id:str = None
        # Every node has zero or more inputs or outputs. Each output itself 
        # is a list (in case one input takes in/aggregates multiple outputs).
        # In some cases, nodes may take in either NodeOutputs *or* strings as
        # inputs (e.g. for string parameters). In that case, the current 
        # pattern is to designate an additional dictionary self._input_strs.
        self._inputs:dict[str, list[NodeOutput]] = {}
        
    # Dump the JSON
    def __repr__(self): 
        return f'<{self.__class__.__name__} with JSON representation\n\
            {json.dumps(self.to_json_rep())}\n>'
    
    # Print the node in a style mimicking how you could construct the node
    # using the class. Indicate the ID in parentheses.
    def __str__(self):
        init_args_str = ',\n\t'.join(self.init_args_strs())
        return f'(node id {self._id})={self.__class__.__name__}(\n\
\t{init_args_str}\n)'
    
    # Essentially the same as __str__, but printed in such a way that it can
    # be run as Python code.
    def construction_str(self):
        init_args_str = ',\n\t'.join(self.init_args_strs())
        return f"{self._id.replace('-', '_')}={self.__class__.__name__}(\n\
\t{init_args_str}\n)"
        
    def init_args_strs(self) -> list[str]: 
        raise NotImplementedError('Subclasses should implement this!')

    # Inputs are a dictionary of NodeOutputs keyed by input fields (the in-edge 
    # labels in the no-code graph/the target handle for the node's in-edge).
    def inputs(self) -> dict[str, list['NodeOutput']]: return self._inputs

    def set_input(self, input_name:str, input:'NodeOutput'):
        if input_name not in self._inputs.keys():
            # this shouldn't actually be reached currently, because missing 
            # inputs should cause the typechecker function to throw errors 
            print(f'WARNING: {input_name} not currently in node\'s inputs.')
        self._inputs[input_name] = input
    
    # Outputs should be a dictionary of NodeOutputs keyed by output fields (the
    # out-edge labels/the source handle for the node's out-edge). Invariant: 
    # a key should equal the corresponding value's output_field.
    # For syntactic sugar, class-specific methods can also return specific 
    # outputs rather than the entire dict, e.g. the method "output()" that 
    # directly gives the NodeOutput object for nodes that only have one output.
    def outputs(self) -> dict[str, 'NodeOutput']: 
        raise NotImplementedError('Subclasses should implement this!')

    # The dictionary that corresponds with the JSON serialization of the node. 
    # This should return a subset of how a node object is stored as part of a
    # pipeline in Mongo, specifically, the following attributes: type, id, and
    # data (and all subfields therein). This should only be called after an id
    # has been assigned to the node.
    # NB: the JSON fields id/data.id and type/data.nodeType are the same.
    @abstractclassmethod
    def to_json_rep(self) -> dict:
        # If the node references a user-defined object that lives on the VS
        # platform (other pipelines, integrations, files, vectorstores,
        # transformations), calling this function will involve an API call
        # to get the details of that user-defined object.
        # TODO: could refactor the setting _id and node_type logic to here.
        raise NotImplementedError('Subclasses should implement this!')
    
    # From a Python dict representing how a node is stored in JSON, create a
    # node object. IMPORTANTLY, this does NOT initialize the _inputs param 
    # with NodeOutput values (and thus doesn't perform typechecks); we expect 
    # NodeOutputs to be inserted post_hoc, and assume they're valid.
    @staticmethod
    @abstractclassmethod
    def _from_json_rep(json_data:dict) -> 'NodeTemplate':
        _ = json_data # if linter complains
        raise NotImplementedError('Subclasses should implement this!')
    
    @classmethod 
    def from_json_rep(cls, json_data: dict) -> 'NodeTemplate':
        n:NodeTemplate = cls._from_json_rep(json_data)
        n._id = json_data['id']
        # Clear the dummy entries in _inputs (some inputs may be strings, in 
        # which case they would be non-None at this point)
        filtered_inputs = {}
        for k, v in n._inputs.items():
            filtered_inputs[k] = [i for i in v if i is not None]
        n._inputs = filtered_inputs
        return n

# A wrapper class for outputs from nodes, for basic "type"-checks and to figure
# out how nodes connect to each other. NOT the same as OutputNode, which is 
# a node that represents the final result of a pipeline.
class NodeOutput:
    def __init__(self, source:NodeTemplate, output_field:str, 
                 output_data_type:PipelineDataType):
        # The Node object producing this output.
        self.source = source
        # The specific output field from the source node (the node handle).
        self.output_field = output_field
        # A string roughly corresponding to the output type. (Strings are 
        # flimsy, but they will do the job.)
        self.output_data_type = output_data_type

    def __repr__(self):
        return f'<NodeOutput of type {self.output_data_type} from \
            {self.source.__class__.__name__} (node id {self.source._id}), \
            output field {self.output_field}>'
    
    def __str__(self):
        return format_node_output_with_name('<NodeOutput>', self)

def format_node_output(output:NodeOutput) -> str:
    return f"(node id {output.source._id}).outputs()['{output.output_field}']"

# Helper functions for printing out NodeOutput sources in string representations
def format_node_output_with_name (output_name:str, output:NodeOutput) -> str: 
    return f"{output_name}={format_node_output(output)}']"

def format_node_output_dict (outputs:dict[str, list[NodeOutput]]) -> str:
   d = {
        k: f"(node id {v[0].source._id}).outputs()['{v[0].output_field}']"
        for k, v in outputs.items()
    }
   return d.__str__().replace('"', '')


# Typecheck nodes upon manual initialization. (When loading pipelines from 
# JSON, we don't call this function.)
# The below code differs from the API implementation in a few ways:
# - Nodes are NodeTemplate objects, not JSON/dicts.
# - Due to the nature of how pipelines are created in the SDK by chaining 
#   earlier nodes' NodeOutputs into the constructors of subsequent nodes, 
#   we already have information about the types of the node's in-edges (i.e. 
#   the output types of the node's in-neighbors) we can perform validation and
#   determine the node's output type (if needed) in one go.
# - We don't return anything here. The node's output types are set elsewhere.
def check_type(name:str, t:PipelineDataType, expected_t:PipelineDataType):
    if not t.intersects(expected_t):
        raise ValueError(f'Invalid input type to {name}: expected {expected_t}, got {t}')
    elif not t.is_subset(expected_t):
        print(f'WARNING: {name} received input type {t}, which may be incompatible with expected type {expected_t}')
    return

# Check the well-formedness of the types of all NodeTemplate inputs passed into
# a node. Assumes the inputs must have been initialized (i.e. the node should 
# not have any empty inputs).
# Note: we could also make this a method within NodeTemplate.
def validate_node_inputs(node: NodeTemplate) -> None:
    node_type = node.node_type
    inputs = node._inputs
    if not node_type:
        raise Exception('Node type not specified')

    # defensive programming: check against the node_type and the class
    match node_type:
        case 'customInput':
            assert(type(node) == InputNode)
        case 'customOutput':
            assert(type(node) == OutputNode)
            assert(len(inputs['value']) == 1)
            input = inputs['value'][0]
            if node.output_type == 'file':
                check_type('OutputNode', input.output_data_type, FILE_TYPE)
            elif node.output_type in ['text', 'formatted_text']:
                check_type('OutputNode', input.output_data_type, TEXT_TYPE)
        case 'text':
            assert(type(node) == TextNode)
            for var_name, v in inputs.items():
                assert(len(v) == 1)
                check_type(f'TextNode input {var_name}', v[0].output_data_type, TEXT_TYPE)
        case 'file':
            assert(type(node) == FileNode)
        case 'pipeline':
            assert(type(node) == PipelineNode)
            pipeline_inputs = node.pipeline_json['inputs'].values() 
            # Overall pipeline inputs and outputs are, for now, only of
            # text or file types.
            for i in pipeline_inputs:
                # this shouldn't happen as there's a check in the constructor
                # that the NodeOutput keys match the 'name' fields of each
                # input's JSON representation
                input_name = i['name']
                if input_name not in inputs.keys():
                    raise ValueError(f'PipelineNode: missing input {input_name}.')
                assert(len(inputs[input_name]) == 1)
                node_input = inputs[input_name][0]
                if i['type'] == 'Text':
                    check_type(f'PipelineNode input {input_name}', node_input.output_data_type, TEXT_TYPE)
                elif i['type'] == 'File':
                    check_type(f'PipelineNode input {input_name}', node_input.output_data_type, FILE_TYPE)
                else:
                    raise ValueError(f"PipelineNode: invalid input type input {input_name}: {i['type']}") 
        case 'integration':
            # TODO: start storing types with integration functions
            # Using AnyType() for now
            for input_name, l in inputs.items():
                for o in l:
                    check_type(f'Integration node input {input_name}', o.output_data_type, AnyType())
        case 'transformation':
            assert(type(node) == TransformationNode)
            # TODO: start storing types with transformations
            # Using AnyType() for now
            for input_name, l in inputs.items():
                for o in l:
                    check_type(f'TransformationNode input {input_name}', o.output_data_type, AnyType())
        case 'fileSave':
            assert(type(node) == FileSaveNode)
            # inputs to fileSave should be of file or list[file] type
            assert(len(inputs['name']) == 1)
            check_type('FileSaveNode input name', inputs['name'][0].output_data_type, TEXT_TYPE)
            for o in inputs['files']:
                check_type('FileSaveNode input files', o.output_data_type, UnionType(FILE_TYPE, ListType(FILE_TYPE)))
        case 'llmOpenAI':
            assert(type(node) == OpenAILLMNode)
            assert(len(inputs['system']) == 1)
            assert(len(inputs['prompt']) == 1)
            check_type('OpenAILLMNode input system', inputs['system'][0].output_data_type, TEXT_TYPE)
            check_type('OpenAILLMNode input prompt', inputs['prompt'][0].output_data_type, TEXT_TYPE)
        case 'llmAnthropic':
            assert(type(node) == AnthropicLLMNode)
            assert(len(inputs['prompt']) == 1)
            check_type('AnthropicLLMNode input prompt', inputs['prompt'][0].output_data_type, TEXT_TYPE)
        case 'imageGen':
            assert(type(node) == ImageGenNode)
            assert(len(inputs['prompt']) == 1)
            check_type('ImageGenNode input prompt', inputs['prompt'][0].output_data_type, TEXT_TYPE)
        case 'speechToText':
            assert(type(node) == SpeechToTextNode)
            assert(len(inputs['audio']) == 1)
            check_type('ImageGenNode input audio', inputs['audio'][0].output_data_type, AUDIO_FILE_TYPE)
        case 'vectorDBLoader':
            assert(type(node) == VectorDBLoaderNode)
            for o in inputs['documents']:
                check_type('VectorDBLoaderNode input documents', o.output_data_type, TEXT_TYPE)
        case 'vectorDBReader':
            assert(type(node) == VectorDBReaderNode)
            assert(len(inputs['query']) == 1)
            assert(len(inputs['database']) == 1)
            check_type('VectorDBReaderNode input query', inputs['query'][0].output_data_type, TEXT_TYPE)
            check_type('VectorDBReaderNode input database', inputs['database'][0].output_data_type, VECTOR_DB_TYPE)
        case 'vectorStore':
            assert(type(node) == VectorStoreNode)
            assert(len(inputs['query']) == 1)
            check_type('VectorStoreNode input query', inputs['query'][0].output_data_type, TEXT_TYPE)
        case 'chatMemory':
            assert(type(node) == ChatMemoryNode)
        case 'condition':
            assert(type(node) == LogicConditionNode)
            # TODO: refactor according to Alex's ultimate implementation in 
            # the API. For now, we just mandate that any input names that 
            # appear in a condition are text.
            input_names = inputs.keys()
            conditional_input_names = set()
            for c in node.conditions:
                for n in input_names:
                    if n in c[0]:
                        conditional_input_names.add(n)
            for cnd_input_name in list(conditional_input_names):
                check_type(f'LogicConditionNode input {cnd_input_name}', inputs[cnd_input_name][0].output_data_type, TEXT_TYPE)
        case 'merge':
            assert(type(node) == LogicMergeNode)
        # TODO: TBD on typechecking for agents
        case 'agent':
            assert(type(node) == AgentNode)
            agent_inputs = node.agent_json['inputs'].values()
            for input in agent_inputs:
                input_name = input['name']
                if input_name not in inputs.keys():
                    raise ValueError(f'AgentNode missing input {input_name}.')
                assert(len(inputs[input_name]) == 1)
                node_input = inputs[input_name][0]
                if input['type'] == 'Text':
                    check_type(f'AgentNode input {input_name}', node_input.output_data_type, TEXT_TYPE)
                elif input['type'] == 'File':
                    check_type(f'AgentNode input {input_name}', node_input.output_data_type, FILE_TYPE)
                else:
                    raise ValueError(f"Invalid input type to AgentNode input {input_name}: {input['type']}")

        case 'splitText':
            assert(type(node) == SplitTextNode)
            assert(len(inputs['text']) == 1)
            check_type('SplitTextNode input text', inputs['text'][0].output_data_type, TEXT_TYPE)
            agent_inputs = node.agent_json['inputs'].values() 
            # Overall pipeline inputs and outputs are, for now, only of
            # text or file types.
            for i in agent_inputs:
                # this shouldn't happen as there's a check in the constructor
                # that the NodeOutput keys match the 'name' fields of each
                # input's JSON representation
                input_name = i['name']
                if input_name not in inputs.keys():
                    raise ValueError(f'AgentNode missing input {input_name}.')
                assert(len(inputs[input_name]) == 1)
                node_input = inputs[input_name][0]
                if i['type'] == 'Text':
                    check_type(f'AgentNode input {input_name}', node_input.output_data_type, TEXT_TYPE)
                elif i['type'] == 'File':
                    check_type(f'AgentNode input {input_name}', node_input.output_data_type, FILE_TYPE)
                else:
                    raise ValueError(f"Invalid input type to AgentNode input {input_name}: {i['type']}") 
        case 'dataLoader':
            # Add asserts for checking that the right input names are in inputs,
            # as it's possible to create a DataLoaderNode directly with
            # possibly-arbitrary input names.
            assert(type(node) == DataLoaderNode or issubclass(type(node), DataLoaderNode))
            match node.loader_type:
                case 'File':
                    assert('file' in inputs and len(inputs['file']) == 1)
                    check_type(
                        'File loader node', 
                        inputs['file'][0].output_data_type, 
                        UnionType(
                            FILE_TYPE, ListType(FILE_TYPE), 
                            TEXT_TYPE, ListType(TEXT_TYPE)
                        )
                    )
                case 'CSV Query':
                    assert('query' in inputs and len(inputs['query']) == 1)
                    assert('csv' in inputs and len(inputs['csv']) == 1)
                    check_type(
                        'CSV Query loader node input query', 
                        inputs['query'][0].output_data_type, 
                        TEXT_TYPE
                    )
                    check_type(
                        'CSV Query loader node input csv',
                        inputs['csv'][0].output_data_type,
                        CSV_FILE_TYPE
                    )
                case 'URL':
                    assert('url' in inputs and len(inputs['url']) == 1)
                    check_type(
                        'URL loader node input url',
                        inputs['url'][0].output_data_type,
                        URL_TYPE
                    )
                case 'Wikipedia':
                    assert('query' in inputs and len(inputs['query']) == 1)
                    check_type(
                        'Wikipedia loader node input query', 
                        inputs['query'][0].output_data_type, 
                        TEXT_TYPE
                    )
                case 'YouTube':
                    assert('url' in inputs and len(inputs['url']) == 1)
                    check_type(
                        'YouTube loader node input url',
                        inputs['url'][0].output_data_type,
                        UnionType(URL_TYPE, ListType(URL_TYPE))
                    )
                case 'Arxiv':
                    assert('query' in inputs and len(inputs['query']) == 1)
                    check_type(
                        'Arxiv loader node input query', 
                        inputs['query'][0].output_data_type, 
                        TEXT_TYPE
                    )
                case 'SerpAPI':
                    assert('apiKey' in inputs and len(inputs['apiKey']) == 1)
                    assert('query' in inputs and len(inputs['query']) == 1)
                    check_type(
                        'SerpAPI loader node input apiKey', 
                        inputs['apiKey'][0].output_data_type, 
                        TEXT_TYPE
                    )
                    check_type(
                        'SerpAPI loader node input query',
                        inputs['query'][0].output_data_type,
                        TEXT_TYPE
                    )
                case 'Git':
                    assert('repo' in inputs and len(inputs['repo']) == 1)
                    check_type(
                        'Git loader node input repo',
                        inputs['repo'][0].output_data_type,
                        URL_TYPE
                    )
                case 'Notion':
                    assert('token' in inputs and len(inputs['token']) == 1)
                    assert('database' in inputs and len(inputs['database']) == 1)
                    check_type(
                        'Notion loader node input token', 
                        inputs['token'][0].output_data_type, 
                        TEXT_TYPE
                    )
                    check_type(
                        'Notion loader node input database',
                        inputs['database'][0].output_data_type,
                        TEXT_TYPE
                    )
                case 'Confluence':
                    assert('username' in inputs and len(inputs['username']) == 1)
                    assert('apiKey' in inputs and len(inputs['apiKey']) == 1)
                    assert('url' in inputs and len(inputs['url']) == 1)
                    check_type(
                        'Confluence loader node input username', 
                        inputs['username'][0].output_data_type, 
                        TEXT_TYPE
                    )
                    check_type(
                        'Confluence loader node input apiKey',
                        inputs['apiKey'][0].output_data_type,
                        TEXT_TYPE
                    )
                    check_type(
                        'Confluence loader node input url', 
                        inputs['url'][0].output_data_type, 
                        TEXT_TYPE
                    )
        case _:
            raise ValueError(f'Unrecognized node type value {node_type} (node class {type(node)})')
    return

###############################################################################
# HOME                                                                        #
###############################################################################

# Input nodes themselves don't have inputs; they define the start of a pipeline.
class InputNode(NodeTemplate):
    def __init__(self, name:str, input_type:str, **kwargs):
        super().__init__()
        self.node_type = 'customInput'
        self.name = name
        # Text or File
        if input_type not in INPUT_NODE_TYPES:
            raise ValueError(f'InputNode: input type {input_type} not supported.')
        self.input_type = input_type
        # InputNodes themselves don't take inputs
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)

    def init_args_strs(self):
        return [
            f"name='{self.name}'", 
            f"input_type='{self.input_type}'"
        ]
        
    def output(self) -> NodeOutput:
        # Input nodes can only return files or text for now
        output_data_type = FILE_TYPE if self.input_type == 'file' else TEXT_TYPE
        return NodeOutput(
            source=self, 
            output_field='value', 
            output_data_type=output_data_type
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
        
    def to_json_rep(self):
        # TODO: category and task_name can probably be made into class variables too.
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'inputName': self.name,
                'inputType': self.input_type.capitalize(),
                'category': 'input',
                'task_name': 'input'
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'InputNode':
        return InputNode(
            name=json_data['data']['inputName'], 
            input_type=json_data['data']['inputType'].lower(),
            skip_typecheck=True
        )

# Outputs are the end of the pipeline and so only take inputs.
class OutputNode(NodeTemplate):
    def __init__(self, name:str, output_type:str, input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = 'customOutput'
        self.name = name
        # Text or File
        if not output_type.lower() in OUTPUT_NODE_TYPES:
            raise ValueError(f'OutputNode: output type {output_type} not supported.')
        self.output_type = output_type
        self._inputs = {'value': [input]}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)

    def init_args_strs(self):
        input = self._inputs['value'][0]
        return [
            f"name='{self.name}'", 
            f"output_type='{self.output_type}'",
            format_node_output_with_name('input', input)
        ]

    def outputs(self): return None
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'outputName': self.name,
                'outputType': self.output_type.capitalize(),
                'category': 'output',
                'task_name': 'output'
            }
        }
        
    @staticmethod 
    def _from_json_rep(json_data:dict) -> 'OutputNode':
        return OutputNode(
            name=json_data['data']['outputName'], 
            output_type=json_data['data']['outputType'].lower(),
            input=None,
            skip_typecheck=True
        )
    
# Text data. This is possibly even a little redundant because we can pass in
# plaintext inputs as additional params to nodes (without instantiating them
# as separate nodes) through code. Right now though I'm trying to get a 1:1 
# correspondance between no-code and code construction; we can discuss this.
class TextNode(NodeTemplate):
    # Text nodes can either just be blocks of text in themselves, or also take
    # other text nodes as inputs (e.g. with text variables like {{Context}}, 
    # {{Task}}). In the latter case, an additional argument text_inputs should
    # be passed in as a dict of input variables to Outputs.
    def __init__(self, text:str, text_inputs:dict[str, NodeOutput] = None, **kwargs):
        super().__init__()
        self.node_type = 'text'
        self.text = text
        # if there are required inputs, they should be of the form {{}} - each
        # of them is a text variable
        text_vars = re.findall(r'\{\{([^{}]+)\}\}', self.text)
        text_vars = [v.strip() for v in text_vars]
        self.text_vars = []
        # remove duplicates while preserving order
        [self.text_vars.append(v) for v in text_vars if v not in self.text_vars]
        
        # if there are variables, we expect them to be matched with inputs
        # they should be passed in a dictionary with the
        # arg name text_inputs. E.g. {"Context": ..., "Task": ...}
        if text_inputs:
            if type(text_inputs) != dict:
                raise TypeError('text_inputs must be a dictionary of text variables to node outputs.')
            num_inputs = len(text_inputs.keys())
            num_vars = len(self.text_vars)
            if num_inputs != num_vars:
                raise ValueError(f'TextNode: number of text inputs ({num_inputs}) does not match number of text variables ({num_vars}).')
            if sorted(list(set(text_inputs.keys()))) != sorted(self.text_vars):
                raise ValueError('TextNode: names of text inputs and text variables do not match.')
            # wrap each NodeOutput into a singleton list to fit the type
            self._inputs = {k: [v] for k, v in text_inputs.items()}
        else:
            if len(self.text_vars) > 0:
                raise ValueError('TextNode: text inputs must be passed in if there are text variables.')
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
            
    def init_args_strs(self):
        return [
            f"text='{self.text}'".replace('\n', '\\n'),
            f"text_inputs={format_node_output_dict(self._inputs)}"
        ]
            
    def output(self) -> NodeOutput: 
        return NodeOutput(
            source=self, 
            output_field='output', 
            output_data_type=TEXT_TYPE
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
        
    def to_json_rep(self):
        input_names = self.text_vars if len(self.text_vars) > 0 else None
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'text': self.text,
                'inputNames': input_names,
                'formatText': True,
                'category': 'task',
                'task_name': 'text',
            } 
        }
        
    def _from_json_rep(json_data:dict) -> 'TextNode':
        text_inputs = None
        if json_data['data']['inputNames']:
            text_inputs = {}
            for name in json_data['data']['inputNames']:
                text_inputs[name] = None
        return TextNode(
            text=json_data['data']['text'],
            text_inputs=text_inputs,
            skip_typecheck=True
        )

# Nodes representing file data, taking no inputs.
### USES USER-CREATED OBJECT - see comments in VectorStoreNode
class FileNode(NodeTemplate):
    def __init__(self, file_names:list[str], 
                 public_key:str=None, private_key:str=None, **kwargs):
        super().__init__()
        self.node_type = 'file'
        if file_names is None or file_names == []:
            raise ValueError('FileNode: file names must be specified.')
        self.file_names = file_names
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key
        # files take no inputs
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)

    def init_args_strs(self):
        return [
            f'file_names={self.file_names}',
            f"public_key='{self._public_key}'",
            f"private_key='{self._private_key}'"
        ]
    
    def set_api_key(self, public_key:str, private_key:str):
        self._public_key = public_key
        self._private_key = private_key

    def output(self) -> NodeOutput:
        return NodeOutput(
            source=self,
            output_field='files',
            output_data_type=ListType(FILE_TYPE)
        )

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        if self._public_key is None or self._private_key is None:
            raise ValueError('FileNode: API key required to fetch files.')
        # Note: there's currently no way in the API code to get files owned 
        # by another user, nor is there a way to get files by their ID.
        response = requests.get(
            API_FILE_FETCH_ENDPOINT,
            data={
                'file_names': self.file_names,
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error fetching files: {response.text}')
        # list of JSONs for each file
        files_json = response.json()
        return {
            'id': self._id, 
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'selectedFiles': files_json, 
                'category': 'task',
                'task_name': 'file'
            }
        }

    @staticmethod 
    def _from_json_rep(json_data:dict) -> 'FileNode':
        file_names = [file_data['name'] for file_data in json_data['data']['selectedFiles']]
        return FileNode(
            file_names=file_names,
            skip_typecheck=True
        )

# Nodes representing entire other pipelines, a powerful tool for abstraction.
# When the node is executed, the pipeline it represents is executed with the
# supplied inputs, and the overall pipeline's output becomes the node's output.
### USES USER-CREATED OBJECT - see comments in VectorStoreNode
# TODO: We could also create (via another class?) a way to take in an existing
# Pipeline object into the constructor.
class PipelineNode(NodeTemplate):
    def __init__(self, pipeline_id:str=None, pipeline_name:str=None, 
                 inputs=dict[str, NodeOutput],
                 username:str=None, org_name:str=None,
                 public_key:str=None, private_key:str=None, **kwargs):
        super().__init__()
        self.node_type = 'pipeline'
        if pipeline_name is None and pipeline_id is None:
            raise ValueError('PipelineNode: either the pipeline ID or name should be specified.')
        self.pipeline_id = pipeline_id 
        self.pipeline_name = pipeline_name 
        self.username = username
        self.org_name = org_name 
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key
        # We'd like to know what the input and output names are upon 
        # initialization so we can validate that the inputs dict matches up.
        # So the API call to get the pipeline JSON is located in the
        # constructor here (compare to other nodes, where it's in to_json_rep)
        if self._public_key is None or self._private_key is None:
            raise ValueError('PipelineNode: API key required to fetch pipeline.')
        response = requests.get(
            API_PIPELINE_FETCH_ENDPOINT,
            data={
                'pipeline_id': pipeline_id,
                'pipeline_name': pipeline_name,
                'username': username,
                'org_name': org_name,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        # No need to construct a Pipeline object here.
        self.pipeline_json:dict = response.json()
        self.pipeline_id = self.pipeline_json['id']
        self.pipeline_name = self.pipeline_json['name']
        # The list of inputs provided should have keys matching the input names
        # defined by the integration function
        input_names = [
            i['name'] for i in self.pipeline_json['inputs'].values()
        ]
        if sorted(list(inputs.keys())) != sorted(input_names):
            raise ValueError(f'PipelineNode: inputs do not match expected input names: expected f{input_names}')
        
        self.batch_mode = kwargs.get('batch_mode', False)

        self._inputs = {
            input_name: [inputs[input_name]] for input_name in input_names
        }

        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    @staticmethod
    def from_pipeline_obj(pipeline_obj, 
                          inputs=dict[str, NodeOutput],
                          public_key=None, private_key=None) -> 'PipelineNode':
        if not pipeline_obj.id:
            print('Pipeline object does not contain a required ID, which likely means that the pipeline has not yet been saved. Attempting to save the pipeline...')
            pipeline_obj.save(public_key, private_key)
            print('Pipeline object successfully saved.')
        # This is inefficient right now, since we save (write to Mongo) and 
        # then immediately query the object (read from Mongo) in the 
        # constructor.
        return PipelineNode(
            pipeline_id=pipeline_obj.id,
            pipeline_name=pipeline_obj.name,
            inputs=inputs,
            public_key=public_key, 
            private_key=private_key
        )

    def init_args_strs(self):
        return [
            f"pipeline_id='{self.pipeline_id}'",
            f"pipeline_name='{self.pipeline_name}'",
            f'inputs={format_node_output_dict(self._inputs)}',
            f"username='{self.username}'",
            f"org_name='{self.org_name}'",
            f"public_key='{self._public_key}'",
            f"private_key='{self._private_key}'",
            f'batch_mode={self.batch_mode}'
        ]

    def set_api_key(self, public_key:str, private_key:str) -> None:
        self._public_key = public_key
        self._private_key = private_key

    def outputs(self):
        os = {}
        for o in self.pipeline_json['outputs'].values():
            output_field = o['name']
            # Pipelines can only return files or text for now
            # note: these correspond with how the output type for an OutputNode
            # is stored in Mongo, which is capitalized 
            output_data_type = None
            if o['type'] == 'File':
                output_data_type = FILE_TYPE 
            elif o['type'] in ['Text', 'Formatted Text']:
                output_data_type = TEXT_TYPE 
            else:
                raise ValueError(f"PipelineNode: invalid pipeline output type {o['type']}")
            os[output_field] = NodeOutput(
                source=self, 
                output_field=output_field, 
                output_data_type=output_data_type
            )
        return os

    def to_json_rep(self):
        pipeline_field_json = {
            # TODO: To my knowledge there is no way for the API to currently
            # return the "category" of a pipeline (favorite, my, imported etc.)
            # But this is stored in a pipeline node's representation as-is 
            # right now. For now I'm just excluding the field, as it doesn't 
            # seem to be used.
            'id': self.pipeline_json['id'],
            'name': self.pipeline_json['name'],
            'inputs': self.pipeline_json['inputs'],
            'outputs': self.pipeline_json['outputs'],
            # TODO: we just use the name as a placeholder; if this field is 
            # important we'll have to figure out a way to determine whether or
            # not the user/org name in this pipeline is different from the 
            # user/org name of whoever is writing this code (perhaps through
            # the Config class?). Same issue in TransformationNode.
            'displayName': self.pipeline_json['name']
        }

        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'pipeline': pipeline_field_json,
                'batchMode': self.batch_mode,
                'category': 'pipeline',
                'task_name': 'pipeline'
            }
        }

    @staticmethod
    def _from_json_rep(json_data:dict) -> 'PipelineNode':
        return PipelineNode(
            pipeline_id=json_data['data']['pipeline']['id'],
            pipeline_name=json_data['data']['pipeline']['name'],
            # We don't have a way to recover the username/org name, or the 
            # API key
            inputs={
                i['name']: [None]
                for i in json_data['data']['pipeline']['inputs'].values()
            },
            skip_typecheck=True
        )
    
# Integrations with third parties.
### USES USER-CREATED OBJECTS - see comments in VectorStoreNode
class IntegrationNode(NodeTemplate):
    def __init__(self, integration:str, integration_name:str, function:str, 
                 inputs=dict[str, list[NodeOutput]],
                 public_key:str=None, private_key:str=None, **kwargs):
        super().__init__()
        self.node_type = 'integration'
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key

        # The specific integration is stored in two sub-fields under the 
        # data field in the node's JSON representation. One field contains 
        # details of the integration itself, which requires an API call to
        # retrieve the integration object from Mongo. The other contains 
        # details of the function to run with the integration, which defines
        # the inputs/outputs of the node and can be deduced from the 
        # constructor arguments provided.
        if integration not in INTEGRATION_PARAMS.keys():
            raise ValueError(f'IntegrationNode: invalid integration {integration}.')
        if function not in INTEGRATION_PARAMS[integration].keys():
            raise ValueError(f'IntegrationNode: invalid function {function} for integration {integration}.')
        self.integration = integration 
        self.integration_name = integration_name
        self.function = function
        self.function_params = INTEGRATION_PARAMS[self.integration][self.function]
        # add the function name to the function params
        self.function_params['name'] = self.function

        # The list of inputs provided should have keys matching the input names
        # defined by the integration function. 
        # Note: each input to an integration node could be a list of 
        # NodeOutputs (multiple in-edges to a node's input field, e.g. saving
        # multiple files to Drive at once). This is different from the input
        # structure for pipeline and transformation nodes.
        input_names = [
            i['name'] for i in self.function_params['inputs']
        ]
        if sorted(list(inputs.keys())) != sorted(input_names):
            raise ValueError(f'IntegrationNode: inputs do not match expected input names: expected {input_names}')
        
        # Specific integrations require additional argument parameters passed
        # in via the constructor rather than NodeOutputs. We store these as
        # a dict.
        self.integration_specific_params = {}

        if self.integration == 'Airtable' and self.function == 'read_tables':
            # Expect a list of dicts with base and table IDs and names for each
            # table to load from
            if not ('airtable_tables' in kwargs):
                raise ValueError('IntegrationNode: base and table names and IDs must be provided to read Airtable tables.')
            for t in kwargs['airtable_tables']:
                if 'base_id' not in t or 'base_name' not in t or 'table_id' not in t or 'table_id' not in t:
                    raise ValueError('IntegrationNode: missing base or table names or IDs in Airtable integration.') 
                self.integration_specific_params['airtable_tables'] = \
                    kwargs['airtable_tables']

        self._inputs = { 
            input_name: inputs[input_name] for input_name in input_names 
        }

        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    def init_args_strs(self):
        init_args_strs = [
            f"integration='{self.integration}'",
            f"integration_name='{self.integration_name}'",
            f"function='{self.function}'",
            f"inputs={format_node_output_dict(self._inputs)}",
            f"public_key='{self._public_key}'",
            f"private_key='{self._private_key}'",
        ] 
        for k, v in self.integration_specific_params.items():
            init_args_strs += [f"{k}={v}"]
        return init_args_strs

    def set_api_key(self, public_key:str, private_key:str) -> None:
        self._public_key = public_key
        self._private_key = private_key

    def outputs(self):
        os = {}
        for o in self.function_params['outputs']:
            output_field = o['name']
            os[output_field] = NodeOutput(
                source=self, 
                output_field=output_field,
                # TODO: start storing types with integration functions on frontend
                # Using AnyType() for now
                output_data_type=AnyType()
            )
        return os
    
    def to_json_rep(self):
        if self._public_key is None or self._private_key is None:
            raise ValueError('IntegrationNode: API key required to fetch integration.')
        # Note: there's currently no way in the API code to get integrations
        # owned by another user, nor is there a way to get integrations by 
        # their ID.
        response = requests.get(
            API_INTEGRATION_FETCH_ENDPOINT,
            data={
                'integration_name': self.integration_name
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching integration: {response.text}")
        integration_json = response.json()
        # don't need to store integration parameters in node's JSON
        if 'params' in integration_json:
            del integration_json['params']

        json_rep = {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'integration': integration_json,
                'function': self.function_params,
                'category': 'integration',
                'task_name': self.function_params['taskName']
            }
        }
        for k, v in self.integration_specific_params.items():
            json_rep[k] = v
        return json_rep
    
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'IntegrationNode':
        return IntegrationNode(
            integration=json_data['data']['integration']['type'],
            integration_name=json_data['data']['integration']['name'],
            function=json_data['data']['function']['name'],
            # For IntegrationNodes, we must pass in the input names to the 
            # constructor, as they will be validated against the integration 
            # and function upon initialization.
            inputs={ 
                i['name']: [None] 
                for i in json_data['data']['function']['inputs'].values()
            },
            skip_typecheck=True
        )

# The classes below are particular "types" of IntegrationNodes, which users 
# may prefer for specificity. They're all created via calls to IntegrationNode.
class SalesforceIntegrationNode(IntegrationNode):
    def __init__(self, integration_name, function, 
                inputs:dict[str, list[NodeOutput]], 
                public_key:str=None, private_key:str=None, **kwargs):
        super().__init__(
            integration='Salesforce',
            integration_name=integration_name,
            function=function,
            inputs=inputs,
            public_key=public_key,
            private_key=private_key,
            **kwargs
        )

class GoogleDriveIntegrationNode(IntegrationNode):
    def __init__(self, integration_name, function, 
                inputs:dict[str, list[NodeOutput]], 
                public_key:str=None, private_key:str=None, **kwargs):
        super().__init__(
            integration='Google Drive',
            integration_name=integration_name,
            function=function,
            inputs=inputs,
            public_key=public_key,
            private_key=private_key,
            **kwargs
        )

class MicrosoftIntegrationNode(IntegrationNode):
    def __init__(self, integration_name, function, 
                inputs:dict[str, list[NodeOutput]], 
                public_key:str=None, private_key:str=None, **kwargs):
        super().__init__(
            integration='Microsoft',
            integration_name=integration_name,
            function=function,
            inputs=inputs,
            public_key=public_key,
            private_key=private_key,
            **kwargs
        )

class NotionIntegrationNode(IntegrationNode):
    def __init__(self, integration_name, function, 
                inputs:dict[str, list[NodeOutput]], 
                public_key:str=None, private_key:str=None, **kwargs):
        super().__init__(
            integration='Notion',
            integration_name=integration_name,
            function=function,
            inputs=inputs,
            public_key=public_key,
            private_key=private_key,
            **kwargs
        )

class AirtableIntegrationNode(IntegrationNode):
    def __init__(self, integration_name, function, 
                inputs:dict[str, list[NodeOutput]], 
                airtable_tables:list[dict]=None,
                public_key:str=None, private_key:str=None, **kwargs):
        super().__init__(
            integration='Airtable',
            integration_name=integration_name,
            function=function,
            inputs=inputs,
            public_key=public_key,
            private_key=private_key,
            airtable_tables=airtable_tables,
            **kwargs
        )

class HubSpotIntegrationNode(IntegrationNode):
    def __init__(self, integration_name, function, 
                inputs:dict[str, list[NodeOutput]], 
                public_key:str=None, private_key:str=None, **kwargs):
        super().__init__(
            integration='HubSpot',
            integration_name=integration_name,
            function=function,
            inputs=inputs,
            public_key=public_key,
            private_key=private_key,
            **kwargs
        )

class SugarCRMIntegrationNode(IntegrationNode):
    def __init__(self, integration_name, function, 
                inputs:dict[str, list[NodeOutput]], 
                public_key:str=None, private_key:str=None, **kwargs):
        super().__init__(
            integration='SugarCRM',
            integration_name=integration_name,
            function=function,
            inputs=inputs,
            public_key=public_key,
            private_key=private_key,
            **kwargs
        )

# Python functions for transforming data.
### USES USER-CREATED OBJECT - see comments in VectorStoreNode
class TransformationNode(NodeTemplate):
    def __init__(self, transformation_name:str, inputs=dict[str, NodeOutput],
                 public_key:str=None, private_key:str=None, **kwargs):
        super().__init__()
        self.node_type = 'transformation'
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key
        self.transformation_name = transformation_name
        # We make an API call to get the transformation JSON here to get the
        # desired outputs - see PipelineNode
        if self._public_key is None or self._private_key is None:
            raise ValueError('TransformationNode: API key required to fetch transformation.')
        # Note: there's currently no way in the API code to get files owned 
        # by another user, nor is there a way to get files by their ID.
        response = requests.get(
            API_TRANSFORMATION_FETCH_ENDPOINT,
            data={
                'transformation_name': self.transformation_name
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error fetching transformation: {response.text}')
        self.transformation_json = response.json()
        input_names = self.transformation_json['inputs']
        # The list of inputs provided should have keys matching the input names
        # defined by the transformation
        if sorted(list(inputs.keys())) != sorted(input_names):
            raise ValueError(f'TransformationNode: inputs do not match expected input names: expected f{input_names}')

        self._inputs = {
            input_name: [inputs[input_name]] for input_name in input_names
        } 

        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)

    def init_args_strs(self):
        return [
            f"transformation_name='{self.transformation_name}'",
            f'inputs={format_node_output_dict(self._inputs)}',
            f"public_key='{self._public_key}'",
            f"private_key='{self._private_key}'"
        ]
    
    def outputs(self):
        os = {}
        for output_field in self.transformation_json['outputs'].keys():
            os[output_field] = NodeOutput(
                source=self,
                output_field=output_field,
                # TODO: start storing types with transformations
                # Using AnyType() for now
                output_data_type=AnyType()
            )
        return os
    
    def to_json_rep(self):
        transformation_field_json = {
            'id': self.transformation_json['id'],
            'name': self.transformation_json['name'],
            'description': self.transformation_json['description'],
            'inputs': self.transformation_json['inputs'],
            'outputs': self.transformation_json['outputs'],
            # In the app repo this calls a helper function to format pipeline
            # names. For the time being this will be the same as the name as
            # the only case in which it isn't the name are if it's owned by the
            # user (which is impossible right now). TODO: may need to fix. Same
            # issue in PipelineNode.
            'displayName': self.transformation_json['name'],
        }

        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'transformation': transformation_field_json,
                'category': 'transformation',
                'task_name': 'transformation'
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'TransformationNode':
        return TransformationNode(
            transformation_name=json_data['data']['transformation']['name'],
            inputs={
                input_name: [None] 
                for input_name in json_data['data']['transformation']['inputs']
            },
            skip_typecheck=True
        )

# File save nodes have no outputs.
class FileSaveNode(NodeTemplate):
    def __init__(self, name_input:NodeOutput, files_input:list[NodeOutput], **kwargs):
        super().__init__()
        self.node_type = 'fileSave'
        self._inputs = {
            'name': [name_input],
            # files aggregates one or more node outputs
            'files': files_input
        }
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)

    def init_args_strs(self):
        name_input = self._inputs['name'][0]
        files_input_strs = [
            f"(node id {i.source._id}).outputs()['{i.output_field}']"
            for i in self._inputs['files']
        ]
        return [
            format_node_output_with_name('name_input', name_input),
            f'files_input={files_input_strs}'
        ]
    
    def outputs(self): return None
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "category": "task",
                "task_name": "save_file"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'FileSaveNode':
        _ = json_data 
        return FileSaveNode(
            name_input=None,
            files_input=[],
            skip_typecheck=True
        )

###############################################################################
# LLMS                                                                        #
###############################################################################

class OpenAILLMNode(NodeTemplate):
    def __init__(self, model:str, system_input:NodeOutput, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = 'llmOpenAI'
        if model not in SUPPORTED_OPENAI_LLMS.keys():
            raise ValueError(f'OpenAILLMNode: invalid model {model}.')
        self.model = model 
        # the user might have passed in more model params through kwargs
        self.max_tokens, self.temp, self.top_p = 1024, 1., 1.
        for optional_param_arg in ['max_tokens', 'temperature', 'top_p']:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        if self.max_tokens > SUPPORTED_OPENAI_LLMS[self.model]:
            raise ValueError(f'OpenAILLMNode: max_tokens {self.max_tokens} is too large for model {self.model}.')
        self._inputs = {'system': [system_input], 'prompt': [prompt_input]}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    def init_args_strs(self):
        system_input = self._inputs['system'][0]
        prompt_input = self._inputs['prompt'][0]
        return [
            f"model='{self.model}'",
            format_node_output_with_name('system_input', system_input),
            format_node_output_with_name('prompt_input', prompt_input),
            f'max_tokens={self.max_tokens}',
            f'temperature={self.temp}',
            f'top_p={self.top_p}'
        ]

    def output(self) -> NodeOutput: 
        return NodeOutput(
            source=self,
            output_field='response', 
            output_data_type=TEXT_TYPE
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'model': self.model,
                'maxTokens': self.max_tokens,
                'temperature': str(round(self.temp, 2)),
                'topP': str(round(self.top_p, 2)),
                'category': 'task',
                'task_name': 'llm_openai'
            }
        }
       
    @staticmethod 
    def _from_json_rep(json_data:dict) -> 'OpenAILLMNode':
        return OpenAILLMNode(
            model=json_data['data']['model'],
            system_input=None,
            prompt_input=None,
            max_tokens=json_data['data']['maxTokens'],
            temperature=float(json_data['data']['temperature']),
            top_p=float(json_data['data']['topP']),
            skip_typecheck=True
        )
        
class AnthropicLLMNode(NodeTemplate):
    def __init__(self, model:str, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = 'llmAnthropic'
        if model not in SUPPORTED_ANTHROPIC_LLMS.keys():
            raise ValueError(f'AnthropicLLMNode: invalid model {model}.')
        self.model = model 
        self.max_tokens, self.temp, self.top_p = 1024, 1., 1.
        for optional_param_arg in ['max_tokens', 'temperature', 'top_p']:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        if self.max_tokens > SUPPORTED_ANTHROPIC_LLMS[self.model]:
            raise ValueError(f'AnthropicLLMNode: max_tokens {self.max_tokens} is too large for model {self.model}.')
        self._inputs = {'prompt': [prompt_input]}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)

    def init_args_strs(self):
        prompt_input = self._inputs['prompt'][0]
        return [
            f"model='{self.model}'",
            format_node_output_with_name('prompt_input', prompt_input)
        ]
    
    def output(self) -> NodeOutput:
        return NodeOutput(
            source=self, 
            output_field='response', 
            output_data_type=TEXT_TYPE
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'model': self.model,
                'maxTokens': self.max_tokens,
                'temperature': str(round(self.temp, 2)),
                'topP': str(round(self.top_p, 2)),
                'category': 'task',
                'task_name': 'llm_anthropic'
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'AnthropicLLMNode':
        return AnthropicLLMNode(
            model=json_data['data']['model'],
            prompt_input=None,
            max_tokens=json_data['data']['maxTokens'],
            temperature=float(json_data['data']['temperature']),
            top_p=float(json_data['data']['topP']),
            skip_typecheck=True
        )

###############################################################################
# MULTIMODAL                                                                  #
###############################################################################

class ImageGenNode(NodeTemplate):
    def __init__(self, model:str, image_size:int, num_images:int, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = 'imageGen'
        if model not in SUPPORTED_IMAGE_GEN_MODELS.keys():
            raise ValueError(f'ImageGenNode: invalid model {model}.')
        self.model = model
        if image_size not in SUPPORTED_IMAGE_GEN_MODELS[self.model][0]:
            raise ValueError(f'ImageGenNode: Invalid image size {image_size}.')
        if num_images not in SUPPORTED_IMAGE_GEN_MODELS[self.model][1]:
            raise ValueError(f'ImageGenNode: Invalid number of images {num_images}.')
        self.image_size = image_size 
        self.num_images = num_images 
        self._inputs = {'prompt': [prompt_input]}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    def init_args_strs(self):
        prompt_input = self._inputs['prompt'][0]
        return [
            f"model='{self.model}'",
            f'image_size={self.image_size}',
            f'num_images={self.num_images}',
            format_node_output_with_name('prompt_input', prompt_input)
        ]

    def output(self) -> NodeOutput:
        return NodeOutput(
            source=self, 
            output_field='images', 
            output_data_type=ListType(IMAGE_FILE_TYPE)
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'model': self.model,
                'size': f'{self.image_size}x{self.image_size}',
                'imageCount': self.num_images,
                'category': 'task',
                'task_name': 'generate_image'
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'ImageGenNode':
        image_size_str = json_data['data']['size']
        image_size = int(image_size_str[:image_size_str.index('x')])
        return ImageGenNode(
            model=json_data['data']['model'],
            image_size=image_size,
            num_images=int(json_data['data']['imageCount']),
            prompt_input=None,
            skip_typecheck=True
        )
    
class SpeechToTextNode(NodeTemplate):
    def __init__(self, model:str, audio_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = 'speechToText'
        if model not in SUPPORTED_SPEECH_TO_TEXT_MODELS:
            raise ValueError(f'SpeechToTextNode: invalid model {model}.')
        self.model = model
        self._inputs = {'audio': [audio_input]}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    def init_args_strs(self):
        audio_input = self._inputs['audio'][0]
        return [
            f"model='{self.model}'",
            format_node_output_with_name('audio_input', audio_input)
        ]

    def output(self) -> NodeOutput:
        return NodeOutput(
            source=self, 
            output_field='text', 
            output_data_type=TEXT_TYPE
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'model': self.model,
                'category': 'task',
                'task_name': 'speech_to_text'
            }
        }
        
    @staticmethod 
    def _from_json_rep(json_data:dict) -> 'SpeechToTextNode':
        return SpeechToTextNode(
            model=json_data['data']['model'],
            audio_input=None,
            skip_typecheck=True
        )

###############################################################################
# DATA LOADERS                                                                #
###############################################################################

# Nodes for loading data from various sources, with (Mongo) node type 
# "dataLoader".
class DataLoaderNode(NodeTemplate):
    # inputs can either be NodeOutputs or strings, so inputs is a dictionary of
    # input names to a list of NodeOutputs or a list of strings
    # note: right now, the length of each input value list should be 1 (see
    # check below), but it's feasible to imagine that we might want to support
    # lists of inputs for each field ("multi-inputs"), e.g. loading several
    # queries (from NodeOutputs or string queries) at once
    def __init__(self, loader_type:str, inputs:dict[str, list],
                 **kwargs):
        super().__init__()
        self.node_type = 'dataLoader'
        if loader_type not in DATALOADER_PARAMS.keys():
            raise ValueError(f'DataLoaderNode: invalid dataloader type {loader_type}.')
        input_names = DATALOADER_PARAMS[loader_type]['input_names']
        if sorted(list(inputs.keys())) != sorted(input_names):
            raise ValueError(f'DataLoaderNode: inputs do not match expected input names: expected {input_names}')
        self.loader_type = loader_type
        self.task_name = DATALOADER_PARAMS[loader_type]['task_name']
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, 'default'
        for optional_param_arg in ['chunk_size', 'chunk_overlap', 'func']:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        # Store the inputs that are NodeOutputs vs. those that are strings
        # in separate dicts
        self._inputs = {}
        self._input_strs = {}
        # only the inputs that are NodeOutputs should be added to _inputs
        if inputs:
            for k, v in inputs.items():
                if len(v) != 1:
                    raise ValueError(f'DataLoaderNode: expected one input for input name {k}, got {len(v)}')
                if type(v[0]) == NodeOutput:
                    self._inputs[k] = v
                elif type(v[0]) == str:
                    self._input_strs[k] = v[0]
                else:
                    raise ValueError(f'DataLoaderNode: input name {k} must be a NodeOutput or a string.')
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)

    def init_args_strs(self):
        inputs_strs = {}
        for k, v in self._inputs.items():
            inputs_strs[k] = (format_node_output(v[0]))
        for k, v in self._input_strs.items():
            inputs_strs[k] = [v]
        return [
            f"loader_type='{self.loader_type}'",
            f'inputs={inputs_strs}',
            f'chunk_size={self.chunk_size}',
            f'chunk_overlap={self.chunk_overlap}',
            f"func='{self.func}'"
        ]

    def output(self) -> NodeOutput: 
        # for most datalaoders the data returned is a document list
        output_data_type = ListType(DOCUMENT_TYPE)
        if self.loader_type in ['CSV Query', 'SerpAPI']:
            output_data_type = TEXT_TYPE
        return NodeOutput(
            source=self,
            output_field='output',
            output_data_type=output_data_type
        )

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        json_rep = {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'loaderType': self.loader_type,
                'function': self.func,
                'chunkSize': self.chunk_size,
                'chunkOverlap': self.chunk_overlap,
                'category': "task",
                'task_name': self.task_name
            }
        }
        # add in string params if they were passed into the constructor
        for k, v in self._input_strs.items():
            json_rep["data"][k] = v
        return json_rep
    
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'DataLoaderNode':
        inputs = {}
        # inputs that were explicitly initialized with strings take the form
        # of additional fields in the JSON, rather than edges
        for k in DATALOADER_PARAMS[json_data['data']['loaderType']]['input_names']:
            if k in json_data['data'].keys():
                inputs[k] = [json_data['data'][k]]
            else:
                inputs[k] = [None]
        return DataLoaderNode(
            loader_type=json_data['data']['loaderType'],
            inputs=inputs,
            chunk_size=json_data['data']['chunkSize'],
            chunk_overlap=json_data['data']['chunkOverlap'],
            func=json_data['data']['function'],
            skip_typecheck=True
        )

# Like with IntegrationNodes, the classes below are particular "types" of 
# data loader nodes. They're all created via calls to DataLoaderNode. Note that
# this means that "printing" a node will always return the DataLoaderNode.
class FileLoaderNode(DataLoaderNode):
    def __init__(self, file_input:NodeOutput, **kwargs):
        super().__init__(
            loader_type='File',
            inputs={'file':[file_input]},
            **kwargs
        )

class CSVQueryLoaderNode(DataLoaderNode):
    def __init__(self, query_input:NodeOutput, csv_input:NodeOutput, **kwargs):
        super().__init__(
            loader_type='CSV Query',
            inputs={'query':[query_input], 'csv':[csv_input]},
            **kwargs
        )

class URLLoaderNode(DataLoaderNode):
    def __init__(self, url_input:NodeOutput, **kwargs):
        super().__init__(
            loader_type='URL',
            inputs={'url':[url_input]},
            **kwargs
        )
        
class WikipediaLoaderNode(DataLoaderNode):
    def __init__(self, query_input:NodeOutput, **kwargs):
        super().__init__(
            loader_type='Wikipedia',
            inputs={'query':[query_input]},
            **kwargs
        )

class YouTubeLoaderNode(DataLoaderNode):
    def __init__(self, url_input:NodeOutput, **kwargs):
        super().__init__(
            loader_type='YouTube',
            inputs={'url':[url_input]},
            **kwargs
        )
    
class ArXivLoaderNode(DataLoaderNode):
    def __init__(self, query_input:NodeOutput, **kwargs):
        super().__init__(
            loader_type='Arxiv',
            inputs={'query':[query_input]},
            **kwargs
        )

class SerpAPILoaderNode(DataLoaderNode):
    def __init__(self, api_key_input, query_input:NodeOutput, **kwargs):
        super().__init__(
            loader_type='SerpAPI',
            inputs={'apiKey':[api_key_input], 'query':[query_input]},
            **kwargs
        )

class GitLoaderNode(DataLoaderNode):
    def __init__(self, repo_input, **kwargs):
        super().__init__(
            loader_type='Git',
            inputs={'repo':[repo_input]},
            **kwargs
        )

class NotionLoaderNode(DataLoaderNode):
    def __init__(self, token_input, database_input, **kwargs):
        super().__init__(
            loader_type='Notion',
            inputs={'token':[token_input], 'database':[database_input]},
            **kwargs
        )

class ConfluenceLoaderNode(DataLoaderNode):
    def __init__(self, username_input, api_key_input, url_input:NodeOutput, **kwargs):
        super().__init__(
            loader_type='Confluence',
            inputs={
                'username':[username_input],
                'apiKey':[api_key_input],
                'url':[url_input]
            },
            **kwargs
        )

###############################################################################
# VECTORDB                                                                    #
###############################################################################

# The implementation of this is akin to that of dataloader nodes.
class VectorDBLoaderNode(NodeTemplate):
    def __init__(self, documents_input:list[NodeOutput], **kwargs):
        super().__init__()
        self.node_type = 'vectorDBLoader'
        self.func, self.chunk_size, self.chunk_overlap = 'default', VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP
        for optional_param_arg in ['chunk_size', 'chunk_overlap', 'func']:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {'documents': documents_input}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    def init_args_strs(self):
        documents_input_strs = [
            f"(node id {i.source._id}).outputs()['{i.output_field}']"
            for i in self._inputs['documents']
        ]
        return [f'documents_input={documents_input_strs}']

    def output(self) -> NodeOutput:
        return NodeOutput(
            source=self, 
            output_field='database', 
            output_data_type=VECTOR_DB_TYPE
        )

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'function': self.func,
                'category': 'task',
                'task_name': 'load_vector_db'
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'VectorDBLoaderNode':
        return VectorDBLoaderNode(
            input=None,
            chunk_size=json_data['data']['chunkSize'],
            chunk_overlap=json_data['data']['chunkOverlap'],
            func=json_data['data']['function'],
            skip_typecheck=True
        )

class VectorDBReaderNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, database_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = 'vectorDBReader'
        self.func, self.max_docs_per_query = 'default', 2
        for optional_param_arg in ['func', 'max_docs_per_query']:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {'query': [query_input], 'database': [database_input]}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    def init_args_strs(self):
        query_input = self._inputs['query'][0]
        database_input = self._inputs['database'][0]
        return [
            format_node_output_with_name('query_input', query_input),
            format_node_output_with_name('database_input', database_input)
        ]

    def output(self) -> NodeOutput:
        # assume the reader returns the query result post-processed back into text
        return NodeOutput(
            source=self, 
            output_field='results', 
            output_data_type=ListType(DOCUMENT_TYPE)
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'function': self.func,
                'category': 'task',
                'task_name': 'query_vector_db',
                'maxDocsPerQuery': self.max_docs_per_query
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'VectorDBReaderNode':
        return VectorDBReaderNode(
            query_input=None,
            database_input=None,
            func=json_data['data']['function'],
            max_docs_per_query=json_data['data']['maxDocsPerQuery'],
            skip_typecheck=True
        )
        
# With a couple of other nodes, this node references an existing object that
# lives in the VS platform, what we generally refer to as a "user-created 
# object" here. Thus, to access it, we need to make an API call to the server
# code in order to get the JSON and store the relevant parameters in the node.
class VectorStoreNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, 
                 vectorstore_id=None, vectorstore_name=None, 
                 public_key:str=None, private_key:str=None,
                 username=None, org_name=None, max_docs_per_query=1,
                 **kwargs):
        super().__init__()
        self.node_type = 'vectorStore'
        if vectorstore_id is None and vectorstore_name is None:
            raise ValueError('VectorStoreNode: either the vectorstore ID or name should be specified.')
        self.vectorstore_id = vectorstore_id
        self.vectorstore_name = vectorstore_name
        self.username = username 
        self.org_name = org_name
        self.max_docs_per_query = max_docs_per_query
        # we'll need to use the API key when fetching the user-defined 
        # vectorstore
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key
        # we don't store vectorstore-specific params like chunk params, since 
        # that is a property of the vectorstore and not the node
        self._inputs = {'query': [query_input]}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    @staticmethod
    def from_vectorstore_obj(vectorstore_obj, 
                             query_input:NodeOutput, 
                             public_key:str=None, private_key:str=None):
        if not vectorstore_obj.id:
            print('VectorStore object does not contain a required ID, which likely means that the VectorStore has not yet been saved. Attempting to save the pipeline...')
            vectorstore_obj.save(public_key, private_key)
            print('VectorStore object successfully saved.')
        # This is inefficient right now, since we save (write to Mongo) and 
        # then immediately query the object (read from Mongo) in the 
        # constructor.
        return VectorStoreNode(
            query_input=query_input, 
            vectorstore_id=vectorstore_obj.id, 
            vectorstore_name=vectorstore_obj.name, 
            public_key=public_key, 
            private_key=private_key
        )
    
    def init_args_strs(self):
        query_input = self._inputs['query'][0]
        return [
            format_node_output_with_name('query_input', query_input),
            f"public_key='{self._public_key}'",
            f"private_key='{self._private_key}'",
            f"vectorstore_id='{self.vectorstore_id}'",
            f"vectorstore_name='{self.vectorstore_name}'",
            f"username='{self.username}'",
            f"org_name='{self.org_name}'",
            f'max_docs_per_query={self.max_docs_per_query}'
        ]

    # If this node was loaded from JSON and changed to reference another
    # vectorstore object, we need to use the API key to query the new object.
    # This setter provides an explicit way to make sure the API key is in the 
    # node (if the key weren't initialized globally).
    def set_api_key(self, public_key:str, private_key:str) -> None:
        self._public_key = public_key
        self._private_key = private_key

    def output(self) -> NodeOutput:
        return NodeOutput(
            source=self, 
            output_field='results', 
            output_data_type=ListType(DOCUMENT_TYPE)
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        if self._public_key is None or self._private_key is None:
            raise ValueError('VectorStoreNode: API key required to fetch vectorstore.')
        # There's currently no notion of "sharing" vectorstores (so username
        # and org_name aren't required right now), but there probably will be 
        # one in the future.
        response = requests.get(
            API_VECTORSTORE_FETCH_ENDPOINT,
            data={
                'vectorstore_id': self.vectorstore_id,
                'vectorstore_name': self.vectorstore_name,
                'username': self.username,
                'org_name': self.org_name
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching vectorstore: {response.text}")
        vectorstore_json = response.json()
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id, 
                'nodeType': self.node_type,
                'maxDocsPerQuery': self.max_docs_per_query,
                # we just copy everything over, including the vectors (if any)
                'vectorStore': vectorstore_json,
                'category': 'task',
                'task_name': 'query_vectorstore'
            }
        }

    @staticmethod 
    def _from_json_rep(json_data:dict) -> 'VectorStoreNode':
        # there isn't a way to recover the API key from the JSON rep; it can
        # be set with set_api_key; also as mentioned above, (author) username
        # and org name data isn't currently saved in Mongo
        return VectorStoreNode(
            query_input=None,
            vectorstore_id=json_data['data']['vectorStore']['id'],
            vectorstore_name=json_data['data']['vectorStore']['name'], 
            max_docs_per_query=json_data['data']['maxDocsPerQuery'],
            skip_typecheck=True
        )

###############################################################################
# LOGIC                                                                       #
###############################################################################

# NB: To establish that these nodes specifically represent logic/control flow,
# these class names are prefixed with "Logic".
class LogicConditionNode(NodeTemplate):
    # inputs should comprise all in-edges, which are the names of all conditions 
    # and values along with the NodeOutputs they correspond to.
    # conditions is a list of (cond, val), where if cond is True the node 
    # returns val (where val is an input name).
    # default is what the node returns in the (final) else case.
    def __init__(self, inputs:dict[str, NodeOutput], 
                 conditions:list[tuple[str, str]], else_value:str,
                 **kwargs):
        super().__init__()
        self.node_type = 'condition'
        input_names = list(inputs.keys())
        if len(set(input_names)) != len(input_names):
            raise ValueError('LogicConditionNode: duplicate input names.')
        for cond in conditions:
            if cond[1] not in input_names:
                raise ValueError(f'LogicConditionNode: Returned value {cond[1]} of condition {cond[0]} was not specified in inputs.')
        if else_value not in input_names:
            raise ValueError(f'LogicConditionNode: Returned value {else_value} of else condition was not specified in inputs.')
        self.input_names = input_names
        self.conditions = conditions
        # NB: self.predicates maps to the JSON "conditions" field. The result
        # of the corresponding predicate in the input argument conditions is
        # the same-indexed element in self.output_names.
        self.predicates = [cond[0] for cond in conditions]
        self.output_names = [cond[1] for cond in conditions] + [else_value]
        # each separate input is an in-edge to the node, with the input name
        # being the user-provided name
        self._inputs = {k: [v] for k, v in inputs.items()}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    def init_args_strs(self):
        input_strs = [
            f"({k}, (node id {v[0].source._id}).outputs()['{v[0].output_field}'])" 
            for k, v in self._inputs.items()
        ]
        return [
            f'inputs={input_strs}'.replace('"', ''),
            f'conditions={self.conditions}',
            f"else_value='{self.output_names[-1]}'"
        ]

    # Unlike most other nodes, this node has several outputs, corresponding to
    # each of the specified conditions (and the else case).
    def outputs(self):
        # the outputs are labelled "output-0", "output-1", etc. followed by
        # "output-else"
        os = {}
        # We can do better than the API code since we still have access to the
        # NodeOutputs in each conditional output (and thus the type)
        for ind in range(len(self.predicates)):
            output_source_name = self.output_names[ind]
            output_data_type = self._inputs[output_source_name][0].output_data_type
            o = NodeOutput(
                source=self, 
                output_field=f'output-{ind}', 
                output_data_type=output_data_type)
            os[o.output_field] = o
        else_output_source_name = self.output_names[-1]
        else_o = NodeOutput(
            source=self, 
            output_field='output-else', 
            output_data_type=self._inputs[else_output_source_name][0].output_data_type
        )
        os[else_o.output_field] = else_o
        return os
    
    # If a user currently wants to index into a specific output, they need to 
    # call the outputs() method and then index into it by name (e.g. 
    # "output-2", "output-else"), or use the helper functions below.
    def output_index(self, i:int) -> NodeOutput:
        if i < 0 or i >= len(self.predicates):
            raise ValueError('LogicConditionNode: index out of range.')
        os = self.outputs()
        return os[f'output-{i}']
    
    def output_else(self) -> NodeOutput: 
        os = self.outputs()
        return os['output-else']
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'conditions': self.predicates,
                'inputNames': self.input_names,
                'outputs': self.output_names,
                'category': 'condition'
            }
        }

    @staticmethod
    def _from_json_rep(json_data:dict) -> 'LogicConditionNode':
        predicates = json_data['data']['conditions']
        output_names = json_data['data']['outputs']
        return LogicConditionNode(
            inputs=[(name, None) for name in json_data['data']['inputNames']],
            conditions=[(predicates[i], output_names[i]) for i in range(len(predicates))],
            else_value=output_names[-1],
            skip_typecheck=True
        )
    
class LogicMergeNode(NodeTemplate):
    def __init__(self, inputs:list[NodeOutput], **kwargs):
        super().__init__()
        self.node_type = 'merge'
        self._inputs = {
            # The JSON name for the in-edge is "input", although the displayed
            # name is "inputs".
            'input': inputs
        }
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
        
    def init_args_strs(self):
        input_strs = [
            f"(node id {i.source._id}).outputs()['{i.output_field}']" 
            for i in self._inputs['input']
        ]
        return [f'inputs={input_strs}'.replace('"', '')]

    def output(self) -> NodeOutput:
        output_data_types = set([o.output_data_type for o in self._inputs['input']])
        return NodeOutput(
            source=self, 
            output_field='output', 
            output_data_type=UnionType(*output_data_types)
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'function': 'default',
                'category': 'merge'
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'LogicMergeNode':
        _ = json_data
        return LogicMergeNode(
            inputs=[],
            skip_typecheck=True
        )


class SplitTextNode(NodeTemplate):
    # Instead of giving choices for the delimiter character, we just take in
    # a string.
    def __init__(self, delimiter:str, text_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = 'splitText'
        if not delimiter:
            raise ValueError('SplitTextNode: delimiter cannot be an empty string.')
        self.delimiter_chars = delimiter
        self.delimiter_name = 'character(s)'
        if delimiter in TEXT_SPLIT_DELIMITER_NAMES:
            self.delimiter_name = TEXT_SPLIT_DELIMITER_NAMES[delimiter]
        self._inputs = {'text': [text_input]}
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    def init_args_strs(self):
        text_input = self._inputs['text'][0]
        return [
            f'delimiter={self.delimiter}',
            format_node_output_with_name('text_input', text_input)
        ]
    
    def output(self) -> NodeOutput:
        return NodeOutput(
            source=self,
            output_field='output',
            output_data_type=ListType(TEXT_TYPE)
        )

    def outputs(self):
        o = self.output()
        return {o.output_field: o}

    def to_json_rep(self):
        character = None if self.delimiter_name != 'character(s)' else self.delimiter_chars
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id, 
                'nodeType': self.node_type,
                'category': 'task',
                'task_name': 'split_text',
                'delimiter': self.delimiter_name,
                'character': character,
            }
        }
    
    @staticmethod 
    def _from_json_rep(json_data:dict) -> 'SplitTextNode':
        delimiter_name = json_data['data']['delimiter']
        delimiter_chars = json_data['data']['character']
        if delimiter_name == 'space':
            delimiter_chars = ' '
        if delimiter_name == 'newline':
            delimiter_chars = '\n'
        return SplitTextNode(
            delimiter=delimiter_chars,
            skip_typecheck=True
        )

###############################################################################
# CHAT                                                                        #
###############################################################################

class ChatMemoryNode(NodeTemplate):
    # Chat memory nodes don't take input
    def __init__(self, memory_type:str, **kwargs):
        super().__init__()
        if memory_type not in CHAT_MEMORY_TYPES:
            raise ValueError(f'ChatMemoryNode: invalid chat memory type {memory_type}.')
        self.node_type = 'chatMemory'
        self.memory_type = memory_type
        self.memory_window_values = {
            # for full text, memory_window isn't used (just take the full text)
            CHAT_MEMORY_TYPES[0]: 0,
            CHAT_MEMORY_TYPES[1]: 0,
            CHAT_MEMORY_TYPES[2]: 10,
            CHAT_MEMORY_TYPES[3]: 2048
        }
        # self.memory_window is set to the value corresponding to 
        # self.memory_type's entry in memory_window_values, which may be 
        # overridden by the constructor arg memory_window
        if 'memory_window' in kwargs:
            if self.memory_type in CHAT_MEMORY_TYPES[:2]:
                raise ValueError("ChatMemoryNode: memory window shouldn't be specified if the chat memory is the full text.")
            self.memory_window_values[self.memory_type] = kwargs['memory_window']
        self.memory_window = self.memory_window_values[self.memory_type]
        # chat memory nodes take no inputs
        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)
    
    def init_args_strs(self):
        return [f"memory_type='{self.memory_type}'"]

    def output(self) -> NodeOutput:
        output_data_type = TEXT_TYPE if self.memory_type == 'Full - Formatted' else ListType(DICT_TYPE)
        return NodeOutput(
            source=self, 
            output_field='value', 
            output_data_type=output_data_type
        )

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'memoryType': self.memory_type,
                'memoryWindow': self.memory_window,
                'memoryWindowValues': self.memory_window_values,
                'category': 'memory',
                'task_name': 'load_memory'
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict) -> 'ChatMemoryNode':
        n = ChatMemoryNode(
            memory_type=json_data['data']['memoryType'],
            skip_typecheck=True
        )
        # overwrite with JSON values
        n.memory_window = json_data['data']['memoryWindow']
        n.memory_window_values = json_data['data']['memoryWindowValues']
        return n

###############################################################################
# AGENTS                                                                       
###############################################################################

# User created object vs Full agent definition
# as a user create object Agent Node just referenes an existing agent by ID 
# TODO - can we move boilerplate into a base class for user created objects
# Start with user created object implementation
# Maybe angent node is analagous to a pipeline node and we have an Agent class that as analagous to a pipeline class and alllows defining the agent with various tools
class AgentNode(NodeTemplate):
    def __init__(self, agent_id:str=None, agent_name:str=None,
        inputs=dict[str, NodeOutput],
        username:str=None, org_name:str=None,
        public_key:str=None, private_key:str=None, **kwargs):      

        super().__init__()
        self.node_type = 'agent'
        if agent_id is None and agent_name is None:
            raise ValueError('AgentNode: either the agent ID or name should be specified.')
        
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.username = username
        self.org_name = org_name
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key

        if self._public_key is None or self._private_key is None:
            raise ValueError('AgentNode: API key required to fetch agent.')
        
        response = requests.get(
            API_AGENT_FETCH_ENDPOINT,
            data={
                'agent_id': self.agent_id,
                'agent_name': self.agent_name,
                'username': self.username,
                'org_name': self.org_name
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching agent: {response.text}")
        
        self.agent_json = response.json()
        self.agent_id = self.agent_json['id']
        self.agent_name = self.agent_json['name']

        input_names = [
            i['name'] for i in self.agent_json['inputs'].values()
        ]

        if sorted(list(inputs.keys())) != sorted(input_names):
            raise ValueError(f'AgentNode: pipeline node inputs do not match expected input names: expected f{input_names}')
        
        self._inputs = {
            input_name: [inputs[input_name]] for input_name in input_names
        }

        if not 'skip_typecheck' in kwargs or not kwargs['skip_typecheck']:
            validate_node_inputs(self)

    @staticmethod 
    def from_agent_obj(agent_obj, 
                       inputs=dict[str, NodeOutput],
                       public_key:str=None, private_key:str=None):
        if not agent_obj.id:
            print('Agent object does not contain a required ID, which likely means that the agent has not yet been saved. Attempting to save...')
            agent_obj.save(public_key, private_key)
            print('Agent object successfully saved.')
        # This is inefficient right now, since we save (write to Mongo) and 
        # then immediately query the object (read from Mongo) in the 
        # constructor.
        return AgentNode(
            agent_id=agent_obj.id,
            agent_name=agent_obj.name,
            inputs=inputs,
            public_key=public_key, 
            private_key=private_key
        )


    def init_args_strs(self):
        return [
            f"agent_id='{self.agent_id}'",
            f"agent_name='{self.agent_name}'",
            f'inputs={format_node_output_dict(self._inputs)}',
            f"username='{self.username}'",
            f"org_name='{self.org_name}'",
            f"public_key='{self._public_key}'",
            f"private_key='{self._private_key}'"
        ]

    def set_api_key(self, public_key:str, private_key:str):
        self._public_key = public_key
        self._private_key = private_key

    def outputs(self) -> dict[str, NodeOutput]:
        os = {}
        for o in self.agent_json['outputs'].values():
            output_field = o['name']
            if o['type'] in ['Text', 'Formatted Text']:
                output_data_type = TEXT_TYPE
            elif o['type'] == 'File':
                output_data_type = FILE_TYPE
            else:
                raise ValueError(f'AgentNode: unsupported output type {o["type"]}')
            os[output_field] = NodeOutput(
                source=self, 
                output_field=output_field, 
                output_data_type=output_data_type
            )
        return os
    
    def output(self) -> NodeOutput:
        return NodeOutput(
            source=self, 
            output_field='output',
            output_data_type=None
        )
    
    def to_json_rep(self):
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id, 
                'nodeType': self.node_type,
                'agentDefinition': self.agent_json,
                'category': 'agent',
            }
        }

    @staticmethod
    def _from_json_rep(json_data:dict) -> 'AgentNode':
        return AgentNode(
            agent_id=json_data['data']['agentDefinition']['id'],
            agent_name=json_data['data']['agentDefinition']['name'],
            inputs= {
                input_name: None for input_name in json_data['data']['agentDefinition']['inputs'].keys()
            },
            skip_typecheck=True
        )
