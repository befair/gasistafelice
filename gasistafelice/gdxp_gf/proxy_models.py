# Insert into this module the proxies of the models to format to XML/GDXP.
# Each model proxied attribute contains information about the attribute 
# kind (resource or element ) and the attribute type, toghether with its
# value.
#
# In the case where the attribute is a resource, it will be represented 
# as an internal resource of a rdf/xml. 

from gasistafelice.supplier.models import Supplier, SupplierStock
from base.const import PHONE,EMAIL,FAX

from const import EXTRA, SINGLE, TREE, MULTIPLE

#class SupplierStockGDXP(SupplierStock):
#
#    class Meta:
#    
#        proxy = True
#        
#    def supplier_gdxp(self):
#
#        return ['resource',
#                'gf',
#                ['rdf:resource',self.supplier]
#                
#        ]
#
#    def product_gdxp(self):
#
#        return ['element',
#                'gf',
#                ['rdf:datatype','\"&xsd;string\"'],
#               
#                self.product.name if self.product is not None else ""
#
#        ]
#        #return ['resource',
#        #        'gf',
#        #        ['rdf:resource',self.product]
#        #]
#
#    def supplier_category_gdxp(self):
#
#        return ['element',
#                'gf',
#                ['rdf:datatype','\"&xsd;string\"'],
#                
#                self.supplier_category.name if self.supplier_category is not None else ""
#
#        ]
#        #return ['resource',
#        #        'gf',
#        #        ['rdf:resource','']
#        #]
#
#    def image_gdxp(self):
#
#        return ['element',
#                'dc',
#                ['',''],
#                self.image.name 
#        ]
#
#    def price_gdxp(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;decimal\"'],
#                str(self.price)
#        ]
#
#    def availability_gdxp(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;boolean\"'],
#                self.availability
#        ]
#    def code_gdxp(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;string\"'],
#                self.code
#        ]
#
#    def amount_available_gdxp(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;integer\"'],
#                str(self.amount_available)
#        ]
#
#    def units_minimum_amount_gdxp(self):
#
#        return ['element',
#                 'gf', 
#                ['rdf:datatype','\"&xsd;integer\"'],
#                str(self.units_minimum_amount)
#        ]
#
#    def units_per_box_gdxp(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;integer\"'],
#                str(self.units_per_box)
#        ]
#
#    def detail_minimum_amount_gdxp(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;decimal\"'],
#                str(self.detail_minimum_amount)
#        ]
#
#    def detail_step_gdxp(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;decimal\"'],
#                str(self.detail_step)
#        ]
#
#    def delivery_notes_gdxp(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;string\"'],
#                self.delivery_notes
#        ]
#        
#    #def deleted_gdxp(self):
#
#    #    return ['element',
#    #             'gf',
#    #            ['rdf:datatype','\"&xsd;boolean\"'],
#    #            self.deleted
#    #    ]

