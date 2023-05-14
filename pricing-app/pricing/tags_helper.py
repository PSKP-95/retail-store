# from typing import List, Set

# from fastapi import HTTPException
# from app.helper import mongo_to_dict
# from pricing.models import Tag
# from bson import ObjectId


# def get_existing_tags(ids: List[str]):
#     tagIds: List = []
#     for id in ids:
#         if ObjectId.is_valid(id):
#             tagIds.append(ObjectId(id))
#     tags = Tag.objects(__raw__={ "_id" : { "$in" : tagIds }})

#     tagIds: Set = set()
#     for tag in tags:
#         tagIds.add(tag.id)

#     return list(tagIds)

# def add_question_in_tags(ids: List[ObjectId], qid: ObjectId):
#     t = Tag.objects(__raw__={ "_id" : { "$in" : ids }}).update(__raw__={'$push': {'questions': qid}})
#     if len(ids) == t:
#         return True
#     return False

# def remove_question_from_tags(ids: List[ObjectId], qid: ObjectId):
#     t = Tag.objects(__raw__={ "_id" : { "$in" : ids }}).update(__raw__={'$pull': {'questions': qid}})
#     print(t)
#     print(ids)
#     if len(ids) == t:
#         return True
#     return False