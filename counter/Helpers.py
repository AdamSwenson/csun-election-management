"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

class ResultFieldProcessor(object):
    """
    Handles transformations of the result into a format which
    the VoteCounter can operate upon
    """
    @staticmethod
    def process_field_values(field):
        """ Splits the fields on comma; trims"""
        return field.split(',')


class Validators(object):

    def __init__(self):
        self.candidate_list = []

    def is_validator_ready(self):
        return len(self.candidate_list) > 0

    def is_in_candidate_list(self, candidate):
        if not self.is_validator_ready():
            msg = "Candidate list is empty. Cannot validate the candidate %s" % candidate
            # todo replace with logger
            print(msg)
            return False

        return candidate in self.candidate_list

if __name__ == '__main__':
    pass