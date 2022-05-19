USA_CITIES_COLNAMES = ["city", "state", "zipcode", "county"]
USA_CITIES_QUERY = """
SELECT DISTINCT ?city ?state ?zipcode ?county
WHERE { 
      ?cityNode rdf:type dbo:City. 

      ?cityNode dbp:name ?city. 
       FILTER(lang(?city) = 'en').

      ?cityNode dbo:subdivision ?stateNode.
      ?stateNode dbp:governor ?temp.
      ?stateNode rdfs:label ?state.
      FILTER(lang(?state)='en').

      ?cityNode dbo:postalCode ?zipcode.

      ?cityNode dbo:subdivision ?countyNode.
      ?countyNode dbo:type dbr:County_\(United_States\).
      ?countyNode dbp:name ?county.
      FILTER(lang(?county)='en').
}
"""

GLOBAL_CITIES_COLNAMES = ["city", "country", "countrycode", "zip"]
GLOBAL_CITIES_QUERY = """
SELECT DISTINCT ?city ?country ?countrycode (SAMPLE(?zip) AS ?zip) 
WHERE { 
      ?cityNode rdf:type dbo:City. 

      ?cityNode dbp:name ?city. 
       FILTER(lang(?city) = 'en').

      ?cityNode dbo:country ?countryNode.
      ?countryNode rdfs:label ?country.
      FILTER(lang(?country) = 'en').

      ?cityNode dbo:postalCode ?zipcode.
      FILTER(?zipcode != "").
      BIND(IF(CONTAINS(?zipcode, ","), STRBEFORE(?zipcode, ","),?zipcode) AS ?zip1)
      BIND(IF(CONTAINS(?zip1, "–"), STRBEFORE(?zip1, "–"), ?zip1) AS ?zip2)
      BIND(IF(CONTAINS(?zip2, "-"), STRBEFORE(?zip2, "-"), ?zip2) AS ?zip)

      ?countryNode dbo:countryCode ?countrycode.      
}
"""

BOOKS_COLNAMES = ["book", "author", "language", "pageCount"]
BOOKS_QUERY = """
SELECT DISTINCT ?book ?author ?language ?pageCount
WHERE { 
      ?bookNode rdf:type dbo:Book. 

      ?bookNode rdfs:label ?book. 
       FILTER(lang(?book) = 'en').

      ?bookNode dbo:author ?authorNode.
      ?authorNode rdfs:label ?author.
       FILTER(lang(?author) = 'en').

      ?bookNode dbp:language ?language.
      FILTER(lang(?language) = 'en').

       ?bookNode dbo:numberOfPages ?_pageCount.
        BIND( xsd:integer(?_pageCount) as ?pageCount).
}
"""

VIDEO_GAMES_COLNAMES = ["game", "platform", "publisher"]
VIDEO_GAMES_QUERY = """
SELECT DISTINCT ?game ?platform ?publisher
WHERE { 
      ?gameNode rdf:type dbo:VideoGame. 

      ?gameNode rdfs:label ?game. 
       FILTER(lang(?game) = 'en').

      ?gameNode dbo:computingPlatform ?platformNode.
      ?platformNode rdfs:label ?platform.
       FILTER(lang(?platform) = 'en').

      ?gameNode dbo:publisher ?publisherNode.
      ?publisherNode rdfs:label ?publisher.
       FILTER(lang(?publisher) = 'en').

       ?gameNode dbo:releaseDate ?date.
       BIND(year(xsd:dateTime(?date)) as ?year).
       FILTER(?year > 2015).
}
"""

PHONES_COLNAMES = ["phone", "os"]
PHONES_QUERY = """
SELECT DISTINCT ?phone ?os
WHERE { 
      ?phoneNode rdf:type dbo:Device.
      ?phoneNode rdfs:label ?phone.
       FILTER(lang(?phone) = 'en').
      {?phoneNode dct:subject dbc:Samsung_mobile_phones.}
             UNION
      {?phoneNode dct:subject dbc:Google_Pixel.}
             UNION
      {?phoneNode dct:subject dbc:OnePlus_mobile_phones.}
             UNION
      {?phoneNode dct:subject dbc:IPhone.}


      ?phoneNode dbo:operatingSystem ?osNode.
       ?osNode rdfs:label ?os.
       FILTER(lang(?os) = 'en').
}
"""

AIRPORTS_COLNAMES = ["city", "country", "airport", "faa"]
AIRPORTS_QUERY = """
SELECT DISTINCT ?city (SAMPLE(?country) AS ?country) ?airport ?faa
WHERE { 
      ?airportNode rdf:type dbo:Airport.
      ?airportNode dbp:name ?airport.
       FILTER(lang(?airport) = 'en').

      ?airportNode dbo:city ?cityNode.
       ?cityNode dbp:name ?city.
       FILTER(lang(?city) = 'en').

      ?airportNode dbo:faaLocationIdentifier ?faa.

           ?cityNode dbo:country ?countryNode.
           ?countryNode dbp:name ?country.
            FILTER(lang(?country) = 'en').
}
"""


CITY_COMPANY_COLNAMES = ["company"]
CITY_COMPANY_QUERY = """
SELECT DISTINCT ?company 
WHERE {

     BIND(%s as ?city)

     ?companyNode dbo:location ?city.
      ?companyNode rdf:type dbo:Company.
     FILTER NOT EXISTS {?companyNode dbo:fate ?fate}
     
      ?companyNode rdfs:label ?company.
      FILTER(lang(?company) = 'en').

}
"""
