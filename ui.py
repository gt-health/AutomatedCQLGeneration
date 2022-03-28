import json
import edifice as ed
from edifice import View, ScrollView, Label, TextInput, IconButton, Dropdown, CheckBox, Icon
from edifice.components.forms import Form

def merge(d1, d2):
    """Helper function to merge two dictionaries."""
    d = d1.copy()
    d.update(d2)
    return d

def add_divider(comp):
    """Helper function for drawing a gray line divider between components"""
    return View(layout="column")(
        comp,
        View(style={"height": 0, "border": "1px solid gray"})
    )

FHIR_Resource_List = ['Observation', 'Condition', 'MedicationStatement']

app_state = ed.StateManager({
    "name": '',
    "type": "",
    "indexEvent.name": '',
    "indexEvent.fhirResource": '',
    "indexEvent.conceptReference": '',
    "indexEvent.returnField": '',
    "indexEvent.returnType": '',
    "returnAggregator.type": ''
})

def _create_state_for_concept(concept_name):
    """Creates the state associated with a particular concept set."""
    return {
        f'{concept_name}.name': '',
        f'{concept_name}.codesets': ''
    }

concepts_state = ed.StateManager(merge(_create_state_for_concept("concept0"), {
    "all_concepts": ["concept0"],
    "next_i": 1,
}))

def _create_state_for_inclusion(inclusion_name):
    """Creates the state associated with a particular inclusion."""
    return {
        f'{inclusion_name}.name': '',
        f'{inclusion_name}.fhirResource': '',
        f'{inclusion_name}.conceptReference': '',
        f'{inclusion_name}.filterType': '',
        f'{inclusion_name}.timeFrameRelativeToIndexEvent.start': '',
        f'{inclusion_name}.timeFrameRelativeToIndexEvent.end': ''
    }

inclusions_state = ed.StateManager(merge(_create_state_for_inclusion("inclusion0"), {
    "all_inclusions": ["inclusion0"],
    "next_i": 1,
}))

def _create_state_for_derived(derived_name):
    """Creates the state associated with a particular derived."""
    return {
        f'{derived_name}.name': '',
        f'{derived_name}.baseInclusion': '',
        f'{derived_name}.fhirField': '',
        f'{derived_name}.fhirReturnResource': 'Observation',
        f'{derived_name}.questionConcept': '',
        f'{derived_name}.answerValueType': 'String',
        f'{derived_name}.answerValue': '',
        f'{derived_name}.renderAnswerWithCQL': 'True',
        f'{derived_name}.sourceNote': ''
    }

deriveds_state = ed.StateManager(merge(_create_state_for_derived("derived0"), {
    "all_deriveds": ["derived0"],
    "next_i": 1,
}))

