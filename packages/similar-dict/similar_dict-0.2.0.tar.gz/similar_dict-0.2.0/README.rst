Similar Dict
============
This is a small test helper that allows you to compare dicts (and sequences of
them) to an expected template. This template can be real values or types.

If they are real values, normal comparison is used.
If it's a type, then `isinstance()` is used to make sure it's of the correct
type, but no value comparison is made.

This allows your test to focus on the things that are important and ignore
things that do not affect the application, but merely its presentation.

Example
-------
Consider the following `pydantic`_ objects::

    class Author(BaseModel):
    given_name: str
    surname: str


    class Book(BaseModel):
        title: str
        published_at: datetime
        author: Author

A json schema for these is built from a dict that pydantic generates via the
`model_json_schema`_ method and will look like this::

    expected_book_schema = {
        "$defs": {
            "Author": {
                "properties": {
                    "given_name": {"title": "Given Name", "type": "string"},
                    "surname": {"title": "Surname", "type": "string"},
                },
                "required": ["given_name", "surname"],
                "title": "Author",
                "type": "object",
            }
        },
        "properties": {
            "title": {"title": "Title", "type": "string"},
            "published_at": {
                "format": "date-time",
                "title": "Published At",
                "type": "string",
            },
            "author": {"$ref": "#/$defs/Author"},
        },
        "required": ["title", "published_at", "author"],
        "title": "Book",
        "type": "object",
    }

Now suppose the you don't really care about the formatting/cases/wording of the
title as it doesn't affect the program. You care about the other stuff in your
test: that the keys are correct and that they serialise to the correct type.

So we change our expected dictionary for a similarity match::

    expected_book_schema = {
        "$defs": {
            "Author": {
                "properties": {
                    "given_name": {"title": str, "type": "string"},
                    "surname": {"title": str, "type": "string"},
                },
                "required": ["given_name", "surname"],
                "title": str,
                "type": "object",
            }
        },
        "properties": {
            "title": {"title": str, "type": "string"},
            "published_at": {
                "format": "date-time",
                "title": str,
                "type": "string",
            },
            "author": {"$ref": "#/$defs/Author"},
        },
        "required": ["title", "published_at", "author"],
        "title": str,
        "type": "object",
    }

HINT: all titles have been replaced with a `str` type.

And so let's look at our test::

    def test_book_schema():
        assert similar_dict(Book.model_json_schema(), expected_book_schema)


This test will succeed, despite that it's not an exact match for the Schema
definition.

.. _model_json_schema: https://docs.pydantic.dev/latest/api/base_model/#pydantic.main.BaseModel.model_json_schema
.. _pydantic: https://pydantic.dev/
