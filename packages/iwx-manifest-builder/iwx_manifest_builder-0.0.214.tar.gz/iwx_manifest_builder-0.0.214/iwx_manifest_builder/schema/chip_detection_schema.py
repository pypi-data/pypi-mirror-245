from marshmallow import Schema, fields


class ChipDetectionAttrsSchema(Schema):
    category_enum= fields.Int()
    score = fields.Float()


class ChipDetectionSchema(Schema):
    chip_detection = fields.Nested(ChipDetectionAttrsSchema())