class AppStateQuestion(ed.Component):

    @ed.register_props
    def __init__(self, label, output_field, default='', input_type='TextInput', input_options=[]):
        super().__init__()
        self.current_text = default
        self.label = label
        self.output_field = output_field
        self.input_type = input_type
        self.input_options = input_options

    def _on_change(self, text):
        output_json_value = app_state.subscribe(self, f'{self.output_field}')
        self.set_state(current_text=text)
        output_json_value.set(text)

    def render(self):
        current_text = self.current_text
        if self.input_type == 'TextInput':
            return View(layout='row')(
                Label(self.label, style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_text, on_change=self._on_change, style={'margin-right': 20})
            )
        elif self.input_type == 'Dropdown':
            return View(layout='row')(
                Label(self.label, style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                Dropdown(selection=current_text, options=self.input_options, on_select=self._on_change, style={'width': 300, 'margin-right': 20}, editable=True)
            )

class IndexEventQuestion(ed.Component):
    @ed.register_props
    def __init__(self):
        super().__init__()
        self.current_name = ''
        self.current_fhir_resource = ''
        self.current_concept_reference = ''
        self.current_return_field = ''
        self.current_return_type = ''

    def _on_change_name(self, text):
        output_json_value = app_state.subscribe(self, 'indexEvent.name')
        self.set_state(current_name=text)
        output_json_value.set(text)

    def _on_change_fhir_resource(self, text):
        output_json_value = app_state.subscribe(self, 'indexEvent.fhirResource')
        self.set_state(current_fhir_resource=text)
        output_json_value.set(text)

    def _on_change_concept_reference(self, text):
        output_json_value = app_state.subscribe(self, 'indexEvent.conceptReference')
        self.set_state(current_concept_reference=text)
        output_json_value.set(text)

    def _on_change_return_field(self, text):
        output_json_value = app_state.subscribe(self, 'indexEvent.returnField')
        self.set_state(current_return_field=text)
        output_json_value.set(text)

    def _on_change_return_type(self, text):
        output_json_value = app_state.subscribe(self, 'indexEvent.returnType')
        self.set_state(current_return_type=text)
        output_json_value.set(text)

    def render(self):
        current_name = self.current_name
        current_fhir_resource = self.current_fhir_resource
        current_concept_reference = self.current_concept_reference
        current_return_field = self.current_return_field
        current_return_type = self.current_return_type
        return View(layout='column')(
            View(layout='row')(
                Label('Name', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_name, on_change=self._on_change_name, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('FHIR Resource', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                Dropdown(current_fhir_resource, on_select=self._on_change_fhir_resource, style={'margin-right': 20, 'width': 300}, options = FHIR_Resource_List)
            ),
            View(layout='row')(
                Label('Concept Reference', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_concept_reference, on_change=self._on_change_concept_reference, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('Return Field', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                Dropdown(current_return_field, on_select=self._on_change_return_field, style={'margin-right': 20, 'width': 300}, options = ['Onset', 'Effective'])
            ),
            View(layout='row')(
                Label('Return Type', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                Dropdown(current_return_type, on_select=self._on_change_return_type, style={'margin-right': 20, 'width': 300}, options = ['dateTime'])
            )
        )

class ConceptQuestion(ed.Component):

    @ed.register_props
    def __init__(self, concept_name):
        super().__init__()
        self.concept_name = concept_name
        self.current_name = ''
        self.current_codesets = ''

    def _on_change_name(self, text):
        concept_set_name = concepts_state.subscribe(self, f'{self.concept_name}.name')
        self.set_state(current_name=text)
        concept_set_name.set(text)

    def _on_change_codesets(self, text):
        concept_set_codesets = concepts_state.subscribe(self, f'{self.concept_name}.codesets')
        self.set_state(current_codesets=text)
        concept_set_codesets.set(text)

    def render(self):
        current_name = self.current_name
        current_codesets = self.current_codesets
        return View(layout='column')(
            View(layout='row')(
                Label('Name', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_name, on_change=self._on_change_name, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('Codesets', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_codesets, on_change=self._on_change_codesets, style={'margin-right': 20})
            )
        )

class InclusionQuestion(ed.Component):

    @ed.register_props
    def __init__(self, inclusion_name):
        super().__init__()
        self.inclusion_name = inclusion_name
        self.current_name = ''
        self.current_fhir_resource = ''
        self.current_concept_reference = ''
        self.current_filter_type = ''
        self.current_timeframe_start = ''
        self.current_timeframe_end = ''

    def _on_change_name(self, text):
        inclusion_name = inclusions_state.subscribe(self, f'{self.inclusion_name}.name')
        self.set_state(current_name=text)
        inclusion_name.set(text)

    def _on_change_fhir_resource(self, text):
        inclusion_fhir_resource = inclusions_state.subscribe(self, f'{self.inclusion_name}.fhirResource')
        self.set_state(current_fhir_resource=text)
        inclusion_fhir_resource.set(text)

    def _on_change_concept_reference(self, text):
        inclusion_concept_reference = inclusions_state.subscribe(self, f'{self.inclusion_name}.conceptReference')
        self.set_state(current_concept_reference=text)
        inclusion_concept_reference.set(text)

    def _on_change_filter_type(self, text):
        inclusion_filter_type = inclusions_state.subscribe(self, f'{self.inclusion_name}.filterType')
        self.set_state(current_filter_type=text)
        inclusion_filter_type.set(text)

    def _on_change_timeframe_start(self, text):
        inclusion_timeframe_start = inclusions_state.subscribe(self, f'{self.inclusion_name}.timeFrameRelativeToIndexEvent.start')
        self.set_state(current_timeframe_start=text)
        inclusion_timeframe_start.set(text)

    def _on_change_timeframe_end(self, text):
        inclusion_timeframe_end = inclusions_state.subscribe(self, f'{self.inclusion_name}.timeFrameRelativeToIndexEvent.end')
        self.set_state(current_timeframe_end=text)
        inclusion_timeframe_end.set(text)

    def render(self):
        current_name = self.current_name
        current_fhir_resource = self.current_fhir_resource
        current_concept_reference = self.current_concept_reference
        current_filter_type = self.current_filter_type
        current_timeframe_start = self.current_timeframe_start
        current_timeframe_end = self.current_timeframe_end
        return View(layout='column')(
            View(layout='row')(
                Label('Name', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_name, on_change=self._on_change_name, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('FHIR Resource', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                Dropdown(selection = current_fhir_resource, on_change=self._on_change_fhir_resource, options = FHIR_Resource_List, style={'margin-right': 20, 'width': 300}, editable=True)
            ),
            View(layout='row')(
                Label('Concept Reference', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_concept_reference, on_change=self._on_change_concept_reference, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('Filter Type', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                Dropdown(current_filter_type, on_change=self._on_change_filter_type, options = ['', 'First'], style={'margin-right': 20, 'width': 300}, editable=True)
            ),
            View(layout='row')(
                Label('Timeframe Relative to Index Event Start', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_timeframe_start, on_change=self._on_change_timeframe_start, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('Timeframe Relative to Index Event End', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_timeframe_end, on_change=self._on_change_timeframe_end, style={'margin-right': 20})
            ),
        )

class DerivedQuestion(ed.Component):

    @ed.register_props
    def __init__(self, derived_name):
        super().__init__()
        self.derived_name = derived_name
        self.current_name = ''
        self.current_base_inclusion = ''
        self.current_fhir_field = ''
        self.current_fhir_return_resource = 'Observation'
        self.current_question_concept = ''
        self.current_answer_value_type = 'String'
        self.current_answer_value = ''
        self.current_render_answer_with_CQL = 'True'
        self.current_source_note = ''

    def _on_change_name(self, text):
        derived_name = deriveds_state.subscribe(self, f'{self.derived_name}.name')
        self.set_state(current_name=text)
        derived_name.set(text)

    def _on_change_base_inclusion(self, text):
        derived_base_inclusion = deriveds_state.subscribe(self, f'{self.derived_name}.baseInclusion')
        self.set_state(current_base_inclusion=text)
        derived_base_inclusion.set(text)

    def _on_change_fhir_field(self, text):
        derived_fhir_field = deriveds_state.subscribe(self, f'{self.derived_name}.fhirField')
        self.set_state(current_fhir_field=text)
        derived_fhir_field.set(text)

    def _on_change_current_fhir_return_resource(self, text):
        derived_fhir_return_resource = deriveds_state.subscribe(self, f'{self.derived_name}.fhirReturnResource')
        self.set_state(current_fhir_return_resource=text)
        derived_fhir_return_resource.set(text)

    def _on_change_question_concept(self, text):
        derived_question_concept = deriveds_state.subscribe(self, f'{self.derived_name}.questionConcept')
        self.set_state(current_question_concept=text)
        derived_question_concept.set(text)

    def _on_change_answer_value_type(self, text):
        derived_answer_value_type = deriveds_state.subscribe(self, f'{self.derived_name}.answerValueType')
        self.set_state(current_answer_value_type=text)
        derived_answer_value_type.set(text)

    def _on_change_answer_value(self, text):
        derived_answer_value = deriveds_state.subscribe(self, f'{self.derived_name}.answerValue')
        self.set_state(current_answer_value=text)
        derived_answer_value.set(text)

    def _on_change_render_answer_with_CQL(self, text):
        derived_render_answer_with_CQL = deriveds_state.subscribe(self, f'{self.derived_name}.renderAnswerWithCQL')
        self.set_state(current_render_answer_with_CQL=text)
        derived_render_answer_with_CQL.set(text)

    def _on_change_source_note(self, text):
        derived_source_note = deriveds_state.subscribe(self, f'{self.derived_name}.sourceNote')
        self.set_state(current_source_note=text)
        derived_source_note.set(text)

    def render(self):
        current_name = self.current_name
        current_base_inclusion = self.current_base_inclusion
        current_fhir_field = self.current_fhir_field
        current_fhir_return_resource = self.current_fhir_return_resource
        current_question_concept = self.current_question_concept
        current_answer_value_type = self.current_answer_value_type
        current_answer_value = self.current_answer_value
        current_render_answer_with_CQL = self.current_render_answer_with_CQL
        current_source_note = self.current_source_note
        return View(layout='column')(
            View(layout='row')(
                Label('Name', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_name, on_change=self._on_change_name, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('Base Inclusion', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_base_inclusion, on_change=self._on_change_base_inclusion, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('FHIR Field', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_fhir_field, on_change=self._on_change_fhir_field, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('FHIR Return Resource', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                Dropdown(current_fhir_return_resource, on_change=self._on_change_current_fhir_return_resource, options = FHIR_Resource_List, style={'margin-right': 20, 'width': 300}, editable=True)
            ),
            View(layout='row')(
                Label('Question Concept', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_question_concept, on_change=self._on_change_question_concept, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('Answer Value Type', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_answer_value_type, on_change=self._on_change_answer_value_type, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('Answer Value', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_answer_value, on_change=self._on_change_answer_value, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('Render Answer with CQL?', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_render_answer_with_CQL, on_change=self._on_change_render_answer_with_CQL, style={'margin-right': 20})
            ),
            View(layout='row')(
                Label('Source Note', style={"align": "left", "margin-left": 20, "margin-right": 10, "margin-top": 10, "margin-bottom": 10}),
                TextInput(current_source_note, on_change=self._on_change_source_note, style={'margin-right': 20})
            ),
        )

class App(ed.Component):

    def add_concept_set(self, click):
        next_key = "concept" + str(concepts_state["next_i"])
        concepts_state.update(merge(_create_state_for_concept(next_key), {
            "all_concepts": concepts_state["all_concepts"] + [next_key],
            "next_i": concepts_state["next_i"] + 1,
        }))

    def add_inclusion(self, click):
        next_key = "inclusion" + str(inclusions_state["next_i"])
        inclusions_state.update(merge(_create_state_for_inclusion(next_key), {
            "all_inclusions": inclusions_state["all_inclusions"] + [next_key],
            "next_i": inclusions_state["next_i"] + 1,
        }))

    def add_derived(self, click):
        next_key = "derived" + str(deriveds_state["next_i"])
        deriveds_state.update(merge(_create_state_for_derived(next_key), {
            "all_deriveds": deriveds_state["all_deriveds"] + [next_key],
            "next_i": deriveds_state["next_i"] + 1,
        }))

    def save_json(self, click):
        app_state_dict = app_state.as_dict()
        concepts_state_dict = concepts_state.as_dict()
        inclusions_state_dict = inclusions_state.as_dict()
        deriveds_state_dict = deriveds_state.as_dict()

        output_json = {
            "name": app_state_dict['name'],
            "type": app_state_dict['type'],
            "concepts": [
                {
                    "name": concepts_state_dict[f'{concept_name}.name'],
                    "codesets":concepts_state_dict[f'{concept_name}.codesets']
                } for concept_name in concepts_state_dict['all_concepts']
            ],
            "indexEvent": {
                "name": app_state_dict['indexEvent.name'],
                "fhirResource": app_state_dict['indexEvent.fhirResource'],
                "conceptReference": app_state_dict['indexEvent.conceptReference'],
                "returnField": app_state_dict['indexEvent.returnField'],
                "returnType": app_state_dict['indexEvent.returnType']
            },
            "inclusions": [
                {
                    "name": inclusions_state_dict[f'{inclusion_name}.name'],
                    "fhirResource": inclusions_state_dict[f'{inclusion_name}.fhirResource'],
                    "conceptReference": inclusions_state_dict[f'{inclusion_name}.conceptReference'],
                    "filterType": inclusions_state_dict[f'{inclusion_name}.filterType'],
                    "timeFrameRelativeToIndexEvent": {
                        "start": inclusions_state_dict[f'{inclusion_name}.timeFrameRelativeToIndexEvent.start'],
                        "end": inclusions_state_dict[f'{inclusion_name}.timeFrameRelativeToIndexEvent.end']
                    }
                } for inclusion_name in inclusions_state_dict['all_inclusions']
            ],
            "deriveds": [
                {
                    "name": deriveds_state_dict[f'{derived_name}.name'],
                    "baseInclusion": deriveds_state_dict[f'{derived_name}.baseInclusion'],
                    "fhirField": deriveds_state_dict[f'{derived_name}.fhirField'],
                    "fhirReturnResource": deriveds_state_dict[f'{derived_name}.fhirReturnResource'],
                    "questionConcept": deriveds_state_dict[f'{derived_name}.questionConcept'],
                    "answerValue": {
                        "valueType": deriveds_state_dict[f'{derived_name}.answerValueType'],
                        "renderAnswerWithCQL": deriveds_state_dict[f'{derived_name}.renderAnswerWithCQL'],
                        "value": deriveds_state_dict[f'{derived_name}.answerValue']
                    },
                    "sourceNote": deriveds_state_dict[f'{derived_name}.sourceNote']
                } for derived_name in deriveds_state_dict['all_deriveds']
            ],
            "returnAggregator": {
                "type": app_state_dict['returnAggregator.type']
            }
        }

        with open(f'{app_state_dict["name"]}.json', 'w') as f:
            json.dump(output_json, f)
        print(f'Saved file as {app_state_dict["name"]}.json')

    def convert_and_save(self, click):
        print('This does nothing for now.')

    def render(self):
        all_concept_sets = concepts_state.subscribe(self, 'all_concepts').value
        all_inclusions = inclusions_state.subscribe(self, 'all_inclusions').value
        all_deriveds = deriveds_state.subscribe(self, 'all_deriveds').value
        return ed.Window(title='Automated CQL Generation')(
            View(layout='row', style={'margin': 10})(
                ScrollView(layout='column', style={'min-width': 500, 'min-height':800})(
                    View(layout='row', style={'border': '2px solid #000000'})(Label(text='Metadata', style={'margin':5}), Icon('question-circle', style={'align':'right', 'margin': 10}, tool_tip = 'This is the metatdata section of the input JSON, which includes the name, the type of form, and the return aggregator type.')),
                    AppStateQuestion(label='Name', output_field='name'),
                    AppStateQuestion(label='Type', output_field='type', input_type='Dropdown', input_options=['IndexEventAndInclusion']),
                    AppStateQuestion(label='Return Aggregator', output_field='returnAggregator.type'),
                    Label(text='Concepts', style={'border': '2px solid #000000'}),
                    *[add_divider(ConceptQuestion(concept_name)) for concept_name in all_concept_sets],
                    IconButton(name="plus", title="Add Concept Set", on_click=self.add_concept_set),
                    Label(text='Index Event', style={'border': '2px solid #000000', 'margin-top': 10}),
                    IndexEventQuestion(),
                    Label(text='Inclusions', style={'border': '2px solid #000000'}),
                    *[add_divider(InclusionQuestion(inclusion_name)) for inclusion_name in all_inclusions],
                    IconButton(name="plus", title="Add Inclusion", on_click=self.add_inclusion),
                    Label(text='Deriveds', style={'border': '2px solid #000000', 'margin-top': 10}),
                    *[add_divider(DerivedQuestion(derived_name)) for derived_name in all_deriveds],
                    IconButton(name="plus", title="Add Derived", on_click=self.add_derived),
                ),
                ScrollView(style={'min-width': 500, 'min-height':800, 'align': 'top'})(
                    Label('{'),
                    Label('\t"name": "'+app_state.subscribe(self, "name").value+'",'),
                    Label('\t"type": "'+app_state.subscribe(self, "type").value+'",'),
                    Label('\t"concepts": ['),
                    *[Label('\t\t{\n\t\t\t"name": "'+concepts_state.subscribe(self, f'{concept_name}.name').value+'",\n\t\t\t"codesets": "'+concepts_state.subscribe(self, f'{concept_name}.codesets').value+'"') for concept_name in all_concept_sets],
                    Label('\t\t},'),
                    Label('\t"indexEvent": {\n\t\t"name": "'+app_state.subscribe(self, "indexEvent.name").value+'",'),
                    Label('\n\t\t"fhirResource": "'+app_state.subscribe(self, "indexEvent.fhirResource").value+'",'),
                    Label('\n\t\t"conceptReference": "'+app_state.subscribe(self, "indexEvent.conceptReference").value+'",'),
                    Label('\n\t\t"returnField": "'+app_state.subscribe(self, "indexEvent.returnField").value+'",'),
                    Label('\n\t\t"returnType": "'+app_state.subscribe(self, "indexEvent.returnType").value+'"\n\t},'),
                    Label('\t"inclusions": ['),
                    *[Label('\t\t{\n\t\t\t"name": "'+inclusions_state.subscribe(self, f'{inclusion_name}.name').value+'",\n\t\t\t"fhirResource": "'+inclusions_state.subscribe(self, f'{inclusion_name}.fhirResource').value+'",\n\t\t\t"conceptReference": "'+inclusions_state.subscribe(self, f'{inclusion_name}.conceptReference').value+'",\n\t\t\t"filterType": "'+inclusions_state.subscribe(self, f'{inclusion_name}.filterType').value+'",\n\t\t\t"timeFrameRelativeToIndexEvent: {\n\t\t\t\t"start": "'+inclusions_state.subscribe(self, f'{inclusion_name}.timeFrameRelativeToIndexEvent.start').value+'",\n\t\t\t\t"end": "'+inclusions_state.subscribe(self, f'{inclusion_name}.timeFrameRelativeToIndexEvent.end').value+'"\n\t\t\t},') for inclusion_name in all_inclusions],
                    Label('\t\t},'),
                    Label('\t"deriveds": ['),
                    *[Label('\t\t{\n\t\t\t"name": "'+deriveds_state.subscribe(self, f'{derived_name}.name').value+'",\n\t\t\t"baseInclusion": "'+deriveds_state.subscribe(self, f'{derived_name}.baseInclusion').value+'",\n\t\t\t"fhirField": "'+deriveds_state.subscribe(self, f'{derived_name}.fhirField').value+'",\n\t\t\t"fhirReturnResource": "'+deriveds_state.subscribe(self, f'{derived_name}.fhirReturnResource').value+'",\n\t\t\t"questionConcept": "'+deriveds_state.subscribe(self, f'{derived_name}.questionConcept').value+'",\n\t\t\t"answerValue": {\n\t\t\t\t"valueType": "'+deriveds_state.subscribe(self, f'{derived_name}.answerValueType').value+'",\n\t\t\t\t"renderAnswerWithCQL: '+deriveds_state.subscribe(self, f'{derived_name}.renderAnswerWithCQL').value+',\n\t\t\t\t"value": "'+deriveds_state.subscribe(self, f'{derived_name}.answerValue').value+'"\n\t\t\t},\n\t\t\t"sourceNote": "'+deriveds_state.subscribe(self, f'{derived_name}.sourceNote').value+'"') for derived_name in all_deriveds],
                    Label('\t\t},'),
                    Label('\t"returnAggregator": {\n\t\t"type":\t"'+app_state.subscribe(self, "returnAggregator.type").value+'"\n\t}\n}'),
                    View(layout='row')(
                        IconButton(name='save', title='Save to JSON File', on_click=self.save_json),
                        IconButton(name='file-export', title='Convert and Save as CQL', on_click=self.convert_and_save)
                    ),
                ),
            )
        )

if __name__ == "__main__":
    ed.App(App()).start()