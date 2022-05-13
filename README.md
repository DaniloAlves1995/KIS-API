# API for email validation

The purpose of this api is to perform email validation according to some business rules requested by the company.

## Architecture

The architecture uses Rest API with a route for validation using the POST method and receiving the email through an `input` field in JSON format.


## Functions Organization

| Funtions | Description |
| --- | --- |
| cleansed_email | Apply process of clearing email and initial validations |
| validation_domain | Gets domain part and check its validation |
| validation_username | Gets user name and check its validation |
| validation_process | Starts the validation process after API call |

## Execution

1. Install used packages:

`pip install flask flask_cors`

2. In the same folder as the file, run:

`python3 challenge.py`

The api will run at address `127.0.0.1:5000` and the end-point is available at address: `127.0.0.1:5000/validationemail`.
When consuming the API use the json pattern to send the field `input`:

`{"input": "danilo.alves@gmail.com"}`

The result obtained for a call like the one shown above is:

`{
	"raw_email": "danilo.alves@gmail.com",
	"domain": "gmail",
	"validation_timestamp": "2022/05/13 11:10:27",
	"domain_valid_indicator\"": true,
	"username_valid_indicator\"": true,
	"cleansed_email": "daniloalves@gmail"
}`



