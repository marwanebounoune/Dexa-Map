import "@pnp/sp/folders";
import * as React from 'react';
import { ActionButton, Async, Stack,  } from 'office-ui-fabric-react';
import { sp, urlPropertieRef } from '../../Constants';
import "@pnp/sp/webs";
import "@pnp/sp/lists";
import "@pnp/sp/security";
import "@pnp/sp/security/list";
import "@pnp/sp/site-users/web";
import "@pnp/sp/site-groups/web";
import { Dialog } from '@microsoft/sp-dialog';
import { WindowPopUp } from "./utils";


export interface IValiderProps {
  idRef: number;
  buttonTitle: string;
  ctx: any;
}

export default function EditerRef (props:IValiderProps){
  let [userConn, setUserConn] = React.useState(null);
  React.useEffect(() => {
    user()
  });
  async function user(){
    let user = await sp.web.currentUser();
    let R = await sp.web.lists.getByTitle("Pins").items.getAll()
    var userConnected:any = null
    var query = function(element) {
      return element.membre_refId === user.Id;
    };
    await sp.web.lists.getByTitle("l_validateurs").items.getAll().then(async (res)=>{
      userConnected = res.filter(query)
      if(userConnected)
        await setUserConn(userConn)
      else
       await setUserConn(null)
    })
  }
  return (
    <Stack horizontal horizontalAlign="start"> 
    <ActionButton iconProps={{iconName: 'Edit'}} text={props.buttonTitle} onClick={(event)=> {event.preventDefault(); WindowPopUp('', urlPropertieRef+props.idRef, "");}}/>
    </Stack>
  );
}