class SupplierGDXP(Supplier):

    class Meta:
        proxy = True

    
    contacts_tree =  [[TREE],
                        [
                            ['ELEMENT',
                             'contacts'
                            ],
                            ['ELEMENT',
                             'contact'
                            ]
                        ]
                    ]


    def name_gdxp(self):

        return [[SINGLE],
                ['name', 
                self.name
                ]
        ]

    def seat_gdxp(self):

        return [
                [TREE],
                [
                    ['ELEMENT',
                    'address'
                    ],
                    [[MULTIPLE],
                    [
                        [[SINGLE],
                        [
                        'street',
                        self.seat.address if self.seat is not None else "" 
                        ]],
                        [[SINGLE],
                        [
                        'locality',
                        self.seat.city if self.seat is not None else "" 
                        ]],
                        [[SINGLE],
                        [
                        'zipcode',
                        self.seat.zipcode if self.seat is not None else "" 
                        ]],
                        [[SINGLE],
                        [
                        'country',
                        ""
                        ]]
                    ]
                    ]
               ]
               ]

    def vat_number_gdxp(self):
    
        return [[SINGLE],
                ['vatNumber', 
                self.vat_number 
                ]
        ]

    def ssn_gdxp(self):
    
        return [[SINGLE],
                ['taxCode', 
                 self.ssn
                ]
            ]

    #def website_gdxp(self):
    #
    #    return [[EXTRA],
    #            [
    #                ['ELEMENT',
    #                'extraFields'
    #                ],
    #                ['extraField',
    #                  self.website,
    #                    ['name',
    #                    'webSite'
    #                    ]
    #                ]
    #            ]
    #            ]
    #    #return [[SINGLE],
    #    #        ['webSite', 
    #    #         self.website
    #    #        ]
    #    #]
    
    def agent_set_gdxp(self):
  
        agents = []
        for person in self.agent_set.all():
            phone_contacts = person.contact_set.filter(flavour=PHONE)
            mail_contacts = person.contact_set.filter(flavour=EMAIL)
            fax_contacts = person.contact_set.filter(flavour=FAX)
            agents.append(
                    [
                    [TREE],
                    [
                        #['ELEMENT',
                        # 'contacts'
                        #],
                        #['ELEMENT',
                        # 'contact'
                        #],
                        ['ELEMENT',
                         'extraContact'
                        ],
                        [[MULTIPLE],
                        [
                            [[SINGLE],
                            [
                            'firstName',
                            person.name
                            ]],
                            [[SINGLE],
                            [
                             'lastName',
                             person.surname
                            ]],
                            [[SINGLE],
                            [
                            'phoneNumber',
                             phone_contacts[0].value if phone_contacts.count > 0 else ""
                            ]],
                            [[SINGLE],
                            [
                            'mobileNumber',
                             phone_contacts[1].value if phone_contacts.count > 1 else ""
                            ]],
                            [[SINGLE],
                            [
                            'faxNumber',
                             fax_contacts[0].value if fax_contacts.count > 0 else ""
                            ]]
                        ]
                        ]
                    ]
                    ])

        if len(agents) > 0:
            self.contacts_tree[1].append(agents)

        return 0
        #return [[TREE],
        #        agents
        #        ]

    def frontman_gdxp(self):
        
        phone_contacts = self.frontman.contact_set.filter(flavour=PHONE)
        mail_contacts = self.frontman.contact_set.filter(flavour=FAX)
        fax_contacts = self.frontman.contact_set.filter(flavour=EMAIL)
       
        self.contacts_tree[1].append([[TREE],
                [
                    #['ELEMENT',
                    # 'contacts'
                    #],
                    #['ELEMENT',
                    # 'contact'
                    #],
                    ['ELEMENT',
                     'extraContact'
                    ],
                    [[MULTIPLE],
                    [
                        [[SINGLE],
                        [
                         'phoneNumber',
                         phone_contacts[0].value if phone_contacts.count > 0 else ""
                        ]],
                        [[SINGLE],
                        [
                         'faxNumber',
                         fax_contacts[0].value if fax_contacts.count > 0 else ""
                        ]],
                        [[SINGLE],
                        [
                         'emailAddress',
                         mail_contacts[0].value if mail_contacts.count > 0 else ""
                        ]],
                        [[SINGLE],
                        [
                         'webSite',
                         self.frontman.website
                        ]]
                    ]
                    ]
                ]
            ])

        return 0
    
    def flavour_gdxp(self):
    
        return [[EXTRA],
                [
                    ['ELEMENT',
                    'extraFields'
                    ],
                    ['extraField',
                    self.flavour,
                        ['name',
                        'flavour'
                        ]
                    ]
                ]
                ]
    
    def n_employers_gdxp(self):
    
        return [[EXTRA],
                [
                    ['ELEMENT',
                    'extraFields'
                    ],
                    ['extraField',
                    self.n_employers,
                        ['name',
                        'employersNumber'
                        ]
                    ]
                ]
                ]
    
    def certifications_gdxp(self):
    
        certifications = []
        
        for cert in self.certifications.all():
            #certifications.append([[SINGLE],
            #    ['certification',
            #    cert.name
            #]
            #])
            certifications.append([[EXTRA],
                [
                    ['ELEMENT',
                    'extraFields'
                    ],
                    ['extraField',
                     cert.name,
                        ['name',
                        'certification'
                        ]
                    ]
                ]
                ])

        return [[MULTIPLE],
                certifications
                ]
    
    def logo_gdxp(self):
    
        return [[EXTRA],
                [
                    ['ELEMENT',
                    'extraFields'
                    ],
                    ['extraField',
                    self.logo.name,
                        ['name',
                        'logo'
                        ]
                    ]
                ]
                ]
    
    def contact_set_gdxp(self):
   
        phone_contacts = self.contact_set.filter(flavour=PHONE)
        mail_contacts = self.contact_set.filter(flavour=FAX)
        fax_contacts = self.contact_set.filter(flavour=EMAIL)
        
        self.contacts_tree[1].append([[TREE],
                [
                    #['ELEMENT',
                    # 'contacts'
                    #],
                    #['ELEMENT',
                    # 'contact'
                    #],
                    ['ELEMENT',
                     'primary'
                    ],
                    [[MULTIPLE],
                    [
                        [[SINGLE],
                        [
                         'phoneNumber',
                         phone_contacts[0].value if phone_contacts.count > 0 else ""
                        ]],
                        [[SINGLE],
                        [
                         'faxNumber',
                         fax_contacts[0].value if fax_contacts.count > 0 else ""
                        ]],
                        [[SINGLE],
                        [
                         'emailAddress',
                         mail_contacts[0].value if mail_contacts.count > 0 else ""
                        ]],
                        [[SINGLE],
                        [
                         'webSite',
                         self.website
                        ]]
                    ]
                    ]
                ]
            ])

        return 0
   
         
        #contacts = []
        #
        #for cont in self.contact_set.all():
        #    contacts.append([[SINGLE],
        #        [CONTACT_CHOICES_MAP[cont.flavour],
        #        cont.value
        #    ]
        #    ])

        #return [[MULTIPLE],
        #        contacts
        #        ]
    
    def iban_gdxp(self):
    
        return [[EXTRA],
                [
                    ['ELEMENT',
                    'extraFields'
                    ],
                    ['extraField',
                    self.iban,
                        ['name',
                        'iban'
                        ]
                    ]
                ]
                ]
    
    def description_gdxp(self):
    
        return [[SINGLE],
                ['note', 
                  self.description,
                ]
        ]
        #return [[EXTRA],
        #        [
        #            ['ELEMENT',
        #            'extraFields'
        #            ],
        #            ['extraField',
        #            self.description,
        #                ['name',
        #                'description'
        #                ]
        #            ]
        #       ]
        #       ]


