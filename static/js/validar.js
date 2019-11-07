function validarcedula()
{
 var i;
 var cedula;
 var acumulado;
 cedula=document.formacedula.cedula.value;
 var instancia;
 acumulado=0;
 for (i=1;i<=9;i++)
 {
  if (i%2!=0)
  {
   instancia=cedula.substring(i-1,i)*2;
   if (instancia>9) instancia-=9;
  }
  else instancia=cedula.substring(i-1,i);
  acumulado+=parseInt(instancia);
 }
 while (acumulado>0)
  acumulado-=10;
 if (cedula.substring(9,10)!=(acumulado*-1))
 {
  alert("Cedula no valida, verificala!!");
  document.formacedula.textocedula.setfocus();
 }
}
