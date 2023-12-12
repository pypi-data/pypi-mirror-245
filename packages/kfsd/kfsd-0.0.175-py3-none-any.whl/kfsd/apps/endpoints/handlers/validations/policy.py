from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.validations.policy import (
    PolicyModelSerializer,
    PolicyViewModelSerializer,
)
from kfsd.apps.models.tables.validations.policy import Policy
from kfsd.apps.endpoints.handlers.validations.rule import gen_rule_handler
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.endpoints.handlers.validations.rule import RuleHandler


def gen_policy_handler(instance):
    handler = PolicyHandler(instance.identifier, False)
    qsData = PolicyModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Policy)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Policy)
def process_post_del(sender, instance, **kwargs):
    pass


class PolicyHandler(BaseHandler):
    VALUES = "values"
    SUMMARY = "summary"
    EVALUATED_VALUES = "evaluated_values"
    ALL_VALUES = "all_values"
    BY_RULES = "by_rules"

    def __init__(self, policyIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=PolicyModelSerializer,
            viewSerializer=PolicyViewModelSerializer,
            modelClass=Policy,
            identifier=policyIdentifier,
            isDBFetch=isDBFetch,
        )
        self.__resp = {}
        self.__evaluatedVals = []

    def getRuleHandlers(self) -> list:
        return [gen_rule_handler(rule) for rule in self.getModelQS().rules.all()]

    def getEvaluatedValues(self):
        return self.__evaluatedVals

    def getAllValues(self):
        return DictUtils.get(self.getModelQSData(), self.ALL_VALUES, [])

    def summarize(self):
        return {
            self.SUMMARY: {
                self.EVALUATED_VALUES: self.getEvaluatedValues(),
                self.ALL_VALUES: self.getAllValues(),
            },
            self.BY_RULES: self.__resp,
        }

    def appendVal(self, source: list, val: any):
        if val and isinstance(val, list):
            source += val
        elif val and isinstance(val, str):
            source.append(val)

    def execRules(self, data):
        for rule in self.getRuleHandlers():
            rule.exec(data)
            self.__resp[rule.getIdentifier()] = rule.summarize()

        evaluatedValues = []
        for k, v in self.__resp.items():
            if v[RuleHandler.IS_SUCCESS]:
                self.appendVal(evaluatedValues, v[RuleHandler.VALUES])

        self.__evaluatedVals = evaluatedValues

    def exec(self, data):
        input = data
        self.execRules(input)
