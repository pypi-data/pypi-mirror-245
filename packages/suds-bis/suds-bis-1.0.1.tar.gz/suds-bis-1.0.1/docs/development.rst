GENERAL DEVELOPMENT NOTES
=================================================

Reproducing problematic use cases:

* Failing web service processing examples can be easily packaged as reproducible
  test cases using the suds library 'message & reply injection' technique.
* Some things you can achieve using this technique (for examples, see existing
  project unit tests):

  * Create a client object based on a fixed WSDL string.
  * Have a client object send a fixed request string without having it construct
    one based on the loaded WSDL schema and received arguments.
  * Have a client object process a fixed reply string without having it send a
    request to an actual external web service.


External documentation:

* SOAP

  * http://www.w3.org/TR/soap

  * Version 1.1.

    * http://www.w3.org/TR/2000/NOTE-SOAP-20000508

  * Version 1.2.

    * Part0: Primer

      * http://www.w3.org/TR/2007/REC-soap12-part0-20070427
      * Errata: http://www.w3.org/2007/04/REC-soap12-part0-20070427-errata.html

    * Part1: Messaging Framework

      * http://www.w3.org/TR/2007/REC-soap12-part1-20070427
      * Errata: http://www.w3.org/2007/04/REC-soap12-part1-20070427-errata.html

    * Part2: Adjuncts

      * http://www.w3.org/TR/2007/REC-soap12-part2-20070427
      * Errata: http://www.w3.org/2007/04/REC-soap12-part2-20070427-errata.html

    * Specification Assertions and Test Collection

      * http://www.w3.org/TR/2007/REC-soap12-testcollection-20070427
      * Errata:
        http://www.w3.org/2007/04/REC-soap12-testcollection-20070427-errata.html

* WS-I Basic Profile 1.1

  * http://www.ws-i.org/Profiles/BasicProfile-1.1.html

* WSDL 1.1

  * http://www.w3.org/TR/wsdl

* XML Schema

  * Part 0: Primer Second Edition - http://www.w3.org/TR/xmlschema-0

    * Non-normative document intended to provide an easily readable description
      of the XML Schema facilities, and is oriented towards quickly
      understanding how to create schemas using the XML Schema language.

  * Part 1: Structures - http://www.w3.org/TR/xmlschema-1
  * Part 2: Datatypes - http://www.w3.org/TR/xmlschema-2

For additional design, research & development project notes see the project's
``notes/`` folder.


RELEASE PROCEDURE
=================================================

1. Update changelog with release notes for the pertinent release.

2. Tag the relevant commit with the relevant version number and
   push. CI will do the rest.


DEVELOPMENT & TESTING ENVIRONMENT
=================================================

1. Install Python.
2. Install Tox.
3. Run ``tox``.


STANDARDS CONFORMANCE
=================================================

There seems to be no complete standards conformance overview for the suds
project. This section contains just some related notes, taken down while hacking
on this project. As more related information is uncovered, it should be added
here as well, and eventually this whole section should be moved to the project's
user documentation.

Interpreting message parts defined by a WSDL schema
---------------------------------------------------

* Each message part is interpreted as a single parameter.

  * What we refer to here as a 'parameter' may not necessarily correspond 1-1 to
    a Python function argument passed when using the suds library's Python
    function interface for invoking web service operations. In some cases suds
    may attempt to make the Python function interfaces more intuitive to the
    user by automatically unwrapping a parameter as defined inside a WSDL schema
    into multiple Python function arguments.

* In order to achieve interoperability with existing software 'in the wild',
  suds does not fully conform to the WSDL 1.1 specification with regard as to
  how message parts are mapped to input data contained in SOAP XML web service
  operation invocation request documents.

  * WSDL 1.1 standard states:

    * 2.3.1 Message Parts.

      * A message may have message parts referencing either an element or a type
        defined in the WSDL's XSD schema.
      * If a message has a message part referencing a type defined in the WSDL's
        XSD schema, then that must be its only message part.

    * 3.5 soap:body.

      * If using document/literal binding and a message has a message part
        referencing a type defined in the WSDL's XSD schema then that part
        becomes the schema type of the enclosing SOAP envelope Body element.

  * Suds supports multiple message parts, each of which may be related either to
    an element or a type.
  * Suds uses message parts related to types, as if they were related to an
    element, using the message part name as the representing XML element name in
    the constructed related SOAP XML web service operation invocation request
    document.
  * WS-I Basic Profile 1.1 standard explicitly avoids the issue by stating the
    following:

    * R2204 - A document/literal binding in a DESCRIPTION MUST refer, in each of
      its soapbind:body element(s), only to wsdl:part element(s) that have been
      defined using the element attribute.

  * Rationale.

    * No other software has been encountered implementing the exact
      functionality specified in the WSDL 1.1 standard.
    * Already done in the original suds implementation.
    * Example software whose implementation matches our own.

      * SoapUI.

        * Tested with version 4.6.1.

      * WSDL analyzer & invoker at `<http://www.validwsdl.com>`_.

WSDL XSD schema interpretation
------------------------------

* ``minOccurs``/``maxOccurs`` attributes on ``all``, ``choice`` & ``sequence``
  schema elements are ignored.

  * Rationale.

    * Already done in the original suds implementation.

  * Extra notes.

    * SoapUI (tested with version 4.6.1).

      * For ``all``, ``choice`` & ``sequence`` schema elements with their
        ``minOccurs`` attribute set to "0", does not explicitly mark elements
        found in such containers as optional.

* Supports sending multiple same-named web service operation parameters, but
  only if they are specified next to each other in the constructed web service
  operation invocation request document.

  * Done by passing a list or tuple of such values to the suds constructed
    Python function representing the web service operation in question.
  * Rationale.

    * Already done in the original suds implementation.

  * Extra notes.

    * Such same-named values break other web service related tools as well, e.g.
      WSDL analyzer & invoker at `<http://www.validwsdl.com>`_.
