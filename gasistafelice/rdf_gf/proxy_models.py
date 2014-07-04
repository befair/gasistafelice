# Insert into this module the proxies of the models to format to XML/RDF.
# Each model proxied attribute contains information about the attribute 
# kind (resource or element ) and the attribute type, toghether with its
# value.
#
# In the case where the attribute is a resource, it will be represented 
# as an internal resource of a rdf/xml. 

from gasistafelice.supplier.models import SupplierStock, Supplier


class SupplierStockRDF(SupplierStock):

    class Meta:
    
        proxy = True
        
    def supplier_rdf(self):

        return ['resource',
                'gf',
                ['rdf:resource',self.supplier]
                
        ]

    def product_rdf(self):

        return ['element',
                'gf',
                ['rdf:datatype','\"&xsd;string\"'],
               
                self.product.name if self.product is not None else ""

        ]
        #return ['resource',
        #        'gf',
        #        ['rdf:resource',self.product]
        #]

    def supplier_category_rdf(self):

        return ['element',
                'gf',
                ['rdf:datatype','\"&xsd;string\"'],
                
                self.supplier_category.name if self.supplier_category is not None else ""

        ]
        #return ['resource',
        #        'gf',
        #        ['rdf:resource','']
        #]

    def image_rdf(self):

        return ['element',
                'dc',
                ['',''],
                self.image.name 
        ]

    def price_rdf(self):

        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;decimal\"'],
                ['catalog','1'],
                str(self.price)
        ]

    def availability_rdf(self):

        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;boolean\"'],
                ['catalog',''],
                self.availability
        ]
    def code_rdf(self):

        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;string\"'],
                self.code
        ]

    def amount_available_rdf(self):

        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;integer\"'],
                str(self.amount_available)
        ]

    def units_minimum_amount_rdf(self):

        return ['element',
                 'gf', 
                ['rdf:datatype','\"&xsd;integer\"'],
                str(self.units_minimum_amount)
        ]

    def units_per_box_rdf(self):

        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;integer\"'],
                str(self.units_per_box)
        ]

    def detail_minimum_amount_rdf(self):

        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;decimal\"'],
                str(self.detail_minimum_amount)
        ]

    def detail_step_rdf(self):

        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;decimal\"'],
                str(self.detail_step)
        ]

    def delivery_notes_rdf(self):

        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;string\"'],
                self.delivery_notes
        ]
        
    def deleted_rdf(self):

        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;boolean\"'],
                self.deleted
        ]

class SupplierRDF(Supplier):

    class Meta:
        proxy = True


    def name_rdf(self):

        return ['element',
                 'gf', 
                ['rdf:datatype','\"&xsd;string\"'],
                self.name
        ]

    def seat_rdf(self):

        return ['element',
                 'gf', 
                ['rdf:datatype','\"&xsd;string\"'], 
                self.seat.city if self.seat is not None else "" 
        ]

    def vat_number_rdf(self):
    
        return ['element',
                 'gf', 
                ['rdf:datatype','\"&xsd;string\"'], 
                self.vat_number 
        ]

    def ssn_rdf(self):
    
        return ['element',
                 'gf', 
                ['rdf:datatype','\"&xsd;string\"'], 
                self.ssn
        ]

    def website_rdf(self):
    
        return ['element',
                 'gf', 
                ['rdf:datatype','\"&xsd;string\"'], 
                self.website
        ]
    
    def agent_set_rdf(self):
   
        agents = {}
        
        for person in self.agent_set:
            app_list = ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;string\"'], 
                person.display_name
            ]
            agents.update(agent=app_list)

        return agents

    def frontman_rdf(self):
            
        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;string\"'], 
                self.frontman.display_name
            ]
    
    def flavour_rdf(self):
    
        return ['element',
                 'gf', 
                ['rdf:datatype','\"&xsd;string\"'], 
                self.flavour
        ]
    
    def n_employers_rdf(self):
    
        return ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;integer\"'],
                self.n_employers
        ]
    
    def certifications_rdf(self):
    
        certifications = {}
        
        for cert in self.certifications:
            app_list = ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;string\"'], 
                cert.name
            ]
            certifications.update(certification=app_list)

        return certifications
    
    def logo_rdf(self):
    
        return ['element',
                 'dc',
                ['', ''],
                self.logo.name
        ]
    
    def contact_set_rdf(self):
    
        contacts = {}
        
        for cont in self.certifications:
            app_list = ['element',
                 'gf',
                ['rdf:datatype','\"&xsd;string\"'], 
                cont.flavour + " : " + cert.value
            ]
            contacts.update(contact=app_list)

        return contacts
    
    def iban_rdf(self):
    
        return ['element',
                 'gf', 
                ['rdf:datatype','\"&xsd;string\"'], 
                self.iban
        ]
    
    def description_rdf(self):
    
        return ['element',
                 'gf', 
                ['rdf:datatype','\"&xsd;string\"'], 
                self.description
        ]

