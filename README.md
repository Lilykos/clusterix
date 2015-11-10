# Clusterix: Visual exploration of clustered data


Clusterix is a tool that will allow users explore clustered data in an interactive manner.
At the moment, the tool mainly tries to solve the problem of affiliations guessing.

## Usage
Currently the project is in a very early stage of implementation, but can be used for data
preprocessing and extraction using the following commands:

`python manage.py runserver`

This command will run the Flask server, after which it can be used to make POST requests to it,
using the url [http://127.0.0.1:5000/add_affiliation/<affiliation string>](http://127.0.0.1:5000/add_affiliation/<affiliation string>).

E.g. the string _Department of Physics and Engineering Physics, Fordham University Bronx, NY 10458, USA_, will return (and save to the db):

```javascript
{
    "country": "USA",
    "country_code": "US",
    "department": "depart physic engin physic",
    "grobid_xml": "<affiliation>... (GROBID xml here)</affiliation>",
    "institution": "fordham univers bronx",
    "laboratory": "",
    "language": "en",
    "post_box": "",
    "post_code": "10458",
    "raw_string": "Department of Physics and Engineering Physics, Fordham University Bronx, NY 10458, USA",
    "raw_string_unicode": "Department of Physics and Engineering Physics, Fordham University Bronx, NY 10458, USA",
    "region": "NY",
    "settlement": ""
}
```

`python manage.py parse_xml <path/to/xml>`

This command has the same processing and extraction workflow as above, but it is used to extract all the
affiliations from a structured xml file.

## Important steps / TODO
- [ ] Crate API
    - [x] Single affiliation REST API
    - [] XML upload API (maybe not really useful, the manager should be enough)
- [ ] Data preprocessing (affiliation specific)
    - [x] Use GROBID API for affiliation parsing
    - [x] Language detection
    - [x] Standard NLP tasks (stemming, stopwords)
    - [ ] Translation for non-english strings?
- [ ] Clustering
    - [ ] Create the clustering process
    - [ ] Output in newick/json for presentation purposes
- [ ] Interface
    - [ ] Bootstrap / Materialize for UI
    - [ ] d3 for the clustering presentation
    - [ ] Frontend - backend communication for changing clustering parameters