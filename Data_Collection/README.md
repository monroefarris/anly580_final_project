## Tweet Collection Script

<br>

**Files:**
- `Tweet_Collection.py`: script to collect tweets based on inputs from `collection_data.yml`
- `collection_data.yml`: file to be adjusted to specify what tweets you want to collect

**To Run:**
1. Update parameters of `collection_data.yml` to input your Twitter dev info & type of tweets you want to collect
2. cd into `Data_Collection` (absolute paths not used for reading `collection_data.yml` from `Tweet_Collection.py`)
3. `python Tweet_Collection.py`
    - NOTE: downgrade to Tweepy v3.10.0 if have tweet pulling error

**Side Note:**
- If you search something and then search again with the same filename indicated in `collection_data.yml`, it will overwrite existing results in the existing csv file. So be sure to change filename if you want to save existing results.