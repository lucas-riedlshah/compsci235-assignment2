class Author:

    def __init__(self, author_id: int, author_full_name: str):
        if not isinstance(author_id, int):
            raise ValueError

        if author_id < 0:
            raise ValueError

        self.__unique_id = author_id

        # Uses the attribute setter method.
        self.full_name = author_full_name

        # Initialize author colleagues data structure with empty set.
        # We use a set so each unique author is only represented once.
        self.__authors_this_one_has_worked_with = set()

        self.__average_rating = None
        self.__ratings_count = None

    @property
    def unique_id(self) -> int:
        return self.__unique_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, author_full_name: str):
        if isinstance(author_full_name, str):
            # make sure leading and trailing whitespace is removed
            author_full_name = author_full_name.strip()
            if author_full_name != "":
                self.__full_name = author_full_name
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def average_rating(self) -> float:
        return self.__average_rating

    @average_rating.setter
    def average_rating(self, average_rating: float):
        if average_rating < 0:
            raise ValueError
        if not isinstance(average_rating, float):
            if isinstance(average_rating, int):
                self.__average_rating = float(average_rating)
                return
            else:
                raise TypeError
        self.__average_rating = average_rating

    @property
    def ratings_count(self) -> int:
        return self.__ratings_count

    @ratings_count.setter
    def ratings_count(self, count: int):
        if count < 0:
            raise ValueError
        if not isinstance(count, int):
            raise TypeError
        self.__ratings_count = count

    def add_coauthor(self, coauthor):
        if isinstance(coauthor, self.__class__) and coauthor.unique_id != self.unique_id:
            self.__authors_this_one_has_worked_with.add(coauthor)

    def check_if_this_author_coauthored_with(self, author):
        return author in self.__authors_this_one_has_worked_with

    def __repr__(self):
        return f'<Author {self.full_name}, author id = {self.unique_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.unique_id == other.unique_id

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __hash__(self):
        return hash(self.unique_id)
