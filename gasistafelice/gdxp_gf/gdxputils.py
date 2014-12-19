# AUTHOR: Matteo Micheletti
#
# A set of utilities useful build a gdxp xml file.
#
# GDXP format syntax can be found here: 
# https://github.com/madbob/GASdotto/wiki/GDXP
#

from xml.etree import ElementTree as ET
from xml.dom import minidom
from lxml import etree as letree

from proxies import proxymodels
from const import EXTRA, SINGLE, TREE, MULTIPLE, RETURN_CODE

from datetime import datetime

#Metadata
MD = {
    'protocolVersion' : 0.2,
    'creationDate' : datetime.now(),
    'applicationSignature' : 'GasistaFelice',
}


def prettify( root):
    """ Return a pretty-printed XML string for the root element of an 
        unformatted gdxp/xml.
    """
   
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)

    return reparsed.toprettyxml(indent="  ")

def to_element( root, prox_instance,**kwargs):
    """ Create an element from the attributes contained into a proxy of
        a given instance, than attach it to the father element.

        %kwargs% can contain additional elements needed to build the element.

        The function is recursive so in-depth element can be attached
        to the correct parent
    """
    ele = ET.SubElement(root,
        "supplier"
    )

    for field_name in prox_instance._meta.get_all_field_names():
        if len(field_name) > 2 :
            if field_name[-3:] != "_id":
                build_element(
                    ele,
                    prox_instance,
                    field_name,
                    **kwargs
                )
            else:
                build_element(
                    ele,
                    prox_instance,
                    field_name[:-3],
                    **kwargs
                )

    build_element(
        ele,
        gdxp_attr=prox_instance.contacts_tree
    )
    build_element(
        ele,
        gdxp_attr=prox_instance.extra_fields_tree
    )
                
    return root


def build_element(element, prox_instance=None, field_name=None, **kwargs):
    """Build an xml element starting from a proxied
       instance, togheter with additional data.	"""

    try:
        if field_name and prox_instance:
            gdxp_attr = getattr(prox_instance,"%s%s" % (field_name,'_gdxp'))()
        else:
            gdxp_attr = kwargs['gdxp_attr']
    except AttributeError as e:
        return

    if gdxp_attr in RETURN_CODE.values():
        return

    if gdxp_attr[0][0] == SINGLE:
        sub = ET.SubElement(element, 
            '%s' % (gdxp_attr[1][0]) 
        )
        sub.text = gdxp_attr[1][1]
    elif gdxp_attr[0][0] == MULTIPLE:
        for elem in gdxp_attr[1]:
            build_element(element, gdxp_attr=elem) 
    elif gdxp_attr[0][0] == EXTRA:
        #app = element
        #for elem in gdxp_attr[1]:
            #if elem[0] == 'ELEMENT':
            #    app = ET.SubElement(app, 
            #        '%s' % (elem[1]) 
            #    )
            #else:
            attr = {gdxp_attr[1][2][0] : gdxp_attr[1][2][1]}
            element = ET.SubElement(element, 
                '%s' % (gdxp_attr[1][0]),
                attr 
            )
            element.text = gdxp_attr[1][1]

    elif gdxp_attr[0][0] == TREE:
        app = element
        for elem in gdxp_attr[1]:
            if elem[0] == 'ELEMENT':
                app = ET.SubElement(app, 
                    '%s' % (elem[1]) 
                )
                try:
                    app.text = elem[2]
                except IndexError as e:
                    pass
            elif elem[0][0] == MULTIPLE:
                build_element(app, gdxp_attr=elem) 
            elif elem[0][0] == TREE:
                build_element(app, gdxp_attr=elem) 
                
                     

def get_proxied(instance):
    """ Return the proxied instance of an objet. A proxy instance 
        contains data useful to build and gdxp/xml representation of
        the proxied instance.
    """

    return proxymodels[instance.__class__.__name__].objects.get(pk=instance.pk)

def build_root():
    """ Create the root of the gdxp to build. 
        The properties relative to the gdxp
        are specified in the %MD% list 
    """
   
    properties = {}

    for item in MD.keys():
        app = {"%s" % item : "%s" % MD[item]}
        properties.update(app)

    return ET.Element("gdxp",
        properties
    )


def build_gdxp( instance,**kwargs):
    """ Return an gdxp/xml representation of a particular instance,
        or a set of different objects linked togheter
    """

    root = build_root()
    
    if instance is not None:
        prox_instance = get_proxied(instance)
        xml = to_element(root,
            prox_instance
        )

    gdxp = prettify(root)
    
    return gdxp
