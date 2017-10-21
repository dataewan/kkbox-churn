#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Form subsets of the data to make it easier to process."""

import csv
import operator
import os
import sys
import tqdm


class Subset(object):

    """Form subsets of the data to make it easier to process."""

    def __init__(self, filename, header=True):
        """Args:
            filename: the name of the file we want to make a subset of.
            header: does the file we're making a subset of have a header.
                Defaults to true.
        """
        self.filename = filename
        self.header = header

        self.trainusers = self.findsubsetusers('data/raw/train.csv')
        self.testusers = self.findsubsetusers(
            'data/raw/sample_submission_zero.csv'
        )
        self.findoutputfile()
        self.form_subset()

    @staticmethod
    def findsubsetusers(membershipfile):
        """Find a set of users in the subset. Store these for validation
        later."""
        subset = set()
        with open(membershipfile, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                msno = row[0]
                subset.add(msno)
        return subset

    def findoutputfile(self):
        """Find out what the output file should be."""
        datadir = 'data/processed'
        trainfilename = os.path.join(
            datadir,
            "train_" + os.path.basename(self.filename)
        )
        testfilename = os.path.join(
            datadir,
            "test_" + os.path.basename(self.filename)
        )
        self.outfiles = {
            'train': open(trainfilename, 'w'),
            'test': open(testfilename, 'w')
        }

    def form_subset(self):
        """Make the subset of the data. Read through every line in the
        membershipfile, see if the user is in the subsetset, write it out to
        output if it is."""
        infile = open(self.filename, 'r')
        reader = csv.reader(infile)
        trainwriter = csv.writer(self.outfiles['train'])
        testwriter = csv.writer(self.outfiles['test'])

        # write the header if we have one
        if self.header:
            header = next(reader)
            trainwriter.writerow(header)
            testwriter.writerow(header)

        # just now, assume that the first item in the row is going to be the
        # msno.
        msnogetter = operator.itemgetter(0)

        for row in tqdm.tqdm(reader):
            if msnogetter(row) in self.trainusers:
                trainwriter.writerow(row)
            if msnogetter(row) in self.testusers:
                testwriter.writerow(row)

        infile.close()
        for outfile in self.outfiles.values():
            outfile.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        S = Subset(sys.argv[1])
    else:
        S = Subset('data/raw/members.csv')
