import pytest

from domain.errors import InvalidEmail, InvalidHashedPassword
from domain.value_objects.email import Email
from domain.value_objects.hashed_password import HashedPassword


class TestEmail:

    @pytest.mark.parametrize(
        "email", ["example@domain.com", "example.example@domain.com", "example+example@domain.com"]
    )
    def test_valid_emails(self, email: str) -> None:
        assert email == Email(email).as_generic_type()

    @pytest.mark.parametrize(
        "email", ["example@domain", "@domain.com", "example@", "example"]
    )
    def test_invalid_emails(self, email: str) -> None:
        with pytest.raises(InvalidEmail):
            Email(email)

class TestHashedPassword:

    @pytest.mark.parametrize(
        "hashed_password", ["$<algorithm>$<options>$<salt>$<hash>", "$<algorithm>$<options-1>$<options-2>$<salt>$<hash>",]
    )
    def test_valid_mfc(self, hashed_password: str) -> None:
        _, algorithm, *options, salt, password_hash = hashed_password.split("$")
        print(hashed_password.split("$"))
        assert hashed_password == HashedPassword(hashed_password).as_generic_type()
        assert algorithm == HashedPassword(hashed_password).algorithm
        assert "$".join(options) == HashedPassword(hashed_password).options
        assert salt == HashedPassword(hashed_password).salt
        assert password_hash == HashedPassword(hashed_password).hash

    @pytest.mark.parametrize(
        "hashed_password", ["$<algorithm>$<options>$<salt>"]
    )
    def test_invalid_mfc(self, hashed_password: str) -> None:
        with pytest.raises(InvalidHashedPassword):
            HashedPassword(hashed_password)
