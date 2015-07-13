describe('GF ng-app', function() {
  it('should have a title', function() {
    browser.get('http://proxy/');
    expect(browser.getTitle()).toEqual('Gasista Felice');
  });
});
