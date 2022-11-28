def createAttractionSubjectsList(setOfCategories):
    result = ''
    for index, category in enumerate(setOfCategories):
        result += category
        if index != len(setOfCategories) - 1:
            result += ','
    return result