## Queries
### Problem 1
Number of triples in KB

```
SELECT (COUNT(*) AS ?triples)
WHERE {
	?a ?b ?c .
}
```

### Problem 2
Number of students

```
SELECT (COUNT(?a) AS ?students),(COUNT(?c) AS ?Courses),COUNT(DISTINCT ?topic) AS ?Topics

WHERE {
	{ ?a rdfs:subClassOf foaf:Person . } 
    UNION 
	{ ?c rdf:type schema:Course  . }
    UNION
	{ ?course owl:sameAs ?topic . }
}
```

### Problem 3
For a course, list all covered topics using their (English) labels and their link to DBpedia
```
SELECT   ?topic, ?link 
WHERE {
    ?courseId schema:courseCode "COMP249" .
    ?courseId owl:sameAs ?link .
    ?link rdfs:label ?topic .
    FILTER (langMatches( lang(?topic), "EN" ) )
}
```

*Note*: If this query is empty, then the database needs to be populated with the labels:

```
SELECT   ?link, ?predicate, ?object 
WHERE {
    ?courseId schema:courseCode ?something .
    ?courseId owl:sameAs ?link .
    ?link ?predicate ?object . 
}

```

### Problem 4
For a given student, list all courses this student completed, together with the grade

```
SELECT "Nick", "Lawson", ?Course, ?Grade  
WHERE {
    ?s rdfs:subClassOf foaf:Person . 
    ?s foaf:firstName "Nick" .
    ?s foaf:lastName "Lawson" .
    ?s cpo:took ?c .
    ?c rdfs:label ?u .
    ?c cpo:grade ?Grade .
    ?u schema:name ?Course .
} 
```


### Problem 5
For a given topic, list all students that are familiar with the topic (i.e., took, and did not fail, a course that covered the topic)

```
SELECT ?FirstName, ?LastName, "COMP248", ?Grade  
WHERE {
    ?s rdfs:subClassOf foaf:Person . 
    ?s foaf:firstName ?FirstName .
    ?s foaf:lastName ?LastName .
    ?u schema:courseCode "COMP248" .
    ?s cpo:took ?c .
    ?c rdfs:label ?u .
    ?c cpo:grade ?Grade .
    FILTER(?Grade != "F") .
} 
```

### Problem 6
For a student, list all topics (no duplicates) that this student is familiar with (based on the completed courses for this student that are better than an “F” grade)

```
SELECT  DISTINCT  ?Name ,?Last, ?Topic, ?Grade 
WHERE {   
    ?s rdfs:subClassOf foaf:Person .
    ?s foaf:firstName "Tyler" .
    ?s foaf:lastName "Perry" .
    ?s cpo:took ?assessment .
    ?s foaf:firstName ?Name.
    ?s foaf:lastName ?Last .
    
    ?assessment  rdfs:label ?courseId .
    ?assessment  cpo:grade ?Grade .
    
    ?courseId schema:courseCode ?Course .
    ?courseId owl:sameAs ?link .
    ?link rdfs:label ?topic .
    
    ?courseId schema:courseCode ?Course .
    ?courseId owl:sameAs ?link .
    ?link rdfs:label ?Topic .
    
    #FILTER(?Grade != "F"). 
    
    FILTER (langMatches( lang(?Topic), "EN" ) ).
} 
```






