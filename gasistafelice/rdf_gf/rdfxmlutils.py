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
#   - the attribute value text representation, if necessary.

from xml.etree import ElementTree as ET
from xml.dom import minidom
from lxml import etree as letree

from proxies import proxymodels

#Namespaces, that is RDF vocabularis
NS = {
    'rdf' : '\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"',
    'dc' : '\"http://purl.org/dc/elements/1.1/\"',
    'gf' : '\"http://GFvocabulary#\"',
}

#list of possible object models to export
TAGS = [
    'suppliers',
    'stocks',
    'products'
]

#list of possible additional sub elements an tags 
ATTRIBUTES = {
    'suppliers' : ['SUPPLIER'],
    'products' : ['PRODUCT'],
    'stocks' : ['STOCK','gf:catalog','CATALOG'],
}

def prettify( root):
    """ Return a pretty-printed XML string for the root element of an 
        unformatted rdf/xml.
    """
    
    doctype='<!DOCTYPE rdf:RDF [<!ENTITY xsd "http://www.w3.org/2001/XMLSchema#">]>'
    rough_string = doctype + ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)

    return reparsed.toprettyxml(indent="  ")

def to_element( root, uri, prox_instance,**kwargs):
    """ Create an element from the attributes contained into a proxy of
        a given instance, than attach it to the father element.

        %Uri% can contain the resource representation of an object.
        %kwargs% can contain additional elements needed to build the element.
    """
    
    if uri is not None:
        ele_attr = { "rdf:about":"\"%s\"" % uri} 
    else:
        ele_attr = { "rdf:about":"%s[%i]" % (ATTRIBUTES.get(kwargs['tag'])[0],kwargs['counter'])}

    ele = ET.SubElement(root,
        "rdf:Description",
        ele_attr
    )

    if len(ATTRIBUTES.get(kwargs['tag'])) is not 1:
        i = 0
        while(True):
            if i >= kwargs.get('n_sub_elements'):
                break
            ele = ET.SubElement(ele,
                ATTRIBUTES.get(kwargs['tag'])[1],
                {"rdf:about" : "%s[%i]" % (ATTRIBUTES.get(kwargs['tag'])[2],i+1)}
            )
            i += 1
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
    else:
        for field in prox_instance._meta.fields:
            if field.attname is not 'id':
                #try:
                if field.attname[-3:] != "_id":
                    build_triple(
                        ele,
                        prox_instance,
                        field.attname,
                        **kwargs
                    )
                else:
                    build_triple(
                        ele,
                        prox_instance,
                        field.attname[:-3],
                        **kwargs
                    )
                
    return root


def build_triple(element, prox_instance, field_name, **kwargs):
    """Build a subject,predicate,object triple starting from a proxied
       instance, togheter with additional data.	"""

    try:
        rdf_attr = getattr(prox_instance,"%s%s" % (field_name,'_rdf'))()
    except AttributeError as e:
        return

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
                app = {rdf_attr[i][0] : "%s[%i]" % (ATTRIBUTES.get(tag)[0],counter)}
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
    """ Return the proxied instance of an objet. A proxy instance 
        contains data useful to build and rdf/xml representation of
        the proxied instance.
    """

    return proxymodels[instance.__class__.__name__].objects.get(pk=instance.pk)

def build_root():
    """ Create the root of the rdf/xml to build. 
        The xml namespaces relative to the rdf/xml vocabularies.
        are specified in the %NS% list 
    """
   
    vocabularies = {}

    for item in NS.keys():
        app = {"xmlns:%s" % item : "%s" % NS[item]}
        vocabularies.update(app)

    print vocabularies
    
    return ET.Element("rdf:RDF",
        vocabularies
        #{ "xmlns:rdf":"%s" % NS['rdf'],
        #  "xmlns:dc":"%s" % NS['dc'],
        #  "xmlns:gf":"%s" % NS['gf']
        #}
    )


def build_rdfxml( uri, instance,**kwargs):
    """ Return an rdf/xml representation of a particular instance,
        or a set of different objects linked togheter
    """

    root = build_root()
    
    #TODO: this value will be computed from data in view
    #n_sub_elements  = kwargs.get('n_sub_elements')
    n_sub_elements  = 1

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
                    'elements': elements,
                    'n_sub_elements' : n_sub_elements,
                }
                xml = to_element(root,
                    None,
                    prox_instance,
                    **ctx
                )

    rdfxml = prettify(root)
    
    return rdfxml 
