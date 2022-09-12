import "@pnp/sp/folders";
import * as React from 'react';
import { ActionButton, Stack,  } from 'office-ui-fabric-react';
import { sp } from '../../Constants';
import "@pnp/sp/webs";
import "@pnp/sp/lists";
import "@pnp/sp/security";
import "@pnp/sp/security/list";
import "@pnp/sp/site-users/web";
import "@pnp/sp/site-groups/web";
import { Dialog } from '@microsoft/sp-dialog';

export interface IValiderProps {
  idRef: number;
  buttonTitle: string;
  ctx: any;
}

export default function ValiderRef (props:IValiderProps){
  let [isValidateur, setIsValidateur]= React.useState(null);

  async function valider(){
    let user = await sp.web.currentUser();
    var _date = new Date().toISOString();
    let itemAvantValid = await sp.web.lists.getByTitle("Pins").items.getById(props.idRef)
    await (await sp.web.lists.ensure("Pins")).list.items.getById(props.idRef).breakRoleInheritance();
    const { Id: roleDefId1 } = await sp.web.roleDefinitions.getByName("Collaboration")();
    const { Id: roleDefId2 } = await sp.web.roleDefinitions.getByName("Après validation des références")();
    const groups1 = await sp.web.siteGroups.getByName("Direction")();
    const groups2 = await sp.web.siteGroups.getByName("Elaborateur_visiteur")();
    await itemAvantValid.roleAssignments.add(groups1.Id, roleDefId1);
    await itemAvantValid.roleAssignments.add(groups2.Id, roleDefId2);
    await sp.web.lists.getByTitle("Pins").items.getById(props.idRef).update({
      validateur_refId: user.Id,
      date_x0020_de_x0020_validation: _date
    }).then(()=>{
      Dialog.alert(`La référence est validée avec succès.`);
    }).catch(console.log)
  }
  async function userValidateur(){
    let user = await sp.web.currentUser();
    let validateurs = await sp.web.lists.getByTitle("l_validateurs").items()
    var query = function(element) {
        return element.membre_refId === user.Id;
    };
    var validateur = validateurs.filter(query)
    if( validateur.length !== 0 )
      setIsValidateur(validateur)
  }
  React.useEffect(() => {
    userValidateur()
  },[])
  
  return (
    <div>{isValidateur?
      <Stack horizontal horizontalAlign="start"> 
        <ActionButton iconProps={{iconName: 'VerifiedBrand'}} text={props.buttonTitle} onClick={() => valider()}/>
      </Stack>:<></>}
    </div>
  );
}

