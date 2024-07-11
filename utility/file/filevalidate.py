### External imports ###

import pandas as pd
from model import fileModel

### Function Declarations ###

def validateFromModel(df: pd.DataFrame, model: fileModel.FileModel) -> bool:
    checklist = {column:False for column in model.neededColumns}
    for column in df.columns:
        if column in checklist:
            checklist[column] = True
    for column in checklist:
        if not checklist[column]:
            return False
    return True