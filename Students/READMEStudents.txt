-Defining Students as a subclass of person
-Defining the various students by ID similar to Concordia ID, and listing their Firs/Last names, email, along with their completed courses.

-Defined various Assessments. Each assessment has a label which refers to an id of a specific course from Courses.ttl. The assessments also have a property "grade" which states a string literal of the grade received for that assessment. Assessments are then refferenced within Student declarations by the "cr:tookCourse" predicate; this is to link the grade of the specified course to the student that took it. 