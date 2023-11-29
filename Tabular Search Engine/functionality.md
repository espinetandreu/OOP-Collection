### Search Engine Functionality:

#### **AND Search:**
- If none of the words in the query are enclosed by "", the search engine performs an AND search.
- In an AND search, all keywords must appear in the results for a match to occur.
- The absence of double quotes indicates that all words are mandatory for a match.

  **Example:**
 
  Query: *'Hello world'*
  
  Result: Documents containing *'Hello'* and *'world'* are matched.

#### **OR Search:**
- If at least one word in the query is enclosed by "", the search engine performs an OR search.
- In an OR search, either of the keywords must appear in the results for a match to occur.
- Words enclosed in double quotes are optional, and their presence enhances the score.

    **Example:**
    
    Query: *'Hello world of "happiness"'*
    
    Result: Documents containing *'Hello'* and *'world'* are matched, and optionally *'happiness'* can be present.

#### **Scoring**
- Each keyword present in the results is assigned a score.
- Keywords enclosed by "" still have impact on the score.

    **Example:**
    
    Query: *'Hello world of "happiness"'*
    
    Result: If the result is *'Hello world'* will have a 0.75 score. If the result is *'Hello world happiness'* will have a 1.0 score.