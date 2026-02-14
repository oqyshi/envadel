from bson import ObjectId


async def test_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()


# --- Authors ---


async def test_create_author(client, mock_authors_collection):
    author_id = ObjectId()
    mock_authors_collection.insert_one.return_value.inserted_id = author_id
    mock_authors_collection.find_one.return_value = {
        "_id": author_id,
        "name": "Tolstoy",
        "book_ids": [],
    }

    resp = await client.post("/authors/", json={"name": "Tolstoy"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Tolstoy"
    assert data["_id"] == str(author_id)
    mock_authors_collection.insert_one.assert_called_once()
    client.mock_send_event.assert_called_once()


async def test_create_author_kafka_event_payload(client, mock_authors_collection):
    author_id = ObjectId()
    mock_authors_collection.insert_one.return_value.inserted_id = author_id
    mock_authors_collection.find_one.return_value = {
        "_id": author_id,
        "name": "Pushkin",
        "book_ids": [],
    }

    await client.post("/authors/", json={"name": "Pushkin"})
    call_kwargs = client.mock_send_event.call_args
    assert call_kwargs.kwargs["event_type"] == "author_created"
    assert call_kwargs.kwargs["data"]["name"] == "Pushkin"


async def test_get_authors_empty(client, mock_authors_collection):
    mock_authors_collection.find.return_value.to_list.return_value = []
    resp = await client.get("/authors/")
    assert resp.status_code == 200
    assert resp.json() == []


async def test_get_authors(client, mock_authors_collection):
    mock_authors_collection.find.return_value.to_list.return_value = [
        {"_id": ObjectId(), "name": "Author 1", "book_ids": []},
        {"_id": ObjectId(), "name": "Author 2", "book_ids": []},
    ]
    resp = await client.get("/authors/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


# --- Books ---


async def test_create_book_no_authors(client, mock_books_collection, mock_authors_collection):
    book_id = ObjectId()
    mock_books_collection.insert_one.return_value.inserted_id = book_id
    mock_books_collection.find_one.return_value = {
        "_id": book_id,
        "title": "War and Peace",
        "description": "Novel",
        "author_ids": [],
    }

    resp = await client.post(
        "/books/",
        json={"title": "War and Peace", "description": "Novel", "author_ids": []},
    )
    assert resp.status_code == 201
    assert resp.json()["title"] == "War and Peace"
    mock_authors_collection.update_many.assert_not_called()


async def test_create_book_with_authors_updates_many_to_many(
    client, mock_books_collection, mock_authors_collection
):
    book_id = ObjectId()
    author_id = ObjectId()
    mock_books_collection.insert_one.return_value.inserted_id = book_id
    mock_books_collection.find_one.return_value = {
        "_id": book_id,
        "title": "Book",
        "description": "Desc",
        "author_ids": [str(author_id)],
    }

    resp = await client.post(
        "/books/",
        json={
            "title": "Book",
            "description": "Desc",
            "author_ids": [str(author_id)],
        },
    )
    assert resp.status_code == 201
    mock_authors_collection.update_many.assert_called_once()
    call_args = mock_authors_collection.update_many.call_args[0]
    assert author_id in call_args[0]["_id"]["$in"]
    assert call_args[1] == {"$addToSet": {"book_ids": str(book_id)}}


async def test_create_book_with_multiple_authors(
    client, mock_books_collection, mock_authors_collection
):
    book_id = ObjectId()
    a1, a2 = ObjectId(), ObjectId()
    mock_books_collection.insert_one.return_value.inserted_id = book_id
    mock_books_collection.find_one.return_value = {
        "_id": book_id,
        "title": "Co-authored",
        "description": "Desc",
        "author_ids": [str(a1), str(a2)],
    }

    resp = await client.post(
        "/books/",
        json={
            "title": "Co-authored",
            "description": "Desc",
            "author_ids": [str(a1), str(a2)],
        },
    )
    assert resp.status_code == 201
    call_args = mock_authors_collection.update_many.call_args[0]
    assert len(call_args[0]["_id"]["$in"]) == 2


async def test_create_book_sends_kafka_event(client, mock_books_collection):
    book_id = ObjectId()
    mock_books_collection.insert_one.return_value.inserted_id = book_id
    mock_books_collection.find_one.return_value = {
        "_id": book_id,
        "title": "Test",
        "description": "Desc",
        "author_ids": [],
    }

    await client.post(
        "/books/", json={"title": "Test", "description": "Desc", "author_ids": []}
    )
    call_kwargs = client.mock_send_event.call_args
    assert call_kwargs.kwargs["event_type"] == "book_created"


async def test_get_books_empty(client, mock_books_collection):
    mock_books_collection.find.return_value.to_list.return_value = []
    resp = await client.get("/books/")
    assert resp.status_code == 200
    assert resp.json() == []


async def test_get_books(client, mock_books_collection):
    mock_books_collection.find.return_value.to_list.return_value = [
        {"_id": ObjectId(), "title": "Book 1", "description": "D1", "author_ids": []},
        {"_id": ObjectId(), "title": "Book 2", "description": "D2", "author_ids": []},
    ]
    resp = await client.get("/books/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
