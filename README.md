
# API END-POINTS

### GET /keywords_main/

Returns all main keywords in the database.

### GET /keywords_modifier/

Returns all modifier keywords in the database.

### GET /get_orders/<id>

Gets all orders for resteraunts with <id>

### PUT /new_order/<id>

Adds new order for user with <id>. Payload must have latitude, longitude, and the id of a keywords group (name=keywords).

### POST /call_uber/

Calls an uber. Pass in slat, slng (starting longitude and latitude), elat, elng.


### POST /child_keywords
Pass in: 'keywords': list of keyword ids, returns list of keywords who are valid children

Proof it works (using jquery):
$.post("http://surgefoodz.herokuapp.com/child_keywords/?format=json", {'keywords': JSON.stringify([1,2])}, function(e){debugger;}, 'json')




### PUT /new_order
Creates a new order. Pass in: user_email (can exist in db or not), keywords: [{'string':'XX', 'main':true},...], latitude, longitude

