A package of Python functions used by BANF's data scientists and developers.

# ※ NOTICE
- README 기록 시점을 기준으로 해당 패키지에서 주로 사용되는 패키지는 data_processing.preprocessing의 ForMeasurement Class
    - 파일로 보유하고 있는 Raw TSV Data를 읽을 수 있는 단위로 전처리된 pandas Dataframe으로 불러오는 기능 (transformFileToDataFrame)
    - Amazon S3의 전처리된 parquet 파일을 저장하는 Bucket으로부터 데이터를 코드 내에서 import 하는 기능 (lookupS3Objects, importS3Objects)
    위 두 기능이 가장 많이 사용되고 있고 실제 다른 부가 기능들은 아직 사용되지 않고 있음.

# Requirements
- python 3
- aws credentials setting (for AWS S3)

# Installation
```bash
pip install banf

# or

python setup.py install
```
# Usage
```python
# import in python or ipython code
from banf.data_processing.preprocessing import ForMeasurement
```
## AWS Credentials Setting

You need to make a file named 'credentials' in '~/.aws' directory.  
in Windows, make directory at %UserProfile%\.aws  
in Linux, make directory at ~/.aws  

This Package use 'default' profile in credentials file.  
So, you must set 'default' profile in credentials file.

```bash
# credentials file sample

[default] ; default Profile section information

aws_access_key_id = YOUR_ACCESS_KEY1

aws_secret_access_key = YOUR_SECRET_KEY1
```

# Acknowledgments
## BANF R&D Team
---
- GW Jeon (BANF Co., Ltd. email : gwjeon@banf.co.kr)
- EG Kim (BANF Co., Ltd. email : egkim@banf.co.kr)
- DH Kim (BANF Co., Ltd. email : kim.donghun@banf.co.kr)