#class ProductRDF(Product):
#
#    class Meta:
#    
#        proxy = True
#        
#    def code_rdf(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;string\"'],
#                self.code
#        ]
#
#    def producer_rdf(self):
#
#        return ['resource',
#                'gf',
#                ['rdf:resource',self.producer]
#                
#        ]
#
#    def category_rdf(self):
#
#        return ['element',
#                'gf',
#                ['rdf:datatype','\"&xsd;string\"'],
#                
#                self.category.name if self.category is not None else ""
#
#        ]
#
#    def mu_rdf(self):
#
#        return ['element',
#                'gf',
#                ['rdf:datatype','\"&xsd;string\"'],
#                
#                self.mu.name if self.mu is not None else ""
#
#        ]
#
#    def pu_rdf(self):
#
#        return ['element',
#                'gf',
#                ['rdf:datatype','\"&xsd;string\"'],
#                
#                self.pu.name if self.pu is not None else ""
#
#        ]
#
#    def muppu_rdf(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;decimal\"'],
#                str(self.muppu)
#        ]
#
#
#    def muppu_is_variable_rdf(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;boolean\"'],
#                self.muppu_is_variable
#        ]
#
#    def vat_percent_rdf(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;decimal\"'],
#                str(self.vat_percent)
#        ]
#
#    def name_rdf(self):
#
#        return ['element',
#                 'gf', 
#                ['rdf:datatype','\"&xsd;integer\"'],
#                str(self.name)
#        ]
#
#    def descriptio_rdf(self):
#
#        return ['element',
#                 'gf',
#                ['rdf:datatype','\"&xsd;integer\"'],
#                str(self.description)
#        ]

