subsets: data/raw/members.csv data/raw/sample_submission_zero.csv data/raw/train.csv data/raw/transactions.csv data/raw/user_logs.csv
	python kkbox/transforms/subsets.py data/raw/members.csv
	python kkbox/transforms/subsets.py data/raw/transactions.csv
	python kkbox/transforms/subsets.py data/raw/user_logs.csv
