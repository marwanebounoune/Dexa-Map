import * as React from 'react';
import { EcartType, Mediane, numStr, Prix_unitaire_max, Prix_unitaire_min, Prix_unitaire_moyen } from '../utils/utils';

interface IPopOutFilter {
  Information:any;
}

export default function PopOutFilter (props:IPopOutFilter) {
  let prix_unit:any = Get_all_Prix_unit();
  
  function Get_all_Prix_unit(){
    let prix_unit:any = [];
    var p_int:number = null;
    props.Information.ref_dexa.forEach(element => {
      var type_de_bien = element.Type_x0020_de_x0020_bien;
      if(type_de_bien === "Résidentiel" || type_de_bien === "Commercial" || type_de_bien === "Professionnel"){
        p_int = parseInt(element.Prix_x0020_unitaire_x0020_pond_x);
      }
      else{
        p_int = parseInt(element.Prix_x0020_unitaire_x0020_terrai);
      }
      prix_unit.push(p_int);
    });
    return prix_unit;
  }
  return (
  <>
    <div>
      <table className="margin-left:25px">
        <tbody>
          <tr>
            <td ><b>Périmètre d'étude</b></td>
            <td >{props.Information.distance} km de rayon</td>
          </tr>
          <tr>
            <td ><b>Nature de référence sélectionnée</b></td>
            <td >{props.Information.type_de_bien}</td>
          </tr>
          {props.Information.ref_dexa.length?
          <tr>
            <td ><b>Nombre de pins (Valactif)</b></td>
            <td >{props.Information.ref_dexa.length} références</td>
          </tr> 
          :<></>}
          <tr>
            <td ><b>Prix unitaire Maximum</b></td>
            <td >{numStr(Prix_unitaire_max(prix_unit), "")},00 Dhs/m2</td>
          </tr>
          <tr>
            <td ><b>Prix unitaire Minimum</b></td>
            <td >{numStr(Prix_unitaire_min(prix_unit), "")},00 Dhs/m2</td>
          </tr>
          <tr>
            <td ><b>Prix unitaire moyen</b></td>
            <td >{numStr(Prix_unitaire_moyen(prix_unit), "")},00 Dhs/m2</td>
          </tr>
          <tr>
            <td ><b>Médiane</b></td>
            <td >{numStr(Mediane(prix_unit), "")},00 Dhs/m2</td>
          </tr>
          <tr>
            <td ><b>Etendue</b></td>
            <td >{numStr(Prix_unitaire_max(prix_unit) - Prix_unitaire_min(prix_unit), "")},00 Dhs/m2</td>
          </tr>
          <tr>
            <td ><b>Ecart type de l'échantillon</b></td>
            <td >{numStr(EcartType(prix_unit), "")},00 Dhs/m2</td>
          </tr>
          {props.Information.dgi_zone[0]?<tr>
            <td ><b>Zone DGI</b></td>
            <td >{props.Information.dgi_zone[0].Title}</td>
          </tr>:<></>}
          {props.Information.dgi_zone[0]?<tr>
            <td ><b>Prix unitaire de la DGI</b></td>
            <td >{numStr(props.Information.dgi_zone[0].Prix_unitaire, "")},00 Dhs/m2</td>
          </tr>:<></>}
        </tbody>
      </table>
    </div>
  </>
  );
};
