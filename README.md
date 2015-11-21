# PageBuilder

Page Builder is a restfull api for creating webpages.

It would be the backend for a service like Weebly or Square Space where a user would create a website.

The API allows creating, updating, getting, and seleting of pages with several element types.
When a user logs in they are given a unique api key to use when making requests to the api.

* Python and Flask were used as the backend Routing.
* Jinja was used for the templating for the demo page
* Users are authenticated using the Google oauth 2 API.
* Data is stored persistently using sqlite.
* The SQL Alchemy Library was used for the ORM.
