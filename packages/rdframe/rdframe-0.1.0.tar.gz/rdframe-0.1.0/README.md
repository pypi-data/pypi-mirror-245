# RDFrame | [SHACL profiles](/shacl) | [CQL profiles](/cql)

## About

This library serves two purposes.

1. Development of X -> SPARQL mappings, currently in two flavours
    1. SHACL interpreted for display, + endpoint definitions as RDF -> SPARQL
    2. [CQL](https://docs.ogc.org/DRAFTS/21-065.html) to SPARQL
       _i.e. a developer would write Python to implement mappings a particular way and can have a tight REPL process
       including visualising examples._
2. End user generation/specification of profiles which use the above.
   _i.e. a user would only use the web interface to specify profiles or specific CQL queries to achieve a desired
   outcome._

## RDFrame GUI components

### Prez SHACL version

1. Runtime values - Data specified at runtime when using for example the URI of an object to retrieve information about;
   the URI of a container object from which member items are listed; limit and offset values for use in pagination.
2. Endpoint Definition. This specifies the class(es) of object(s) to be returned from an endpoint, along with
   information about ordering, and pagination.

    1. Where a sh:target / sh:select is used, variables can be defined in the sh:select using a `$`. These values will
       be populated at runtime with, in priority order:
        1. Runtime values
        2. Default values specified with the endpoint definition. At present custom properties have been used to define
           default limit and offset values. This
3. Profile Definition. Used to specifiy which properties of focus objects should be returned.
4. SPARQL query. This is generated from the above three inputs.
5. Example data. This is any RDF data which can be used to test or demonstrate use of the profile/endpoint definition.
6. Results. The result of applying the generated SPARQL query against the Example data.

### CQL version

Description forthcoming - available at `/cql`

## Patterns to address common use cases

The current set of SHACL profiles are tailored towards a set of known use cases for [Prez](https://github.com/RDFLib/prez).

### 1.1 List objects based on their relationship to a container object.

Endpoint definition requirements:

1. The container object's URI, either specified as a runtime value.
2. sh:target / sh:select statement
3. sh:targetClass

The sh:targetClass is required due to a limitation with using `sh:select` as a string. The sh:targetClass is required in
order to generate the Construct part of the generated SPARQL query. The sh:select subquery is only validated and
inserted - there is no programmatic extraction of components.

Properties of the focus objects to include/exclude are specified in a profile (see 3.1 -> 3.3).

#### 1.1.1 Add triples to the CONSTRUCT part of the query from the FOCUS NODE selection

Optionally, triples can be added to the CONSTRUCT part of the query from the FOCUS NODE selection.
Triples to add can be defined via sh:rule / with sh:subject sh:predicate sh:object.
If a Literal is used as the range for any of these (sh:subject sh:predicate sh:object), and the Literal starts with a '?',
it will be translated into a variable in the generated SPARQL query.
Note: by default only the CLASS of an object is included from the focus node selection. This is the only provided 
mechanism to provide additional triples from the SELECT subquery which is used for focus node selection. Properties for
inclusion can be specified in the profile (via SHACL property shapes).

### 1.2 List objects based on their class.

Endpoint definition requirements:

1. sh:targetClass - the class of object to be listed.

Properties of the focus objects to include/exclude are specified in a profile (see 3.1 -> 3.3).

### 2.1 Describe an object given its URI

Endpoint definition requirements:

1. A runtime value for the object for example: `{"object": "http://my-object-uri"}`
2. `sh:targetNode "$object"` within the endpoint definition.

Properties of the focus objects to include/exclude are specified in a profile (see 3.1 -> 3.3).

### 3.1 Include all properties of a focus node

Includes all direct properties of a given focus node i.e. as a triple pattern `<focus_uri> ?p ?o`

There does not appear to be a relevant concept to borrow from SHACL that provides a mechanism to specify the retrieval
of all predicate values from a given focus node. As this is a common use case when displaying data, for conciseness an
extension property has been created:

`http://example.com/shacl-extension#allPredicateValues`

This property is used in place of specified path values under `sh:path`, for example:

```
ex:OpenNodeShape
    a              sh:NodeShape ;
    sh:property [
        sh:path shext:allPredicateValues ;
    ] ;
```

### 3.2 Include specified properties of a focus node

Specifying properties to include implies all properties NOT specifically included are to be **excluded**.

Specified property paths can be included using [SHACL Propety Paths](https://www.w3.org/TRhttps://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#property-paths)

These can either be specified directly using `sh:path` on a property shape, or multiple property paths can be specified
using `sh:union`.

#### 3.2.1 Include specified properties simple - single property path

Profile requirement:

1. `sh:path <property path expression>`

#### 3.2.2 Include specified properties complex - multiple property paths

Profile requirement:

1. ```
   sh:path ( sh:union ( <property path expression 1> <property path expression 2> ...) )
   ```

### 3.3 Exclude specified properties of a focus node

Specifying properties to exclude implies all *direct* properties NOT excluded are to be **included**.

Profile requirement:

1. Property shapes includes a sh:maxCount of 0

NB: the current assumption is that a user can either include specified

Use of patterns in Prez endpoints

### 3.4 Include blank node property chains

Although the SHACL vocabulary provides for ways to identify blank nodes, it does not appear there is a concise way to
specify that property chains including blank nodes should be included in the description of a focus node. For this
reason a custom property has been created. This property can be included on the nodeshape in a profile. The property is
`http://example.com/shacl-extension#bnode-depth`. The range of the property is the number of blank node (object/subject
pairs) to follow. It is used as follows:

```
ex:OpenNodeShape
    a sh:NodeShape ;
    shext:bnode-depth 2 ;
.
```

### 4.1 Include specific object values

Profile requirement:

1. Specify object values using `sh:hasValue` for a single value or `sh:in` with an RDF list for multiple values.

## Use of patterns in Prez endpoints

The following table shows where different patterns are used in the proposed Prez endpoint definitions.

| Endpoint                                                                                   | Endpoint Definition Pattern                                         | Profile Definition Patterns                                                                                                                                   |
|--------------------------------------------------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Catprez Catalog Listing](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#cp-catalog-listing_tab)                                  | 1.2 List objects based on their class.                              |                                                                                                                                                               |
| [Catprez Catalog Object](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#cp-catalog-object_tab)                                    | 2.1 Describe an object given its URI                                | 3.1 Include all properties of a focus node <br> 3.4 Include blank node property chains                                                                        |
| [Catprez Resource Listing](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#cp-resource-listing_tab)                                | 1.1 List objects based on their relationship to a container object. | 3.2.2 Include specified properties complex - multiple property paths                                           |
| [Catprez Resource Object](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#cp-resource-object_tab)                                  | 2.1 Describe an object given its URI                                | 3.1 Include all properties of a focus node <br> 3.4 Include blank node property chains                                                                        |
| [Vocprez Vocabulary Listing](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#vp-vocab-listing_tab)                                 | 1.2 List objects based on their class.                              |                                                                                                                                                               |
| [Vocprez Vocabulary Object](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#vp-vocab-object-top-level_tab)                         | 2.1 Describe an object given its URI                                | 3.1 Include all properties of a focus node <br> 3.4 Include blank node property chains                                                                        |
| [Vocprez Vocabulary Object Children Page 1/2](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#vp-vocab-object-children-page-1_tab) | 1.1 List objects based on their relationship to a container object. | 3.1 Include all properties of a focus node                                                                         |
| [Vocprez Vocabulary Concept Object](#)                                                     | 2.1 Describe an object given its URI                                | 3.1 Include all properties of a focus node <br> 3.4 Include blank node property chains <br> 3.2.2 Include specified properties complex - multiple property paths |
| [Vocprez Collection Listing](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#vp-collection-listing_tab)                            | 1.2 List objects based on their class.                              |                                                                                                                                                               |
| [Vocprez Collection Object](#)                                                             | 2.1 Describe an object given its URI                                | 3.1 Include all properties of a focus node <br> 3.4 Include blank node property chains                                                                        |
| [Vocprez Collection Concept Object](#)                                                     | 2.1 Describe an object given its URI                                | 3.1 Include all properties of a focus node <br> 3.4 Include blank node property chains                                                                        |
| [Spaceprez Dataset Listing](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#sp-dataset-listing_tab)                                | 1.2 List objects based on their class.                              |                                                                                                                                                               |
| [Spaceprez Dataset Object](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#sp-dataset-object_tab)                                  | 2.1 Describe an object given its URI                                | 3.1 Include all properties of a focus node <br> 3.4 Include blank node property chains                                                                        |
| [Spaceprez Feature Collection Listing](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#sp-feature-collection-listing_tab)          | 1.1 List objects based on their relationship to a container object. |                                                                                                                 |
| [Spaceprez Feature Collection Object](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#sp-feature-collection-object_tab)            | 2.1 Describe an object given its URI                                | 3.3 Exclude specified properties of a focus node <br> 3.4 Include blank node property chains                                                                        |
| [Spaceprez Feature Listing](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#sp-feature-listing_tab)                                | 1.1 List objects based on their relationship to a container object. |                                                                                                                                                               |
| [Spaceprez Feature Object](https://rdframe.sgraljii8d3km.ap-southeast-2.cs.amazonlightsail.com/shacl/#sp-feature-object_tab)                                  | 2.1 Describe an object given its URI                                | 3.1 Include all properties of a focus node <br> 3.4 Include blank node property chains                                                                        |

## Appendix - why use sh:union and property shapes?

Direct and Precise: sh:union and property paths allow direct referencing of specific properties, offering clear and granular control over displayed properties. They support SPARQL property path syntax for complex property relationships, and using sh:union, they can be specified together in a single RDF List.  
- sh:inversePath
- sh:alternativePath
- sh:path
As these property paths are used in the profile, they are about the selection of properties *after a set of focus nodes* has been selected, as such the most common use cases are where a union of properties is required, rather than a logical and. sh:union can be mapped directly to SPARQL union, giving a clear and direct mapping from the profile to the SPARQL query.

As these are specified off of a property node, sh:minCount and sh:maxCount are also available, and can be used to indicate optional properties (sh:minCount 0) or to indicate that a property should be excluded (sh:maxCount 0).