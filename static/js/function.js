document.addEventListener('DOMContentLoaded', function() {
    // Attach click event to viewmaps buttons
    var viewmapButtons = document.getElementsByClassName('viewmaps');
    for (var i = 0; i < viewmapButtons.length; i++) {
      viewmapButtons[i].addEventListener('click', function() {
        var row = this.closest('tr');
        var oltName = row.querySelectorAll('td')[0].textContent;
        var routerName = row.querySelectorAll('td')[1].textContent;
  
        submitForm1(oltName, routerName);
        submitForm2(oltName, routerName);
      });
    }
  });
  
  function submitForm1(oltName, routerName) {
    var form1 = document.createElement('form');
    form1.method = 'POST';
    form1.action = '/treemap';
  
    var inputOltName1 = document.createElement('input');
    inputOltName1.type = 'hidden';
    inputOltName1.name = 'oltName';
    inputOltName1.value = oltName;
    form1.appendChild(inputOltName1);
  
    var inputRouterName1 = document.createElement('input');
    inputRouterName1.type = 'hidden';
    inputRouterName1.name = 'routerName';
    inputRouterName1.value = routerName;
    form1.appendChild(inputRouterName1);
  
    document.body.appendChild(form1);
    form1.submit();
    document.body.removeChild(form1);
  }
  
  function submitForm2(oltName, routerName) {
    var form2 = document.createElement('form');
    form2.method = 'POST';
    form2.action = '/tree';
  
    var inputOltName2 = document.createElement('input');
    inputOltName2.type = 'hidden';
    inputOltName2.name = 'oltName';
    inputOltName2.value = oltName;
    form2.appendChild(inputOltName2);
  
    var inputRouterName2 = document.createElement('input');
    inputRouterName2.type = 'hidden';
    inputRouterName2.name = 'routerName';
    inputRouterName2.value = routerName;
    form2.appendChild(inputRouterName2);
  
    document.body.appendChild(form2);
    form2.submit();
  }
  
  