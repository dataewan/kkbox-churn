#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Form subsets of the data to make it easier to process."""

import csv
import os
import operator


class Subset(object):

    """Form subsets of the data to make it easier to process."""

    def __init__(self, filename, membershipfile, outfilename=None,
                 header=True):
        """Args:
            filename: the name of the file we want to make a subset of.
            membershipfile: the file (either train or sample submission) that
                contains the mnsos we want to extract.
            outfilename: name of the file that we want to create. defaults to
                `None`, in that case we figure out what filename we want.
            header: does the file we're making a subset of have a header.
                Defaults to true.
        """
        self.filename = filename
        self.membershipfile = membershipfile
        self.outfilename = outfilename
        self.header = header

        self.subset = set()

        self.findsubsetusers()
        self.findoutputfile()
        self.form_subset()

    def findsubsetusers(self):
        """Find a set of users in the subset. Store these for validation
        later."""
        with open(self.membershipfile, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                msno = row[0]
                self.subset.add(msno)

    def findoutputfile(self):
        """Find out what the output file should be."""
        if self.outfilename is not None:
            self.outfile = open(self.outfilename, 'w')
        else:
            name_lookup = {
                'train.csv': 'train',
                'sample_submission_zero.csv': 'test'
            }
            member_basename = os.path.basename(self.membershipfile)
            if member_basename not in name_lookup:
                raise Exception(
                    "Can't figure out if this is the test or the training set."
                )
            datadir = 'data/processed'
            self.outfile = open(
                os.path.join(
                    datadir,
                    name_lookup[member_basename] + "_" +
                    os.path.basename(self.filename)
                ), 'w'
            )

    def form_subset(self):
        """Make the subset of the data. Read through every line in the
        membershipfile, see if the user is in the subsetset, write it out to
        output if it is."""
        infile = open(self.filename, 'r')
        reader = csv.reader(infile)
        writer = csv.writer(self.outfile)

        # write the header if we have one
        if self.header:
            writer.writerow(next(reader))

        # just now, assume that the first item in the row is going to be the
        # msno.
        msnogetter = operator.itemgetter(0)

        for row in reader:
            if msnogetter(row) in self.subset:
                writer.writerow(row)

        infile.close()
        self.outfile.close()


if __name__ == "__main__":
    S = Subset('data/raw/members.csv', 'data/raw/train.csv')
