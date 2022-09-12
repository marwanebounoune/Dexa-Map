import { MessageBar, MessageBarType } from 'office-ui-fabric-react';
import * as React from 'react';
import { EcartType, Mediane, numStr, Prix_unitaire_max, Prix_unitaire_min, Prix_unitaire_moyen } from '../utils/utils';


interface IPopOutProps {
  evaluation:any;
}

export default function PopOut (props:IPopOutProps) {
  let prix_unit:any = props.evaluation.array_prix_dexa;
  const SevereExample = ({message}) => (
        <MessageBar
          messageBarType={MessageBarType.severeWarning}
        >
          {message}
        </MessageBar>
  );
  return (
  <>
    <div>
      {props.evaluation.nbr_ref_dexa === 0 ? <SevereExample message={"Pas d'estimation pour ce bien, échec de trouver une occurrence approximative."}/>:<></>}
      {props.evaluation.nbr_ref_dexa > 0 && props.evaluation.nbr_ref_dexa < 3 ? <SevereExample message={"L'estimation non fiable, le nombre des occurrences approximatives est trop faible"}/>:<></>}
      <table className="margin-left:25px">
        <thead>
          <tr>
            <th colSpan={2}>Avis de valeur sur le bien.</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td ><b>Prix Unitaire éstimé</b></td>
            <td >{isNaN(props.evaluation.prix_estimer)?0:numStr(Math.floor(props.evaluation.prix_estimer), "")},00 Dhs/m2</td>
          </tr>
          <tr>
            <td ><b>Prix Total éstimé</b></td>
            <td >{isNaN(props.evaluation.prix_total)?0:numStr(Math.floor(props.evaluation.prix_total), "")},00 Dhs/m2</td>
          </tr>
          <tr>
            <td ><b>Périmètre d'étude</b></td>
            <td >{props.evaluation.perimetre} m de rayon</td>
          </tr>
          <tr>
            <td ><b>Nature de référence sélectionnée</b></td>
            <td >{props.evaluation.type_de_bien}</td>
          </tr>
          {props.evaluation.nbr_ref_dexa?
          <tr>
            <td ><b>Nombre de pins (Valactif)</b></td>
            <td >{props.evaluation.nbr_ref_dexa} références</td>
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
            <td ><b>Zone DGI</b></td>
            <td >{props.evaluation.dgi_zone.Title}</td>
          </tr>
          <tr>
            <td ><b>Prix unitaire de la DGI</b></td>
            <td >{props.evaluation.dgi_zone.Prix_unitaire},00 Dhs/m2</td>
          </tr>
        </tbody>
      </table>
    </div>
  </>
  );
};
