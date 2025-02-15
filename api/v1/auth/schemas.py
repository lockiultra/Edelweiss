from pydantic import BaseModel, field_validator, ValidationError, EmailStr


class User(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def validate_password(cls, password: str): # noqa
        uppercase: bool = False
        lowercase: bool = False
        numbers: bool = False

        for sym in password:
            uppercase = uppercase or sym.isupper()
            lowercase = lowercase or sym.islower()
            numbers = numbers or sym.isalpha()
        if not all((uppercase, lowercase, numbers)):
            raise ValidationError('Incorrect password')
        return password


class UserCreate(User):
    email: EmailStr


class UserLogin(User):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
