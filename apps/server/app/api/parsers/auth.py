from app.api.parsers import RequestParser

signup_parser = RequestParser()
signup_parser.add_argument(name="first_name", required=True, type=str, location="json")
signup_parser.add_argument(name="last_name", required=True, type=str, location="json")
signup_parser.add_argument(name="email", required=True, type=str, location="json")
signup_parser.add_argument(name="phone", required=False, type=str, location="json")
signup_parser.add_argument(name="password", required=True, type=str, location="json")

login_parser = RequestParser()
login_parser.add_argument(name="email", required=True, type=str, location="json")
login_parser.add_argument(name="password", required=True, type=str, location="json")
