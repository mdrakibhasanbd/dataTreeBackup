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
    console.log("I am first")
  }
  