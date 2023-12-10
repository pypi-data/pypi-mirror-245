# Simple API Call Counter

## Environment
1. Python 3.11.x

It is recommended to set with pyenv.
<br>If you can configure the Python execution environment in another way, you can skip the pyenv guide below.

### pyenv

~~~shell
$ pyenv install 3.11.2
$ pyenv virtualenv 3.11.2 url_counter
$ pyenv local url_counter
~~~

### Install

~~~shell
$ pip install -e .
~~~

### Run

~~~shell
$ counter --help  # Show me the help.

$ counter -d . -r -f  # Counts urls from all (json and log) files under the current folder and 
                      # creates a result file (however, json files starting with result_ are not included!)
~~~

#### Example of Using Options (Refer to the Help)
~~~shell
$ counter 000.json  # Display the count result from 000.json on the screen

$ counter 000.json -f  # Display the count result from 000.json on the screen and create a result_{date_time}.json file

$ counter 000.json 111.json 222.json ...  # Count multiple json files and display the results on the screen

$ counter 000.json 111.json 222.json ...  -f  # Count multiple json files, display the results on the screen, and create a result file

$ counter -d ./0000  # Count all json files in the 0000 folder and display the result (subfolders are not processed)

$ counter -d ./0000  -f  # Count all json files in the 0000 folder, display the result, and create files (subfolders are not included)

$ counter -d -r -f ./0000  # Count all json files in the 0000 folder, display the result, and create files (including subfolders)
~~~

### Test (unittest with pytest)

~~~shell
$ pytest -svx -rsa tests
~~~

## Result File Format

Format: result_{date_time(%Y%m%d_%H%M%S)}.json
~~~jsonc
{
    "targets": [ 
        list of counted files 
    ],
    "result": [
        "Counted URL: 1st place in frequency",
        "Counted URL: Sorted in descending order of frequency"
    ]
}
~~~
Sample: result_20231209_201928.json
~~~jsonc
{
    "targets": [
        "tests/samples/nginx.log"
    ],
    "result": [
        "GET /api/docs: 18",
        "GET /api: 17",
        "POST /api/v1/social/signup: 4",
        "DELETE /api/v1/users/95: 2",
        "PUT /api/v1/users/me: 1",
        "POST /api/v1/social/profile/format: 1",
        "POST /api/v1/social/profile: 1"
    ]
}
~~~

## One More Thing (About the ignore option)
If you want to specify lines to exclude from the counter. (e.g. request from a specific IP address, etc.)
<br>You can set export ignores=1.1.1.1 or export ignores=1.1.1.1,2.2.2.2 (no space allowed).

~~~shell
$ export ignores=1.1.1.1

or for multiple ignores.
$ export ignores=1.1.1.1,2.2.2.2
~~~

And surprisingly, this option can work with any string. (e.g. '/api/token')
~~~shell
$ export ignores='/api/token'

or for multiple ignores.
$ export ignores='/api/token',2.2.2.2
~~~
