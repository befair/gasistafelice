describe('GF ng-app', function() {
  it('should have a title', function() {
    browser.get('http://proxy/');
    expect(browser.getTitle()).toEqual('Gasista Felice');
  });

  it('should connect to the UI and get the user orders', function() {
    browser.get('http://proxy/');
    // fill login form
    element(by.css('#username')).sendKeys('01gas1');
    element(by.css('#password')).sendKeys('des');

    // click on 'GO' button!
    element(by.css('.btn')).click();

    // expect to be the user 01gas1
    element(by.binding('person.display_name')).getText().then(function(name) {
      expect(name).toBe("Ciao Gasista_01 DelGas_01");
    });
  });

  it('should increment/decrement the price/qty when "+/-" are clicked', function () {
    // get the first item in the table
    var item = element.all(by.repeater('product in order.pm.products')).get(1);

    // click 20 time on '+'
    for (var i=0; i < 20; i++)
      item.element(by.css('.glyphicon-plus')).click();

    // click 10 times on '-'
    for (var i=0; i < 10; i++)
      item.element(by.css('.glyphicon-minus')).click();

    // qty should be 10
    expect(item.element(by.model('product.quantity')).getAttribute('value')).toBe('10');

    // product.quantity * product.price is used to output the total price
    // so we can get that with by.binding('product.quantity')
    // does the code need revision? the bindings maybe shouldn't make operations
    item.element(by.binding('product.quantity')).getText().then(function (price) {
      expect(price).toBe('€ 250,00');
    });
  });

  it('should never decrement the price/qty under 0', function () {
    var item = element.all(by.repeater('product in order.pm.products')).get(1);

    for (var i=0; i < 20; i++)
      item.element(by.css('.glyphicon-minus')).click();

    expect(item.element(by.model('product.quantity')).getAttribute('value')).toBe('0');

    item.element(by.binding('product.quantity')).getText().then(function (price) {
      expect(price).toBe('€ 0,00');
    });
  });

  /*
  it('should add a product to the basket', function() {
    var item = element.all(by.repeater('product in order.pm.products')).get(2);
    for (var i=0; i < 3; i++)
      item.element(by.css('.glyphicon-plus')).click();
    element(by.buttonText('Aggiungi al paniere')).click();
  });
  */
});
