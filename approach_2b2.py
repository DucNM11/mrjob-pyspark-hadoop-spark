#!/usr/bin/env python3
"""Evaluate the top 10 smart contracts by total Ether received.
An outline of the subtasks required to extract this information is provided below,
focusing on a MRJob based approach. This is, however, is not the only way to
complete the task, as there are several other viable ways of completing this assignment."""
from mrjob.job import MRJob
from mrjob.step import MRStep


class top_amt(MRJob):

    value_list = []

    def mapper_join(self):
        with open('approach_2_b.txt') as f:
            for line in f:
                fields = line.split('\t')
                add = fields[0].replace('\"', '')
                self.value_list = self.value_list.append(add)

    def mapper(self, _, line):
        try:
            fields = line.split(',')
            if len(fields) == 7:
                contract = fields[2]
                if contract in self.value_list:
                    yield (None, (contract, int(fields[3])))
        except:
            pass

    def combiner(self, key, values):
        sorted_values = sorted(values, reverse=True, key=lambda tup: tup[1])
        i = 0

        for val in sorted_values:
            yield (None, (val[0], val[1]))
            i += 1
            if i >= 10:
                break

    def reducer(self, key, values):
        sorted_values = sorted(values, reverse=True, key=lambda tup: tup[1])
        i = 0

        for val in sorted_values:
            yield (val[0], val[1])
            i += 1
            if i >= 10:
                break

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_join,
                   mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer)
        ]


if __name__ == '__main__':
    top_amt.run()