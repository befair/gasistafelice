var handleAlertPopup = function() {
  var EC = protractor.ExpectedConditions;
  browser.wait(EC.alertIsPresent(), 5000);
  browser.switchTo().alert().accept();
};

describe('GF ng-app', function() {

  [0,1].map(function(index) {

    it('should have a title', function() {
      if (!index)
        browser.driver.manage().window().maximize();
      else
        browser.driver.manage().window().setSize(768, 1024);
      browser.get('http://proxy:8080/');
      expect(browser.getTitle()).toEqual('Gasista Felice');
    });

    it('should connect to the user order page', function() {
      // fill login form
      element(by.model('app.username')).sendKeys('01gas1');
      element(by.model('app.password')).sendKeys('des');

      // click on 'GO' button!
      // $$(selector) = element(by.css(selector))
      $$('#go').click();

      // check current url
      expect(browser.getLocationAbsUrl())
        .toBe('/order/');

      // check user displayed name
      if (index) {
        $$('.navbar-toggle').click();
        expect(element(by.binding('person.display_name')).getText())
          .toBe("Gasista_01 DelGas_01");
        $$('.navbar-toggle').click();
      }
      else
        expect(element(by.binding('person.display_name')).getText())
          .toBe("Gasista_01 DelGas_01");
    });

    it('should increment/decrement the price/qty when "+/-" are clicked', function () {
      // get the second item in the table
      var item = element.all(
                   by.repeater('product in order.pm.products')
                 ).get(1);

      // click 20 time on '+'
      for (var i=0; i < 20; i++)
        item.$$('.glyphicon-plus').click();

      // click 10 times on '-'
      for (var i=0; i < 10; i++)
        item.$$('.glyphicon-minus').click();

      // qty should be 10
      expect(item.element(by.model('product.quantity'))
        .getAttribute('value'))
          .toBe('10');

      // price should be 250 euros
      expect(item.element(by.binding('product.quantity'))
        .getText())
          .toBe('€ 250,00');
    });

    it('should never decrement the price/qty under 0', function () {
      var item = element.all(
                   by.repeater('product in order.pm.products')
                 ).get(1);

      for (var i=0; i < 20; i++)
        item.$$('.glyphicon-minus').click();

      expect(item.element(by.model('product.quantity'))
        .getAttribute('value'))
          .toBe('0');

      expect(item.element(by.binding('product.quantity'))
        .getText())
          .toBe('€ 0,00');
    });

    it('should add a product to the basket', function() {
      var item = element.all(
                   by.repeater('product in order.pm.products')
                 ).get(2);

      // set the quantity to 3
      item.element(by.model('product.quantity')).clear();
      item.element(by.model('product.quantity')).sendKeys('3');

      // add to the basket
      element(by.buttonText('Aggiungi al paniere')).click();

      // handle the alert popup
      handleAlertPopup();

      // go to the basket
      browser.setLocation('basket');

      // get the first order
      item = element.all(
               by.repeater('item in basket.open_ordered_products')
             ).get(0);

      // get all the column from the first order
      var columns = item.$$('td');

      // expects to have 8 columns (counting the hidden ones)
      expect(columns.count())
        .toBe(8);

      // check the fields
      expect(columns.get(0)
        .getText())
          .toBe('Ord. 59');
      expect(columns.get(1)
        .getText())
          .toBe('Fornitore 01');
      expect(columns.get(2)
        .getText())
          .toBe('Scarpe Uomo (paio)');
      expect(columns.get(3)
        .getText())
          .toBe('€ 20,00');
      expect(item.element(by.model('item.quantity'))
        .getAttribute('value'))
          .toBe('3');
      expect(columns.get(6)
        .getText())
          .toBe('€ 60,00');
    });

    it('should logout', function() {
      if(index)
        $$('.navbar-toggle').click();
      $$('#btn-logout').click();
    });
  });
});
