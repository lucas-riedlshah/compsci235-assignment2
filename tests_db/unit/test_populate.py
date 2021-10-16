from sqlalchemy import select, inspect

from library.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'book_authors', 'books', 'publishers', 'reviews', 'users']

def test_database_populate_select_all_books(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables["books"]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append((row['id'], row['title']))
        
        assert len(all_books) == 20
        assert all_books[0] == (707611, 'Superman Archives, Vol. 2')

def test_database_populate_select_all_authors(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables["authors"]])
        result = connection.execute(select_statement)

        all_authors = []
        for row in result:
            all_authors.append((row['id'], row['full_name']))
        
        assert len(all_authors) == 31
        assert all_authors[0] == (14965, 'Garth Ennis')

def test_database_populate_select_all_publishers(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables["publishers"]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append((row['id'], row['name']))
        
        assert len(all_publishers) == 12
        assert all_publishers[3] == (4, 'DC Comics')