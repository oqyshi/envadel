from bson import ObjectId

from app.models import AuthorBase, AuthorDB, BookBase, BookDB


def test_author_base_defaults():
    author = AuthorBase(name="Tolstoy")
    assert author.name == "Tolstoy"
    assert author.book_ids == []


def test_author_base_with_book_ids():
    ids = [str(ObjectId()), str(ObjectId())]
    author = AuthorBase(name="Tolstoy", book_ids=ids)
    assert author.book_ids == ids


def test_author_db_from_mongo_doc():
    oid = ObjectId()
    author = AuthorDB(_id=oid, name="Tolstoy", book_ids=[])
    assert author.id == str(oid)
    assert author.name == "Tolstoy"


def test_book_base_defaults():
    book = BookBase(title="War and Peace", description="A novel")
    assert book.title == "War and Peace"
    assert book.author_ids == []


def test_book_base_with_author_ids():
    ids = [str(ObjectId()), str(ObjectId())]
    book = BookBase(title="Book", description="Desc", author_ids=ids)
    assert len(book.author_ids) == 2


def test_book_db_from_mongo_doc():
    oid = ObjectId()
    book = BookDB(_id=oid, title="Book", description="Desc", author_ids=[])
    assert book.id == str(oid)


def test_pyobjectid_converts_objectid_to_str():
    oid = ObjectId()
    author = AuthorDB(_id=oid, name="Test", book_ids=[oid])
    assert isinstance(author.id, str)
    assert isinstance(author.book_ids[0], str)
