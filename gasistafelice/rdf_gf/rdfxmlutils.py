# AUTHOR: Matteo Micheletti
#
# A set of utilities useful to translate an object, or a set of objets,
# into a rdf/xml file.
#
# The models of the objects to be represented need to be proxied so that
# every proxied attribute contains information to make the translation.
#
# Each proxied attribute should return a list containing:
#   
#   - the attribute kind;
#   - the attribute given namespace;
#   - a list of elements couple with the rdf/xml types, according to the 
#      attribute types;
#   - the attribute value tex representation, if necessary.

from xml.etree import ElementTree as ET
from xml.dom import minidom
from lxml import etree as letree

from proxies import proxymodels

NS = {
    'rdf' : '\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"',
    'dc' : '\"http://purl.org/dc/elements/1.1/\"',
    'gf' : '\"http://GFvocabulary#\"',
}

TAGS = [
    'suppliers',
    'products'
]

ATTRIBUTES = {
    'suppliers' : 'SUPPLIER',
    'products' : 'PRODUCT',
}

def prettify( root):
    """ Return a pretty-printed XML string for the root element of an unformatted
        rdf/xml.
    """
    
    doctype='<!DOCTYPE rdf:RDF [<!ENTITY xsd "http://www.w3.org/2001/XMLSchema#">]>'
    rough_string = doctype + ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)

    return reparsed.toprettyxml(indent="  ")

def to_element( root, uri, prox_instance,**kwargs):
    """ Return an element from the attributes contained into a proxy of
        a given instance
    """

    if uri is not None:
        ele_attr = { "rdf:about":"\"%s\"" % uri} 
    else:
        ele_attr = { "rdf:about":"%s[%i]" % (ATTRIBUTES.get(kwargs['tag']),kwargs['counter'])}

    ele = ET.SubElement(root,
        "rdf:Description",
        ele_attr
    )

    for field in prox_instance._meta.fields:
        if field.attname is not 'id':
            try:
                build_triple(
	                ele,
                    prox_instance,
                    field.attname,
                    **kwargs
                )
            except AttributeError as e:
                build_triple(
	                ele,
                    prox_instance,
                    field.attname[:-3],
                    **kwargs
                )
                
    return root


def build_triple(element, prox_instance, field_name, **kwargs):
    """Build a subject,predicate,object triple starting from an element	"""

    rdf_attr = getattr(prox_instance,"%s%s" % (field_name,'_rdf'))()

    if rdf_attr[2][0] is not '':
        attrs = {}
        i = 2;
        while True:

             if i >= len(rdf_attr) or (type(rdf_attr[i]) is not list):
                 break
                 
             counter = 0
             if rdf_attr[i][0] == 'rdf:resource':
                 for elem in kwargs['elements']:
                     if rdf_attr[i][1] == elem[1][0]:
                        tag = elem[0]
                        counter = elem[1][1]

             if counter is 0:
                app = {rdf_attr[i][0] : rdf_attr[i][1]}
             else:
                app = {rdf_attr[i][0] : "%s[%i]" % (ATTRIBUTES.get(tag),counter)}
             attrs.update(app)
             i += 1

        sub = ET.SubElement(element, 
            '%s:%s' % (rdf_attr[1],field_name),
            attrs
        )
    else:
        sub = ET.SubElement(element, 
            '%s:%s' % (rdf_attr[1],field_name) 
        )

    if rdf_attr[0] is 'element':
        sub.text = rdf_attr[-1]


def get_proxied(instance):
    """ Return the proxy instance of an objet. A proxy instance 
        contains data useful to build and rdf/xml representation of
        the proxied instance.
    """

    return proxymodels[instance.__class__.__name__].objects.get(pk=instance.pk)

def build_root():
    """ The xml namespaces relatives to the rdf/xml vocabularies. """
    
    return ET.Element("rdf:RDF",
        { "xmlns:rdf":"%s" % NS['rdf'],
          "xmlns:dc":"%s" % NS['dc'],
          "xmlns:gf":"%s" % NS['gf']
        }
    )


def build_rdfxml( uri, instance,**kwargs):
    """ Return an rdf/xml representation of a particular instance,
        or a set of different objects linked togheter
    """

    root = build_root()

    if instance is not None:
        prox_instance = get_proxied(instance)
        xml = to_element(root,
            uri,
            prox_instance
        )
    else:
        elements = []
        for kwarg in kwargs:
            for ele in kwargs[kwarg]:
                elements.append([kwarg,ele])
        for tag in TAGS:
            for elem in kwargs[tag]:
                prox_instance = get_proxied(elem[0])
                ctx = {
                    'tag' : tag,
                    'counter' : elem[1],
                    'elements': elements
                }
                xml = to_element(root,
                    None,
                    prox_instance,
                    **ctx
                )

    rdfxml = prettify(root)
    
    return rdfxml 
