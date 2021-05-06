import logging
from typing import Any, Text, Dict, List,Optional,Union
from rasa_sdk.events import UserUtteranceReverted, Restarted, SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from actions.SchemeApis import get_Scheme


logger = logging.getLogger(__name__)
REQUESTED_SLOT = "requested_slot"
EventType = Dict[Text, Any]

class SchemeForm(FormAction):
    """Example of a custom form action"""
    def __init__(self):
        super(SchemeForm, self).__init__()
        self.good_rela=[]
        self.good_value=[]
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_提供方案"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        """A list of required slots that the form has to fill"""
        return ['disease']
    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[EventType]]:
        """Request the next slot and utter template if needed,
        else return None"""
        disease = tracker.get_slot('disease')
        if disease==None:
            self.good_rela=[]
            self.good_value=[]

        if self.good_rela==[]:
            self.good_rela=self.required_slots(tracker)
        """新增需求（重选分支）"""
        entities=tracker.latest_message['entities']
        print('*'*50)
        print(entities)
        if len(entities)>0:
            entity=entities[-1]['entity']
            if entity in self.good_rela:
                loc=self.good_rela.index(entity)
                print(self.good_rela)
                self.good_rela=self.good_rela[0:loc+1]
                # slot_keys=tracker.current_slot_values().keys()
                slot_keys=tracker.current_slot_values().keys()
                for slot_key in slot_keys:
                    if slot_key not in self.good_rela:
                        # print(slot_key)
                        tracker.current_slot_values()[slot_key]=None
                # tracker.current_slot_values()['症状']='很tm严重'
                slots=tracker.current_slot_values()
                # testslot=tracker.get_slot('症状')
                print(slots)
        print('*'*50)
        """新增需求（重选分支）"""
        #disease也许可能是列表
        if isinstance(disease, list):
            disease = disease[0]
        #目前完成的癌种
        if disease is not None and disease not in ['乳腺癌','肺癌','肝癌','胃癌','鼻咽癌','胰腺癌']:
            return None
        #通过当前需要的slot 确定下一条边
        all_list=[tracker.get_slot(i) for i in self.good_rela]
        new_list = list(filter(lambda x: x != None, all_list))
        value=None
        if new_list!=[]:
            rela,value=get_Scheme(new_list)
            #下一条边是治疗方案的时候停止填充
            if rela[-1] != '治疗方案':
                self.good_rela = self.required_slots(tracker) + rela
            else:
                self.good_value = value
        print('good_rela', self.good_rela)
        for slot in self.good_rela:
            if self._should_request_slot(tracker, slot):
                logger.debug(f"Request next slot '{slot}'")
                if value is None:
                    dispatcher.utter_message(template=f"utter_ask_{slot}", **tracker.slots)
                else:
                    # dispatcher.utter_custom_json({"select":value})


                    value = [{str(index): i } for index, i in enumerate(value)]
                    dispatcher.utter_message(template=f"utter_ask_{slot}",buttons=value,encoding='utf-8')
                    # dispatcher.utter_button_template(template=f"utter_ask_{slot}",buttons= value,tracker=tracker)

                return [SlotSet(REQUESTED_SLOT, slot)]
        # no more required slots to fill
        return None
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        disease = tracker.get_slot('disease')
        if isinstance(disease,list):
            disease=disease[0]
        if disease==None:
            return [Restarted()]
        if disease not in ['乳腺癌','肺癌','肝癌','胃癌','鼻咽癌','胰腺癌']:
            dispatcher.utter_message('该癌种方案还在努力中。。。。。。。')
        if self.good_value!=[]:
            dispatcher.utter_custom_json({"scheme":self.good_value})
        return []

